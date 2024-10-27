import streamlit as st
import whisper
from moviepy.editor import VideoFileClip
import tempfile
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

st.title("Summarisation App for Education")
API_KEY = st.sidebar.text_input("Enter your Gemini Api Key:")

# models
if API_KEY:
    
    genai.configure(api_key=API_KEY)

genmodel = genai.GenerativeModel("gemini-pro")
prompt="""You are Text summarizer. You will be taking the transcript text of a video or an audio and summarizing the entire text in detail and providing the summary in points and in english only. Text:"""
model = whisper.load_model("base")



# functions
def transcribe_audio(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_file.read())
        temp_file.flush()

        result = model.transcribe(temp_file.name)
        return result['text']

def transcribe_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(video_file.read())
        temp_file.flush()

        try:
            video = VideoFileClip(temp_file.name)
            audio = video.audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".aac") as audio_file:
                audio.write_audiofile(audio_file.name, codec='aac')
                audio_file.flush()
                result = model.transcribe(audio_file.name)
                return result['text']
        finally:
            video.close()

def transcribe_yt(id):
    trans = ''
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id, languages=['en'])
        trans = transcript
    except NoTranscriptFound:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(id, languages=['hi'])
            trans = transcript

        except NoTranscriptFound:
            print("No transcript found for this video in English or Hindi.")
            return None
        
    text = ""
    for i in trans:
        text += " "+i['text']
    return text

def summarise(text, prompt):
    response=genmodel.generate_content(prompt+text)
    return response

# =================================================

media_type = st.sidebar.selectbox("Select Media Type", ("Select", "Video", "Audio", "Youtube Video"))
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #555;
    }
    </style>
    <div class="footer">
        <p>Created by Kushaagra</p>
    </div>
    """, unsafe_allow_html=True)
if media_type == "Select":
    st.write("**STEP 1:** *Enter your Gemini Api Key*")
    st.write("**STEP 2:** *Select your media type that you want to summarise*")
elif media_type == "Audio":
    st.subheader("Audio Summariser")
    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg"])
    if audio_file is not None:
        st.audio(audio_file)
        
        if st.button("Summarise"):
            with st.spinner("Summarising the Audio..."):
                transcription = transcribe_audio(audio_file)
                # st.text_area("Transcription", value=transcription, height=300)
                try:
                    summ = summarise(transcription, prompt)
                    st.success("Summarisation completed!")
                    st.subheader("Summary")
                    st.write(summ.text)
                except:
                    st.warning("Please enter a valid Gemini Api Key.")

elif media_type == "Video":
    st.subheader("Video Summariser")

    video_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])
    if video_file is not None:
        st.video(video_file)
        
        if st.button("Summarise"):
            with st.spinner("Summarising the Video..."):
                transcription = transcribe_video(video_file)
                # st.subheader("Transcript")
                # st.text_area("Transcription", value=transcription, height=300)
                try:
                    summ = summarise(transcription, prompt)
                    st.success("Summarisation completed!")
                    st.subheader("Summary")
                    st.write(summ.text)
                except:
                    st.warning("Please enter a valid Gemini Api Key.")
elif media_type == "Youtube Video":
    st.subheader("Youtube Video Summariser")
    st.write("Hindi Language videos are also supported")
    url = st.text_input("Enter the URL of an youtube video  ", placeholder="https://www.youtube.com/watch?v=abcdefg")
    if url:
        id= ''
        try:
            id2 = url.split("&")[0].split("=")[1]
            id = id2
        except:
            st.warning("Please enter a valid Youtube URL.")

        with st.spinner("Summarising..."):
                transript = transcribe_yt(id)
                # st.write(transript)
                # if transcription:
                try:
                    summ = summarise(transript, prompt)
                    st.success("Summarisation completed!")
                    st.subheader("Summarise")
                    st.write(summ.text)
                except:
                    st.warning("Please enter a valid Gemini Api Key.")





if media_type == "Audio" and audio_file is None:
    st.write("Please upload an audio file.")
elif media_type == "Video" and video_file is None:
    st.write("Please upload a video file.")
