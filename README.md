<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# SOBITS Speech Recognition


<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#セットアップ">セットアップ</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行操作方法">実行・操作方法</a></li>
    <li><a href="#共通パラメータ">共通パラメータ</a></li>
    <li><a href="#トラブルシューティング">トラブルシューティング</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>

<!-- レポジトリの概要 -->
## 概要

SOBITS Speech Recognitionは様々なSpeech to Text (STT)をROS2のAction通信に対応させ，まとめたものです．

現在以下のSTTに対応しています．

- VOSK 
- Whisper
- NeMo ASR
- Sherpa-ONNX

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- セットアップ -->
## セットアップ
ここで，本レポジトリのセットアップ方法について説明します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 環境条件
まず，以下の環境を整えてから，次のインストール方法に進んでください．
| System  | Version |
| ------------- | ------------- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS | Jazzy Jalisco |
| Python | 3.12 |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### インストール方法
1. ROS2の`src`フォルダに移動します．
    ```sh
    cd ~/colcon_ws/src/
    ```

2. 本レポジトリをcloneします．
    ```sh
    git clone -b jazzy-devel https://github.com/TeamSOBITS/sobits_speech_recognition.git
    ```
3. レポジトリの中へ移動します．
    ```sh
    cd sobits_speech_recognition/
    ```
4. 依存パッケージをインストールします．
    ```sh
    bash install.sh
    ```
5. パッケージをコンパイルします．
    ```sh
    cd ~/colcon_ws/
    ```
    ```sh
    colcon build --symlink-install
    ```
    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- 実行・操作方法 -->
## 実行・操作方法
実行する前に，使用するSTTのモデルをダウンロードする必要があります．

各STT名をクリックするとダウンロードと実行方法を閲覧できます．

| STT名 | 精度 | 認識速度 | 特徴 |
| --- | --- | --- | --- |
| [Whisper](README_detail.md#whisper-top) | ☆☆☆☆ | ☆☆ | 多言語対応，翻訳可，プロンプト可，バッチモデル |
| [Sherpa-ONNX](README_detail.md#sherpa-top) | ☆☆ | ☆☆☆☆ | 3桁以上の数のモデルを使用可能，軽量|
| [NeMo](README_detail.md#nemo-top) | ☆☆☆☆☆ | ☆☆☆☆☆ | 使用メモリ量大，GPU推奨 |
| [VOSK](README_detail.md#vosk-top) | ☆ | ☆☆☆☆ | 多言語対応，超軽量，ストリーミングモデル |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 共通のパラメータ
以下は各launchファイルで共通のパラメータです．

| パラメータ | 説明 | デフォルト値 |
| --- | --- | --- |
| mic_volume	| マイクの入力音量をパーセンテージで設定する．プログラム終了後は元の音量に戻る．例: "150%" | "" |
| use_feedback | Feedbackを使用するかどうか | True |


以下はエコーキャンセルに関するパラメータです． `use_echo_cancel`が`True`のときに有効です．

| パラメータ | 説明 | デフォルト値 |
| --- | --- | --- |
| use_echo_cancel | エコーキャンセルを使用するかどうか | False |
| noise_suppression | ノイズを抑制する．| False |
| analog_gain_control | マイクのハードウェアレベルで入力音量を自動調整する．大きな音は抑え，小さな音は増幅することで音割れや聞き取りにくさを防ぐ． | False |
| digital_gain_control | マイクのソフトウェアレベルで入力音量を自動調整する． | False |


---
以下はFeedbackに関するパラメータです．
`use_feedback`が`True`のときのみ有効です．
以下の値を変更しても最終認識結果には影響しません．

| パラメータ | 説明 | デフォルト値 |
| --- | --- | --- |
| vad_name | フィードバックの際に使用する音声アクティビティ検出(VAD)の手法．VADの使用によりフィードバックの認識精度が向上する．Noneを選択するとVADを使用せずAction Clientで指定したFeedback Rateの秒数ごとに音声認識を行う． | ten_vad |
| hop_size | VADモデルが音声データを処理するチャンク（断片）のサイズ．160 or 256を選択可能．値が小さいほど応答性が上がるが，CPU負荷が増える | 256 |
| threshold | VADモデルが音声を検出するための確率のしきい値．値を高くすると誤検出が減るが，かすれた声や小さな声が無視される可能性がある | 0.5 |
| min_wipe_duration | ノイズを無視し音声認識するために必要な声の最短の長さ．VADが発話と認識した区間がこの秒数より短い場合，ノイズとして無視され音声認識の処理を行わない． | 0.2 |
| extra_audio_duration_sec | フィードバックごとに音声の前後に含める追加のオーディオ時間 | 0.2 | 
| max_speech_duration | 1回の発話を区切る最大秒数．	 | 30.0 | 

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## トラブルシューティング
音声認識結果がないときは以下の順で確認してください．

1. マイクが接続されているか
    - Ubuntuの設定で，サウンドの入力デバイスが使用するマイクになっているか確認してください．
    - その際，入力の音量ゲージが動いているかを確認してください．動いていなければマイクに音が入っていません．

2. 録音できているか
  - 以下のコマンドで，音声認識した際に録音した音声ファイルを確認してください
    1. ディレクトリに移動 (パスは環境によって異なることがあります)
        ```sh
        cd ~/colcon_ws/install/sobits_speech_recognition/share/sobits_speech_recognition/sound_file/
        ```
    2. ディレクトリ内を確認
        ```sh
        ls
        ```
        - 何も表示されない場合，録音できていません．
        - `final_output.wav`と表示された場合は録音できています．
    3. 音声ファイルの再生
        ```sh
        ffplay final_output.wav
        ```
        - 何も聞こえない場合，録音できていません
        - ノイズが大きい場合，音割れしている可能性があります．入力音量を下げてみてください．
        - はっきり聞こえる場合，音声認識に問題があります．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## マイルストーン

現時点のバッグや新規機能の依頼を確認するためにIssueページ をご覧ください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 参考文献
* [TEN VAD](https://github.com/TEN-framework/ten-vad)
* [module-echo-cancel](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/?utm_source=chatgpt.com#module-echo-cancel)

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


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
