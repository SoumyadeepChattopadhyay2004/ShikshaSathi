import streamlit as st
from groq import Groq
import json
import re
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShikshaSathi – AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root variables ── */
:root {
    --orange: #F97316;
    --orange-light: #FB923C;
    --orange-dark: #EA580C;
    --teal: #14B8A6;
    --navy: #0F172A;
    --slate: #1E293B;
    --slate2: #334155;
    --text: #F1F5F9;
    --muted: #94A3B8;
    --border: rgba(249,115,22,0.2);
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp { background: var(--navy); }

/* ── Hide default elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0F172A 0%, #1a1035 50%, #0F172A 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(249,115,22,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(20,184,166,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #F97316 0%, #FB923C 50%, #14B8A6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(249,115,22,0.12);
    border: 1px solid rgba(249,115,22,0.35);
    color: var(--orange-light);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 50px;
    margin-bottom: 0.9rem;
}

/* ── Mode cards ── */
.mode-card {
    background: var(--slate);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.25s ease;
}
.mode-card:hover {
    border-color: var(--orange);
    background: rgba(249,115,22,0.08);
    transform: translateY(-2px);
}
.mode-card.active {
    border-color: var(--orange);
    background: rgba(249,115,22,0.12);
    box-shadow: 0 0 20px rgba(249,115,22,0.15);
}
.mode-icon { font-size: 1.6rem; margin-bottom: 0.4rem; }
.mode-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text);
}
.mode-desc { font-size: 0.82rem; color: var(--muted); margin-top: 0.2rem; }

/* ── Section headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header span.accent { color: var(--orange); }

/* ── Input styling ── */
.stTextArea textarea, .stTextInput input {
    background: var(--slate) !important;
    border: 1px solid var(--slate2) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border 0.2s ease !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 2px rgba(249,115,22,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(249,115,22,0.35) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Result card ── */
.result-card {
    background: var(--slate);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-top: 1.2rem;
    position: relative;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--orange) 0%, var(--teal) 100%);
    border-radius: 16px 0 0 16px;
}

/* ── Quiz card ── */
.quiz-card {
    background: var(--slate);
    border: 1px solid var(--slate2);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.quiz-card:hover { border-color: var(--orange-light); }
.quiz-question {
    font-family: 'Syne', sans-serif;
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.8rem;
}
.quiz-option {
    display: block;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--slate2);
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    margin: 0.3rem 0;
    font-size: 0.88rem;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.15s;
}
.quiz-option.correct {
    background: rgba(20,184,166,0.15);
    border-color: var(--teal);
    color: #5eead4;
    font-weight: 500;
}

/* ── Flashcard ── */
.flashcard {
    background: linear-gradient(135deg, #1E293B 0%, #162032 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1rem;
    text-align: center;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
}
.flashcard::after {
    content: '';
    position: absolute;
    bottom: -20px; right: -20px;
    width: 100px; height: 100px;
    background: radial-gradient(circle, rgba(249,115,22,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.flashcard-term {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--orange-light);
    margin-bottom: 0.6rem;
}
.flashcard-def {
    font-size: 0.9rem;
    color: var(--muted);
    line-height: 1.6;
}
.flashcard-num {
    position: absolute;
    top: 0.8rem; right: 1rem;
    font-size: 0.72rem;
    color: var(--slate2);
    font-weight: 600;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080f1a !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1rem !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--slate) !important;
    border: 1px solid var(--slate2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--orange) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--slate2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--orange); }

/* ── Success / error ── */
.stSuccess { background: rgba(20,184,166,0.1) !important; border: 1px solid var(--teal) !important; border-radius: 10px !important; }
.stError { background: rgba(239,68,68,0.1) !important; border: 1px solid #ef4444 !important; border-radius: 10px !important; }

/* ── Stat pills ── */
.stat-row { display: flex; gap: 0.7rem; flex-wrap: wrap; margin-bottom: 1.2rem; }
.stat-pill {
    background: rgba(249,115,22,0.1);
    border: 1px solid rgba(249,115,22,0.25);
    color: var(--orange-light);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 14px;
    border-radius: 50px;
    letter-spacing: 0.03em;
}
</style>
""", unsafe_allow_html=True)


# ── Groq client ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    api_key = st.secrets["groq"]["api_key"]
    return Groq(api_key=api_key)


def call_groq(messages: list, temperature: float = 0.7, max_tokens: int = 2048) -> str:
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


# ── Helpers ────────────────────────────────────────────────────────────────────
def stream_text(text: str, delay: float = 0.008):
    """Simulate streaming by yielding chars."""
    for char in text:
        yield char
        time.sleep(delay)


def parse_json_safely(text: str):
    """Strip markdown fences and parse JSON."""
    clean = re.sub(r"```json|```", "", text).strip()
    return json.loads(clean)


# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "flashcard_data" not in st.session_state:
    st.session_state.flashcard_data = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.8rem 0 1.4rem 0;'>
        <div style='font-size:2.4rem;'>📚</div>
        <div style='font-family: Syne, sans-serif; font-size:1.2rem; font-weight:800;
                    background: linear-gradient(90deg,#F97316,#14B8A6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>ShikshaSathi</div>
        <div style='font-size:0.75rem; color:#94A3B8; margin-top:4px;'>AI-Powered Study Buddy</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    mode = st.selectbox(
        "✨ Choose Mode",
        ["💡 Concept Explainer", "📝 Notes Summarizer", "🧠 Quiz Generator", "🃏 Flashcard Maker", "💬 Study Chat"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:0.78rem;font-weight:700;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.6rem;'>Settings</div>", unsafe_allow_html=True)

    subject = st.selectbox(
        "Subject Area",
        ["General", "Mathematics", "Physics", "Chemistry", "Biology",
         "History", "Geography", "Computer Science", "Economics", "Literature"],
    )

    level = st.selectbox(
        "Student Level",
        ["Middle School (6–8)", "High School (9–12)", "Undergraduate", "Competitive Exam"],
    )

    language = st.selectbox("Explanation Language", ["English", "Hindi", "Hinglish"])

    st.markdown("---")

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.quiz_data = []
        st.session_state.flashcard_data = []
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.rerun()

    st.markdown("""
    <div style='margin-top:2rem; padding:1rem; background:rgba(249,115,22,0.06);
                border:1px solid rgba(249,115,22,0.15); border-radius:12px;'>
        <div style='font-size:0.75rem; color:#94A3B8; line-height:1.6;'>
            🚀 Powered by <b style='color:#F97316;'>Groq + LLaMA3</b><br>
            Fast inference. Free API.<br>
            Built for Indian students 🇮🇳
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div class='hero-badge'>🇮🇳 Made for Indian Students</div>
    <div class='hero-title'>ShikshaSathi</div>
    <div class='hero-sub'>Your AI-powered study companion — explain, summarize, quiz & revise smarter.</div>
</div>
""", unsafe_allow_html=True)

# ── Mode: Concept Explainer ────────────────────────────────────────────────────
if mode == "💡 Concept Explainer":
    st.markdown("<div class='section-header'>💡 Concept <span class='accent'>Explainer</span></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        concept = st.text_input("Enter a concept or topic you want to understand:", placeholder="e.g. Photosynthesis, Newton's Laws, Recursion, French Revolution…")
    with col2:
        depth = st.selectbox("Depth", ["Simple (ELI5)", "Standard", "In-depth"])

    analogy = st.checkbox("🔗 Include a real-world analogy", value=True)
    examples = st.checkbox("📌 Give examples", value=True)
    key_points = st.checkbox("📋 List key takeaways", value=True)

    if st.button("✨ Explain This Concept"):
        if not concept.strip():
            st.warning("Please enter a concept to explain!")
        else:
            extras = []
            if analogy: extras.append("Include a memorable real-world analogy.")
            if examples: extras.append("Give 1-2 concrete examples.")
            if key_points: extras.append("End with 3-5 bullet-point key takeaways.")

            depth_map = {
                "Simple (ELI5)": "Explain it simply as if to a 12-year-old. Use very plain language.",
                "Standard": "Explain clearly for a school/college student.",
                "In-depth": "Give a thorough explanation covering mechanisms, nuances, and edge cases.",
            }

            prompt = f"""You are ShikshaSathi, a friendly and brilliant Indian study tutor.
Subject area: {subject}
Student level: {level}
Response language: {language}
Depth: {depth_map[depth]}

Explain the concept: "{concept}"

{chr(10).join(extras)}

Format your response cleanly with clear sections. Use simple headings (no markdown symbols like ###, use bold text or plain labels instead). Make it engaging, warm, and encouraging."""

            with st.spinner("🔍 Thinking…"):
                result = call_groq([{"role": "user", "content": prompt}], temperature=0.6)

            st.markdown(f"""
            <div class='result-card'>
                <div class='stat-row'>
                    <span class='stat-pill'>📚 {subject}</span>
                    <span class='stat-pill'>🎯 {level}</span>
                    <span class='stat-pill'>📏 {depth}</span>
                </div>
                <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;
                            color:#F97316;margin-bottom:1rem;'>"{concept}"</div>
            </div>
            """, unsafe_allow_html=True)

            with st.container():
                st.write(result)

            st.session_state.history.append({"type": "explain", "topic": concept, "content": result})


# ── Mode: Notes Summarizer ────────────────────────────────────────────────────
elif mode == "📝 Notes Summarizer":
    st.markdown("<div class='section-header'>📝 Notes <span class='accent'>Summarizer</span></div>", unsafe_allow_html=True)

    notes_input = st.text_area(
        "Paste your study notes, textbook paragraph, or lecture content:",
        height=220,
        placeholder="Paste any text here — lecture notes, textbook chapter, article…",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        summary_length = st.selectbox("Summary Length", ["Short (3-5 lines)", "Medium (1 paragraph)", "Detailed (structured)"])
    with col2:
        output_format = st.selectbox("Output Format", ["Paragraph", "Bullet Points", "Mind Map Style"])
    with col3:
        highlight_terms = st.checkbox("🔑 Highlight key terms", value=True)

    if st.button("📝 Summarize Notes"):
        if not notes_input.strip():
            st.warning("Please paste some notes to summarize!")
        else:
            length_map = {
                "Short (3-5 lines)": "Write a very concise 3-5 line summary.",
                "Medium (1 paragraph)": "Write a clear summary in one well-structured paragraph.",
                "Detailed (structured)": "Write a detailed structured summary with sections.",
            }
            format_map = {
                "Paragraph": "Write in flowing paragraph form.",
                "Bullet Points": "Use bullet points (•) for each key idea.",
                "Mind Map Style": "Organize as a mind-map-style outline with main topics and sub-points.",
            }

            prompt = f"""
You are a strict educational content formatter.

Subject: {subject}
Level: {level}
Language: {language}

Convert the content below into structured study notes.

CONTENT:
---
{notes_input[:4000]}
---

YOU MUST FOLLOW THIS FORMAT EXACTLY:

Introduction:
<text>

Real-World Analogy:
<text>

Examples:
- example 1
- example 2

Key Takeaways:
- point 1
- point 2
- point 3

STRICT RULES:
- Each heading MUST be on its own line
- Add a blank line AFTER every section
- Do NOT merge headings with text
- Do NOT write paragraphs on the same line as headings
- Use bullet points ONLY in Examples and Key Takeaways
- No extra sections allowed
"""

            with st.spinner("📚 Summarizing your notes…"):
                result = call_groq([{"role": "user", "content": prompt}], temperature=0.5, max_tokens=1500)

            word_count = len(notes_input.split())
            st.markdown(f"""
            <div class='stat-row'>
                <span class='stat-pill'>📄 {word_count} words input</span>
                <span class='stat-pill'>✂️ {summary_length}</span>
                <span class='stat-pill'>📐 {output_format}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)

            st.session_state.history.append({"type": "summary", "content": result})


# ── Mode: Quiz Generator ────────────────────────────────────────────────────
elif mode == "🧠 Quiz Generator":
    st.markdown("<div class='section-header'>🧠 Quiz <span class='accent'>Generator</span></div>", unsafe_allow_html=True)

    topic_input = st.text_area(
        "Enter a topic OR paste notes to generate a quiz from:",
        height=120,
        placeholder="e.g. 'The French Revolution' or paste study notes…",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        num_questions = st.slider("Number of Questions", 3, 10, 5)
    with col2:
        q_type = st.selectbox("Question Type", ["Multiple Choice (MCQ)", "True/False", "Mixed"])
    with col3:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])

    if st.button("🧠 Generate Quiz"):
        if not topic_input.strip():
            st.warning("Please enter a topic or paste notes!")
        else:
            type_map = {
                "Multiple Choice (MCQ)": "all multiple-choice questions with 4 options (A, B, C, D)",
                "True/False": "all True/False questions",
                "Mixed": "a mix of MCQ and True/False questions",
            }

            prompt = f"""You are ShikshaSathi quiz engine. Generate a {difficulty} difficulty quiz.
Topic/Content: {topic_input[:3000]}
Subject: {subject} | Level: {level}
Generate exactly {num_questions} questions. Format: {type_map[q_type]}

Return ONLY a valid JSON array (no markdown, no extra text) like:
[
  {{
    "q": "Question text here?",
    "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
    "answer": "A",
    "explanation": "Brief explanation why A is correct."
  }}
]
For True/False, options should be ["A. True", "B. False"] and answer "A" or "B".
Return ONLY the JSON array, nothing else."""

            with st.spinner("🎯 Crafting your quiz…"):
                raw = call_groq([{"role": "user", "content": prompt}], temperature=0.7, max_tokens=2000)

            try:
                quiz_data = parse_json_safely(raw)
                st.session_state.quiz_data = quiz_data
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.success(f"✅ {len(quiz_data)} questions generated! Scroll down to attempt the quiz.")
            except Exception as e:
                st.error(f"Could not parse quiz. Try again. ({e})")
                st.code(raw)

    # Render quiz
    if st.session_state.quiz_data:
        st.markdown("---")
        st.markdown(f"<div class='section-header'>📋 Your Quiz <span class='accent'>({len(st.session_state.quiz_data)} Questions)</span></div>", unsafe_allow_html=True)

        for i, q in enumerate(st.session_state.quiz_data):
            with st.container():
                st.markdown(f"""
                <div class='quiz-card'>
                    <div class='quiz-question'>Q{i+1}. {q['q']}</div>
                </div>
                """, unsafe_allow_html=True)

                options = q.get("options", ["A. True", "B. False"])
                chosen = st.radio(
                    f"q{i}",
                    options,
                    key=f"q_{i}",
                    label_visibility="collapsed",
                )
                st.session_state.quiz_answers[i] = chosen[0] if chosen else None

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("✅ Submit Quiz"):
                st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            score = 0
            st.markdown("---")
            st.markdown("<div class='section-header'>📊 Quiz <span class='accent'>Results</span></div>", unsafe_allow_html=True)

            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.quiz_answers.get(i, "")
                correct = q.get("answer", "")
                is_correct = str(user_ans).strip().upper() == str(correct).strip().upper()
                if is_correct:
                    score += 1
                icon = "✅" if is_correct else "❌"
                expl = q.get("explanation", "")

                with st.expander(f"{icon} Q{i+1}: {q['q'][:60]}…"):
                    st.markdown(f"**Your answer:** {user_ans}  |  **Correct:** {correct}")
                    if expl:
                        st.info(f"💡 {expl}")

            pct = int((score / len(st.session_state.quiz_data)) * 100)
            color = "#14B8A6" if pct >= 70 else "#F97316" if pct >= 40 else "#EF4444"
            st.markdown(f"""
            <div style='text-align:center; padding:2rem; background:var(--slate);
                        border:1px solid {color}33; border-radius:16px; margin-top:1rem;'>
                <div style='font-family:Syne,sans-serif;font-size:3rem;font-weight:800;color:{color};'>{pct}%</div>
                <div style='font-size:1rem;color:var(--muted);margin-top:0.3rem;'>
                    {score} / {len(st.session_state.quiz_data)} correct
                </div>
                <div style='font-size:0.9rem;color:var(--text);margin-top:0.5rem;'>
                    {"🏆 Excellent! Keep it up!" if pct>=80 else "👍 Good effort! Review the explanations." if pct>=50 else "📖 Keep studying — you'll get there!"}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Mode: Flashcard Maker ────────────────────────────────────────────────────
elif mode == "🃏 Flashcard Maker":
    st.markdown("<div class='section-header'>🃏 Flashcard <span class='accent'>Maker</span></div>", unsafe_allow_html=True)

    fc_input = st.text_area(
        "Enter topic or paste notes to generate flashcards:",
        height=140,
        placeholder="e.g. 'Cell Biology', 'Indian Independence Movement', or paste notes…",
    )

    col1, col2 = st.columns(2)
    with col1:
        num_cards = st.slider("Number of Flashcards", 5, 20, 10)
    with col2:
        card_style = st.selectbox("Card Style", ["Term → Definition", "Question → Answer", "Concept → Example"])

    if st.button("🃏 Generate Flashcards"):
        if not fc_input.strip():
            st.warning("Please enter a topic or notes!")
        else:
            style_map = {
                "Term → Definition": "term-definition pairs",
                "Question → Answer": "question-answer pairs",
                "Concept → Example": "concept-example pairs",
            }

            prompt = f"""You are ShikshaSathi flashcard engine.
Topic/Notes: {fc_input[:3000]}
Subject: {subject} | Level: {level}
Generate {num_cards} {style_map[card_style]} as flashcards.

Return ONLY a valid JSON array (no markdown):
[
  {{"front": "Term or Question", "back": "Definition, Answer, or Example"}}
]
Keep each card concise and memorable. Return ONLY the JSON array."""

            with st.spinner("🃏 Creating flashcards…"):
                raw = call_groq([{"role": "user", "content": prompt}], temperature=0.7, max_tokens=2000)

            try:
                fc_data = parse_json_safely(raw)
                st.session_state.flashcard_data = fc_data
                st.success(f"✅ {len(fc_data)} flashcards ready!")
            except Exception as e:
                st.error(f"Could not parse flashcards. Try again. ({e})")

    if st.session_state.flashcard_data:
        st.markdown("---")
        st.markdown(f"<div class='section-header'>📇 Flashcards <span class='accent'>({len(st.session_state.flashcard_data)} cards)</span></div>", unsafe_allow_html=True)

        cols = st.columns(2)
        for i, card in enumerate(st.session_state.flashcard_data):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='flashcard'>
                    <div class='flashcard-num'>#{i+1}</div>
                    <div class='flashcard-term'>{card.get('front','')}</div>
                    <div class='flashcard-def'>{card.get('back','')}</div>
                </div>
                """, unsafe_allow_html=True)

        # Download as text
        cards_text = "\n\n".join([f"Q: {c['front']}\nA: {c['back']}" for c in st.session_state.flashcard_data])
        st.download_button(
            "⬇️ Download Flashcards (.txt)",
            data=cards_text,
            file_name="shiksha_sathi_flashcards.txt",
            mime="text/plain",
        )


# ── Mode: Study Chat ────────────────────────────────────────────────────
elif mode == "💬 Study Chat":
    st.markdown("<div class='section-header'>💬 Study <span class='accent'>Chat</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.88rem;color:#94A3B8;margin-bottom:1.2rem;'>Ask anything — your personal tutor is ready 24/7.</div>", unsafe_allow_html=True)

    # Chat history display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.history:
            st.markdown("""
            <div style='text-align:center; padding:2.5rem 1rem; color:#475569;'>
                <div style='font-size:2rem;margin-bottom:0.6rem;'>👋</div>
                <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:600;'>
                    Hello! I'm ShikshaSathi.<br>Ask me anything about your studies!
                </div>
                <div style='font-size:0.82rem;margin-top:0.5rem;color:#334155;'>
                    Try: "Explain quantum physics simply" or "Solve this equation for me"
                </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.history:
            if msg.get("type") == "chat":
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    st.markdown(f"""
                    <div style='display:flex; justify-content:flex-end; margin-bottom:0.8rem;'>
                        <div style='background:rgba(249,115,22,0.15);border:1px solid rgba(249,115,22,0.3);
                                    border-radius:14px 14px 2px 14px; padding:0.7rem 1rem;
                                    max-width:75%; font-size:0.9rem; color:#F1F5F9;'>
                            {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='display:flex; align-items:flex-start; gap:0.6rem; margin-bottom:0.8rem;'>
                        <div style='font-size:1.3rem; flex-shrink:0; margin-top:2px;'>🤖</div>
                        <div style='background:var(--slate);border:1px solid var(--border);
                                    border-radius:2px 14px 14px 14px; padding:0.8rem 1.1rem;
                                    max-width:80%; font-size:0.9rem; color:#E2E8F0; line-height:1.65;'>
                            {content.replace(chr(10), "<br>")}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    with col1:
        user_msg = st.text_input("Your question:", placeholder="Ask anything about your studies…", label_visibility="collapsed")
    with col2:
        send = st.button("Send ➤")

    if send and user_msg.strip():
        st.session_state.history.append({"type": "chat", "role": "user", "content": user_msg})

        chat_history = [
            {
                "role": "system",
                "content": f"""You are ShikshaSathi, a warm and brilliant Indian study tutor.
Subject focus: {subject} | Student level: {level} | Language: {language}
Be concise, clear, encouraging. Use simple language. You can use examples from Indian context.
Never refuse a genuine study question. If the question is off-topic, gently redirect to studies."""
            }
        ]
        for msg in st.session_state.history:
            if msg.get("type") == "chat":
                chat_history.append({"role": msg["role"], "content": msg["content"]})

        with st.spinner("🤔 Thinking…"):
            reply = call_groq(chat_history, temperature=0.7, max_tokens=800)

        st.session_state.history.append({"type": "chat", "role": "assistant", "content": reply})
        st.rerun()


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:1rem 0; color:#334155; font-size:0.78rem;'>
    📚 <b style='color:#F97316;'>ShikshaSathi</b> · Built with Streamlit + Groq + LLaMA3 · 
    <span style='color:#475569;'>Empowering every Indian student 🇮🇳</span>
</div>
""", unsafe_allow_html=True)