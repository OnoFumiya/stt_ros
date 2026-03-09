#!/bin/bash
echo "╔══╣ Install: NeMo STARTING ╠══╗"

export PIP_BREAK_SYSTEM_PACKAGES=1

SCRIPT_DIR=$(cd $(dirname $0); pwd)
set -e

echo "--- Updating apt package lists ---"
export DEBIAN_FRONTEND=noninteractive
sudo apt update -y

echo "--- Installing NeMo Toolkit (ASR) ---"
pip3 install -U pip setuptools wheel typing_extensions
pip3 install nemo_toolkit[asr]

echo "--- Installing VAD ---"
pip3 install git+https://github.com/TEN-framework/ten-vad.git

echo "--- Fixing Library Versions for Stability ---"
pip3 install --force-reinstall numba==0.61.2
pip3 install --force-reinstall "numpy==1.26.4"
pip3 install --force-reinstall coverage==6.2

echo "--- Pre-downloading NeMo ASR model (Cache) ---"
python3 -c "import nemo.collections.asr as nemo_asr; nemo_asr.models.ASRModel.from_pretrained(model_name='nvidia/parakeet-tdt-0.6b-v2')"

echo "--- Restoring Build Tools for ROS 2 compatibility ---"
pip3 install -U setuptools pip wheel colcon-common-extensions

echo "╚══╣ Install: NeMo FINISHED ╠══╝"