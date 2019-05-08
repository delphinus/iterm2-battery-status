#!/usr/bin/env python3

import ctypes

from datetime import datetime
from functools import wraps
from iterm2 import Connection, StatusBarComponent, StatusBarRPC, run_forever
from iterm2.statusbar import Knob
from math import floor
from subprocess import CalledProcessError, check_output
from typing import Any, Callable, List, TypeVar, cast
import re

chars = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
thunder = "ϟ"
width = 5

# ref https://github.com/python/mypy/issues/1551#issuecomment-253978622
TFun = TypeVar("TFun", bound=Callable[..., Any])


class battery_info(ctypes.Structure):
    _fields_ = [
        ("percent", ctypes.c_int),
        ("elapsed", ctypes.c_int),
        ("status", ctypes.c_char_p),
        ("error", ctypes.c_char_p),
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
    lib = ctypes.cdll.LoadLibrary(
        "/Users/jinnouchi.yasushi/git/dotfiles/submodules/iterm2-battery-status/battery.so"
    )
    lib.battery.restype = battery_info
    lib.battery.argtypes = ()

    @StatusBarRPC
    async def battery_status(knobs: List[Knob]) -> str:
        return _battery_status()

    @memoize()
    def _battery_status() -> str:
        result = lib.battery()

        # TODO: reconsider conditions

        battery: str
        if result.status == b"AC Power" and result.percent == 100:
            battery = width * chars[-1]
        elif result.status == b"AC Power":
            mid: int = floor(width / 2)
            battery = mid * " " + thunder + (width - mid - 1) * " "
        elif result.status == b"Battery Power":
            unit: int = len(chars)
            total_char_len: int = len(chars) * width
            char_len: int = floor(total_char_len * result.percent / 100)
            full_len: int = floor(char_len / unit)
            remained: int = char_len % unit
            space_len: int = width - full_len - (0 if remained == 0 else 1)
            battery = chars[-1] * full_len
            if remained != 0:
                battery += chars[remained - 1]
            battery += " " * space_len
        else:
            battery = " " * width

        icon = "🔋"
        if result.elapsed == 0:
            elapsed = ""
        else:
            minutes, seconds = divmod(result.elapsed, 60)
            elapsed = f" {minutes:d}:{seconds:02d}"
        return f"{icon} |{battery}| {result.percent:d}%{elapsed}"

    await component.async_register(connection, battery_status, timeout=None)


run_forever(main)
