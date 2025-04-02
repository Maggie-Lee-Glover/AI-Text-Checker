import streamlit as st
import re
import textstat
import difflib
import requests

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(page_title="AI Text Checker", layout="wide")
st.title("🧠 AI Text Detection & Style Comparison Tool")

# ------------------------------
# FUNCTIONS
# ------------------------------
def split_sentences(text):
    return re.split(r'(?<=[.!?]) +', text.strip())

def calculate_humanness(sentence: str):
    try:
        readability = textstat.flesch_reading_ease(sentence)
        complexity = textstat.sentence_complexity(sentence)
        syllables = textstat.syllable_count(sentence)
        ai_score = 0
        if readability > 60:
            ai_score += 0.2
        if complexity < 1.5:
            ai_score += 0.4
        if syllables < 20:
            ai_score += 0.4
        return round((1 - ai_score) * 100, 2)
    except:
        return 50

def highlight_sentences(text):
    sentences = split_sentences(text)
    highlights = []
    for s in sentences:
        score = calculate_humanness(s)
        if score < 50:
            highlights.append((s, '🔴'))
        elif score < 75:
            highlights.append((s, '🟡'))
        else:
            highlights.append((s, '🟢'))
    return highlights

def compare_to_sample(user_text, sample_text):
    user_sents = split_sentences(user_text.lower())
    sample_sents = split_sentences(sample_text.lower())
    matcher = difflib.SequenceMatcher(None, ' '.join(user_sents), ' '.join(sample_sents))
    return round(matcher.ratio() * 100, 2)

def detect_with_api(text, api_key):
    try:
        url = "https://api.gptzero.me/v2/predict"  # Replace if using another API
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(url, json={"document": text}, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get("documents", [{}])[0].get("score", None)
        return None
    except:
        return None

# ------------------------------
# INPUTS
# ------------------------------
input_text = st.text_area("Paste
