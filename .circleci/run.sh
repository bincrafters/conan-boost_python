#!/bin/bash

set -e
set -x

if which pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi
pyenv activate conan

python build.py
