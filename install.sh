#!/bin/bash
echo "╔══╣ Install: STT ROS (STARTING) ╠══╗"

export PIP_BREAK_SYSTEM_PACKAGES=1

set -e

echo "--- Updating apt package lists and installing system dependencies ---"
export DEBIAN_FRONTEND=noninteractive
sudo apt update -y
sudo apt install pulseaudio-utils ffmpeg libc++1 -y

echo "╚══╣ Install: STT ROS (FINISHED) ╠══╝"