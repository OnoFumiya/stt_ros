#!/bin/bash
echo "╔══╣ Install: Whisper (STARTING) ╠══╗"

sudo apt update -y

echo "--- Installing Python packages via pip3 ---"
python3 -m pip install -U pip --break-system-packages
python3 -m pip install git+https://github.com/openai/whisper.git --break-system-packages

echo "--- Installing Faster-Whisper ---"
python3 -m pip install -U faster-whisper --break-system-packages

echo "--- Installing VAD ---"
pip3 install -U --force-reinstall -v git+https://github.com/TEN-framework/ten-vad.git --break-system-packages


echo "--- Install numba ---"
pip3 install --force-reinstall numba==0.61.2 --break-system-packages
pip3 install --force-reinstall "numpy==1.26.4" --break-system-packages

echo "--- Install coverage ---"
pip3 install --force-reinstall coverage==6.2 --break-system-packages

python3 -c "import whisper; whisper.load_model('small')"

echo "╚══╣ Install: Whisper (FINISHED) ╠══╝"
