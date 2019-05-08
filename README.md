# iterm2-battery-status

A component to show battery status for iTerm2's status bar feature

## What's this?

The latest [iTerm2][] (> v3.3.0) has a new feature: [Status Bar][]. iTerm2 has several components to show info from your Mac, but it lacks one from battery (v3.3.0 beta5, at least). This repo adds it.

[iTerm2]: https://iterm2.com
[Status Bar]: https://www.iterm2.com/3.3/documentation-status-bar.html

## Gallery

* Charged  
  <img width="127" alt="スクリーンショット 2019-05-05 16 54 17" src="https://user-images.githubusercontent.com/1239245/57190757-2da3e900-6f59-11e9-829d-ca3894353b9e.png">
* Charging  
  <img width="155" alt="スクリーンショット 2019-05-05 16 55 58" src="https://user-images.githubusercontent.com/1239245/57190760-31377000-6f59-11e9-8100-b8f7dab07354.png">
* Discharging  
  <img width="157" alt="スクリーンショット 2019-05-05 16 57 02" src="https://user-images.githubusercontent.com/1239245/57190764-32689d00-6f59-11e9-808f-4064bf734687.png">

## How to use

You need to enable [Python API][] in iTerm2. Then, run the install command as below.

[Python API]: https://iterm2.com/python-api/

```sh
cd /path/to/this/repo
make install
# This compiles compiles dependencies and copy files into ~/Library/Application Support/iTerm2/Scripts/Autolaunch
```

After restarting iTerm2, you can choose the battery component in preferences: **Preferences > Profiles > Session > Status bar enabled > Configure Status Bar**.

## Thanks

The idea to show battery as Unicode bar characters comes from [Code-Hex/battery][].

[Code-Hex/battery]: https://github.com/Code-Hex/battery

## See also

* [Running a Script — iTerm2 Python API 0.26 documentation](https://iterm2.com/python-api/tutorial/running.html)
* [iTerm2 にステータスバーが付いた - Qiita](https://qiita.com/delphinus/items/1748937aefeb241bdcee) (Japanese)
