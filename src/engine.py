from unsloth import FastLanguageModel
import torch

print("Loading model — please wait...")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "hobbesthecomputerscientist/Llama-3.1-8B-Mock-Trial-AI-v3",
    max_seq_length = 2048,
    load_in_4bit = True,
    device_map = "sequential",
    dtype = None,
)

FastLanguageModel.for_inference(model)
print("✅ Model loaded successfully!")

def run_inference(prompt: str, max_new_tokens: int = 512) -> str:
    """Run the model on a prompt and return the response text."""
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=2048,
    ).to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode only the newly generated tokens
    new_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
