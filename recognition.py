import speech_recognition as sr
from aip import AipSpeech
import os

def record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("请说些什么")
        audio = r.listen(source)

        with open("voices_record.wav", "wb") as f:
            f.write(audio.get_wav_data())
        print("录音结束")

record()
print("录音文件大小:", os.path.getsize("voices_record.wav"))

APP_ID = "51962123"
API_KEY = "xgjQ4QDI6Y8IBNQjePGSBTEj "
SECRET_KEY = "8pAEOB69qOzc7p9pZGh40DIUTEWrTnlB "
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = 'voices_record.wav'

def listen():
    with open(path, "rb") as fp:
        voices = fp.read()
    try:
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537})   
        result_text = result["result"][0]
        print("你说的是：" + result_text)
        return result_text
    except Exception as e:
        print("错误:", e)

result = listen()
print("识别结果：", result)