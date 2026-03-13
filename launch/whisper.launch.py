import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory("sobits_speech_recognition")

    stt_name_arg = DeclareLaunchArgument(
        "stt_name",
        default_value="whisper",
        description="Name of the STT engine to use (e.g., whisper, vosk)"
    )
    model_name_arg = DeclareLaunchArgument(
        "model_name",
        default_value="small",
        description="Model size or path for the STT engine"
    )
    language_arg = DeclareLaunchArgument(
        "language",
        default_value="en",
        description="Language code for recognition (e.g., en, ja)"
    )
    task_arg = DeclareLaunchArgument(
        "task",
        default_value="transcribe",
        description="Task type: transcribe or translate"
    )
    use_prompt_arg = DeclareLaunchArgument(
        "use_prompt",
        default_value="False",
        description="Whether to use initial prompt for Whisper"
    )
    backend_arg = DeclareLaunchArgument(
        "backend",
        default_value="whisper",
        description="Inference backend (whisper, faster-whisper)"
    )
    device_arg = DeclareLaunchArgument(
        "device",
        default_value="",
        description="Device to run inference on (cuda, cpu)"
    )
    compute_type_arg = DeclareLaunchArgument(
        "compute_type",
        default_value="float16",
        description="Quantization type (float16, int8, float32)"
    )
    mic_volume_arg = DeclareLaunchArgument(
        "mic_volume",
        default_value="",
        description="Microphone input volume level"
    )
    use_feedback_arg = DeclareLaunchArgument(
        "use_feedback",
        default_value="True",
        description="Enable or disable intermediate feedback"
    )
    vad_name_arg = DeclareLaunchArgument(
        "vad_name",
        default_value="ten_vad",
        description="Name of the VAD processor to use"
    )
    hop_size_arg = DeclareLaunchArgument(
        "hop_size",
        default_value="256",
        description="Hop size for VAD processing"
    )
    threshold_arg = DeclareLaunchArgument(
        "threshold",
        default_value="0.5",
        description="VAD confidence threshold"
    )
    min_wipe_duration_arg = DeclareLaunchArgument(
        "min_wipe_duration",
        default_value="0.2",
        description="Minimum duration to consider speech finished"
    )
    extra_audio_duration_sec_arg = DeclareLaunchArgument(
        "extra_audio_duration_sec",
        default_value="0.2",
        description="Extra audio to include at the end of segments"
    )
    max_speech_duration_arg = DeclareLaunchArgument(
        "max_speech_duration",
        default_value="30.0",
        description="Maximum duration of a single speech segment"
    )
    use_echo_cancel_arg = DeclareLaunchArgument(
        "use_echo_cancel",
        default_value="False",
        description="Enable acoustic echo cancellation"
    )
    noise_suppression_arg = DeclareLaunchArgument(
        "noise_suppression",
        default_value="False",
        description="Enable noise suppression"
    )
    analog_gain_control_arg = DeclareLaunchArgument(
        "analog_gain_control",
        default_value="False",
        description="Enable analog gain control"
    )
    digital_gain_control_arg = DeclareLaunchArgument(
        "digital_gain_control",
        default_value="False",
        description="Enable digital gain control"
    )
    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace for the nodes"
    )

    stt_server_node = Node(
        package="sobits_speech_recognition",
        executable="stt_server",
        name="stt_server",
        namespace=LaunchConfiguration('namespace'),
        output="screen",
        parameters=[
            os.path.join(pkg_share, "config", "whisper_prompt.yaml"),
            {
                "stt_name": LaunchConfiguration("stt_name"),
                "model_name": LaunchConfiguration("model_name"),
                "language": LaunchConfiguration("language"),
                "task": LaunchConfiguration("task"),
                "device": LaunchConfiguration("device"),
                "backend": LaunchConfiguration("backend"),
                "compute_type": LaunchConfiguration("compute_type"),
                "mic_volume": LaunchConfiguration("mic_volume"),
                "use_feedback": LaunchConfiguration("use_feedback"),
                "min_wipe_duration": LaunchConfiguration("min_wipe_duration"),
                "extra_audio_duration_sec": LaunchConfiguration("extra_audio_duration_sec"),
                "max_speech_duration": LaunchConfiguration("max_speech_duration"),
                "vad_name": LaunchConfiguration("vad_name"),
                "hop_size": LaunchConfiguration("hop_size"),
                "threshold": LaunchConfiguration("threshold"),
                "use_echo_cancel": LaunchConfiguration("use_echo_cancel"),
                "noise_suppression": LaunchConfiguration("noise_suppression"),
                "analog_gain_control": LaunchConfiguration("analog_gain_control"),
                "digital_gain_control": LaunchConfiguration("digital_gain_control"),
                "use_prompt": LaunchConfiguration("use_prompt"),
            }
        ]
    )

    return LaunchDescription([
        stt_name_arg,
        model_name_arg,
        language_arg,
        task_arg,
        use_prompt_arg,
        backend_arg,
        device_arg,
        compute_type_arg,
        mic_volume_arg,
        use_feedback_arg,
        vad_name_arg,
        hop_size_arg,
        threshold_arg,
        min_wipe_duration_arg,
        extra_audio_duration_sec_arg,
        max_speech_duration_arg,
        use_echo_cancel_arg,
        noise_suppression_arg,
        analog_gain_control_arg,
        digital_gain_control_arg,
        namespace_arg,
        stt_server_node
    ])