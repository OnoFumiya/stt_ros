#!/bin/bash
echo "╔══╣ Install: sobits_speech_recognition (STARTING) ╠══╗"

export PIP_BREAK_SYSTEM_PACKAGES=1

SCRIPT_DIR=$(pwd)
set -e

echo "--- Updating apt package lists and installing system dependencies ---"
export DEBIAN_FRONTEND=noninteractive
sudo apt update -y
sudo apt install pulseaudio-utils ffmpeg libc++1 -y

echo "--- Cloning ROS packages ---"
cd ..
SOBITS_MSGS_REPO="sobits_interfaces"
if [ ! -d "$SOBITS_MSGS_REPO" ]; then
    git clone -b ${ROS_DISTRO}-devel https://github.com/TeamSOBITS/sobits_interfaces.git
fi

cd "$SCRIPT_DIR"

echo "╚══╣ Install: sobits_speech_recognition (FINISHED) ╠══╝"