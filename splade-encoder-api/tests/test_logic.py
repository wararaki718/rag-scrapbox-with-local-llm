from unittest.mock import MagicMock

import torch

from api.encoder import SpladeEncoder


def test_encoder_logic():
    # Mock the tokenizer and model to avoid downloading/running them
    encoder = SpladeEncoder.__new__(SpladeEncoder)
    encoder.device = "cpu"

    def mock_convert(idx):
        return f"token_{idx}"

    encoder.tokenizer = MagicMock()
    encoder.tokenizer.convert_ids_to_tokens = mock_convert
    encoder.model = MagicMock()

    # Mock tokenizer output
    mock_inputs = {
        "input_ids": torch.tensor([[1, 2, 3]]),
        "attention_mask": torch.tensor([[1, 1, 1]]),
    }

    # Create an object that has a .to() method and returns our mock_inputs dict
    class MockBatch(dict):
        def to(self, device):
            return self

    encoder.tokenizer.return_value = MockBatch(mock_inputs)

    # Mock model output
    mock_output = MagicMock()
    # Logits: [batch=1, seq=3, vocab=5]
    mock_output.logits = torch.tensor(
        [
            [
                [0.1, 0.2, 0.3, 0.4, 0.5],
                [0.5, 0.4, 0.3, 0.2, 0.1],
                [0.1, 0.5, 0.1, 0.5, 0.1],
            ]
        ]
    )
    encoder.model.return_value = mock_output

    # Run encode
    # ReLU(logits) -> all positive here
    # log(1+ReLU) -> some values
    # Max over seq dim
    result = encoder.encode("dummy text")

    assert isinstance(result, dict)
    assert len(result) > 0
    for k, v in result.items():
        assert isinstance(k, str)
        assert isinstance(v, float)
    print("Test passed!")


if __name__ == "__main__":
    test_encoder_logic()
