import streamlit as st
from transcribe import transcribe
from summarize import summarize

st.set_page_config(
    page_title="Call Transcriber",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0e0e0e !important;
    color: #e8e8e8;
    font-family: 'IBM Plex Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: #0e0e0e;
    padding: 2rem 2.5rem;
}

h1 {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
    color: #f0f0f0 !important;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #555;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] label {
    color: #888 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: #111 !important;
    border: 1px dashed #333 !important;
    border-radius: 6px !important;
}

/* Run button */
.stButton > button {
    background: #c8f04e !important;
    color: #0e0e0e !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.8rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #d9ff5a !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background: #2a2a2a !important;
    color: #555 !important;
    cursor: not-allowed !important;
}

/* Output box wrapper */
.box-wrap {
    background: #121212;
    border: 1px solid #222;
    border-radius: 10px;
    overflow: hidden;
}

.box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 1rem;
    background: #181818;
    border-bottom: 1px solid #222;
}

.box-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #c8f04e;
}



.box-content {
    padding: 1rem;
    min-height: 340px;
    max-height: 540px;
    overflow-y: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.75;
    color: #ccc;
    white-space: pre-wrap;
    word-break: break-word;
}

.box-content.empty {
    color: #333;
    font-style: italic;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
}

/* Spinner color override */
.stSpinner > div { border-top-color: #c8f04e !important; }

/* Hide streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
header { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
</style>


""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("<h1>🎙️ Call Transcriber</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transcribe &amp; summarize audio calls</div>', unsafe_allow_html=True)

# ── Upload + Run ─────────────────────────────────────────────────────────────
col_up, col_btn = st.columns([4, 1])

with col_up:
    uploaded = st.file_uploader(
        "Upload audio file",
        type=["mp3", "wav", "m4a", "ogg", "flac", "webm", "mp4"],
        label_visibility="collapsed"
    )

with col_btn:
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    run = st.button("▶ Run", disabled=(uploaded is None))

# ── Session state ─────────────────────────────────────────────────────────────
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "stage" not in st.session_state:
    st.session_state.stage = "idle"  # idle → transcribing → summarizing → done
if "pending_file" not in st.session_state:
    st.session_state.pending_file = None

# ── Kick off on Run ───────────────────────────────────────────────────────────
if run and uploaded:
    st.session_state.transcript = ""
    st.session_state.summary = ""
    st.session_state.pending_file = uploaded
    st.session_state.stage = "transcribing"
    st.rerun()

# ── Stage: transcribing ───────────────────────────────────────────────────────
if st.session_state.stage == "transcribing":
    with st.spinner("Transcribing…"):
        st.session_state.transcript = transcribe(st.session_state.pending_file)
    st.session_state.stage = "summarizing"
    st.rerun()

# ── Stage: summarizing ────────────────────────────────────────────────────────
if st.session_state.stage == "summarizing":
    with st.spinner("Summarizing…"):
        st.session_state.summary = summarize(
            st.session_state.transcript,
            filename=st.session_state.pending_file.name
        )
    st.session_state.stage = "done"

# ── Output boxes ──────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="medium")

import re
import html

def format_transcript(text):
    """Bold the [MM:SS] Speaker: prefix on each line."""
    lines = text.split("\n")
    out = []
    for line in lines:
        escaped = html.escape(line)
        # Match [timestamp] Speaker: or just Speaker:
        formatted = re.sub(
            r'^(\[?\d{2}:\d{2}\]?\s*\w[\w\s]*:)',
            r'<strong>\1</strong>',
            escaped
        )
        out.append(formatted)
    return "<br>".join(out)

def format_summary(text):
    """Bold the Field_Label: keys on each line."""
    lines = text.split("\n")
    out = []
    for line in lines:
        escaped = html.escape(line)
        formatted = re.sub(
            r'^(\w[\w_&amp;\s]*:)',
            r'<strong>\1</strong>',
            escaped
        )
        out.append(formatted)
    return "<br>".join(out)

def render_box(label, content, box_id):
    empty_msg = f"— {label.lower()} will appear here —"
    inner_class = "box-content" if content else "box-content empty"
    if content:
        if box_id == "transcript-box":
            formatted = format_transcript(content)
        else:
            formatted = format_summary(content)
        inner_html = f'<div id="{box_id}" class="{inner_class}">{formatted}</div>'
    else:
        inner_html = f'<div id="{box_id}" class="{inner_class}">{empty_msg}</div>'

    st.markdown(f"""
    <div class="box-wrap">
        <div class="box-header">
            <span class="box-label">{label}</span>
        </div>
        {inner_html}
    </div>
    """, unsafe_allow_html=True)

with left:
    render_box("Transcript", st.session_state.transcript, "transcript-box")

with right:
    render_box("Summary", st.session_state.summary, "summary-box")