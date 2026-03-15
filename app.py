import streamlit as st
from PIL import Image
import base64
import io
import requests
import json
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Story Forge AI",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400&display=swap');

:root {
    --bg:        #0d0b08;
    --surface:   #141210;
    --surface2:  #1a1714;
    --border:    #2a2520;
    --gold:      #c9a84c;
    --gold-dim:  #7a6230;
    --text:      #e8e0d4;
    --muted:     #7a7060;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Crimson Pro', serif;
}
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 2px; }

.hero { text-align: center; padding: 2rem 0 1.5rem; }
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem; font-weight: 900; color: var(--gold);
    letter-spacing: 0.04em; line-height: 1.05;
    text-shadow: 0 0 60px rgba(201,168,76,0.3); margin: 0;
}
.hero-italic { font-style: italic; color: #e8c97a; }
.hero-tagline {
    font-family: 'Crimson Pro', serif; font-style: italic;
    font-size: 1.15rem; color: var(--muted); margin-top: 6px; letter-spacing: 0.05em;
}
.hero-rule { border: none; border-top: 1px solid var(--gold-dim); width: 200px; margin: 1.2rem auto 0; opacity: 0.5; }
.ornament { color: var(--gold-dim); font-size: 1.2rem; margin: 0 12px; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stTextInput > div > input {
    background: var(--bg) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important; border-radius: 6px !important;
}
.sidebar-section {
    font-family: 'Playfair Display', serif; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold-dim); margin: 1.2rem 0 0.5rem;
}

.section-label {
    font-family: 'Playfair Display', serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 8px;
}
.img-frame { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; background: var(--surface); }

.info-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.2);
    border-radius: 6px; padding: 5px 12px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--gold-dim); margin: 3px;
}

.story-wrap { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }
.story-header {
    background: linear-gradient(135deg, #1a1510, #221c14);
    border-bottom: 1px solid var(--border); padding: 1.4rem 2rem 1.2rem;
}
.story-genre-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 6px;
}
.story-title {
    font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 700;
    font-style: italic; color: var(--gold); line-height: 1.2;
    text-shadow: 0 2px 20px rgba(201,168,76,0.25);
}
.story-body {
    padding: 1.8rem 2.2rem 2rem; font-family: 'Crimson Pro', serif;
    font-size: 1.1rem; line-height: 2; color: #d4c9b8; white-space: pre-wrap;
}
.story-body::first-letter {
    font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 900;
    color: var(--gold); float: left; line-height: 0.75; margin: 8px 8px 0 0;
    text-shadow: 0 0 30px rgba(201,168,76,0.4);
}
.chars-section {
    border-top: 1px solid var(--border); padding: 1.2rem 2.2rem; display: flex; gap: 10px; flex-wrap: wrap;
}
.char-chip {
    background: var(--surface2); border: 1px solid var(--border); border-radius: 20px;
    padding: 5px 14px; font-family: 'Crimson Pro', serif; font-size: 0.88rem; color: var(--text);
}
.char-name { color: var(--gold); font-weight: 600; }

.stButton > button {
    background: linear-gradient(135deg, #8b6914, #c9a84c) !important;
    border: none !important; border-radius: 8px !important; color: #0d0b08 !important;
    font-family: 'Playfair Display', serif !important; font-weight: 700 !important;
    font-size: 1rem !important; letter-spacing: 0.06em !important;
    padding: 0.7rem 1.5rem !important; width: 100% !important; transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.9 !important; }
.stButton > button:disabled { background: var(--border) !important; color: var(--muted) !important; opacity: 0.6 !important; }

.stSelectbox > div > div {
    background: var(--surface2) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'Crimson Pro', serif !important; font-size: 1rem !important;
}

.err-box {
    background: rgba(139,38,53,0.15); border: 1px solid rgba(139,38,53,0.4);
    border-radius: 10px; padding: 1rem 1.4rem; color: #e87c8a;
    font-family: 'Crimson Pro', serif; font-size: 1rem;
}
.ok-box {
    background: rgba(45,90,61,0.2); border: 1px solid rgba(45,90,61,0.5);
    border-radius: 10px; padding: 0.8rem 1.2rem; color: #6fcf97;
    font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
}
.warn-box {
    background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.25);
    border-radius: 10px; padding: 0.8rem 1.2rem; color: var(--gold-dim);
    font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
}

.stDownloadButton > button {
    background: transparent !important; border: 1px solid var(--gold-dim) !important;
    color: var(--gold) !important; font-family: 'Crimson Pro', serif !important;
    font-size: 0.9rem !important; border-radius: 8px !important; padding: 0.45rem 1.2rem !important; width: auto !important;
}
.empty-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 500px; border: 1px dashed var(--border); border-radius: 16px;
    text-align: center; padding: 2rem;
}
.model-chip {
    display: inline-block; background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.3);
    border-radius: 4px; padding: 2px 8px; font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: var(--gold);
}
</style>
""", unsafe_allow_html=True)


# ── Ollama helpers ─────────────────────────────────────────────────────────────

OLLAMA_BASE = "http://localhost:11434"

VISION_MODELS = [
    "llava:13b",
    "llava:34b",
    "llava-llama3",
    "moondream",
    "bakllava",
    "llava-phi3",
]


def get_ollama_models() -> list[str]:
    """Fetch models currently pulled in Ollama."""
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=4)
        if r.status_code == 200:
            names = [m["name"] for m in r.json().get("models", [])]
            return names
    except Exception:
        pass
    return []


def check_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def image_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()


def call_ollama(model: str, prompt: str, image: Image.Image) -> str:
    """Call Ollama /api/generate with an image."""
    img_b64 = image_to_base64(image)
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
    }
    r = requests.post(
        f"{OLLAMA_BASE}/api/generate",
        json=payload,
        timeout=300,
    )
    r.raise_for_status()
    return r.json().get("response", "")


# ── Genre / config data ────────────────────────────────────────────────────────

GENRES = {
    "Horror":    {"icon": "🕷️", "tone": "dark, terrifying, suspenseful, gothic",         "desc": "Dark & Terrifying"},
    "Fantasy":   {"icon": "🧝", "tone": "epic, magical, wonder-filled, mythic",           "desc": "Epic & Magical"},
    "Sci-Fi":    {"icon": "🚀", "tone": "futuristic, technological, thought-provoking",   "desc": "Futuristic & Cosmic"},
    "Mystery":   {"icon": "🔎", "tone": "suspenseful, intriguing, atmospheric, twisty",   "desc": "Suspense & Intrigue"},
    "Romance":   {"icon": "🌹", "tone": "passionate, emotional, tender, evocative",       "desc": "Passionate & Tender"},
    "Adventure": {"icon": "⚔️", "tone": "thrilling, fast-paced, heroic, daring",          "desc": "Thrilling & Heroic"},
}

LENGTH_MAP = {
    "Short  (~150 words)": 150,
    "Medium (~300 words)": 300,
    "Long   (~500 words)": 500,
}

POV_OPTIONS = ["Third Person", "First Person", "Second Person (You)"]


def build_prompt(genre: str, length: int, pov: str, extra: str) -> str:
    tone = GENRES[genre]["tone"]
    pov_map = {
        "Third Person":        "Write in third-person (he/she/they).",
        "First Person":        "Write in first-person (I/me/my).",
        "Second Person (You)": "Write in second-person, addressing the reader as 'you'.",
    }
    extra_line = f"\nExtra instructions: {extra.strip()}" if extra.strip() else ""
    return f"""You are a master storyteller. Look at this image carefully.
Create a compelling {genre} story inspired by what you see.

Rules:
- Genre: {genre}. Tone must be: {tone}.
- Length: approximately {length} words.
- POV: {pov_map[pov]}
- Invent 2-3 vivid named characters that fit the scene.
- Write an evocative TITLE (3-7 words).
- Reference specific visual details from the image.{extra_line}

Respond using EXACTLY this format, with no extra commentary:

TITLE: [your title here]

CHARACTERS:
- [Name] | [Role] | [One-sentence description]
- [Name] | [Role] | [One-sentence description]

STORY:
[Your full story here]"""


def parse_output(raw: str):
    title, characters, story = "Untitled", [], raw
    try:
        if "TITLE:" in raw:
            title = raw.split("TITLE:")[1].split("\n")[0].strip().strip('"').strip("'")
        if "CHARACTERS:" in raw and "STORY:" in raw:
            chars_block = raw.split("CHARACTERS:")[1].split("STORY:")[0]
            for line in chars_block.strip().splitlines():
                line = line.strip().lstrip("-").strip()
                if "|" in line and len(line) > 4:
                    characters.append(line)
        if "STORY:" in raw:
            story = raw.split("STORY:")[1].strip()
    except Exception:
        pass
    return title, characters, story


# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem;'>
        <div style='font-family: Playfair Display, serif; font-size:1.4rem;
                    font-weight:900; font-style:italic; color:#c9a84c;'>
            Story Forge
        </div>
        <div style='font-size:0.68rem; color:#7a7060; letter-spacing:0.15em; text-transform:uppercase;'>
            Powered by Ollama · 100% Local
        </div>
    </div>
    <hr style='border-color:#2a2520; margin: 0.8rem 0 0.6rem'>
    """, unsafe_allow_html=True)

    # ── Ollama status ──
    st.markdown("<div class='sidebar-section'>Ollama Status</div>", unsafe_allow_html=True)
    ollama_ok = check_ollama_running()

    if ollama_ok:
        st.markdown("<div class='ok-box'>✓ Ollama is running</div>", unsafe_allow_html=True)
        available_models = get_ollama_models()
        vision_available = [m for m in available_models if any(v in m for v in ["llava", "moondream", "bakllava", "phi3"])]
    else:
        st.markdown("""
        <div class='err-box'>
            ✗ Ollama not detected<br>
            <span style='font-size:0.78rem;'>Start it with: <code>ollama serve</code></span>
        </div>
        """, unsafe_allow_html=True)
        available_models = []
        vision_available = []

    # ── Model selector ──
    st.markdown("<div class='sidebar-section'>Vision Model</div>", unsafe_allow_html=True)

    if vision_available:
        selected_model = st.selectbox("", vision_available, label_visibility="collapsed")
        st.markdown(f"<div class='ok-box' style='margin-top:4px;'>✓ Ready to use</div>", unsafe_allow_html=True)
    else:
        # Let user type a model name manually
        selected_model = st.selectbox("", VISION_MODELS, label_visibility="collapsed")
        st.markdown(f"""
        <div class='warn-box' style='margin-top:4px;'>
            ⚠ Model not pulled yet.<br>
            Run in terminal:<br>
            <code style='color:#c9a84c;'>ollama pull {selected_model}</code>
        </div>
        """, unsafe_allow_html=True)

    if available_models and not vision_available:
        st.markdown(f"<div style='font-size:0.75rem; color:#7a7060; margin-top:6px;'>No vision model found among your {len(available_models)} installed model(s).</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2a2520; margin: 1rem 0'>", unsafe_allow_html=True)

    # ── Story settings ──
    st.markdown("<div class='sidebar-section'>Genre</div>", unsafe_allow_html=True)
    selected_genre = st.selectbox("", list(GENRES.keys()), label_visibility="collapsed")
    g = GENRES[selected_genre]
    st.markdown(f"<div style='font-style:italic; color:#7a7060; font-size:0.88rem; margin-top:4px;'>{g['icon']} {g['desc']}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section' style='margin-top:1rem;'>Story Length</div>", unsafe_allow_html=True)
    selected_length = st.selectbox("", list(LENGTH_MAP.keys()), index=1, label_visibility="collapsed")

    st.markdown("<div class='sidebar-section' style='margin-top:1rem;'>Point of View</div>", unsafe_allow_html=True)
    selected_pov = st.selectbox(" ", POV_OPTIONS, label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2a2520; margin: 1rem 0'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section'>Extra Instructions</div>", unsafe_allow_html=True)
    extra_instructions = st.text_area("", placeholder="e.g. Add a mysterious old letter, set it at dusk…", height=85, label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2a2520; margin: 1rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#4a4438; line-height:1.8;'>
        <b style='color:#7a7060;'>Setup guide:</b><br>
        1. Install → <code>winget install Ollama.Ollama</code><br>
        2. Start &nbsp;→ <code>ollama serve</code><br>
        3. Pull &nbsp;&nbsp;→ <code>ollama pull llava</code>
    </div>
    """, unsafe_allow_html=True)


# ── Hero header ────────────────────────────────────────────────────────────────

st.markdown("""
<div class='hero'>
    <div class='hero-title'>Story <span class='hero-italic'>Forge</span></div>
    <div class='hero-tagline'>
        <span class='ornament'>✦</span>
        Upload an image. Summon a story. No API key needed.
        <span class='ornament'>✦</span>
    </div>
    <hr class='hero-rule'>
</div>
""", unsafe_allow_html=True)

# ── Main columns ───────────────────────────────────────────────────────────────

col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    st.markdown("<div class='section-label'>Upload Your Image</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")

    if uploaded:
        image = Image.open(uploaded)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        st.markdown("<div class='img-frame'>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        w, h = image.size
        size_kb = len(uploaded.getvalue()) / 1024
        st.markdown(f"""
        <div style='display:flex; flex-wrap:wrap; gap:4px; margin-top:10px;'>
            <span class='info-badge'>📐 {w}×{h}</span>
            <span class='info-badge'>🗜 {size_kb:.0f} KB</span>
            <span class='info-badge'>{g['icon']} {selected_genre}</span>
            <span class='info-badge'>🤖 <span class='model-chip'>{selected_model}</span></span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='border:1px dashed #2a2520; border-radius:12px; min-height:280px;
                    display:flex; flex-direction:column; align-items:center; justify-content:center;
                    color:#4a4438; font-style:italic; font-size:1rem; padding:2rem; text-align:center;'>
            <div style='font-size:2.5rem; opacity:0.3; margin-bottom:10px;'>🖼️</div>
            Drop your image here<br>
            <span style='font-size:0.8rem;'>JPG · PNG · WEBP · BMP</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
    can_run = uploaded and ollama_ok
    generate_btn = st.button("✦ Forge the Story", disabled=not can_run)

    if not ollama_ok:
        st.markdown("""
        <div class='err-box' style='margin-top:0.6rem;'>
            ⚠ Start Ollama first:<br>
            <code style='font-size:0.82rem;'>ollama serve</code>
        </div>
        """, unsafe_allow_html=True)
    elif not uploaded:
        st.markdown("<div style='color:#4a4438; font-size:0.88rem; margin-top:0.5rem; font-style:italic;'>↑ Upload an image to begin.</div>", unsafe_allow_html=True)


# ── Output ─────────────────────────────────────────────────────────────────────

with col_right:
    output_placeholder = st.empty()

    if "story_result" not in st.session_state:
        st.session_state.story_result  = None
        st.session_state.story_title   = None
        st.session_state.story_chars   = []
        st.session_state.story_genre   = None
        st.session_state.story_model   = None
        st.session_state.story_elapsed = None

    if generate_btn and uploaded and ollama_ok:
        with output_placeholder.container():
            with st.spinner(f"Running {selected_model} locally… this may take 30–90 seconds."):
                t0 = time.time()
                try:
                    prompt = build_prompt(
                        selected_genre,
                        LENGTH_MAP[selected_length],
                        selected_pov,
                        extra_instructions,
                    )
                    raw = call_ollama(selected_model, prompt, image)
                    title, characters, story = parse_output(raw)
                    st.session_state.story_result  = story
                    st.session_state.story_title   = title
                    st.session_state.story_chars   = characters
                    st.session_state.story_genre   = selected_genre
                    st.session_state.story_model   = selected_model
                    st.session_state.story_elapsed = round(time.time() - t0, 1)
                except requests.exceptions.ConnectionError:
                    st.session_state.story_result = "ERROR:Could not connect to Ollama. Make sure it's running: ollama serve"
                except Exception as e:
                    st.session_state.story_result = f"ERROR:{e}"

    if st.session_state.story_result:
        with output_placeholder.container():
            if str(st.session_state.story_result).startswith("ERROR:"):
                st.markdown(f"<div class='err-box'>❌ {st.session_state.story_result[6:]}</div>", unsafe_allow_html=True)
            else:
                genre_info = GENRES.get(st.session_state.story_genre, {})
                icon  = genre_info.get("icon", "📖")
                desc  = genre_info.get("desc", "")
                model = st.session_state.story_model or selected_model
                elapsed = st.session_state.story_elapsed

                chars_html = ""
                if st.session_state.story_chars:
                    chips = ""
                    for c in st.session_state.story_chars:
                        parts = [p.strip() for p in c.split("|")]
                        name    = parts[0] if parts else c
                        tooltip = " · ".join(parts[1:]) if len(parts) > 1 else ""
                        chips += f"<div class='char-chip'><span class='char-name'>{name}</span>{' · ' + tooltip if tooltip else ''}</div>"
                    chars_html = f"<div class='chars-section'>{chips}</div>"

                story_escaped = (
                    st.session_state.story_result
                    .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                )

                st.markdown(f"""
                <div class='story-wrap'>
                    <div class='story-header'>
                        <div class='story-genre-badge'>
                            {icon} {desc} &nbsp;·&nbsp; {st.session_state.story_genre}
                            &nbsp;·&nbsp; <span class='model-chip'>{model}</span>
                            &nbsp;·&nbsp; {elapsed}s
                        </div>
                        <div class='story-title'>{st.session_state.story_title}</div>
                    </div>
                    <div class='story-body'>{story_escaped}</div>
                    {chars_html}
                </div>
                """, unsafe_allow_html=True)

                full_text = (
                    f"# {st.session_state.story_title}\n\n"
                    f"Genre: {st.session_state.story_genre} | Model: {model}\n\n"
                )
                if st.session_state.story_chars:
                    full_text += "## Characters\n" + "\n".join(f"- {c}" for c in st.session_state.story_chars) + "\n\n"
                full_text += "## Story\n\n" + st.session_state.story_result

                st.markdown("<div style='margin-top:0.8rem;'>", unsafe_allow_html=True)
                st.download_button(
                    "⬇ Download Story",
                    data=full_text,
                    file_name=f"{st.session_state.story_title.replace(' ', '_')}.txt",
                    mime="text/plain",
                )
    else:
        output_placeholder.markdown("""
        <div class='empty-state'>
            <div style='font-size:3rem; opacity:0.2; margin-bottom:1rem;'>✒️</div>
            <div style='font-family: Crimson Pro, serif; font-style:italic; color:#4a4438; font-size:1rem;'>
                Your story awaits.<br>
                Upload an image and click Forge.
            </div>
        </div>
        """, unsafe_allow_html=True)
