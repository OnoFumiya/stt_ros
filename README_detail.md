<a name="readme-top"></a>

[JA](README_detail.md) | [EN](README_detail.en.md)

[戻る](README.md)

<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li><a href="#whisper">Whisper</a></li>
    <li><a href="#sherpa-onnx">Sherpa-ONNX</a></li>
    <li><a href="#nemo-asr">NeMo ASR</a></li>
    <li><a href="#vosk">VOSK</a></li>
  </ol>
</details>

<a name="whisper-top"></a>

# Whisper
[Whisper](https://github.com/openai/whisper)はOpenAIが開発したウェブから収集された68万時間に及ぶ多言語・マルチタスクの教師ありデータに基づいて学習した自動音声認識（ASR）システムです．

精度を維持しつつ推論速度の大幅な向上とVRAM消費の削減を実現した[faster-whisper](https://github.com/SYSTRAN/faster-whisper)も使用可能です．

<p align="right">(<a href="#whisper-top">Whisperトップに戻る</a>)</p>

## インストール方法
1. sobits_speech_recognitionのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_speech_recognition/install/
    ```

2. モデルをインストール
    ```bash
    bash whisper.sh
    ```

<p align="right">(<a href="#whisper-top">Whisperトップに戻る</a>)</p>

## モデルのダウンロード方法
1. 以下のコマンドでGUIを起動します．
    ```sh
    ros2 run sobits_speech_recognition dl_whisper
    ```
2. モデルをクリックして選択します．
3. Downloadボタンを押してモデルをダウンロードします．
4. 完了したら閉じます．

- ダウンロード済みモデルは以下のコマンドでも確認できます
    ```sh
    ls ~/.sobits_speech_recognition/whisper_models/
    ```

<p align="right">(<a href="#whisper-top">Whisperトップに戻る</a>)</p>

## 実行・操作方法
1. Ubuntuの設定で，サウンドの入力デバイスを使用するマイクに設定します．

1. [whisper.launch.py](launch/whisper.launch.py)を起動
    ```bash
    ros2 launch sobits_speech_recognition whisper.launch.py
    ```

2. Action Clientを起動
    - timeout_sec: マイクを開く秒数．負の値のときキャンセルを送信するまでフィードバックを返し続ける
    - silent_mode: trueのときは検出時と終了時に音がならない
    - feedback_rate: use_feedbackがTrueでvad_nameがNoneのときに返ってくる途中の音声認識結果の頻度
    ```sh
    ros2 action send_goal /speech_recognition sobits_interfaces/action/SpeechRecognition "timeout_sec: 5
    silent_mode: false
    feedback_rate: 0.5" -f
    ```


<p align="right">(<a href="#whisper-top">Whisperトップに戻る</a>)</p>

## パラメータ
以下は[whisper.launch.py](launch/whisper.launch.py)で設定できるwhisper独自のパラメータです．

| パラメータ | 説明 | デフォルト値 |
| --- | --- | --- |
| model_name | 実行する Whisper モデル *1 | small |
| language | 音声認識を行う言語．[対応言語一覧](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py) | en |
| task | 実行するタスク．`transcribe`（文字起こし）または`translate`（英語への翻訳）を選択可能． | transcribe |
| use_prompt | プロンプトを用いるかどうか | False |
| backend | 使用するバックエンド: `whisper` または `faster-whisper` | whisper |
| device | 使用する計算デバイス (`cpu` or `cuda`)．空の場合，利用可能なGPUがあれば優先的に選択し，なければCPUが自動選択される．| "" |
| compute_type | faster-whisper使用時の計算タイプ: `float16` or `int8_float16` or `int8` | float16 |

*1 サイズが小さい順に``tiny``, ``base``, ``small``, ``medium``, ``large``, ``large-v2``, ``large-v3``, ``large-v3-turbo``があります．
Faster-Whisperも同じモデルサイズに対応しますが，推論は高速かつ省メモリです．
詳細は[モデル一覧](https://huggingface.co/collections/openai/whisper-release-6501bba2cf999715fd953013)を参照してください．

- `model_name`, `backend`, `compute_type`, `use_feedback`, `vad_name`, とエコーキャンセル関連以外のパラメータはlaunchファイル起動後でも変更可能です．
    - 例：min_wipe_durationを0.1に変更する場合
        ```sh
        ros2 param set /stt_server min_wipe_duration 0.1
        ```

<p align="right">(<a href="#whisper-top">Whisperトップに戻る</a>)</p>

## プロンプト
[config/whisper_prompt.yaml](config/whisper_prompt.yaml)でモデルに与える「プロンプト」や文脈を指定します．

プロンプトで特定の単語やフレーズ，固有名詞をモデルに事前に教えることで，モデルの予測を誘導し認識精度が向上します．

<p align="right">(<a href="#whisper-top">Whisperトップに戻る</a>)</p>

<a name="sherpa-top"></a>

# Sherpa-ONNX
Speech Recognition Sherpa ONNXは，ONNX Runtimeを活用した音声認識エンジン [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) をROS 2 のAction通信で利用するためのパッケージです．

CPU環境で動作します．また，ストリーミング認識（逐次認識）とバッチ認識（一括認識）の両方に対応しており，膨大なモデル群から様々なモデルを選択できます．

<p align="right">(<a href="#sherpa-top">Sherpaトップに戻る</a>)</p>

## インストール方法
1. sobits_speech_recognitionのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_speech_recognition/install/
    ```

2. モデルをインストール
    ```bash
    bash sherpa.sh
    ```

<p align="right">(<a href="#sherpa-top">Sherpaトップに戻る</a>)</p>


## モデルのダウンロード方法
1. 以下のコマンドでGUIを起動します．
    ```sh
    ros2 run sobits_speech_recognition dl_sherpa
    ```
  - 起動後は以下が表示されます．
  ![img](docs/sherpa_image.png)
      - Recommended
        - おすすめのモデルを表示します．
      - Search (GitHub)
        - 現在利用可能なモデルをGitHubから取得し表示します．
        - Keywordを3つまで指定してモデル名の絞り込み検索ができます．
        - PC環境で動作しない可能性があるモデルは赤色で表示されます．
      - Installed Models
        - インストール済みのモデル一覧を表示します．
        - インストール済みのモデルはDelete Selectedボタンで削除できます．
    
    <details>
    <summary><b>モデル選定について</b></summary>


    - モデルの性能・リソース要件はサイズや実行環境によって変わります．以下は参考程度にしてください．
    - ストリーミングモデル：音声をリアルタイムで逐次処理するモデルです
      - transducer
        - ストリーミングを主用途とするモデル．オフライン推論にも利用可能だが，主にリアルタイム認識向け．
      - wenet_ctc
        - 安定動作が特徴で，産業用途でも採用されることが多い．
      - zipformer2_ctc
        - 低遅延かつ効率的で，ストリーミング用途に適する（オフラインでも利用可能）．
      - paraformer
        - 低レイテンシで高速に動作する設計．軽量構成も可能で組込み用途にも向く．
      - nemo_ctc
        - 高い認識性能を示すが，特にCPU環境では他の軽量モデルより重くなることがある（GPU環境での利用が想定されることが多い）．
      - t_one_ctc 
        - 非常に軽量な構成を目指したモデル．CPUリソースを節約したい環境に有効．

    - バッチモデル：音声をまとめて処理するモデルです
      - whisper
        - 高精度かつ多言語対応．翻訳機能も備えるが計算負荷は高め（特に大きなモデルはGPU推奨）．
      - sense_voice
        - 感情検知やITN（数値整形）などの付加機能を持ち，多機能な書き起こしが可能．
      - nemo_canary
        - 多言語認識および高精度な翻訳機能を提供するモデル群．
      - transducer
        - ストリーミングを主用途とするが，オフライン処理にも利用可能（両対応）．
      - moonshine
        - 精度と速度のバランスが良いモデル．
      - fire_red_asr
        - 精度は高いがメモリ消費量が大きい傾向にある．
      - paraformer
        - バッチでも動作可能で，計算リソースが限られた環境でも高速に動作する構成が可能．
      - zipformer
        - 効率的で低遅延な構造を持ち，ストリーミング／オフラインの両方で利用可能．
      - dolphin
        - 省メモリで複数言語に対応することを目指した汎用モデル．
      - medasr
        -  医療用語を含む口述作業に適しています．
      - telespeech
        - 大規模データで学習されており，特に中国語などで高い精度を示すことがある．
      - omnilingual
        - 多数の言語(1600以上)に対応することを目的とした多言語ASRモデル．
      - tdnn
        - 古典的かつ軽量なニューラル構造（TDNN系）．ASRの基盤として広く用いられる（特定のタスク専用ではない）．
      - wenet
        - 安定した動作が特徴で，産業用途にも適用されることが多い．
      - nemo
        - 高精度な認識を示すが，処理速度やリソース要件はモデルのサイズや実行環境に依存する．
      - fun_asr_nano
        - LLMを組み合わせた超小型モデル．プロンプトを指定可能．
      
      </details>

2. モデルをクリックして選択します．
3. Downloadボタンを押してモデルをダウンロードし展開します．
4. 完了したらCloseをクリックして閉じます．

- すべてのモデルは[こちら](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models)でも確認できます．

- インストール済みのモデル一覧は以下のコマンドでも確認できます．
    ```sh
    ls ~/.sobits_speech_recognition/sherpa_models/
    ```
<p align="right">(<a href="#sherpa-top">Sherpaトップに戻る</a>)</p>

## 実行・操作方法
1. Ubuntuの設定で，サウンドの入力デバイスを使用するマイクに設定します．

1. [sherpa.launch.py](launch/sherpa.launch.py)を起動
    ```bash
    ros2 launch sobits_speech_recognition sherpa.launch.py
    ```

2. Action Clientを起動
    - timeout_sec: マイクを開く秒数．負の値のときキャンセルを送信するまでフィードバックを返し続ける
    - silent_mode: trueのときは検出時と終了時に音がならない
    - feedback_rate: use_feedbackがTrueでvad_nameがNoneのときに返ってくる途中の音声認識結果の頻度
    ```sh
    ros2 action send_goal /speech_recognition sobits_interfaces/action/SpeechRecognition "timeout_sec: 5
    silent_mode: false
    feedback_rate: 0.5" -f
    ```

<p align="right">(<a href="#sherpa-top">Sherpaトップに戻る</a>)</p>

## パラメータ
Sherpa独自のパラメータは[sherpa.launch.py](launch/sherpa.launch.py)で設定可能なものと，[sherpa_params.yaml](config/sherpa_params.yaml)で設定可能なものの2種類があります．

以下は[sherpa.launch.py](launch/sherpa.launch.py)で設定できるパラメータです．

| パラメータ | 説明 | デフォルト値 |
| --- | --- | --- |
| model_name | 音声認識モデルの名前| sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06 |
| device | 使用する計算デバイス． 現在は`cpu`のみに対応| cpu |
| config_path | 各モデルごとに設定できるパラメータファイルのパス | [config/sherpa_params.yaml](config/sherpa_params.yaml) |

- `model_name`, `use_feedback`, `vad_name`とエコーキャンセル関連以外のパラメータはlaunchファイル起動後でも変更可能です．
  - 例：`min_wipe_duration`を0.1に変更する場合
    ```sh
    ros2 param set /stt_server min_wipe_duration 0.1
    ```
[sherpa_params.yaml](config/sherpa_params.yaml)ではモデルの種類ごとに以下のパラメータを指定できます．

- `global_settings`：全モデル共通のパラメータ群です．

  | パラメータ | 説明 | デフォルト値 |
  | --- | --- | --- |
  | decoding_method | 探索アルゴリズム．`greedy_search` or `modified_beam_search` | greedy_search |
  
    - `greedy_search`: 最も確率の高い候補を1つ選ぶ速度優先モード．低負荷でレスポンスが早いが，精度はやや落ちる．
    - `modified_beam_search`: 複数の候補を並行して探索する精度優先モード．文脈に沿った正確な認識が可能だが，CPU負荷が増える．

- `streaming_models`: 音声をリアルタイムで逐次処理するモデルです．

  <details>
  <summary><b>ストリーミングモデルのパラメータ</b></summary>

  - 以下はストリーミングモデルで共通のパラメータです．

    | パラメータ | 説明と調整の影響 | デフォルト |
    | --- | --- | --- |
    | enable_endpoint_detection | 無音検知による自動区切りの有効化．`true` で発話終了を自動判別． | false |
    | rule1_min_trailing_silence | 発話前の無音判定秒数．値を下げると開始判定が早まるが，ノイズに弱くなる． | 2.4 |
    | rule2_min_trailing_silence | 発話中の区切り秒数．値を下げると認識が早く確定するが，言葉の間で途切れやすくなる． | 1.2 |
    | rule3_min_utterance_length | 最大継続秒数．この値を超えると強制的に認識を確定し，分割する． | 20.0 |
  
  - 以下はモデルごとに個別で設定可能なパラメータです．
    - `num_threads`はモデル種類ごとに設定可能です
      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | num_threads | 推論に使用するCPUスレッド数．上げると処理が早くなるが，CPU負荷が増大する． | 2 |
    - `transducer`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | max_active_paths | 探索する候補の数．値を増やすと精度が上がるが，処理が重くなる．| 4 |
      | blank_penalty | 無音に対するペナルティ．値を上げると，より積極的に文字を出そうとする．| 0.0 |
      | temperature_scale | 予測の多様性の調整．値を上げると自信のある結果が選ばれやすくなる．　| 2.0 |

    - `wenet_ctc`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | chunk_size | 処理の単位（フレーム数）．小さいほど低遅延になるが，文脈の理解度が下がる．| 16 |
      | num_left_chunks | 過去のデータをどれだけ参照するか．増やすと精度が安定するが計算負荷が増える．| 4 |

    - `zipformer2_ctc`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | ctc_max_active |　CTCデコード時に保持する最大状態数．大きいほど計算が精密になる． | 3000|

    - `paraformer`, `nemo_ctc`, `t_one_ctc`に設定できる個別パラメータは`num_threads`のみです．
  
  </details>

---
- `batch_models`: 音声をまとめて処理するモデルです．

  <details>
  <summary><b>バッチモデルの種類ごとのパラメータ</b></summary>
  
  - 以下はモデルごとに個別で設定可能なパラメータです．
    - `num_threads`はモデル種類ごとに設定可能です．

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | num_threads | 推論に使用するCPUスレッド数．上げると処理が早くなるが，CPU負荷が増大する． | 2 |

    - `whisper`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | language | 認識対象の言語（`ja`, `en`等）．`auto`（自動判別）も指定可能．| "en" |
      | task | 処理内容．`transcribe` or `translate`| "transcribe" |
      | tail_paddings | 音声末尾のパディング数．-1 はモデルの最適値を自動使用．| -1 |
    
    - `sense_voice`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | language | 対象言語．`auto`, `zh`, `en`, `ja`, `ko` 等が指定可能 | "auto" |
      | use_itn | 数値や記号を読みやすく整形するか | true |
    
    - `nemo_canary`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | src_lang | 入力音声の言語．| "en" |
      | tgt_lang | 出力テキストの言語 | "en" |

    - `transducer`

      | パラメータ | 説明 | デフォルト値 |
      | --- | --- | --- |
      | max_active_paths | 探索する候補の数．値を増やすと精度が上がるが，処理が重くなる． | 4 |
      | blank_penalty | 無音に対するペナルティ．値を上げると，より積極的に文字を出そうとする． | 0.0 |

    - `moonshine`,  `fire_red_asr`, `paraformer`, `zipformer`, `dolphin`, 
        `medasr`, `telespeech`, `omnilingual`, `tdnn`, `wenet`, `nemo`に設定できる個別パラメータは`num_threads`のみです．
      
  </details>

<p align="right">(<a href="#sherpa-top">Sherpaトップに戻る</a>)</p>

<a name="nemo-top"></a>

# NeMo ASR

Nemo ASRは[NeMo Framework](https://github.com/NVIDIA/NeMo)の自動音声認識（ASR）機能です．GPUを搭載したPCでの使用を推奨します．

[NVIDIA NeMo Framework](https://docs.nvidia.com/nemo-framework/user-guide/latest/overview.html)は，大規模言語モデル（LLM），マルチモーダルモデル（MM），自動音声認識（ASR），テキスト読み上げ（TTS），そしてコンピュータービジョン（CV）の分野に取り組む研究者やPyTorch開発者向けに構築された，スケーラブルでクラウドネイティブな生成AIフレームワークです．


<p align="right">(<a href="#nemo-top">NeMoトップに戻る</a>)</p>

## インストール方法
1. sobits_speech_recognitionのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_speech_recognition/install/
    ```

2. モデルをインストール
    ```bash
    bash nemo.sh
    ```

<p align="right">(<a href="#nemo-top">NeMoトップに戻る</a>)</p>

## 実行・操作方法
1. Ubuntuの設定で，サウンドの入力デバイスを使用するマイクに設定します．

1. [nemo.launch.py](launch/nemo.launch.py)を起動
    ```bash
    ros2 launch sobits_speech_recognition nemo.launch.py
    ```

2. Action Clientを起動
    - timeout_sec: マイクを開く秒数．負の値のときキャンセルを送信するまでフィードバックを返し続ける
    - silent_mode: trueのときは検出時と終了時に音がならない
    - feedback_rate: use_feedbackがTrueでvad_nameがNoneのときに返ってくる途中の音声認識結果の頻度
    ```sh
    ros2 action send_goal /speech_recognition sobits_interfaces/action/SpeechRecognition "timeout_sec: 5
    silent_mode: false
    feedback_rate: 0.5" -f
    ```

<p align="right">(<a href="#nemo-top">NeMoトップに戻る</a>)</p>

## パラメータ
以下は[nemo.launch.py](launch/nemo.launch.py)で設定できるNeMo独自のパラメータです．

| パラメータ名 | 説明 | デフォルト値 |
| --- | --- | --- |
| model_name | 音声認識モデルの名前 *| nvidia/parakeet-tdt-0.6b-v2 |
| device | 使用する計算デバイス (`cpu` or `cuda`)．空の場合，利用可能なGPUがあれば優先的に選択し，なければCPUが自動選択される．| "" |

- モデルを変更する場合，[sobits_speech_recognition/download_utils/dl_nemo.py](sobits_speech_recognition/download_utils/dl_nemo.py)の`nvidia/parakeet-tdt-0.6b-v2`を使用したいモデル名に変更し，以下のコマンドでダウンロードしてください．
    ```sh
    ros2 run sobits_speech_recognition dl_nemo
    ```

- `model_name`, `use_feedback`, `vad_name`とエコーキャンセル関連以外のパラメータはlaunchファイル起動後でも変更可能です．
  - 例：`min_wipe_duration`を0.1に変更する場合
    ```sh
    ros2 param set /stt_server min_wipe_duration 0.1
    ```

<p align="right">(<a href="#nemo-top">NeMoトップに戻る</a>)</p>


<a name="vosk-top"></a>

# VOSK
[Vosk](https://github.com/alphacep/vosk-api)は音声認識ツールキットです．

<p align="right">(<a href="#vosk-top">VOSKトップに戻る</a>)</p>

## インストール方法
1. sobits_speech_recognitionのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_speech_recognition/install/
    ```

2. モデルをインストール
    ```bash
    bash vosk.sh
    ```

<p align="right">(<a href="#vosk-top">VOSKトップに戻る</a>)</p>

## モデルダウンロード方法

1. 以下のコマンドでGUIを起動します．

    ```bash
    ros2 run sobits_speech_recognition dl_vosk 
    ```

> **Note**
> [list of models compatible with Vosk-API](https://alphacephei.com/vosk/models).の言語モデルを使用できます．


2. 以下のようなGUIが表示されます．
    ![img1](docs/vosk_image.png)  
    - 英語を使用する場合：
      - Select language：English
      - Select model：vosk-model-small-en-us-0.15

    - 日本語を使用する場合：
      - Select Model：Japanese
      - Select model：vosk-model-ja-0.22
    - ダウンロードしたモデルは以下のコマンドでも確認できます
      ```sh
      ls ~/.sobits_speech_recognition/vosk_models/
      ```

<p align="right">(<a href="#vosk-top">VOSKトップに戻る</a>)</p>


## 実行・操作方法
1. Ubuntuの設定で，サウンドの入力デバイスを使用するマイクに設定します．

1. [vosk.launch.py](launch/vosk.launch.py)を起動
    ```bash
    ros2 launch sobits_speech_recognition vosk.launch.py
    ```

2. Action Clientを起動
    - timeout_sec: マイクを開く秒数．負の値のときキャンセルを送信するまでフィードバックを返し続ける
    - silent_mode: trueのときは検出時と終了時に音がならない
    - feedback_rate: use_feedbackがTrueでvad_nameがNoneのときに返ってくる途中の音声認識結果の頻度
    ```sh
    ros2 action send_goal /speech_recognition sobits_interfaces/action/SpeechRecognition "timeout_sec: 5
    silent_mode: false
    feedback_rate: 0.5" -f
    ```

<p align="right">(<a href="#vosk-top">VOSKトップに戻る</a>)</p>

## パラメータ
以下は[vosk.launch.py](launch/vosk.launch.py)で設定できるVOSK独自のパラメータです．

| パラメータ名 | 説明 | デフォルト値 |
| --- | --- | --- |
| model| 使用するVOSKモデル．軽量モデルや大容量モデルなどを選択できる．| vosk-model-small-en-us-0.15|

<p align="right">(<a href="#vosk-top">VOSKトップに戻る</a>)</p>