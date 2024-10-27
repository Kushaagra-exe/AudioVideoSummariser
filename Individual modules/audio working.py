import streamlit as st
import whisper
import tempfile
import google.generativeai as genai

# genai
# API_KEY = os.getenv("API_KEY")
genmodel = genai.GenerativeModel("gemini-pro")
prompt="""You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. Text:"""
def summarise(text, prompt):
    response=genmodel.generate_content(prompt+text)
    return response
# ======================================================


model = whisper.load_model("base")

def transcribe_audio(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_file.flush()

        result = model.transcribe(temp_file.name)
        return result['text']

st.title("Audio Transcription with Whisper")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(uploaded_file)
            st.text_area("Transcription", value=transcription, height=300)
            summ = summarise(transcription, prompt)
            st.subheader("Summarise")
            st.write(summ.text)
            st.success("Transcription completed!")

