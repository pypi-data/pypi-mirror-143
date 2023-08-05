# command2img


[![GitHub license](https://img.shields.io/github/license/emanuel-alves/command2img?color=blue)](https://github.com/emanuel-alves/command2img/blob/main/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/command2img?color=blue&label=pypi%20download)](https://pypi.org/project/command2img/)
[![PyPI](https://img.shields.io/pypi/v/command2img?color=blue&label=version)](https://pypi.org/project/command2img/)
## Motivation

This program was developed from the need I had to capture the output of a program as an image to insert into a report.

## Install

To install it, you can use the python package manager:

    pip install command2img

## Update

    pip install --upgrade command2img

## Uninstall 

    pip uninstall command2img

## Examples

### using exa (tree):
    exa --tree --icons | command2img
![tree image](https://raw.githubusercontent.com/emanuel-alves/command2img/main/images/tree.png)

### using echo:
    echo "Example echo" | command2img -fs 50 -m 15
![echo image](https://raw.githubusercontent.com/emanuel-alves/command2img/main/images/echo.png)

### using cat:
    cat README.md | command2img -bg "black" -tf "white" 
![cat image](https://raw.githubusercontent.com/emanuel-alves/command2img/main/images/cat.png)
