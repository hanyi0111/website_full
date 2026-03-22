from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
# 配置CORS，允许所有来源
CORS(app, origins="*")

# 配置OpenAI API
client = openai.OpenAI(
    base_url='https://api1.oaipro.com/v1',
    api_key=os.getenv('OPENAI_API_KEY'),
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        # 系统提示词，包含个人信息
        system_prompt = """你是吕怡晗的AI助手，负责回答关于她的个人背景、项目经验和AI产品相关问题。
        
        个人信息：
        - 姓名：吕怡晗
        - 职业：AI产品经理
        - 教育背景：桂林电子科技大学管理科学与工程专业（硕士），河南医药大学信息管理与信息系统专业（本科）
        - 实习经历：字节跳动AI数据技术实习生，美的集团产品经理实习生
        - 项目经验：基于改进RAG的大模型药品说明书摘要生成研究，基于关键字的大屏动态文字实时检索系统（省级）
        - 技能：Python、SPSS、MATLAB、Figma、Xmind、GemDesign，擅长大模型迭代、Prompt工程、RAG技术等
        - 联系方式：手机13072660129，邮箱2667270650@qq.com
        
        请以专业、友好的语气回答问题，提供准确的信息。"""
        
        # 调用OpenAI API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=500
        )
        
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "抱歉，我暂时无法回答这个问题。你可以尝试重新提问或直接联系吕怡晗。"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)