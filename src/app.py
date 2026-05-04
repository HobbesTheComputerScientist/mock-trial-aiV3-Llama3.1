import gradio as gr
from Processor import extract_text_from_pdf, extract_witness_text
from Engine import run_inference_prompt
from Prompts import (
    get_analysis_prompt,
    get_objection_prompt,
    get_witness_prompt,
    get_question_simulator_prompt,
    get_objection_simulator_prompt,
    get_objection_feedback_prompt,
)
 
# ── Shared CSS (Custom Design) ───────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap');
:root {
    --bg:          #0d0d0f;
    --surface:     #14141a;
    --surface2:    #1c1c26;
    --border:      #2a2a38;
    --gold:        #c9a84c;
    --gold-light:  #e2c97e;
    --text:        #e8e4d8;
    --text-muted:  #7a7870;
    --accent:      #6b3e26;
}
body, .gradio-container {
    background: var(--bg) !important;
    font-family: 'Source Serif 4', serif !important;
    color: var(--text) !important;
}
#header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
#header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: var(--gold);
    margin: 0 0 .3rem;
    letter-spacing: .04em;
}
#header p {
    color: var(--text-muted);
    font-style: italic;
    font-size: .95rem;
    margin: 0;
}
.tab-nav button {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: .95rem !important;
    padding: .55rem 1.3rem !important;
    border-radius: 4px 4px 0 0 !important;
    transition: all .2s;
}
.tab-nav button.selected, .tab-nav button:hover {
    background: var(--surface2) !important;
    color: var(--gold-light) !important;
    border-bottom-color: var(--surface2) !important;
}
textarea, input[type=text], .gr-input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'Source Serif 4', serif !important;
    border-radius: 6px !important;
}
label span, .gr-form label {
    color: var(--text-muted) !important;
    font-size: .8rem !important;
    text-transform: uppercase;
    letter-spacing: .08em;
}
button.primary, button[variant=primary], .gr-button-primary {
    background: linear-gradient(135deg, var(--gold) 0%, #a07830 100%) !important;
    border: none !important;
    color: #0d0d0f !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    letter-spacing: .06em !important;
    border-radius: 6px !important;
    padding: .6rem 1.6rem !important;
    transition: opacity .2s;
}
.output-box textarea {
    background: #10101a !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    line-height: 1.7 !important;
}
.upload-zone {
    border: 1px dashed var(--border) !important;
    background: var(--surface) !important;
    border-radius: 8px !important;
}
"""
 
# ── State for Objection Simulator ────────────────────────────────────────────
_objection_sim_state = {"current_question": "", "exam_type": "Direct Examination"}
 
# ── Logic Functions ───────────────────────────────────────────────────────────
 
def case_analysis(file, question):
    if not file: return "Please upload a statement PDF."
    text = extract_text_from_pdf(file)
    prompt = get_analysis_prompt(text, question)
    return run_inference_prompt(prompt, temperature=0.2)
 
 
def objection_checker(question, exam_type):
    if not question: return "Please enter a question to check."
    prompt = get_objection_prompt(question, exam_type)
    return run_inference_prompt(prompt, temperature=0.1)
 
 
def witness_simulator(exam_type, witness_type, name, file, question):
    if not file: return "Please upload the witness statement PDF."
    # Use witness-aware segmenter if a name is provided
    if name and name.strip():
        text = extract_witness_text(file, witness_name=name, max_chars=6000)
    else:
        text = extract_text_from_pdf(file, max_chars=6000)
    strategy = "Guarded and Authoritative" if "Cross" in exam_type else "Relatable and Helpful"
    if witness_type == "Expert Witness":
        strategy += " with technical precision."
    prompt = get_witness_prompt(text, name or "the witness", strategy, question)
    return run_inference_prompt(prompt, temperature=0.7)
 
 
def question_simulator_generate(file, witness_name, exam_type, difficulty):
    """Generates a practice question from the case packet for the specified witness."""
    if not file: return "Please upload a case packet PDF."
    if not witness_name or not witness_name.strip():
        return "Please enter a witness name to target the question."
    text = extract_witness_text(file, witness_name=witness_name, max_chars=6000)
    prompt = get_question_simulator_prompt(text, witness_name, exam_type, difficulty)
    return run_inference_prompt(prompt, temperature=0.8)
 
 
def objection_sim_generate(exam_type):
    """Generates a question for the objection drill. Returns the question and stores it in state."""
    prompt = get_objection_simulator_prompt(exam_type)
    question = run_inference_prompt(prompt, temperature=0.9)
    _objection_sim_state["current_question"] = question
    _objection_sim_state["exam_type"] = exam_type
    return question, ""  # Reset feedback when a new question is generated
 
 
def objection_sim_evaluate(user_objection, exam_type):
    """Evaluates the user's objection against the stored question."""
    question = _objection_sim_state.get("current_question", "")
    if not question:
        return "Please generate a question first."
    if not user_objection or not user_objection.strip():
        return "Please enter your objection before submitting."
    prompt = get_objection_feedback_prompt(question, exam_type, user_objection)
    return run_inference_prompt(prompt, temperature=0.1)
 
 
# ── Build Interface ───────────────────────────────────────────────────────────
with gr.Blocks(title="Mock Trial AI") as demo:
 
    gr.HTML("""
    <div id="header">
        <h1>⚖️ Mock Trial AI</h1>
        <p>V4 · Fine-tuned Courtroom Logic · Powered by Llama 3.1 • Optimized via Groq LPU</p>
    </div>
    """)
 
    with gr.Tabs():
 
        # ── Tab 1: Case Analysis ──────────────────────────────────────────────
        with gr.TabItem("📄 Case Analysis"):
            gr.HTML("""
                <div style="background-color: #1c1c26; padding: 12px; border-radius: 8px; border: 1px solid #c9a84c; margin-bottom: 20px;">
                    <p style="color: #e2c97e; margin: 0; font-size: 0.95rem; font-family: 'Source Serif 4', serif;">
                        ⚖️ <strong>PRO-TIP:</strong> Optimized for <strong>individual witness statements</strong>. 
                        Uses an 8k character intelligent segmenter.
                    </p>
                </div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    ca_file = gr.File(label="Statement PDF", file_types=[".pdf"], elem_classes=["upload-zone"])
                    ca_question = gr.Textbox(label="Strategic Question", placeholder="e.g. Analyze the physical evidence...", lines=4)
                    ca_btn = gr.Button("Execute Analysis", variant="primary")
                with gr.Column(scale=1):
                    ca_output = gr.Textbox(label="AI Legal Analysis", lines=18, interactive=False, elem_classes=["output-box"])
            ca_btn.click(fn=case_analysis, inputs=[ca_file, ca_question], outputs=ca_output)
 
        # ── Tab 2: Objection Checker ──────────────────────────────────────────
        with gr.TabItem("🔨 Objection Checker"):
            with gr.Row():
                with gr.Column(scale=1):
                    oc_question = gr.Textbox(label="Examination Question", placeholder='e.g. "Isn\'t it true..."', lines=4)
                    oc_type = gr.Radio(choices=["Direct Examination", "Cross Examination"], value="Direct Examination", label="Examination Type")
                    oc_btn = gr.Button("Check for Objections", variant="primary")
                with gr.Column(scale=1):
                    oc_output = gr.Textbox(label="Objection Analysis", lines=16, interactive=False, elem_classes=["output-box"])
            oc_btn.click(fn=objection_checker, inputs=[oc_question, oc_type], outputs=oc_output)
 
        # ── Tab 3: Witness Simulator ──────────────────────────────────────────
        with gr.TabItem("🎭 Witness Simulator"):
            gr.HTML("""
                <div style="background-color: #1c1c26; padding: 12px; border-radius: 8px; border: 1px solid #c9a84c; margin-bottom: 20px;">
                    <p style="color: #e2c97e; margin: 0; font-size: 0.95rem; font-family: 'Source Serif 4', serif;">
                        🔍 <strong>PRO-TIP:</strong> Enter the witness name to activate <strong>smart page targeting</strong> — 
                        only pages mentioning that witness will be analyzed.
                    </p>
                </div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    ws_exam_type = gr.Radio(choices=["Direct Examination", "Cross Examination"], value="Direct Examination", label="Examination Type")
                    ws_witness_type = gr.Radio(choices=["Expert Witness", "Non-Expert Witness"], value="Non-Expert Witness", label="Witness Type")
                    ws_name = gr.Textbox(label="Witness Name", placeholder="e.g. Dr. Jane Smith")
                    ws_statement = gr.File(label="Witness Statement PDF", file_types=[".pdf"], elem_classes=["upload-zone"])
                    ws_question = gr.Textbox(label="Your Question", placeholder="Ask the witness...", lines=3)
                    ws_btn = gr.Button("Ask Witness", variant="primary")
                with gr.Column(scale=1):
                    ws_output = gr.Textbox(label="Witness Response", lines=16, interactive=False, elem_classes=["output-box"])
            ws_btn.click(fn=witness_simulator, inputs=[ws_exam_type, ws_witness_type, ws_name, ws_statement, ws_question], outputs=ws_output)
 
        # ── Tab 4: Question Simulator ─────────────────────────────────────────
        with gr.TabItem("❓ Question Simulator"):
            gr.HTML("""
                <div style="background-color: #1c1c26; padding: 12px; border-radius: 8px; border: 1px solid #c9a84c; margin-bottom: 20px;">
                    <p style="color: #e2c97e; margin: 0; font-size: 0.95rem; font-family: 'Source Serif 4', serif;">
                        🎯 <strong>WITNESS PRACTICE:</strong> Upload your case packet, specify a witness, 
                        and the AI will generate a realistic examination question for you to practice answering.
                    </p>
                </div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    qs_file = gr.File(label="Case Packet PDF", file_types=[".pdf"], elem_classes=["upload-zone"])
                    qs_witness_name = gr.Textbox(label="Witness Name", placeholder="e.g. Officer James Reyes")
                    qs_exam_type = gr.Radio(
                        choices=["Direct Examination", "Cross Examination"],
                        value="Direct Examination",
                        label="Examination Type"
                    )
                    qs_difficulty = gr.Radio(
                        choices=["Easy", "Medium", "Hard"],
                        value="Medium",
                        label="Difficulty"
                    )
                    qs_btn = gr.Button("Generate Question", variant="primary")
                with gr.Column(scale=1):
                    qs_output = gr.Textbox(
                        label="Practice Question",
                        lines=6,
                        interactive=False,
                        elem_classes=["output-box"],
                        placeholder="Your question will appear here..."
                    )
                    gr.HTML("""
                        <div style="margin-top: 12px; background-color: #1c1c26; padding: 12px; border-radius: 8px; border: 1px solid #2a2a38;">
                            <p style="color: #7a7870; margin: 0; font-size: 0.85rem; font-style: italic; font-family: 'Source Serif 4', serif;">
                                💡 Use this question to practice your witness testimony. 
                                Switch to <strong>Witness Simulator</strong> to get AI feedback on your answer.
                            </p>
                        </div>
                    """)
            qs_btn.click(fn=question_simulator_generate, inputs=[qs_file, qs_witness_name, qs_exam_type, qs_difficulty], outputs=qs_output)
 
        # ── Tab 5: Objection Simulator ────────────────────────────────────────
        with gr.TabItem("⚡ Objection Simulator"):
            gr.HTML("""
                <div style="background-color: #1c1c26; padding: 12px; border-radius: 8px; border: 1px solid #c9a84c; margin-bottom: 20px;">
                    <p style="color: #e2c97e; margin: 0; font-size: 0.95rem; font-family: 'Source Serif 4', serif;">
                        ⚡ <strong>OBJECTION DRILL:</strong> The AI generates a question — you decide whether to object and on what grounds. 
                        In scope: <strong>Leading · Hearsay · Compound · Argumentative · Speculation · Assumes Facts Not in Evidence · Calls for a Narrative</strong>
                    </p>
                </div>
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    os_exam_type = gr.Radio(
                        choices=["Direct Examination", "Cross Examination"],
                        value="Direct Examination",
                        label="Examination Type"
                    )
                    os_gen_btn = gr.Button("Generate Question", variant="primary")
                    os_generated = gr.Textbox(
                        label="Attorney's Question",
                        lines=4,
                        interactive=False,
                        elem_classes=["output-box"],
                        placeholder="Click 'Generate Question' to begin the drill..."
                    )
                    os_objection_input = gr.Textbox(
                        label="Your Objection",
                        placeholder='e.g. "Objection, leading." or "No objection." or "Objection, hearsay."',
                        lines=3
                    )
                    os_submit_btn = gr.Button("Submit Objection", variant="primary")
                with gr.Column(scale=1):
                    os_feedback = gr.Textbox(
                        label="Judge's Ruling",
                        lines=16,
                        interactive=False,
                        elem_classes=["output-box"],
                        placeholder="The judge's ruling will appear here after you submit your objection..."
                    )
 
            os_gen_btn.click(
                fn=objection_sim_generate,
                inputs=[os_exam_type],
                outputs=[os_generated, os_feedback]
            )
            os_submit_btn.click(
                fn=objection_sim_evaluate,
                inputs=[os_objection_input, os_exam_type],
                outputs=os_feedback
            )
 
# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        css=CSS,
        footer_links=["gradio", "settings"]
    )
 
