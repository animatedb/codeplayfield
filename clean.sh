#!/bin/bash

find . -type d -name '__pycache__' -prune -exec rm -rf {} \;
find . -type d -name '.ipynb_checkpoints' -prune -exec rm -rf {} \;
find . -type d -name '.mypy_cache' -prune -exec rm -rf {} \;

