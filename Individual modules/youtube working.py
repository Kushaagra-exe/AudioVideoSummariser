from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import google.generativeai as genai

# genai
# API_KEY = os.getenv("API_KEY")
genai.configure(api_key='API')
genmodel = genai.GenerativeModel("gemini-pro")
prompt="""You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. Text:"""
def summarise(text, prompt):
    response=genmodel.generate_content(prompt+text)
    return response

def transcribe(id):
    transript = YouTubeTranscriptApi.get_transcript(id)
    text = ""
    for i in transript:
        text += " "+i['text']
    return text

st.title("Audio Transcription from URL with Whisper")

url = st.text_input("Enter the URL of an audio file", placeholder="https://example.com/audio.wav")



if url:
    try:
        id = url.split("&")[0].split("=")[1]
        with st.spinner("Transcribing..."):
                transript = transcribe(id)
                st.write(transript)
                summ = summarise(transript, prompt)

                st.subheader("Summarise")
                st.write(summ.text)
                st.success("Transcription completed!")
                # st.text_area("Transcription", value=transcription, height=300)
    except:
        st.warning("Please enter a valid Youtube URL.")

    # if id:
    #     if st.button("Transcribe"):
    #         with st.spinner("Transcribing..."):
    #             st.write(id)
    #             # if transcription:
    #             st.success("Transcription completed!")
    #             # st.text_area("Transcription", value=transcription, height=300)
    # else:
    #     st.warning("Please enter a valid Youtube URL.")