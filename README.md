# iterm2-battery-status

A component to show battery status for iTerm2's status bar feature

## What's this?

The latest [iTerm2][] (> v3.3.0) has a new feature: [Status Bar][]. iTerm2 has several components to show info from your Mac, but it lacks one from battery (v3.3.0 beta5, at least). This repo adds it.

[iTerm2]: https://iterm2.com
[StatusBar]: https://www.iterm2.com/3.3/documentation-status-bar.html

## How to use

You need to enable [Python API][] in iTerm2. Then, put scripts on this repo into the directory as below.

[Python API]: https://iterm2.com/python-api/

```sh
cp iterm2-battery.py ~/Library/Application Support/iTerm2/Scripts/Autolaunch
```

After restarting iTerm2, you can choose the battery component in preferences: **Preferences > Profiles > Session > Status bar enabled > Configure Status Bar**.

## Thanks

The idea to show battery as Unicode bar characters comes from [Code-Hex/battery][].

[Code-Hex/battery]: https://github.com/Code-Hex/battery

## See also

* [Running a Script — iTerm2 Python API 0.26 documentation](https://iterm2.com/python-api/tutorial/running.html)
* [iTerm2 にステータスバーが付いた - Qiita](https://qiita.com/delphinus/items/1748937aefeb241bdcee) (Japanese)
