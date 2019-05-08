#!/usr/bin/env python3

from ctypes import Structure, c_char_p, c_int, cdll
from datetime import datetime
from functools import wraps
from iterm2 import Connection, StatusBarComponent, StatusBarRPC, run_forever
from iterm2.statusbar import Knob
from math import floor
from pathlib import Path
from typing import Any, Callable, List, TypeVar, cast

chars = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
thunder = "ϟ"
width = 5

# ref https://github.com/python/mypy/issues/1551#issuecomment-253978622
TFun = TypeVar("TFun", bound=Callable[..., Any])


class battery_info(Structure):
    _fields_ = [
        ("percent", c_int),
        ("elapsed", c_int),
        ("charging", c_int),
        ("status", c_char_p),
        ("error", c_char_p),
    ]


class memoize:
    """
    memoize is a decorator to cache the result value and reduce calling heavy
    functions. The caches expires in 60 seconds.
    """

    memo = ""
    calculated = float(0)
    timeoutSeconds = 60

    def __call__(self, function: TFun) -> TFun:
        @wraps(function)
        def wrapper() -> Any:
            now = datetime.now().timestamp()
            if now > self.calculated + self.timeoutSeconds:
                self.memo = function()
                self.calculated = now
            return self.memo

        return cast(TFun, wrapper)


async def main(connection: Connection) -> None:
    component: StatusBarComponent = StatusBarComponent(
        "Battery",
        "Show battery remaining",
        [],
        "|███▎  | 66% 2:34",
        30,
        "cx.remora.battery",
    )
    plugged = "🔌"

    lib_path = Path(__file__).resolve().parent / "battery.so"
    lib = cdll.LoadLibrary(str(lib_path))
    lib.battery.restype = battery_info
    lib.battery.argtypes = ()

    @StatusBarRPC
    async def battery_status(knobs: List[Knob]) -> str:
        return _battery_status()

    @memoize()
    def _battery_status() -> str:
        result = lib.battery()

        # TODO: reconsider conditions

        icon = "🔋"
        battery = _battery(result.status, result.percent)
        time = _time(result.elapsed, result.charging)
        return f"{icon} |{battery}| {result.percent:d}%{time}"

    def _battery(status: str, percent: int) -> str:
        if status == b"AC Power" and percent == 100:
            return width * chars[-1]
        elif status == b"AC Power":
            mid: int = floor(width / 2)
            return mid * " " + thunder + (width - mid - 1) * " "
        elif status == b"Battery Power":
            unit: int = len(chars)
            total_char_len: int = len(chars) * width
            char_len: int = floor(total_char_len * percent / 100)
            full_len: int = floor(char_len / unit)
            remained: int = char_len % unit
            space_len: int = width - full_len - (0 if remained == 0 else 1)
            battery = chars[-1] * full_len
            if remained != 0:
                battery += chars[remained - 1]
            battery += " " * space_len
            return battery

        return " " * width

    def _time(elapsed: int, charging: int) -> str:
        if elapsed == 0 and charging == 0:
            return ""
        elif elapsed == -1 or charging == -1:
            return " -:- "  # calculating

        seconds = max(elapsed, charging)
        return " {0:d}:{1:02d}".format(*divmod(seconds, 60))

    await component.async_register(connection, battery_status, timeout=None)


run_forever(main)
