<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# SOBITS Speech Recognition

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#launch-and-usage">Launch and Usage</a></li>
    <li><a href="#common-parameters">Common Parameters</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#milestone">Milestone</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- OVERVIEW -->
## Introduction

SOBITS Speech Recognition integrates various Speech-to-Text (STT) engines into ROS 2 Action communication.

The following STT engines are currently supported.

- VOSK
- Whisper
- NeMo ASR
- Sherpa-ONNX

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Here you will find instructions on setting up this package locally.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites

First, please set up the following environment before proceeding to the next installation stage.

| System  | Version |
| ------------- | ------------- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS | Jazzy Jalisco |
| Python | 3.12 |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1. Go to the `src` folder of your ROS 2 workspace.
    ```sh
    cd ~/colcon_ws/src/
    ```

2. Clone this repository.
    ```sh
    git clone -b jazzy-devel https://github.com/TeamSOBITS/sobits_speech_recognition.git
    ```

3. Move into the repository.
    ```sh
    cd sobits_speech_recognition/
    ```

4. Install the dependencies.
    ```sh
    bash install.sh
    ```

5. Build the package.
    ```sh
    cd ~/colcon_ws/
    colcon build --symlink-install
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LAUNCH AND USAGE -->
## Launch and Usage

Before running, you must download the model for the STT engine you wish to use.

Click on each STT name to view download and usage instructions.

| STT | Accuracy | Speed | Features |
| --- | --- | --- | --- |
| [Whisper](README_detail.en.md#whisper-top) | ☆☆☆☆ | ☆☆ | Multilingual, translation, prompt support, batch model |
| [Sherpa-ONNX](README_detail.en.md#sherpa-top) | ☆☆ | ☆☆☆☆ | 100+ models available, lightweight |
| [NeMo](README_detail.en.md#nemo-top) | ☆☆☆☆☆ | ☆☆☆☆☆ | High memory usage, GPU recommended |
| [VOSK](README_detail.en.md#vosk-top) | ☆ | ☆☆☆☆ | Multilingual, ultra-lightweight, streaming model |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Common Parameters

The following parameters are common to all launch files.

| Parameter | Description | Default |
| --- | --- | --- |
| mic_volume | Sets the microphone input volume as a percentage. Returns to the original volume after shutdown. (e.g., "150%") | "" |
| use_feedback | Whether to use intermediate feedback | True |
| change_default_sink | Whether to switch the system default output sink to `speaker_aec` when `speaker_aec` is created | True |
| restore_default_sink_on_stop | Whether to restore the previous default sink on shutdown if this node changed it | True |

`change_default_sink` and `restore_default_sink_on_stop` control different phases.

- `change_default_sink`
  - Controls whether the node switches the default sink to `speaker_aec` while it is running.
- `restore_default_sink_on_stop`
  - Controls whether the node restores the original default sink when it stops, but only if this node changed it.

For example:

- `change_default_sink=True`, `restore_default_sink_on_stop=True`
  - Use `speaker_aec` while running and restore the previous sink on shutdown.
- `change_default_sink=True`, `restore_default_sink_on_stop=False`
  - Switch to `speaker_aec` while running and keep it after shutdown.
- `change_default_sink=False`, `restore_default_sink_on_stop=False`
  - Never change the default sink.

> [!NOTE]
`speaker_aec` is a virtual sink created from the default output device that exists when the server starts.
When `use_echo_cancel=True`, select the desired output device in the GUI or with `pactl` before launching the server.
If you change the output device in the GUI after the server has started, the already-created `speaker_aec` parent device is not updated automatically.

The following parameters relate to echo cancellation and are only active when `use_echo_cancel` is `True`.

| Parameter | Description | Default |
| --- | --- | --- |
| use_echo_cancel | Enable acoustic echo cancellation | False |
| noise_suppression | Suppress background noise | False |
| analog_gain_control | Automatically adjust microphone input volume at the hardware level to prevent clipping and low-volume audio | False |
| digital_gain_control | Automatically adjust microphone input volume at the software level | False |

---
The following parameters control feedback behavior.
They are only active when `use_feedback` is `True`.
Changing these values does not affect the final recognition result.

| Parameter | Description | Default |
| --- | --- | --- |
| vad_name | Voice Activity Detection (VAD) method used for feedback. Using VAD improves feedback accuracy. Setting to `None` disables VAD and performs recognition at the interval specified by the Action Client's `feedback_rate`. | ten_vad |
| hop_size | Chunk size for VAD processing. Accepts `160` or `256`. Smaller values improve responsiveness but increase CPU load. | 256 |
| threshold | Probability threshold for the VAD model. Higher values reduce false positives but may miss soft or faint speech. | 0.5 |
| min_wipe_duration | Minimum speech duration required to trigger recognition. Segments shorter than this value are treated as noise and ignored. | 0.2 |
| extra_audio_duration_sec | Extra audio padding (in seconds) added before and after each feedback segment. | 0.2 |
| max_speech_duration | Maximum duration (in seconds) of a single speech segment before it is forced to finalize. | 30.0 |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Troubleshooting

If you are not getting any recognition results, check the following in order.

1. Confirm the microphone is connected.
    - In Ubuntu Settings, verify that the sound input device is set to the correct microphone.
    - Check that the input volume meter is moving. If it is not, no audio is reaching the microphone.

2. Confirm that recording is working.
    - Use the following steps to check the recorded audio file after performing speech recognition.
    1. Navigate to the directory (path may vary by environment).
        ```sh
        cd ~/colcon_ws/install/sobits_speech_recognition/share/sobits_speech_recognition/sound_file/
        ```
    2. List the contents of the directory.
        ```sh
        ls
        ```
        - If nothing appears, recording is not working.
        - If `final_output.wav` is listed, recording succeeded.
    3. Play the audio file.
        ```sh
        ffplay final_output.wav
        ```
        - If you hear nothing, recording is not working.
        - If the audio is very noisy or distorted, try lowering the input volume.
        - If the audio is clear, the issue is with the speech recognition engine itself.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Milestone

Please see the [Issues page][issues-url] to check current bugs and new feature requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

* [TEN VAD](https://github.com/TEN-framework/ten-vad)
* [module-echo-cancel](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/?utm_source=chatgpt.com#module-echo-cancel)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/sobits_speech_recognition.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/sobits_speech_recognition/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/sobits_speech_recognition.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/sobits_speech_recognition/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/sobits_speech_recognition.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/sobits_speech_recognition/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/sobits_speech_recognition.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/sobits_speech_recognition/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/sobits_speech_recognition.svg?style=for-the-badge
[license-url]: LICENSE
