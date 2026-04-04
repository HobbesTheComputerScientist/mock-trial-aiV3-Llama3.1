def run_inference_prompt(prompt: str, temperature: float = 0.7, max_new_tokens: int = 512) -> str:
    """Run inference using a plain formatted prompt string."""
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
            temperature=temperature,
            do_sample=temperature > 0.01,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


# ── Tab 1: Case Analysis ──────────────────────────────────────────────────────
def case_analysis(file_obj, question: str) -> str:
    if not question.strip():
        return "⚠️ Please enter a question."

    case_text = extract_text_from_pdf(file_obj)

    prompt = (
        "You are a Senior Prosecutor/Defender. Based ONLY on the provided statement below, "
        "list the 3 strongest pieces of physical evidence (DNA, Serial Numbers, fingerprints, "
        "ballistics, surveillance footage, etc.) and explain in detail why each piece proves "
        "guilt Beyond a Reasonable Doubt. DO NOT mention any evidence not explicitly found in "
        f"the text below.\n\n"
        f"Case Statement:\n{case_text}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    return run_inference_prompt(prompt, temperature=0.2)


# ── Tab 2: Objection Checker ──────────────────────────────────────────────────
def objection_checker(exam_question: str, exam_type: str) -> str:
    if not exam_question.strip():
        return "⚠️ Please enter an examination question."

    prompt = (
        "You are an elite Trial Attorney. Your goal is to monitor the Opposing Counsel's "
        "examination for any violations of the Rules of Evidence. If the question is "
        "objectionable, state the objection clearly with the legal grounds. If the question "
        "is permissible, respond with No objection. If objecting, explain why the question "
        "is objectionable and what the attorney must do to fix the question. If no objection, "
        "explain why the evidence is admissible.\n\n"
        f"Examination Type: {exam_type}\n"
        f"Question: \"{exam_question}\"\n\n"
        "Analysis:"
    )
    return run_inference_prompt(prompt, temperature=0.01)


# ── Tab 3: Witness Simulator ──────────────────────────────────────────────────
def witness_simulator(
    exam_type: str,
    witness_type: str,
    witness_name: str,
    statement_file,
    question: str,
) -> str:
    if not question.strip():
        return "⚠️ Please enter a question to ask the witness."
    if not witness_name.strip():
        witness_name = "the witness"

    case_text = extract_text_from_pdf(statement_file)

    if witness_type == "Expert Witness":
        if exam_type == "Direct Examination":
            strategy = (
                "The Confident Professional: You are organized, authoritative, and calm. "
                "Speak in structured, logical sequences. Reference dates and exhibits precisely. "
                "You are helpful and want to provide clarity for the jury."
            )
            t = 0.2
        else:
            strategy = (
                "The Guarded Authority: You are professional but wary. You provide short, "
                "precise answers. Do not volunteer logical sequences. You protect your "
                "professional credibility and don't give the opposing lawyer an inch."
            )
            t = 0.5
    else:  # Non-Expert Witness
        if exam_type == "Direct Examination":
            strategy = (
                "The Relatable Victim: You are emotional, slow-paced, and vulnerable. "
                "Use sensory details and personal weight. Make the jury feel the human "
                "experience. You are forthcoming and helpful."
            )
            t = 0.4
        else:
            strategy = (
                "The Wrongly Accused: You are defensive and feel pressured. You stick to "
                "your story firmly but stay emotional. You feel like you are being 'drilled' "
                "and respond with guarded, self-protective answers."
            )
            t = 0.6

    prompt = (
        f"Roleplay: You are the witness {witness_name}.\n"
        f"Strategy: {strategy}\n"
        f"Strict Fact Base: {case_text}\n\n"
        f"Attorney ({exam_type}): {question}\n"
        f"{witness_name}:"
    )
    return run_inference_prompt(prompt, temperature=t)
