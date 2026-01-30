import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer


class SpladeEncoder:
    def __init__(
        self, model_id: str = "hotchpotch/japanese-splade-v2", device: str = None
    ):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForMaskedLM.from_pretrained(model_id).to(self.device)
        self.model.eval()

    def encode(self, text: str, return_tokens: bool = True):
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

            # SPLADE log(1 + ReLU(logits))
            # Max pooling over the sequence dimension
            # Ensure attention mask is used to avoid padding tokens
            log_relu_logits = torch.log(1 + torch.relu(logits))
            if "attention_mask" in inputs:
                log_relu_logits = log_relu_logits * inputs["attention_mask"].unsqueeze(
                    -1
                )

            sparse_vector = torch.max(log_relu_logits, dim=1).values.squeeze()

        # Extract non-zero elements and their indices
        indices = torch.nonzero(sparse_vector).flatten()
        values = sparse_vector[indices]

        # Convert to dictionary
        if return_tokens:
            # {token: weight}
            result = {
                self.tokenizer.convert_ids_to_tokens(int(idx.item())): float(val.item())
                for idx, val in zip(indices, values, strict=False)
            }
        else:
            # {token_id: weight}
            result = {
                str(idx.item()): float(val.item())
                for idx, val in zip(indices, values, strict=False)
            }

        return result

    def get_tokens_and_weights(self, sparse_dict: dict):
        """Helper to convert token IDs back to tokens.

        Handles both ID and token keys for backward compatibility.
        """
        new_dict = {}
        for k, v in sparse_dict.items():
            try:
                # If k is an ID
                token = self.tokenizer.convert_ids_to_tokens(int(k))
                new_dict[token] = v
            except (ValueError, TypeError):
                # If k is already a token
                new_dict[k] = v
        return new_dict
