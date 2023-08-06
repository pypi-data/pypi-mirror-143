# FILEWATCH

  

![Banner](https://i.ibb.co/LPRRgXW/filewatch-banner.png)

![PyPI - License](https://img.shields.io/pypi/l/filewatch-cli?style=for-the-badge) ![PyPI](https://img.shields.io/pypi/v/filewatch-cli?style=for-the-badge) ![PyPI - Format](https://img.shields.io/pypi/format/filewatch-cli?style=for-the-badge) 
> FILEWATCH is a file watcher that allows you to watch files if something changes run arguments

<h1 align="center">Installation 🚀</h1>
<h4>REQUIREMENTS</h4>

 - Python Should Be Installed On The Machine
 - Package Requirements `click`, `colorama`, `commonmark`, `Pygments`, `rich`.

```
$ pip install filewatch
```

<h1 align="center">Usage 😎</h1>

Get Help
```
> python -m filewatch --help
Usage: python -m filewatch [OPTIONS]

  FILEWATCH is a file watcher that allows you to watch files if something
  changes run arguments

Options:
  -p, --path TEXT          Path of file to watch
  -args, --arguments TEXT  Arguments to run when file changes
  -d, --delay INTEGER      Delay in seconds
  --help                   Show this message and exit.
```
## Basic Use
```
python -m filewatch -p "<filepath>" -args "<arguments>"
```
`-p` and `-args ` are aliases for `--path` and `--arguments`

#### EXAMPLES
The below example is for `scss` or `sass` file 
```
python -m filewatch -p "./index.scss" -args "sass ./index.scss ./index.css"
```
<h1 align="center">📃License📃</h1>
<p align="center">This project is developed under <a href="https://github.com/tinasty/filewatch/blob/main/LICENSE">MIT</a> license</p>
