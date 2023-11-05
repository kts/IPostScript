# IPostScript

[jupyter](https://jupyter.org/) kernel for [PostScript](https://en.wikipedia.org/wiki/PostScript) ([ghostscript](https://www.ghostscript.com/))

## Requirements

You must have `ghostscript` installed (https://www.ghostscript.com/)

`gs` must be in your `$PATH`. (on Windows, `gswin64c.exe`).

## Install

```bash
pip install jupyter

git clone https://github.com/kts/IPostScript.git
cd IPostScript

#install package:
pip install .

#install jupyter kernel:
python -m IPostScript.install
```

## Usage

Console usage:

```
$ jupyter console --kernel postscript
Jupyter console 6.6.3

PostScript kernel...
In [1]: 2 3 mul =
6
In [2]: 
```

Browser notebook:

```
$ jupyter notebook
# then select "New" > "Notebook: PostScript"
```

## Features

* tab-completion for 371 PostScript/GhostScript keywords (built-in commands)

## Links

Based on https://github.com/takluyver/bash_kernel

see also,

* https://jupyter-client.readthedocs.io/en/stable/wrapperkernels.html

* https://pypi.org/project/metakernel/

* https://github.com/Calysto/octave_kernel
