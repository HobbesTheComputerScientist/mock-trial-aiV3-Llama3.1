import gradio as gr

# ── Shared CSS ────────────────────────────────────────────────────────────────
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

/* Header */
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

/* Tabs */
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

/* Inputs */
textarea, input[type=text], .gr-input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'Source Serif 4', serif !important;
    border-radius: 6px !important;
}
textarea:focus, input:focus {
    border-color: var(--gold) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,.15) !important;
}

/* Labels */
label span, .gr-form label {
    color: var(--text-muted) !important;
    font-size: .8rem !important;
    text-transform: uppercase;
    letter-spacing: .08em;
}

/* Radio / Checkbox */
.gr-radio label, .gr-checkbox label {
    color: var(--text) !important;
}

/* Buttons */
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
button.primary:hover { opacity: .88 !important; }

/* Output boxes */
.output-box textarea {
    background: #10101a !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    line-height: 1.7 !important;
}

/* Upload zone */
.upload-zone {
    border: 1px dashed var(--border) !important;
    background: var(--surface) !important;
    border-radius: 8px !important;
}
.upload-zone:hover {
    border-color: var(--gold) !important;
}

/* Divider */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
"""

# ── Build Interface ───────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="Mock Trial AI") as demo:

    gr.HTML("""
    <div id="header">
        <h1>⚖️ Mock Trial AI</h1>
        <p>Powered by Llama-3.1-8B · Fine-tuned for courtroom excellence</p>
    </div>
    """)

    with gr.Tabs():

        # ── Tab 1: Case Analysis ──────────────────────────────────────────────
        with gr.TabItem("📄 Case Analysis"):
            gr.Markdown(
                "**Upload your case packet and ask any question about the facts, "
                "legal arguments, or strategy.**"
            )
            with gr.Row():
                with gr.Column(scale=1):
                    ca_file = gr.File(
                        label="Case Packet (PDF)",
                        file_types=[".pdf"],
                        elem_classes=["upload-zone"],
                    )
                    ca_question = gr.Textbox(
                        label="Your Question",
                        placeholder="e.g. What are the strongest arguments for the defense?",
                        lines=4,
                    )
                    ca_btn = gr.Button("Analyze", variant="primary")
                with gr.Column(scale=1):
                    ca_output = gr.Textbox(
                        label="AI Analysis",
                        lines=16,
                        interactive=False,
                        elem_classes=["output-box"],
                    )
            ca_btn.click(
                fn=case_analysis,
                inputs=[ca_file, ca_question],
                outputs=ca_output,
            )

        # ── Tab 2: Objection Checker ──────────────────────────────────────────
        with gr.TabItem("🔨 Objection Checker"):
            gr.Markdown(
                "**Paste an examination question to check whether it's objectionable "
                "and what grounds apply.**"
            )
            with gr.Row():
                with gr.Column(scale=1):
                    oc_question = gr.Textbox(
                        label="Examination Question",
                        placeholder='e.g. "Isn\'t it true that you were there the whole time?"',
                        lines=4,
                    )
                    oc_type = gr.Radio(
                        choices=["Direct Examination", "Cross Examination"],
                        value="Direct Examination",
                        label="Examination Type",
                    )
                    oc_btn = gr.Button("Check for Objections", variant="primary")
                with gr.Column(scale=1):
                    oc_output = gr.Textbox(
                        label="Objection Analysis",
                        lines=16,
                        interactive=False,
                        elem_classes=["output-box"],
                    )
            oc_btn.click(
                fn=objection_checker,
                inputs=[oc_question, oc_type],
                outputs=oc_output,
            )

        # ── Tab 3: Witness Simulator ──────────────────────────────────────────
        with gr.TabItem("🎭 Witness Simulator"):
            gr.Markdown(
                "**Simulate questioning a witness. The AI responds in character "
                "based on the witness statement and context you provide.**"
            )
            with gr.Row():
                with gr.Column(scale=1):
                    ws_exam_type = gr.Radio(
                        choices=["Direct Examination", "Cross Examination"],
                        value="Direct Examination",
                        label="Examination Type",
                    )
                    ws_witness_type = gr.Radio(
                        choices=["Expert Witness", "Non-Expert Witness"],
                        value="Non-Expert Witness",
                        label="Witness Type",
                    )
                    ws_name = gr.Textbox(
                        label="Witness Name",
                        placeholder="e.g. Dr. Jane Smith",
                    )
                    ws_statement = gr.File(
                        label="Witness Statement (PDF, optional)",
                        file_types=[".pdf"],
                        elem_classes=["upload-zone"],
                    )
                    ws_question = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask the witness a question...",
                        lines=3,
                    )
                    ws_btn = gr.Button("Ask Witness", variant="primary")
                with gr.Column(scale=1):
                    ws_output = gr.Textbox(
                        label="Witness Response",
                        lines=16,
                        interactive=False,
                        elem_classes=["output-box"],
                    )
            ws_btn.click(
                fn=witness_simulator,
                inputs=[ws_exam_type, ws_witness_type, ws_name, ws_statement, ws_question],
                outputs=ws_output,
            )

# ── Launch ────────────────────────────────────────────────────────────────────
demo.launch(
    share=True,       # Creates a public gradio.live link
    debug=False,
    show_error=True,
)
