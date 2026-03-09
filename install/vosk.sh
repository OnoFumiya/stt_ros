#!/bin/bash

echo "╔══╣ Install: Vosk (OPTIMIZED) ╠══╗"

export PIP_BREAK_SYSTEM_PACKAGES=1

sudo apt update
sudo apt install -y \
    python3-tk \

python3 -m pip install -U pip
python3 -m pip install \
    vosk \

pip3 install -U "numpy==1.26.4" \

echo "╚══╣ Install: Vosk (FINISHED) ╠══╝"