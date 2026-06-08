import gradio as gr
from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    sources = "\n".join(f"• {source}" for source in result["sources"])

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# OMSCS AI Course Review Assistant")
    gr.Markdown("Ask questions about OMSCS AI specialization courses using your collected review documents.")

    question = gr.Textbox(label="Your question", placeholder="Example: What do students say about ML4T?")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=6)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])

demo.launch()