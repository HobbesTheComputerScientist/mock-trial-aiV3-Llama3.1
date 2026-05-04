# ── SYSTEM MESSAGE ──
SYSTEM_MESSAGE = (
    "You are a professional Mock Trial Legal Assistant. "
    "STRICT RULES: 1. Do not repeat yourself. 2. Be concise. "
    "3. Never restate or 'echo' the user's question in your opening. " 
    "4. If you finish your point, stop immediately. 5. Never loop phrases."
)
 
# ── CASE ANALYSIS PROMPT ──
def get_analysis_prompt(case_text, question):
    return (
        f"You are a Senior Prosecutor/Defender. Based ONLY on the provided statement below, "
        f"list the 3 strongest pieces of physical evidence (DNA, Serial Numbers, fingerprints, "
        f"ballistics, surveillance footage, etc.).\n\n"
        f"CRITICAL LOGIC RULES:\n"
        f"1. VALENCE ACCURACY: You must correctly identify which side a fact favors. "
        f"Remember: A defendant's 'lack of knowledge' or 'confusion' is a STRENGTH for the Defense (negates intent) "
        f"and a HURDLE for the Prosecution. Do not misattribute these benefits.\n"
        f"2. DIVERSITY OF ARGUMENT: Once you have analyzed a piece of evidence, you are strictly forbidden "
        f"from mentioning it again. Do not pivot back to previous points. Every sentence must provide NEW insight.\n"
        f"3. NO REPETITION/LOOPING: Do not use circular phrasing or repeat your concluding thoughts. "
        f"If the analysis is complete, stop immediately.\n\n"
        f"Remember: Proving the defendant has intent and premeditation helps Prosecution. Proving the defendant was unintentional and did not premeditate helps Defense\n\n"
        f"FULL CASE STATEMENT:\n{case_text}\n\n"
        f"USER SPECIFIC QUESTION: {question}\n\n"
        "LEGAL ANALYSIS:"
    )
 
# ── OBJECTION CHECKER PROMPT ──
def get_objection_prompt(question, exam_type):
    return (
        f"You are an elite Trial Attorney. Your goal is to monitor the Opposing Counsel's "
        f"examination for any violations of the Rules of Evidence. "
        f"EXAM TYPE: {exam_type}\n"
        f"QUESTION: \"{question}\"\n\n"
        "TASK: If the question is objectionable, state the objection clearly with the legal grounds. "
        "If the question is permissible, respond with 'No objection.' "
        "If objecting, explain why the question is objectionable and what the attorney must do to fix the question. "
        "If no objection, explain why the evidence is admissible.\n\n"
        "RULING:"
    )
 
# ── WITNESS SIMULATOR PROMPT ──
def get_witness_prompt(case_text, name, strategy, question):
    return (
        f"FACT BASE: {case_text}\n\n"
        f"ROLEPLAY: You are the witness {name}. Your strategy is to be {strategy}. "
        "Answer the question in character. Stay under 100 words. Do not repeat the lawyer's question.\n\n"
        f"ATTORNEY QUESTION: {question}\n"
        f"{name}:"
    )
 
# ── QUESTION SIMULATOR PROMPT ──
# Generates a practice examination question from a case packet for a specific witness
def get_question_simulator_prompt(case_text, witness_name, exam_type, difficulty):
    difficulty_guide = {
        "Easy": "straightforward, open-ended questions (who, what, where, when) that establish basic facts.",
        "Medium": "probing questions that test recall and consistency with the statement.",
        "Hard": "aggressive or complex questions that attempt to expose inconsistencies, test credibility, or introduce impeachment."
    }.get(difficulty, "probing questions that test recall and consistency.")
 
    return (
        f"You are an experienced trial attorney preparing to examine witness: {witness_name}.\n"
        f"EXAMINATION TYPE: {exam_type}\n"
        f"DIFFICULTY: {difficulty} — Generate {difficulty_guide}\n\n"
        f"WITNESS STATEMENT / CASE PACKET (relevant sections):\n{case_text}\n\n"
        f"TASK: Generate ONE realistic {exam_type} question directed at {witness_name}. "
        f"The question must be directly grounded in the facts of the statement above. "
        f"Do NOT include commentary, preamble, or explanation — output only the question itself.\n\n"
        f"QUESTION:"
    )
 
# ── OBJECTION SIMULATOR PROMPT ──
# Generates an objectionable (or clean) question for lawyers to practice objecting to
def get_objection_simulator_prompt(exam_type):
    return (
        f"You are a trial attorney conducting a {exam_type}.\n\n"
        f"TASK: Generate ONE examination question that may or may not be objectionable. "
        f"Vary the type: sometimes generate leading questions (on direct), hearsay, compound questions, "
        f"argumentative questions, speculation, or questions assuming facts not in evidence. "
        f"Occasionally generate a clean, unobjectionable question to keep the lawyer honest.\n\n"
        f"STRICT RULES:\n"
        f"- Output ONLY the question. No labels, no explanations, no preamble.\n"
        f"- Do NOT include a witness name or case facts — this is a general drill.\n"
        f"- The question should sound realistic and courtroom-appropriate.\n\n"
        f"QUESTION:"
    )
 
# ── OBJECTION SIMULATOR FEEDBACK PROMPT ──
# Evaluates the user's objection against the generated question
def get_objection_feedback_prompt(generated_question, exam_type, user_objection):
    return (
        f"You are a strict mock trial judge evaluating a law student's objection.\n\n"
        f"EXAM TYPE: {exam_type}\n"
        f"ATTORNEY'S QUESTION: \"{generated_question}\"\n"
        f"STUDENT'S OBJECTION: \"{user_objection}\"\n\n"
        f"TASK: Evaluate whether the student's objection is correct.\n"
        f"1. STATE whether the objection is SUSTAINED or OVERRULED.\n"
        f"2. EXPLAIN the correct legal basis — what is objectionable (or not) about the question.\n"
        f"3. If the student's objection was wrong or incomplete, explain what the correct objection should have been.\n"
        f"4. If no objection was warranted, explain why the question was permissible.\n\n"
        f"NOTE: The following objections are in scope for this drill: Leading, Hearsay, Compound, "
        f"Argumentative, Speculation, Assumes Facts Not in Evidence, Calls for a Narrative.\n\n"
        f"JUDGE'S RULING:"
    )
