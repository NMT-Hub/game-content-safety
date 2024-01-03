import gradio as gr
from chatgpt_label_data import label_toxity_text


async def greet(text, model):
    if model == "gpt3.5-turbo":
        explanation, label = await label_toxity_text(text)
        return {"label": label, "explanation": explanation}
    elif model == "finetuned mT5":
        return {"label": "unclear", "explanation": "暂不支持"}
    elif model == "Baidu API":
        return {"label": "unclear", "explanation": "暂不支持"}
    elif model == "Roberta":
        return {"label": "unclear", "explanation": "暂不支持"}
    else:
        return {"label": "unclear", "explanation": "暂不支持"}


text_input = gr.Textbox(placeholder="Please input your text here.", label="输入待检测文本")
action_buttons = gr.Radio(
    ["gpt3.5-turbo", "finetuned mT5", "Baidu API", "Roberta"],
    label="可选模型",
    value="gpt3.5-turbo",
)
json_output = gr.JSON(label="检测结果")


demo = gr.Interface(
    fn=greet,
    inputs=[text_input, action_buttons],
    outputs=json_output,
    title="IFUN 文本内容安全检测系统",
    examples=[
        ["boss u motherfucker"],
        ["草你妈"],
        ["搏一搏单车变摩托，赶紧来吧，可直接加微f-fak-fas"],
        ["我认为Player16195000005提问的Q5答案是A:1.5公里"],
        ["我解散了所有部隊……這樣你就可以攻擊我的別墅"],
        ["法克油"],
        ["who is that? new porn star?"],
        ["宝石便宜卖了,加v 线下私聊"],
    ],
)


if __name__ == "__main__":
    demo.launch(show_api=True, share=True)
