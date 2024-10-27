import streamlit as st
import whisper
from moviepy.editor import VideoFileClip
import tempfile
import google.generativeai as genai

# genai
# API_KEY = os.getenv("API_KEY")
genai.configure(api_key='API')
genmodel = genai.GenerativeModel("gemini-pro")
prompt="""You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. Text:"""
def summarise(text, prompt):
    response=genmodel.generate_content(prompt+text)
    return response
# ======================================================
model = whisper.load_model("base")

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

st.title("Video Transcription with Whisper")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    transcription = '' 
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            transcription += ''' I've run the CSYML and today you are going to talk about two of the most used methods in ensemble learning, begging and boosting. We'll see how each algorithm works and what are the similarities and the difference between the two. So let's not waste any more time and let's dig in. To start with, let's suppose that we have a dataset. What begging does with this dataset is quite simple. You create and sub-data sets of equal size by sampling with replacement from the original dataset, a technique known as boost wrapping and train a classifier on each sub-data set. Then at the end we use all these models to make a prediction in an ensemble classifier. So in a nutshell, begging consists of two steps. One is boost wrapping the dataset and two is aggregating the results. Henceforth its name, begging. When you use boosting on the other hand, the way you create these models changes quite a bit. So let's suppose that you have that same dataset. The first thing you do is to train a classifier on this dataset and see which samples were correct classified by the model and which ones were incorrect classified. Then you use this information to wait up the samples which were incorrect classified by the model. So that when you train the next model, it pays more attention to those samples and hopefully it learns to correct it, classify them. Then you look again at the incorrect classified samples, weigh them up, train a new model, look at its predictions, weigh up the misclassify samples, and so on and so on until you get a desired number of models. At the end, as in the begging case, you use all these models in an ensemble to make predictions on your data. Now let's see what are the similarities and the differences between the two by firstly looking at how they work. So at a high level, both methods builds an ensemble of models, but begging beats them in parallel and boosting beats them sequentially. Knowing this may help us in choosing which one to use depending on the computing resources and development time we have at our disposal. If we have a lot of computing, then due to its parallel nature, begging may be a more suitable algorithm since it may take a lot less time to train the models. And we might get no significant improvement in training for boosting due to its sequential nature. Another thing that we might consider when looking at this two ensemble learning methods is the data set on which they train the classifiers. So both models builds a separate data for each model, but they do it differently. begging uses a subset of the original data set that is generated by sampling with replacement while boosting uses the same samples as in the original data set. Also another important distinction is that in begging, the samples are unweighted while boosting their weighted in regards to the predictions given by the previous classifier. How each ensemble makes the predictions is yet another important dimension to analyze. So what methods make predictions by taking the average of the models, but in begging the classifiers are equally weighted while boosting the models are weighted in the ensemble based on their training performance. As in any machine learning problem, the bias and variance of the system plays an important role in the final performance. In our case, because they are an ensemble, both begging and boosting are good at reducing the variance. However, begging has closed the zero bias reduction. The reason being that because we don't change the weighting of our data when sampling, the bias of the individual model is transferred to the ensemble. This doesn't happen in the boosting case since the samples are waiting from one model to another, but unfortunately this makes boosting more prone to overfeeding in comparison with begging. I know that I may have less equations on answering this video and things like why do we sample with replacement in begging or why is boosting prone to overfeeding more exactly may have popped in your mind? Well, I've done that on purpose mostly because you may notice a thing that this question having common. The why, which is the main theme on this channel, so I tend to make videos about these subjects in the future. This was the video for today. I hope you enjoyed it. Please leave a like if you did. Share with me your touch in the comments section. Subscribe to be up to date with a new content. And until next time, I wish you wonderful time. Bye bye!'''
            st.subheader("Transcript")
            st.text_area("Transcription", value=transcription, height=300)
            summ = summarise(transcription, prompt)
            st.subheader("Summarise")
            st.write(summ.text)
            st.success("Transcription completed!")


