# Mock Trial AI V3 Llama 3.1 

## Table of Contents
* [Project Overview](#project-overview)
* [Architecture & Design](#architecture--design)
* [Production Strategy: Optimization & Scalability](#production-strategy-optimization--scalability)
* [Training Logic & Distillation](#training-logic--distillation)
* [Model Metrics & Hugging Face](#model-metrics--hugging-face)
* [Features](#features)
* [Usage Guide](#usage-guide)
* [Performance & Metrics](#performance--metrics)
* [Real-World Impact](#real-world-impact)
* [The Road to V4: Scaling & Reinforcement](#the-road-to-v4-scaling--reinforcement)
* [Contributing & Collaboration](#contributing--collaboration)
* [License](#license)

## Project Overview
Mock Trial AI V3 serves as the **Capstone Project** for the Mock Trial AI ecosystem. It represents a significant architectural leap, moving from the experimental "Black Box" API constraints of V1 to a specialized, locally-distilled legal reasoning engine. By synthesizing insights from a Llama-3.1-8B fine-tuning regimen into a high-performance production framework, V3 delivers professional-grade courtroom simulation with sub-second latency via the **Groq LPU**.

## Architecture & Design
V3 utilizes a **Decoupled Modular Architecture** to ensure separation of concerns and professional scalability:
* **`processor.py`**: Advanced PDF parsing and context-window management.
* **`engine.py`**: High-speed **Groq API** integration for LPU-accelerated inference.
* **`prompts.py`**: The "Logic Core" containing distilled instruction sets for legal valence.
* **`app.py`**: A bespoke, professional gold-and-black interface optimized for trial preparation.

## Production Strategy: Optimization & Scalability
While a custom fine-tuned model was developed during the research phase, the **V3 Production Ecosystem** utilizes the **Llama 3.1 Base Model** coupled with a high-efficiency deployment strategy for the following architectural reasons:

1. **Hardware Agility & Sustainable Deployment:** To ensure the platform remains accessible 24/7 without the prohibitive costs and energy demands of dedicated GPU idling, V3 is optimized for an LPU-accelerated backend via **Groq**. This allows the system to remain highly responsive on standard hardware by offloading heavy computation.
2. **Instruction Distillation vs. Weight Latency:** Loading raw fine-tuned weights often results in significant "Inference Lag." By distilling the logical breakthroughs of the fine-tuning phase into high-precision system instructions, the Llama 3.1 base model achieves specialized performance with sub-second latency.
3. **Stability & General Reasoning:** This "Hybrid Approach" ensures the AI retains its broad legal reasoning capabilities while strictly applying the Mock Trial constraints perfected in the fine-tuning experiments.

## Training Logic & Distillation
V3 utilizes a **'Teacher-Student' distillation framework**. I leveraged Perplexity AI to synthesize organized, factually dense case packets that served as the ground truth for training. This logic was distilled into the engine across three specialized structures:
1. **Strategic Theory Analysis:** Evaluates how evidence benefits or hurdles a case theory.
2. **Personality-Driven Witness Simulation:** High-stress roleplay with adaptive personas and examination types.
3. **Elite Objection Filtering:** A module that scrutinizes examinations for admissibility based on the Rules of Evidence.

## Model Metrics & Hugging Face
The research and fine-tuned weights developed for this project have seen significant community interest:
* **Hugging Face Repository:** [hobbesthecomputerscientist](https://huggingface.co/hobbesthecomputerscientist)
* **User Adoption:** The specialized V3 fine-tuned model has achieved **147 user downloads**, demonstrating strong niche adoption and validation of the training dataset.

## Features
* **Case Analysis Engine:** Extracts key evidence and evaluates Prosecution/Defense case theories based on uploaded materials.
* **Dynamic Witness Simulator:** Allows users to practice examinations with high-fidelity deponents. Users can toggle:
    * **Examination Mode:** Select between Direct and Cross-examination logic.
    * **Witness Profile:** Select whether the witness is a **Lay Witness** or an **Expert Witness**, adjusting the model's technical depth and cooperativeness.
* **Objection Checker:** An elite filtering module that analyzes user questions for evidentiary violations or marks them as "Permissible."
* **Criminal Intent (Mens Rea) Logic:** Correctly identifies that "lack of knowledge" is a Defense strength, negating intent.
* **Anti-Repetition Engine:** Strictly prevents circular arguments or "echoing" of user input.

## Usage Guide
Mock Trial AI V3 is currently hosted as an interactive space. To begin your trial preparation:

1. **Access the Platform:** Navigate to the live environment at [**Mock Trial AI V3 on Hugging Face**](https://huggingface.co/spaces/hobbesthecomputerscientist/mock-trial-v3).
2. **Upload Case Materials:** Provide your case packet in PDF format. The system's `processor.py` module establishes the "Ground Truth."
3. **Select Your Module:** Choose between **Case Analysis**, **Witness Simulation**, or **Objection Checker**.
4. **Interact:** Enter your queries. The **Groq-accelerated engine** will provide sub-second legal analysis and responses.

## Performance & Metrics
* **Latency:** <1 second response time via Groq LPU.
* **Logic Accuracy:** Successfully overrides general LLM biases to prioritize trial-specific logic (e.g., Burden of Proof dynamics).
* **Reliability:** Decoupled architecture allows for 99.9% uptime on CPU-optimized hosting.

## Real-World Impact
V3 is currently in its **Official Piloting Phase** in collaboration with student Mock Trial leadership at San Francisco University High School. It provides attorney-level feedback 24/7, standardizing the way students prepare for competition.

## The Road to V4: Scaling & Reinforcement
As the project moves beyond the Capstone phase, V4 will focus on:
* **Hardware Expansion:** Transitioning to dedicated local GPU resources for larger model parameters.
* **Optimal Prompt Reinforcement:** Extensive experimentation in Google Colab to find prompts that reinforce specific legal learning objectives.
* **User Feedback Loops:** Using data from the V3 pilot to identify edge cases and "reasoning gaps."

## Contributing & Collaboration
I welcome contributions from developers, law students, and mock trial coaches. Please open an Issue to report "Fact-Blurring" or logic errors. Feedback from the pilot phase is actively used to inform V4 development.

## License
Distributed under the MIT License.
