import os
import torch
import nemo.collections.asr as nemo_asr
from omegaconf import OmegaConf, open_dict
from .base_engine import BaseEngine


class NemoEngine(BaseEngine):
    def __init__(self, node):
        super().__init__(node)
        self.is_streamable = False
        self.use_external_vad = True
        self._load_model()
        self.node.get_logger().info(
            f"[NeMo] Engine Ready. "
            f"(Model: {self.model_name}, "
            f"Type: {type(self.model).__name__}, "
            f"Device: {self.model.device})"
        )

    def _load_model(self):
        self.node.declare_parameter('model_name', 'nvidia/parakeet-tdt-0.6b-v2')
        self.node.declare_parameter('device', '')

        self.model_name = self.node.get_parameter('model_name').value
        device_param = self.node.get_parameter('device').value
        device = device_param if device_param else (
            "cuda:0" if torch.cuda.is_available() else "cpu"
        )

        try:
            self.node.get_logger().info(f"[NeMo] Loading model: {self.model_name}")
            self.model = nemo_asr.models.ASRModel.from_pretrained(
                model_name=self.model_name
            ).to(torch.device(device))
            self.model.eval()

            model_class_name = type(self.model).__name__
            is_tdt = 'TDT' in model_class_name or 'tdt' in self.model_name.lower()
            if is_tdt:
                decoding_cfg = OmegaConf.create({
                    "strategy": "greedy",
                    "model_type": "tdt",
                    "durations": [0, 1, 2, 3, 4],
                    "greedy": {
                        "max_symbols": 10,
                        "use_cuda_graph_decoder": False,
                    },
                })
                self.model.change_decoding_strategy(decoding_cfg)
            self.node.get_logger().info(
                f"[NeMo] Loaded as {model_class_name} on {self.model.device}, "
                f"TDT={'Yes' if is_tdt else 'No'}, CUDA Graphs disabled."
            )

        except Exception as e:
            self.node.get_logger().fatal(f"[NeMo] Model loading failed: {e}")
            raise

    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            return ""

        try:
            with torch.no_grad():
                results = self.model.transcribe(
                    [audio_path],
                    batch_size=1,
                    verbose=False,
                )

            if not results:
                return ""

            result = results[0]

            if hasattr(result, 'text'):
                return result.text.strip()
            if isinstance(result, str):
                return result.strip()
            return str(result).strip()

        except Exception as e:
            self.node.get_logger().error(f"[NeMo] Transcription error: {e}")
            return ""