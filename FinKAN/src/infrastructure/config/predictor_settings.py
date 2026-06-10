from dataclasses import dataclass


@dataclass(frozen=True)
class PredictorSettings:
    """Configuração tipada e validada usada pelo Predictor em produção."""

    seq_len: int
    pred_len: int
    n_targets: int
    scale: bool = True
    scalers_path: str = "scalers/"

    @classmethod
    def from_config(cls, config: dict) -> "PredictorSettings":
        try:
            return cls(
                seq_len=int(config["seq_len"]),
                pred_len=int(config["pred_len"]),
                n_targets=int(config["n_targets"]),
                scale=bool(config.get("scale", True)),
                scalers_path=str(config.get("scalers_path", "scalers/")),
            )
        except KeyError as e:
            raise ValueError(f"Configuração obrigatória ausente para o Predictor: {e}") from e
