# 📚 ShikshaSathi — AI-Powered Study Buddy

An AI-powered study companion for Indian students built with **Streamlit** and **Groq (LLaMA3-70B)**.

---

## ✨ Features

| Mode | What it does |
|------|-------------|
| 💡 **Concept Explainer** | Explains any topic simply with analogies, examples & key takeaways |
| 📝 **Notes Summarizer** | Condenses long notes into crisp summaries or bullet points |
| 🧠 **Quiz Generator** | Auto-generates MCQ / True-False quizzes with scoring & explanations |
| 🃏 **Flashcard Maker** | Creates revision flashcards (Term→Def, Q→A, Concept→Example) |
| 💬 **Study Chat** | 24/7 conversational tutor for any study question |

---

## 🚀 Quick Start

### 1. Clone / download the project
```bash
cd shiksha_sathi
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
Edit `.streamlit/secrets.toml`:
```toml
[groq]
api_key = "gsk_YOUR_GROQ_API_KEY_HERE"
```
Get a **free** API key at → https://console.groq.com

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
shiksha_sathi/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── .streamlit/
    ├── secrets.toml        # Groq API key (keep private!)
    └── config.toml         # Streamlit theme config
```

---

## 🔧 Configuration

In the sidebar you can choose:
- **Subject Area** — Math, Physics, Chemistry, History, CS, etc.
- **Student Level** — Middle School → Competitive Exam
- **Language** — English / Hindi / Hinglish

---

## 🌐 Deploy to Streamlit Cloud

1. Push to GitHub (add `.streamlit/secrets.toml` to `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as entry point
4. Add secret under **Settings → Secrets**:
   ```
   [groq]
   api_key = "gsk_..."
   ```

---

