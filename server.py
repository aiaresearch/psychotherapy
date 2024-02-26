from flask import Flask, render_template, request, jsonify
from zhipuai import ZhipuAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 初始化智谱AI客户端
client = ZhipuAI(api_key="2a8e2b310d4e524c0cfed8fd501cb11e.yJIpbQ4OzsXo60y3") 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('login')
def index():
    return render_template('login.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['input']

        # 调用智谱AI的对话模型
        response = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": user_input}]
        )

        # 提取AI的回复并返回给前端
        ai_response = response.choices[0].message.content
        return jsonify({'output': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")