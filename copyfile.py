from flask import Flask, request, jsonify,render_template
from zhipuai import ZhipuAI
from flask_cors import CORS
from flask_sslify import SSLify
import os
import wave

import speech_recognition as sr
from aip import AipSpeech

def switchFile(path):
    newPath = 'newAudio.wav'

    n = 16000

        # 打开音频
    with wave.open(path, 'rb') as wr:
        params = wr.getparams()
        nframes = wr.getnframes()
        data = wr.readframes(nframes)
      
    # 写入新音频
    with wave.open(newPath, 'wb') as ww:
        ww.setparams(params)
        ww.setframerate(n)
        # 帧数据是字节串格式，索引 = 秒数 * 采样字节长度 * 采样频率
        ww.writeframes(data)

app = Flask(__name__, static_folder='templates')
sslify = SSLify(app)
CORS(app)

client = ZhipuAI(api_key = "2a8e2b310d4e524c0cfed8fd501cb11e.yJIpbQ4OzsXo60y3")

# 读取文件
def get_file_content(file_path):
    with open(file_path,'rb') as fp:
       content = fp.read()
       return content
    
@app.route('/chat', methods=['POST'])
def ask():
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({"error": "问题不能为空"}), 400
        print(user_question)
    # 调用智谱AI的对话模型
        response = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": user_question}]
        )
    # 提取AI的回复并返回给前端
        ai_response = response.choices[0].message.content
        print(response.choices)
        return jsonify({'output': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        print('No file uploaded')
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        print('No file selected')
        return jsonify({'error': 'No file selected'}), 400

    # 保存上传的文件
    file.save(file.filename)

    # 调用语音转文字的函数
    text = recognize_speech(file)
    print('text: ',text,file.filename)
    return jsonify({'text': text})

@app.get("/")
def index():
    return render_template("index.html")

def recognize_speech(file):
    APP_ID = '51962123'
    API_KEY = 'xgjQ4QDI6Y8IBNQjePGSBTEj '
    SECRET_KEY = '8pAEOB69qOzc7p9pZGh40DIUTEWrTnlB '

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    newPath = switchFile('./'+file.filename) 
    data = get_file_content(newPath) # 读取新路径的音频文件

    print(file.filename)
    result = client.asr(data, 'wav', 16000, {'dev_pid': 1537})
    print('result: ',result)
    if result['err_no'] == 0:
        text = result['result'][0]
    else:
        text = 'Error: ' + str(result['err_no'])

    return text


# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_dir, './templates/cert.pem')
key_path = os.path.join(current_dir, './templates/key.pem')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=2000)
    app.run(ssl_context=(cert_path, key_path),port=443,debug=True)
