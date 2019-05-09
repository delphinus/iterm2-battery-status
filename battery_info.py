#!/usr/bin/env python3
from pathlib import Path
import sys

iterm2_lib_dir = Path(
    "~/Library/ApplicationSupport/iTerm2/iterm2env-3.7.2/versions/3.7.2/lib/python3.7/site-packages"
)
sys.path.append(str(iterm2_lib_dir.expanduser()))

from iterm2_battery import battery

bat = battery()
print(bat.status())
