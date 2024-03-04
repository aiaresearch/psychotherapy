from flask import Flask, request, jsonify,render_template
from zhipuai import ZhipuAI
from flask_cors import CORS

import speech_recognition as sr
from aip import AipSpeech

import ffmpeg
def switchFile(path):
    newPath = 'newAudio.wav'
    ffmpeg.input(path).output(newPath, ar=16000).run(overwrite_output=True)
    # stream = ffmpeg.input(path)
    # stream = ffmpeg.output(stream, newPath, ar=16000, overwrite=True)
    # ffmpeg.run(stream)

    return newPath


app = Flask(__name__)
CORS(app)

client = ZhipuAI(api_key="2a8e2b310d4e524c0cfed8fd501cb11e.yJIpbQ4OzsXo60y3")

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

def recognize_speech(file):
    APP_ID = '51962123'
    API_KEY = 'xgjQ4QDI6Y8IBNQjePGSBTEj '
    SECRET_KEY = '8pAEOB69qOzc7p9pZGh40DIUTEWrTnlB '

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # audio_data = file.read()
    newPath = switchFile('./'+file.filename) # 转换码率，生产一个新的音频文件，并返回音频文件的路径
    data = get_file_content(newPath) # 读取新路径的音频文件
    # binary_audio = base64.b64decode(file.read())
    # data = get_file_content('./'+file.filename)

    print(file.filename)
    result = client.asr(data, 'wav', 16000, {'dev_pid': 1537})
    print('result: ',result)
    if result['err_no'] == 0:
        text = result['result'][0]
    else:
        text = 'Error: ' + str(result['err_no'])

    return text



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
