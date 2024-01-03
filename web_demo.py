import gradio as gr
from chatgpt_label_data import label_toxity_text
from baidu import get_text_censor
from roberta import roberta_toxicity_classify


async def greet(text, model, *args, **kwargs):
    if model == "gpt3.5-turbo":
        explanation, label = await label_toxity_text(text)
        return {"label": label, "explanation": explanation}, description
    elif model == "finetuned mT5":
        return {"label": "unclear", "explanation": "暂不支持"}, description
    elif model == "Baidu API":
        return await get_text_censor(text), ""
    elif model == "Roberta":
        return roberta_toxicity_classify(text), "natural: 正常 toxity: 毒性"
    else:
        return {"label": "unclear", "explanation": "暂不支持"}, ""


text_input = gr.Textbox(placeholder="Please input your text here.", label="输入待检测文本")
action_buttons = gr.Radio(
    ["gpt3.5-turbo", "finetuned mT5", "Baidu API", "Roberta"],
    label="可选模型",
    value="gpt3.5-turbo",
)
json_output = gr.JSON(label="检测结果")


description = """
### 分类说明: 
- 正常(natural)：不含有毒性内容。玩家之间的正常交流。
- 色情(pornography)：发送色情评论或色情信息的链接。
- 暴力(violent)：发送暴力言论。
- 毒性(toxity)：发送辱骂性言论。
- 政治(politics)：发送政治敏感言论。
- 广告(advertising)：发送与游戏无关的宣传信息，以及相关社交媒体链接。
- 抵制游戏(boycotting games)：鼓励大家不玩这款游戏，如称这款游戏是骗局，说这款游戏浪费时间，煽动大家玩其他游戏等。
- 作弊(cheating)：言论特征：包括但不限于在游戏中发表如“我是内部人”，“我将使用脚本”，“我可以黑账号”等作弊相关言论。
- 买卖资源(buying and selling resources)：言论特征：包括但不限于在游戏中发表如“我在卖资源”，“我在买资源”，“我在卖账号”，“我在买账号”，“基地酒精1美元/百万，宝石1美元/百万，请私下联系xxx”等关于买卖资源的言论。
- 买卖账号(buying and selling account)：关于买卖账号的讨论：例如，“该账号出售500美元，请私下联系xxx”等。
- 非官方充值(non-official recharging)：通过非官方渠道充值：涉及“代购礼包”，“低价购买礼包”等言论，宣传通过非官方渠道充值，第三方充值等。
- 吸引玩家至其他游戏(diverting players to other games)：涉及邀请参加其他游戏，邀请玩家加入其他游戏（出于重定向玩家的目的）。
"""

model_descriptions = """
- gpt3.5-turbo: 基于GPT3.5的文本分类模型, ICL + COT直接分类
- finetuned mT5: 基于gpt3.5-turbo生成的COT数据, 使用mT5进行微调
- Baidu API: 调用百度API进行文本检测
- Roberta: 基于Roberta的简单文本二分类,只有natural和toxity两类
"""

demo = gr.Interface(
    fn=greet,
    inputs=[text_input, action_buttons, gr.Markdown(label="分类说明", value=model_descriptions)],
    outputs=[json_output, gr.Markdown(label="模型输出说明")],
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
