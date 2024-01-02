import gradio as gr


def greet(text):
    return {
        "text": text,
    }


demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(placeholder="Please input your text here."),
    outputs=gr.JSON(),
    title="Ifun 敏感文本检测",
    description="Please input your text to check if it is sensitive.",
    examples=[["boss u motherfucker", "草你妈"]],
)

if __name__ == "__main__":
    demo.launch(show_api=True, share=True)
