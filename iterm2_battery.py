#!/usr/bin/env python3

from ctypes import Structure, c_char_p, c_int, cdll
from datetime import datetime
from functools import wraps
from iterm2 import Connection, StatusBarComponent, StatusBarRPC, run_forever
from iterm2.statusbar import Knob
from math import floor
from pathlib import Path
from typing import Any, Callable, List, TypeVar, cast

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


class battery:
    chars = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    thunder = "ϟ"
    width = 5
    lib_path = Path(__file__).resolve().parent / "battery.so"
    icon = "🔋"
    plugged = "🔌"

    def __init__(self) -> None:
        self.lib = cdll.LoadLibrary(str(battery.lib_path))
        self.lib.battery.restype = battery_info
        self.lib.battery.argtypes = ()

    def status(self) -> str:
        result = self.lib.battery()
        if result.error is not None:
            return battery.plugged

        bat = self._battery(result.status, result.percent)
        time = self._time(result.elapsed, result.charging)
        return f"{battery.icon} |{bat}| {result.percent:d}%{time}"

    def _battery(self, status: str, percent: int) -> str:
        if status == b"AC Power" and percent == 100:
            return battery.width * battery.chars[-1]
        elif status == b"AC Power":
            mid: int = floor(battery.width / 2)
            return mid * " " + battery.thunder + (battery.width - mid - 1) * " "
        elif status == b"Battery Power":
            unit: int = len(battery.chars)
            total_char_len: int = len(battery.chars) * battery.width
            char_len: int = floor(total_char_len * percent / 100)
            full_len: int = floor(char_len / unit)
            remained: int = char_len % unit
            space_len = battery.width - full_len - (0 if remained == 0 else 1)
            bat = battery.chars[-1] * full_len
            if remained != 0:
                bat += battery.chars[remained - 1]
            bat += " " * space_len
            return bat

        return " " * battery.width

    def _time(self, elapsed: int, charging: int) -> str:
        if elapsed == 0 and charging == 0:
            return ""
        elif elapsed == -1 or charging == -1:
            return " -:- "  # calculating

        seconds = max(elapsed, charging)
        return " {0:d}:{1:02d}".format(*divmod(seconds, 60))


async def main(connection: Connection) -> None:
    component: StatusBarComponent = StatusBarComponent(
        "Battery",
        "Show battery remaining",
        [],
        "|███▎  | 66% 2:34",
        30,
        "cx.remora.battery",
    )
    bat = battery()

    @StatusBarRPC
    async def battery_status(knobs: List[Knob]) -> str:
        return _battery_status()

    @memoize()
    def _battery_status() -> str:
        return bat.status()

    await component.async_register(connection, battery_status, timeout=None)


run_forever(main)
