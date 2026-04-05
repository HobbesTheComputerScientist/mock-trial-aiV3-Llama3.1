import gradio as gr
from Processor import extract_text_from_pdf
from Engine import run_inference_prompt
from Prompts import get_analysis_prompt, get_objection_prompt, get_witness_prompt

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

# ── Logic Functions (Connecting UI to Engine) ────────────────────────────────

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
    text = extract_text_from_pdf(file, max_chars=6000)
    # Determine strategy based on exam type
    strategy = "Guarded and Authoritative" if "Cross" in exam_type else "Relatable and Helpful"
    if witness_type == "Expert Witness":
        strategy += " with technical precision."
    
    prompt = get_witness_prompt(text, name, strategy, question)
    return run_inference_prompt(prompt, temperature=0.7)

# ── Build Interface ───────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="Mock Trial AI") as demo:

    gr.HTML("""
    <div id="header">
        <h1>⚖️ Mock Trial AI</h1>
        <p>V3 · Fine-tuned Courtroom Logic · Powered by Groq</p>
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

# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch()
