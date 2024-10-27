from flask import Flask, request, jsonify
import whisper
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

def generate_gemini_content(transcript_text, prompt):
    genmodel = genai.GenerativeModel("gemini-pro")
    response=genmodel.generate_content(prompt+transcript_text)
    return response.text

prompt="""You are Yotube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. Text:"""

app = Flask(__name__)

model = whisper.load_model("base")

@app.route('/summarise', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    audio_path = f"./temp/{file.filename}"
    file.save(audio_path)

    result = model.transcribe(audio_path)
    response=model.generate_content(prompt+result)

    return jsonify({"Summary": response.text})

if __name__ == '__main__':
    app.run(debug=True)
