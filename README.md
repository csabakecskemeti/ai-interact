aihub

Supported Platforms
===================

  * MacOS

Requirements
============

  * Python 3.11.7
  * Tesseract
  * Open AI API compatible LLVM service access

Install
=======

  * Install dependencies:
```
$ brew install pyenv tesseract
```
  * Setup `pyenv`: Please follow the instructions described at https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv

  * Install Python environment:
```
$ pyenv install 3.11.7
$ pyenv virtualenv 3.11.7 aihub
$ pyenv activate aihub
$ pip install -r requirements.txt
```

  * Configure LLVM service access:
```
$ vi aihub/config.json
[Perform necessary edit]
```

  * Start the app:
```
$ cd aihub && python -m aihub_bootstrap
```

Usage
=====

  * Press `Shift + F1`
  * Click the top left, then the bottom right corner of an error message
  * Read the solution in UI window
