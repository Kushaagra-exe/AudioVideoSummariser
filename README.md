# Audio Video Summariser

### Description
Audio Video Summariser is an app designed to simplify and summarize the content of videos, audios, and YouTube videos. This tool can be especially useful in education, enabling quick learning by extracting and delivering essential information in a concise format.

---

## Features
- **Summarize audio and video files** to capture main points and insights.
- **Summarize YouTube videos** by extracting transcripts and generating concise summaries.
- **Supports multiple languages** via Whisper's capabilities.
- Simple, interactive user interface built with Streamlit.

---

## Modules Used

- **Streamlit**: For the web-based user interface.
- **Whisper**: To transcribe and process audio content.
- **MoviePy**: For handling video file manipulations.
- **tempfile**: For temporary file handling.
- **google.generativeai**: To access Gemini API for summary generation.
- **youtube_transcript_api**: To fetch transcripts from YouTube videos.

---

## Prerequisites

1. **Install Python 3.x**: Ensure Python 3.x is installed on your system.
2. **API Key**: Obtain a Gemini API key and set it up as described below.

---

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Audio-Video-Summariser.git
   cd Audio-Video-Summariser
   ```
2. **Install Required Packages**: Use the following command to install the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up Whisper**:To enable audio transcription, install OpenAI's Whisper:
    ```bash
    pip install git+https://github.com/openai/whisper.git
    ```
---

## Running the App

1. **Run Streamlit App**: Start the app with the following command:
    ```bash
   streamlit run app.py
   ```
2. **Access the App**: Once the server is running, open your browser and go to http://localhost:8501 to access the application interface.

---

## Usage Examples
### Video Summarisation
![vid gif.gif](Media%2Fvid%20gif.gif)


### Audio Summarisation
![aud gif.gif](Media%2Faud%20gif.gif)

### Youtube Summarisation
![yt gif.gif](Media%2Fyt%20gif.gif)