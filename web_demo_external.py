import openai
import gradio as gr
from chatgpt_label_data import label_toxicity_text
from roberta import roberta_toxicity_classify
from eval_xlm import predict


async def greet(text, model, *args, **kwargs):
    if model == "精准模式":
        try:
            return await label_toxicity_text(text), description
        except openai.BadRequestError:
            return await roberta_toxicity_classify(text), "natural: 合规 toxicity: 不合规"
    elif model == "快速模式":
        return predict(text), description
    else:
        return {"label": "unclear", "explanation": "暂不支持"}, ""


text_input = gr.Textbox(placeholder="Please input your text here.", label="输入待检测文本")
action_buttons = gr.Radio(
    ["快速模式", "精准模式"],
    label="选择模式：",
    value="快速模式",
)
json_output = gr.JSON(label="检测结果")


description = """
### 分类说明: 
- 合规(compliant)：不含有毒性内容。玩家之间的正常交流。
- 色情(pornography)：发送色情评论或色情信息的链接。
- 暴力(violent)：发送暴力言论。
- 毒性(toxicity)：发送辱骂性言论。
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
注意：文本框内不要输入过长的文本，聊天内容一般都在100字以内，过长的文本会导致模型预测不准确。
### 模式说明:
- 快速模式：适合对大量玩家的聊天记录进行批量检测，检测结果较为粗略，但速度更快，适合实时批量调用。
- 精准模式：适合对某个玩家的聊天记录进行精准复校验，检测结果更加准确，不适合实时批量调用。

上线后，可以使用快速模式对所有玩家的聊天记录进行批量检测，对于检测结果为不合规的玩家，再使用精准模式进行精准复校验。
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
    demo.launch(show_api=True, share=True, server_name='0.0.0.0')
