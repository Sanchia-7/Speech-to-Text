# 🎙️ Azure Speech-to-Text Application

This project is a **Speech-to-Text application** built using **Microsoft Azure Cognitive Services** and **Streamlit**.
It converts **spoken audio** (via microphone or uploaded audio files) into **grammatically correct text with proper punctuation**.

The application uses Azure’s **Speech SDK** with **TrueText** post-processing for high-quality transcription.

---

## ✨ Features

- 🎤 Microphone Speech Recognition
- 📂 Upload Audio Files (Any Audio File Type)
- 🧠 AI-powered Speech-to-Text using Azure
- ✍️ Automatic punctuation & grammar
- 🖥️ Clean Streamlit UI

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Azure Cognitive Services (Speech-to-Text)
- Azure Speech SDK
- pydub
- FFmpeg
- python-dotenv

---

## 📁 Project Structure

```markdown
project/
├── app.py
├── README.md
├── requirements.txt
└── .env
```
---

## 🔐 Environment Variables

Create a `.env` file:

```bash 
AZURE_SPEECH_KEY=your_key_here  
AZURE_SPEECH_REGION=your_region_here
```
---

## 📦 Install Dependencies

```bash 
pip install -r requirements.txt
```
---

## ▶️ Run the Application
```
streamlit run app.py
```

---

