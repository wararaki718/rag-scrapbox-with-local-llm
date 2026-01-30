import os

from .encoder import SpladeEncoder

MODEL_ID = os.getenv("MODEL_ID", "hotchpotch/japanese-splade-v2")
encoder = SpladeEncoder(model_id=MODEL_ID)


def get_encoder() -> SpladeEncoder:
    return encoder
