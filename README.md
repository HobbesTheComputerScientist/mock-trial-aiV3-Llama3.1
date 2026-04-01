# mock-trial-aiV3-Llama3.1
Fine-tuned legal AI for mock trial witness simulation and objection detection

Installation
To set up the V3 Inference Engine, we recommend using a CUDA-enabled environment:

# Install specialized kernels for Llama 3.1
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes

# Install standard dependencies
pip install -r requirements.txt
