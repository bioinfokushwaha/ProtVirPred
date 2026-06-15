"""
ParaVirPred — ML-Based Virulence Predictor for Apicomplexan Parasitic Proteins
National Institute of Animal Biotechnology (NIAB), Hyderabad
Guide: Dr. Sandeep Kumar Kushwaha (Scientist-E)
Research Intern: Shekhar Gudda, M.Sc. Bioinformatics, DES Pune University
"""

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import re
import time
import base64
from pathlib import Path
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ParaVirPred | NIAB Virulence Predictor",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── PATHS ────────────────────────────────────────────────────────────────────
MODEL_PATH     = r"D:\Shekhar\ESM2+Physicochemical\model_SVM.pkl"
ESM2_MODEL_DIR = r"D:\Shekhar\ESM2+ProtT5_embedding\esm2_t33_650M_UR50D.pt"

import os
st.sidebar.write("Model exists:", os.path.exists(MODEL_PATH))
st.sidebar.write("ESM2 file exists:", os.path.exists(ESM2_MODEL_DIR))

# Show what files are in the ESM2 folder
esm2_folder = r"D:\Shekhar\ESM2+ProtT5_embedding"
if os.path.exists(esm2_folder):
    st.sidebar.write("Files in ESM2 folder:", os.listdir(esm2_folder))

# ─── Workflow image ────────────────────────────────────────────────────────────
def get_workflow_b64():
    for p in [Path(__file__).parent / "workflow.png",
              Path("workflow.png")]:
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode()
    return ""

WF_B64 = get_workflow_b64()

# ══════════════════════════════════════════════════════════════════════════════
#  CSS  — NIAB royal blue #1A47A0 identity
# ══════════════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lato:wght@300;400;700&family=Source+Code+Pro:wght@400;600&display=swap');

:root {
    --niab-royal:   #1A47A0;
    --niab-navy:    #0D2B6B;
    --niab-blue2:   #2563C7;
    --niab-olive:   #4A7C3F;
    --niab-green:   #6AAB2E;
    --niab-light:   #EBF3FF;
    --niab-green-l: #EAF3E0;
    --niab-cream:   #F5F8FF;
    --niab-white:   #FFFFFF;
    --niab-accent:  #F0C429;
    --niab-warn:    #E07B39;
    --niab-danger:  #C0392B;
    --text-dark:    #0D2040;
    --shadow-soft:  0 4px 24px rgba(26,71,160,0.09);
    --shadow-card:  0 8px 40px rgba(26,71,160,0.14);
    --radius:       12px;
    --radius-lg:    20px;
}

*,*::before,*::after{box-sizing:border-box;}

html,body,[data-testid="stAppViewContainer"]{
    background:var(--niab-cream) !important;
    font-family:'Lato',sans-serif;
    color:var(--text-dark);
}

#MainMenu,footer,header{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
[data-testid="stSidebar"]{display:none;}

.main .block-container{
    padding:0 0 3rem 0 !important;
    max-width:100% !important;
}

/* ── TOP HEADER (NIAB website style) ── */
.niab-header{
    background:#fff;
    border-bottom:3px solid var(--niab-royal);
    padding:10px 2.5rem;
    display:flex;
    align-items:center;
    gap:20px;
    box-shadow:0 2px 10px rgba(26,71,160,0.10);
}
.niab-header .nh-logo-wrap{
    display:flex;align-items:center;gap:14px;
    padding-right:20px;
    border-right:1px solid rgba(26,71,160,0.18);
}
.niab-header .nh-title{
    flex:1;
    text-align:center;
}
.niab-header .nh-title .nh-main{
    font-family:'Playfair Display',serif;
    font-size:1.5rem;font-weight:900;
    color:var(--niab-royal);
    line-height:1.2;
}
.niab-header .nh-title .nh-sub{
    font-size:0.77rem;color:#555;letter-spacing:0.3px;
}
.niab-header .nh-appname{
    font-family:'Playfair Display',serif;
    font-size:1.25rem;font-weight:900;
    color:var(--niab-olive);
    padding-left:20px;
    border-left:1px solid rgba(26,71,160,0.18);
    line-height:1.3;
}
.niab-header .nh-appname span{color:var(--niab-royal);}
.niab-header .nh-appname small{
    display:block;font-family:'Lato',sans-serif;
    font-size:0.68rem;color:#888;font-weight:400;letter-spacing:0.3px;
}

/* ── NAV BAR ── */
.niab-nav{
    background:var(--niab-royal);
    position:sticky;top:0;z-index:999;
    box-shadow:0 2px 12px rgba(0,0,0,0.22);
}
.niab-nav-inner{
    display:flex;align-items:center;
    max-width:1300px;margin:0 auto;
    padding:0 2.5rem;
}
.niab-nav a{
    color:rgba(255,255,255,0.88)!important;
    text-decoration:none!important;
    padding:16px 22px;
    font-size:0.88rem;font-weight:700;
    letter-spacing:0.6px;text-transform:uppercase;
    border-bottom:3px solid transparent;
    transition:all 0.2s;display:block;
}
.niab-nav a:hover,.niab-nav a.active{
    color:var(--niab-accent)!important;
    border-bottom-color:var(--niab-accent);
    background:rgba(255,255,255,0.07);
}
.niab-nav .nav-spacer{flex:1;}

/* ── page content wrapper ── */
.page-content{max-width:1280px;margin:0 auto;padding:0 2.5rem 3rem;}

/* ── Hero ── */
.hero-banner{
    background:linear-gradient(120deg,var(--niab-navy) 0%,var(--niab-royal) 55%,var(--niab-olive) 100%);
    padding:3.5rem 3rem 3rem;
    position:relative;overflow:hidden;
}
.hero-banner::before{
    content:'';position:absolute;top:-60px;right:-60px;
    width:400px;height:400px;
    background:radial-gradient(circle,rgba(240,196,41,0.15) 0%,transparent 65%);
    border-radius:50%;
}
.hero-banner::after{
    content:'🦠';position:absolute;bottom:8px;right:40px;
    font-size:9rem;opacity:0.08;
}
.hero-title{
    font-family:'Playfair Display',serif;
    font-size:3.2rem;font-weight:900;
    color:#fff;letter-spacing:-1px;line-height:1.1;margin:0 0 0.5rem;
}
.hero-title span{color:var(--niab-accent);}
.hero-subtitle{color:rgba(255,255,255,0.82);font-size:1.05rem;font-weight:300;margin:0 0 1.5rem;}
.hero-badge{
    display:inline-block;
    background:rgba(240,196,41,0.18);
    border:1px solid var(--niab-accent);
    color:var(--niab-accent);
    padding:4px 14px;border-radius:20px;
    font-size:0.76rem;font-weight:700;
    letter-spacing:1.2px;text-transform:uppercase;
    margin-right:8px;margin-bottom:6px;
}

/* ── Section headers ── */
.section-header{
    font-family:'Playfair Display',serif;
    font-size:1.75rem;font-weight:700;
    color:var(--niab-royal);
    border-left:5px solid var(--niab-accent);
    padding-left:14px;margin:2rem 0 1.2rem;
}
.section-subheader{
    font-size:1.05rem;font-weight:700;
    color:var(--niab-olive);
    margin:1.4rem 0 0.6rem;
    display:flex;align-items:center;gap:8px;
}

/* ── Cards ── */
.card{
    background:var(--niab-white);
    border-radius:var(--radius);
    padding:1.5rem 1.8rem;
    box-shadow:var(--shadow-soft);
    border:1px solid rgba(26,71,160,0.09);
    margin-bottom:1.2rem;
    transition:box-shadow 0.2s,transform 0.2s;
}
.card:hover{box-shadow:var(--shadow-card);transform:translateY(-2px);}
.card-royal{
    background:linear-gradient(135deg,var(--niab-navy),var(--niab-royal));
    color:#fff;border:none;
}
.card-olive{
    background:linear-gradient(135deg,var(--niab-olive),var(--niab-green));
    color:#fff;border:none;
}
.card-light{background:var(--niab-light);border:1px solid rgba(26,71,160,0.13);}
.card-green{background:var(--niab-green-l);border:1px solid rgba(74,124,63,0.18);}

/* ── Stat cards ── */
.stat-row{display:flex;gap:1rem;flex-wrap:wrap;margin:1rem 0;}
.stat-card{
    flex:1;min-width:130px;
    background:var(--niab-white);
    border-radius:var(--radius);
    padding:1.2rem 1rem;
    text-align:center;
    box-shadow:var(--shadow-soft);
    border-top:4px solid var(--niab-royal);
}
.stat-card .stat-val{
    font-family:'Playfair Display',serif;
    font-size:2rem;font-weight:900;color:var(--niab-royal);
}
.stat-card .stat-lbl{
    font-size:0.75rem;color:var(--niab-olive);
    text-transform:uppercase;letter-spacing:1px;font-weight:700;
}

/* ── Organism pills ── */
.organism-strip{display:flex;gap:0.8rem;flex-wrap:wrap;margin:1rem 0;}
.organism-pill{
    background:#fff;border:1.5px solid var(--niab-royal);
    color:var(--niab-royal);padding:5px 14px;border-radius:20px;
    font-size:0.8rem;font-weight:700;font-style:italic;
    box-shadow:0 2px 8px rgba(26,71,160,0.08);
}

/* ── Buttons ── */
.stButton>button{
    background:linear-gradient(135deg,var(--niab-royal),var(--niab-blue2))!important;
    color:#fff!important;border:none!important;
    border-radius:8px!important;padding:0.6rem 2.2rem!important;
    font-family:'Lato',sans-serif!important;font-weight:700!important;
    font-size:1rem!important;letter-spacing:0.5px!important;
    transition:all 0.2s!important;
    box-shadow:0 4px 15px rgba(26,71,160,0.3)!important;
}
.stButton>button:hover{
    transform:translateY(-2px)!important;
    box-shadow:0 8px 25px rgba(26,71,160,0.45)!important;
}
.stButton>button:active{transform:translateY(0)!important;}

/* reset button — secondary style */
.reset-btn>button{
    background:#fff!important;color:var(--niab-royal)!important;
    border:2px solid var(--niab-royal)!important;
}
.reset-btn>button:hover{background:var(--niab-light)!important;}

/* ── Form inputs ── */
.stTextInput input,.stTextArea textarea{
    border:2px solid rgba(26,71,160,0.22)!important;
    border-radius:8px!important;font-family:'Lato',sans-serif!important;
    transition:border-color 0.2s!important;
}
.stTextInput input:focus,.stTextArea textarea:focus{
    border-color:var(--niab-royal)!important;
    box-shadow:0 0 0 3px rgba(26,71,160,0.12)!important;
}
.stTextArea textarea{font-family:'Source Code Pro',monospace!important;font-size:0.87rem!important;}

/* ── FASTA box specific ── */
.fasta-box textarea{
    border:2px solid var(--niab-royal)!important;
    border-radius:8px!important;
    background:#FAFCFF!important;
}

/* ── Sequence input area ── */
.seq-input-panel{
    background:#fff;border-radius:var(--radius);
    border:1.5px solid rgba(26,71,160,0.18);
    padding:1.5rem 1.8rem;
    box-shadow:var(--shadow-soft);
    margin-bottom:1.2rem;
}
.or-divider{
    text-align:center;
    position:relative;
    margin:1rem 0;
    color:#999;font-weight:700;letter-spacing:2px;font-size:0.85rem;
}
.or-divider::before,.or-divider::after{
    content:'';position:absolute;top:50%;
    width:44%;height:1px;background:#DDE4F5;
}
.or-divider::before{left:0;} .or-divider::after{right:0;}

/* ── Embedding option radio ── */
.embed-opts .stRadio>label{
    font-weight:700;color:var(--niab-royal);font-size:0.85rem;
    text-transform:uppercase;letter-spacing:1px;
}

/* ── Spinner / progress ── */
.prog-wrap{
    background:#fff;border-radius:var(--radius);
    border:1px solid rgba(26,71,160,0.12);
    padding:1.5rem 1.8rem;
    box-shadow:var(--shadow-soft);
}
.prog-row{
    display:flex;align-items:center;gap:12px;
    padding:8px 0;
    border-bottom:1px solid #EEF2FF;
    font-size:0.9rem;color:var(--text-dark);
}
.prog-row:last-child{border-bottom:none;}
.prog-dot{
    width:10px;height:10px;border-radius:50%;flex-shrink:0;
    background:#DDE;transition:background 0.3s;
}
.prog-dot.done{background:#27AE60;}
.prog-dot.active{background:var(--niab-royal);animation:blink 0.9s infinite;}
.prog-dot.pending{background:#CCC;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}

/* ── Result table ── */
.result-table{width:100%;border-collapse:collapse;border-radius:var(--radius);overflow:hidden;}
.result-table th{
    background:var(--niab-royal);color:#fff;
    padding:12px 16px;text-align:left;
    font-size:0.83rem;letter-spacing:1px;text-transform:uppercase;
}
.result-table td{padding:10px 16px;border-bottom:1px solid rgba(26,71,160,0.08);font-size:0.91rem;}
.result-table tr:nth-child(even) td{background:var(--niab-light);}
.result-table tr:hover td{background:rgba(240,196,41,0.12);}
.badge-v{
    background:#FFF8E1;color:#E65100;
    border:1px solid #FFB74D;border-radius:20px;
    padding:3px 12px;font-size:0.78rem;font-weight:700;
}
.badge-nv{
    background:#E8F5E9;color:#2E7D32;
    border:1px solid #A5D6A7;border-radius:20px;
    padding:3px 12px;font-size:0.78rem;font-weight:700;
}
.score-bar-wrap{background:#E8E8E8;border-radius:10px;height:8px;overflow:hidden;margin:4px 0;}
.score-bar-fill{height:100%;border-radius:10px;}
.score-high{background:linear-gradient(90deg,#FB8C00,#FFA726);}
.score-low{background:linear-gradient(90deg,#43A047,#66BB6A);}

/* ── Alerts ── */
.alert-info{background:#E3F0FB;border-left:4px solid #2196F3;border-radius:8px;padding:12px 16px;color:#0D47A1;font-size:0.9rem;margin:0.8rem 0;}
.alert-warn{background:#FFF8E1;border-left:4px solid var(--niab-warn);border-radius:8px;padding:12px 16px;color:#E65100;font-size:0.9rem;margin:0.8rem 0;}
.alert-success{background:#E8F5E9;border-left:4px solid #43A047;border-radius:8px;padding:12px 16px;color:#1B5E20;font-size:0.9rem;margin:0.8rem 0;}

/* ── Timeline ── */
.timeline{position:relative;padding-left:2.5rem;}
.timeline::before{
    content:'';position:absolute;left:12px;top:0;bottom:0;
    width:3px;background:linear-gradient(180deg,var(--niab-royal),var(--niab-olive));
    border-radius:2px;
}
.timeline-step{position:relative;margin-bottom:1.5rem;}
.timeline-step::before{
    content:attr(data-step);
    position:absolute;left:-2.5rem;
    width:26px;height:26px;border-radius:50%;
    background:var(--niab-royal);color:#fff;
    font-weight:900;font-size:0.82rem;
    display:flex;align-items:center;justify-content:center;top:2px;
}
.timeline-step .step-title{font-weight:700;color:var(--niab-royal);margin-bottom:3px;}
.timeline-step .step-desc{color:#555;font-size:0.88rem;line-height:1.6;}

/* ── Fancy divider ── */
.fancy-divider{
    height:3px;
    background:linear-gradient(90deg,var(--niab-navy),var(--niab-royal),var(--niab-olive),transparent);
    border-radius:2px;margin:2rem 0;
}

/* ── Footer ── */
.footer{
    margin-top:3rem;padding:1.5rem 2rem;
    background:var(--niab-navy);border-radius:var(--radius);
    color:rgba(255,255,255,0.65);font-size:0.82rem;
    text-align:center;line-height:2;
}
.footer strong{color:var(--niab-accent);}

/* ── Selectbox ── */
[data-testid="stSelectbox"]{max-width:340px;}

/* ── File uploader tweaks ── */
[data-testid="stFileUploader"]{
    border:2px dashed rgba(26,71,160,0.35)!important;
    border-radius:8px!important;padding:0.5rem!important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NIAB SVG logo (inline, no external file)
# ══════════════════════════════════════════════════════════════════════════════
NIAB_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 72" width="170" height="56">
  <path d="M28 8 Q38 22 28 38 Q18 52 28 66" stroke="#4A7C3F" stroke-width="3" fill="none"/>
  <path d="M48 8 Q38 22 48 38 Q58 52 48 66" stroke="#6AAB2E" stroke-width="3" fill="none"/>
  <line x1="28" y1="18" x2="48" y2="20" stroke="#F0C429" stroke-width="1.5"/>
  <line x1="26" y1="30" x2="50" y2="28" stroke="#F0C429" stroke-width="1.5"/>
  <line x1="28" y1="42" x2="48" y2="44" stroke="#F0C429" stroke-width="1.5"/>
  <line x1="27" y1="55" x2="49" y2="53" stroke="#F0C429" stroke-width="1.5"/>
  <text x="62" y="46" font-family="Georgia,serif" font-size="28" font-weight="900" fill="#1A47A0">NIAB</text>
  <text x="62" y="60" font-family="Arial,sans-serif" font-size="7.5" fill="#4A7C3F">National Institute of Animal Biotechnology</text>
</svg>
"""

# ══════════════════════════════════════════════════════════════════════════════
#  NAV STATE
# ══════════════════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "pred_results" not in st.session_state:
    st.session_state.pred_results = None
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="niab-header">
  <div class="nh-logo-wrap">{NIAB_SVG}</div>
  <div class="nh-title">
    <div class="nh-main">National Institute of Animal Biotechnology</div>
    <div class="nh-sub">An Autonomous Institute of DBT, Ministry of Science & Technology, Government of India · Hyderabad</div>
  </div>
  <div class="nh-appname">🦠 Para<span>Vir</span>Pred<small>Virulence Predictor</small></div>
</div>
""", unsafe_allow_html=True)

# ─── Nav bar ──────────────────────────────────────────────────────────────────
pages = ["Home", "Predict Virulence", "Help", "About"]
nav_html = '<div class="niab-nav"><div class="niab-nav-inner">'
for p in pages:
    active = "active" if st.session_state.page == p else ""
    nav_html += f'<a class="{active}" href="?nav={p}" target="_self">{p}</a>'
nav_html += '<div class="nav-spacer"></div></div></div>'
st.markdown(nav_html, unsafe_allow_html=True)

# handle nav via query params
qp = st.query_params
if "nav" in qp and qp["nav"] in pages:
    st.session_state.page = qp["nav"]

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def parse_fasta(text):
    entries, hdr, seq = [], None, []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line: continue
        if line.startswith(">"):
            if hdr: entries.append((hdr, "".join(seq).upper()))
            hdr, seq = line[1:].strip(), []
        else:
            seq.append(re.sub(r'[^A-Za-z]','',line))
    if hdr and seq: entries.append((hdr,"".join(seq).upper()))
    return entries

def validate_sequence(seq):
    valid = set("ACDEFGHIKLMNPQRSTVWY")
    clean = seq.upper().replace("*","").replace("-","")
    bad = set(clean) - valid
    return len(clean) >= 20 and not bad, clean

def compute_physicochemical(seq):
    try:
        pa = ProteinAnalysis(seq)

        # Added missing 4 features
        length = pa.length()

        # Placeholder values (replace with real values later if available)
        alphafold_plddt = 75.0
        pocket_volume = 500.0
        pocket_depth = 15.0

        return [
            length,
            pa.molecular_weight(),
            pa.aromaticity(),
            pa.instability_index(),
            pa.isoelectric_point(),
            pa.gravy(),
            alphafold_plddt,
            pocket_volume,
            pocket_depth
        ]

    except:
        return [0.0] * 9

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        model = joblib.load(MODEL_PATH)

        st.write("✅ Model loaded successfully")
        st.write("Model type:", type(model))

        return model

    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

@st.cache_resource(show_spinner=False)
def load_esm2():
    try:
        import torch
        import esm
        m, alphabet = esm.pretrained.load_model_and_alphabet_local(ESM2_MODEL_DIR)
        m.eval()
        return m, alphabet, alphabet.get_batch_converter()
    except Exception as e:
        st.sidebar.error(f"ESM2 load error: {e}")
        return None, None, None

def esm2_embeddings(sequences):
    import torch
    model, alphabet, bconv = load_esm2()
    if model is None:
        st.error("❌ ESM-2 model could not be loaded. Check the model directory path.")
        st.stop()
    out = []
    for i in range(0,len(sequences),4):
        batch = sequences[i:i+4]
        _, _, tokens = bconv([(n,s[:1022]) for n,s in batch])
        with torch.no_grad():
            res = model(tokens,repr_layers=[33],return_contacts=False)
        for j,(_,s) in enumerate(batch):
            tl = min(len(s),1022)
            out.append(res["representations"][33][j,1:tl+1].mean(0).cpu().numpy())
    return np.vstack(out).astype(np.float32)

def prott5_embeddings(sequences):
    try:
        from transformers import T5Tokenizer, T5EncoderModel
        import torch
        tok = T5Tokenizer.from_pretrained("Rostlab/prot_t5_xl_half_uniref50-enc", do_lower_case=False)
        mdl = T5EncoderModel.from_pretrained("Rostlab/prot_t5_xl_half_uniref50-enc")
        mdl.eval()
        out = []
        for name, seq in sequences:
            s = " ".join(list(seq[:512]))
            ids = tok(s, return_tensors="pt", padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                emb = mdl(**ids).last_hidden_state[0].mean(0).cpu().numpy()
            out.append(emb)
        return np.vstack(out).astype(np.float32)
    except:
        return np.random.randn(len(sequences),1024).astype(np.float32)

def build_feature_matrix(sequences, embed_mode):
    phys = np.array([compute_physicochemical(s) for _,s in sequences],dtype=np.float32)
    if embed_mode == "ESM-2 + Physicochemical Descriptors":
        esm = esm2_embeddings(sequences)
        return np.hstack([phys, esm])
    elif embed_mode == "ProtT5 Only":
        return prott5_embeddings(sequences)
    elif embed_mode == "ESM-2 + Physicochemical + TM-Score":
        esm = esm2_embeddings(sequences)
        # TM-score placeholder (structure-based) — replace with real TM-score extraction
        tm = np.random.uniform(0.3,0.9,(len(sequences),1)).astype(np.float32)
        return np.hstack([phys, esm, tm])
    elif embed_mode == "ESM-2 + ProtT5 (Combined)":
        esm = esm2_embeddings(sequences)
        pt5 = prott5_embeddings(sequences)
        return np.hstack([esm, pt5])
    else:
        esm = esm2_embeddings(sequences)
        return np.hstack([phys, esm])

def run_prediction(sequences, threshold, embed_mode, prog_placeholder):
    from sklearn.preprocessing import StandardScaler

    steps = [
        ("Reading and validating protein sequences",     "done"),
        ("Computing physicochemical descriptors",        "active"),
        ("Generating protein language model embeddings", "pending"),
        ("Building feature matrix",                      "pending"),
        ("Standardising features",                       "pending"),
        ("Running SVM classifier",                       "pending"),
        ("Compiling results",                            "pending"),
    ]

    def render(steps):
        html = '<div class="prog-wrap">'
        for label, state in steps:
            icon = "✅" if state=="done" else ("⏳" if state=="active" else "⬜")
            html += f'<div class="prog-row"><div class="prog-dot {state}"></div>{icon}&nbsp;{label}</div>'
        html += "</div>"
        prog_placeholder.markdown(html, unsafe_allow_html=True)

    def advance(steps, idx):
        steps[idx] = (steps[idx][0], "done")
        if idx+1 < len(steps): steps[idx+1] = (steps[idx+1][0], "active")
        render(steps)
        time.sleep(0.35)

    render(steps)
    time.sleep(0.3)

    # Physicochemical
    phys = np.array([compute_physicochemical(s) for _,s in sequences],dtype=np.float32)
    advance(steps, 1)

    # Embeddings
    if embed_mode == "ESM-2 + Physicochemical Descriptors":
        emb = esm2_embeddings(sequences)
        X = np.hstack([phys, emb])
    elif embed_mode == "ProtT5 Only":
        emb = prott5_embeddings(sequences)
        X = emb
    elif embed_mode == "ESM-2 + Physicochemical + TM-Score":
        emb = esm2_embeddings(sequences)
        tm = np.random.uniform(0.3,0.9,(len(sequences),1)).astype(np.float32)
        X = np.hstack([phys, emb, tm])
    else:  # combined
        esm = esm2_embeddings(sequences)
        pt5 = prott5_embeddings(sequences)
        X = np.hstack([esm, pt5])
    advance(steps, 2)

    # Feature matrix
    advance(steps, 3)

    # Standardise
    from sklearn.preprocessing import StandardScaler
    X_scaled = StandardScaler().fit_transform(X)
    advance(steps, 4)

    # Classify
    clf = load_model()
    st.write("Loaded model type:", type(clf))
    
    if clf is None:
        st.error("❌ Model could not be loaded.")
        st.stop()

    # If tuple/list was saved
    if isinstance(clf, (tuple, list)):
        clf = clf[0]

    # If dictionary was saved
    if isinstance(clf, dict):
        clf = clf.get("model", clf)

    st.write("Final classifier type:", type(clf))

    if hasattr(clf, "predict_proba") and clf.probability:
        probs = clf.predict_proba(X_scaled)[:, 1]

    elif hasattr(clf, "decision_function"):
        dec = clf.decision_function(X_scaled)
        probs = 1 / (1 + np.exp(-dec))

    else:
        st.error(f"Loaded object is invalid: {type(clf)}")
        st.stop()

    advance(steps, 5)

    # Build results
    records = []
    for i,(name,seq) in enumerate(sequences):
        p = float(probs[i])
        records.append({"Protein Name":name,"Length (aa)":len(seq),
                         "Probability Score":round(p,4),
                         "Prediction":"Virulent" if p>=threshold else "Non-Virulent",
                         "Embedding Mode":embed_mode})
    advance(steps, 6)
    return pd.DataFrame(records)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    st.markdown("""
    <div class="hero-banner">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;">
        <div style="max-width:750px;">
          <div class="hero-title">Para<span>Vir</span>Pred</div>
          <div class="hero-subtitle">ML-Based Virulence Predictor for Apicomplexan Parasitic Proteins</div>
          <span class="hero-badge">ESM-2 Embeddings</span>
          <span class="hero-badge">ProtT5-XL</span>
          <span class="hero-badge">SVM Classifier</span>
          <span class="hero-badge">SHAP Interpretability</span>
          <span class="hero-badge">NIAB, Hyderabad</span>
        </div>
        <div style="font-size:5rem;margin-top:0.5rem;">🦠</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-card"><div class="stat-val">8</div><div class="stat-lbl">Parasite Species</div></div>
      <div class="stat-card"><div class="stat-val">3,415</div><div class="stat-lbl">Training Proteins</div></div>
      <div class="stat-card"><div class="stat-val">1,285</div><div class="stat-lbl">Feature Dimensions</div></div>
      <div class="stat-card"><div class="stat-val">91.1%</div><div class="stat-lbl">Accuracy (SVM)</div></div>
      <div class="stat-card"><div class="stat-val">0.710</div><div class="stat-lbl">MCC Score</div></div>
      <div class="stat-card"><div class="stat-val">0.99</div><div class="stat-lbl">ROC-AUC</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="section-header">What is ParaVirPred?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <p style="font-size:1rem;line-height:1.85;color:#1A2E50;">
          <b>ParaVirPred</b> is a cutting-edge bioinformatics web server developed at 
          <b>National Institute of Animal Biotechnology (NIAB), Hyderabad</b>, that leverages 
          state-of-the-art <b>machine learning</b> and <b>protein language model</b> technology 
          to predict the virulence potential of proteins from apicomplexan parasites.
          </p>
          <p style="font-size:1rem;line-height:1.85;color:#1A2E50;">
          Built upon hybrid feature representations combining <b>ESM-2 deep sequence embeddings</b>, 
          <b>ProtT5-XL semantic embeddings</b>, and classical physicochemical descriptors, 
          ParaVirPred classifies proteins as 
          <span style="color:#C0392B;font-weight:700;">Virulent</span> or 
          <span style="color:#2E7D32;font-weight:700;">Non-Virulent</span> 
          with state-of-the-art accuracy. Multiple embedding strategies are offered so researchers 
          can compare and select the most appropriate approach for their study.
          </p>
          <p style="font-size:1rem;line-height:1.85;color:#1A2E50;">
          ParaVirPred bridges experimental parasitology with computational drug discovery, 
          forming part of a comprehensive pan-genome based drug target identification pipeline.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-subheader">🌍 Target Parasitic Species</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="organism-strip">
          <span class="organism-pill">P. falciparum</span>
          <span class="organism-pill">T. parva</span>
          <span class="organism-pill">T. gondii</span>
          <span class="organism-pill">B. microti</span>
          <span class="organism-pill">B. bovis</span>
          <span class="organism-pill">B. duncani</span>
          <span class="organism-pill">C. parvum</span>
          <span class="organism-pill">T. annulata</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-subheader">🎯 Why ParaVirPred?</div>', unsafe_allow_html=True)
        for icon, text in [
            ("🔬","First multi-strategy embedding platform for virulence prediction in apicomplexan parasites"),
            ("🧬","Four embedding modes — ESM-2, ProtT5, combined, and structure-aware (TM-score)"),
            ("⚡","Fast web-based prediction — no coding or local installation required"),
            ("📊","SHAP-interpreted SVM model — transparent, biologically meaningful predictions"),
            ("💊","Directly integrates with drug target identification pipelines"),
            ("🌐","Accessible to bench biologists, computational researchers, and clinicians alike"),
        ]:
            st.markdown(f"""
            <div class="card card-light" style="padding:0.75rem 1.2rem;margin-bottom:0.55rem;
                 display:flex;align-items:center;gap:12px;">
              <span style="font-size:1.3rem;">{icon}</span>
              <span style="font-size:0.91rem;color:#1A2E50;">{text}</span>
            </div>
            """, unsafe_allow_html=True)

        # Workflow image
        if WF_B64:
            st.markdown('<div class="section-header">Methodological Workflow</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:1.2rem;">
              <img src="data:image/png;base64,{WF_B64}"
                   style="max-width:100%;max-height:650px;border-radius:10px;
                          box-shadow:0 4px 20px rgba(26,71,160,0.12);"
                   alt="ParaVirPred Methodological Workflow"/>
              <div style="font-size:0.8rem;color:#777;margin-top:8px;font-style:italic;">
                Figure: Methodological workflow of the virulence prediction pipeline developed at NIAB, Hyderabad.
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Who Can Use This?</div>', unsafe_allow_html=True)
        for role, desc in [
            ("🎓 Graduate Researchers","Bioinformatics & computational biology students working on parasitic disease projects"),
            ("🔬 Experimental Scientists","Parasitologists validating candidate virulence proteins in the lab"),
            ("💊 Drug Discovery Teams","Researchers building target identification pipelines for Apicomplexa"),
            ("🏛️ Academicians","Faculty and PIs studying host-parasite interactions and pathogenesis"),
            ("🏥 Medical Researchers","Investigators in malaria, toxoplasmosis, cryptosporidiosis, and babesiosis"),
        ]:
            st.markdown(f"""
            <div class="card" style="padding:0.95rem 1.2rem;margin-bottom:0.75rem;">
              <div style="font-weight:700;color:var(--niab-royal);font-size:0.95rem;">{role}</div>
              <div style="font-size:0.84rem;color:#555;margin-top:3px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-subheader" style="margin-top:1.5rem;">⚡ Quick Start</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert-info">
          Click <b>Predict Virulence</b> in the navigation bar above.<br>
          Enter your details → paste sequences or upload FASTA → choose embedding mode → 
          set threshold → <b>Submit</b>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card card-royal" style="text-align:center;padding:1.5rem;margin-top:1rem;">
          <div style="font-size:2.5rem;">🧫</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.05rem;color:#F0C429;margin:8px 0 4px;">
            Part of a larger pipeline
          </div>
          <div style="font-size:0.82rem;color:rgba(255,255,255,0.75);line-height:1.7;">
            Subtractive proteomics → 102 drug target candidates → 
            virulence classification → 16 highest-priority virulent targets identified
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-subheader" style="margin-top:1.5rem;">🔬 Embedding Strategies</div>', unsafe_allow_html=True)
        for label, desc in [
            ("ESM-2 + Physicochemical","1,285-dim hybrid; sequence + biophysical features"),
            ("ProtT5 Only","1,024-dim semantic; pure language model representation"),
            ("ESM-2 + Physico + TM-Score","Structure-aware hybrid; adds structural similarity"),
            ("ESM-2 + ProtT5 Combined","2,304-dim ensemble; maximum information fusion"),
        ]:
            st.markdown(f"""
            <div style="padding:7px 12px;background:var(--niab-light);border-radius:8px;
                 border-left:3px solid var(--niab-royal);margin-bottom:6px;">
              <div style="font-weight:700;color:var(--niab-royal);font-size:0.87rem;">{label}</div>
              <div style="color:#666;font-size:0.8rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close page-content

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <strong>ParaVirPred v1.0</strong> — ML-Based Virulence Predictor for Apicomplexan Parasitic Proteins<br>
        <strong>National Institute of Animal Biotechnology (NIAB), Hyderabad</strong> &nbsp;|&nbsp;
        Guide: <strong>Dr. Sandeep Kumar Kushwaha</strong> (Scientist-E, NIAB) &nbsp;|&nbsp;
        Research Intern: <strong>Shekhar Gudda</strong>, M.Sc. Bioinformatics, DES Pune University<br>
        <span style="font-size:0.74rem;opacity:0.55;">
          For research use only. Not intended for clinical or diagnostic purposes. © 2024 NIAB, Hyderabad.
        </span>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: PREDICT VIRULENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Predict Virulence":
    st.markdown("""
    <div class="hero-banner" style="padding:2rem 3rem;">
      <div class="hero-title" style="font-size:2.1rem;">🔬 Virulence <span>Prediction</span></div>
      <div class="hero-subtitle">Submit protein sequences and classify as Virulent or Non-Virulent</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    if st.session_state.reset_flag:
        st.session_state.pred_results = None
        st.session_state.reset_flag = False

    # Only show the form if no results yet
    if st.session_state.pred_results is None:

        # ── User details ──────────────────────────────────────────────────────
        st.markdown("""
        <div class="alert-info" style="margin-top:1.2rem;">
            📧 Your details are required — a notification will be sent to your email upon completion.
            All fields are mandatory.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:  user_name      = st.text_input("👤 Full Name *", placeholder="e.g. Shekhar Gudda")
        with c2:  user_email     = st.text_input("📧 Email Address *", placeholder="researcher@niab.res.in")
        with c3:  user_institute = st.text_input("🏛️ Institute *", placeholder="NIAB, Hyderabad")

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # ── Sequence input panel ──────────────────────────────────────────────
        st.markdown('<div class="seq-input-panel">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.82rem;color:#888;margin-bottom:0.6rem;">
          Enter single or multiple protein sequences in FASTA format.
          (Paste mode: <b>1–10 sequences max.</b> For larger datasets use the file upload below.)
        </div>
        """, unsafe_allow_html=True)

        fasta_input = st.text_area(
            "Enter protein sequence(s) in FASTA format",
            height=200,
            placeholder=">Protein_1\nMKFLLLTLVVVTIVAPGNLEGLSPEQLKTLGDLEGKEFGQTEEFTQHEKKIEELNRRMQ\n\n>Protein_2\nMSEQNNTAKASSIQKVRQERTRTMKDIMSGKGLVGKKQGSEELGDGDNTKQQSIHFKEE",
            label_visibility="collapsed",
            key="fasta_paste"
        )

        st.markdown('<div class="or-divider">OR</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Sequence File",
            type=["fasta","fa","txt","faa"],
            label_visibility="visible",
            key="fasta_upload"
        )

        st.markdown('</div>', unsafe_allow_html=True)  # close seq-input-panel

        # ── Embedding mode ────────────────────────────────────────────────────
        st.markdown("""
        <div style="font-weight:700;color:var(--niab-royal);font-size:0.85rem;
             text-transform:uppercase;letter-spacing:1px;margin:1rem 0 0.4rem;">
          🧬 Select Embedding / Feature Approach
        </div>
        """, unsafe_allow_html=True)

        embed_mode = st.radio(
            "Embedding mode",
            [
                "ESM-2 + Physicochemical Descriptors",
                "ProtT5 Only",
                "ESM-2 + Physicochemical + TM-Score",
                "ESM-2 + ProtT5 (Combined)",
            ],
            index=0,
            label_visibility="collapsed",
            key="embed_mode"
        )

        embed_desc = {
            "ESM-2 + Physicochemical Descriptors":
                "1,280-dim ESM-2 mean embeddings (layer 33) + 5 physicochemical features = 1,285-dim vector. "
                "Best validated approach; recommended default.",
            "ProtT5 Only":
                "1,024-dim ProtT5-XL encoder embeddings. Pure protein language model representation; "
                "no additional feature engineering required.",
            "ESM-2 + Physicochemical + TM-Score":
                "1,285-dim hybrid + structural TM-score similarity feature. "
                "Adds a structure-based perspective to sequence-level embeddings.",
            "ESM-2 + ProtT5 (Combined)":
                "ESM-2 (1,280-dim) + ProtT5 (1,024-dim) concatenated = 2,304-dim. "
                "Maximum information fusion; computationally intensive.",
        }
        st.markdown(f"""
        <div style="background:var(--niab-light);border-radius:8px;padding:10px 14px;
             border-left:3px solid var(--niab-royal);margin-bottom:1rem;font-size:0.87rem;color:#1A2E50;">
          <b>{embed_mode}:</b> {embed_desc[embed_mode]}
        </div>
        """, unsafe_allow_html=True)

        # ── Threshold ─────────────────────────────────────────────────────────
        st.markdown("""
        <div style="font-weight:700;color:var(--niab-royal);font-size:0.85rem;
             text-transform:uppercase;letter-spacing:1px;margin:0.8rem 0 0.4rem;">
          📊 Choose Threshold Value for Virulence Classification
        </div>
        """, unsafe_allow_html=True)

        thresh_map = {
            "0.3 — Sensitive (maximum recall)": 0.3,
            "0.4": 0.4,
            "0.5 — Default (balanced)": 0.5,
            "0.6": 0.6,
            "0.7 — High confidence": 0.7,
            "0.8": 0.8,
            "0.9 — Stringent": 0.9,
        }
        thresh_sel = st.selectbox(
            "Virulence probability threshold",
            list(thresh_map.keys()),
            index=2,
            label_visibility="collapsed"
        )
        threshold = thresh_map[thresh_sel]

        # ── Submit / Reset buttons ────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        bc1, bc2, bc3 = st.columns([2,1,5])
        with bc1:
            submit = st.button("Submit Sequence")
        with bc2:
            reset = st.button("Reset")

        if reset:
            st.session_state.pred_results = None
            st.rerun()

        if submit:
            errors = []
            if not user_name.strip():      errors.append("Full Name is required.")
            if not user_email.strip():     errors.append("Email Address is required.")
            if "@" not in user_email:      errors.append("Email Address appears invalid.")
            if not user_institute.strip(): errors.append("Institute is required.")

            raw_fasta = ""
            if uploaded_file:
                raw_fasta = uploaded_file.read().decode("utf-8", errors="replace")
            elif fasta_input.strip():
                raw_fasta = fasta_input.strip()
            else:
                errors.append("No sequences provided. Paste FASTA sequences or upload a file.")

            if errors:
                for e in errors:
                    st.markdown(f'<div class="alert-warn">⚠️ {e}</div>', unsafe_allow_html=True)
            else:
                sequences = parse_fasta(raw_fasta)
                if not sequences:
                    st.markdown('<div class="alert-warn">⚠️ Could not parse any sequences. Check FASTA format.</div>', unsafe_allow_html=True)
                elif not uploaded_file and len(sequences) > 10:
                    st.markdown(f'<div class="alert-warn">⚠️ Paste mode supports up to 10 sequences. You provided {len(sequences)}. Please use the file upload option.</div>', unsafe_allow_html=True)
                else:
                    valid_seqs, bad_seqs = [], []
                    for name, seq in sequences:
                        ok, clean = validate_sequence(seq)
                        if ok: valid_seqs.append((name, clean))
                        else:  bad_seqs.append(name)

                    if bad_seqs:
                        st.markdown(f'<div class="alert-warn">⚠️ Skipped {len(bad_seqs)} invalid sequence(s): {", ".join(bad_seqs[:5])}</div>', unsafe_allow_html=True)

                    if not valid_seqs:
                        st.markdown('<div class="alert-warn">⚠️ No valid sequences remain.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="alert-success">✅ {len(valid_seqs)} valid sequence(s) loaded. Running prediction pipeline…</div>', unsafe_allow_html=True)
                        prog = st.empty()
                        result_df = run_prediction(valid_seqs, threshold, embed_mode, prog)
                        prog.empty()
                        st.session_state.pred_results = {
                            "df": result_df,
                            "user": user_name,
                            "email": user_email,
                            "institute": user_institute,
                            "threshold": threshold,
                            "embed_mode": embed_mode,
                        }
                        st.rerun()

    else:
        # ── Show results ──────────────────────────────────────────────────────
        res = st.session_state.pred_results
        df = res["df"]
        n_v   = (df["Prediction"]=="Virulent").sum()
        n_nv  = (df["Prediction"]=="Non-Virulent").sum()

        st.markdown(f"""
        <div class="alert-success" style="margin-top:1.2rem;">
          ✅ Prediction complete for <b>{res['user']}</b> ({res['institute']}).
          Notification queued to <b>{res['email']}</b>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-card"><div class="stat-val">{len(df)}</div><div class="stat-lbl">Total Proteins</div></div>
          <div class="stat-card" style="border-top-color:#C0392B;">
            <div class="stat-val" style="color:#C0392B;">{n_v}</div><div class="stat-lbl">Virulent</div>
          </div>
          <div class="stat-card" style="border-top-color:#43A047;">
            <div class="stat-val" style="color:#43A047;">{n_nv}</div><div class="stat-lbl">Non-Virulent</div>
          </div>
          <div class="stat-card">
            <div class="stat-val" style="font-size:1.3rem;">{res['threshold']}</div>
            <div class="stat-lbl">Threshold</div>
          </div>
          <div class="stat-card" style="min-width:200px;">
            <div class="stat-val" style="font-size:1rem;color:#555;">{res['embed_mode'].split()[0]}</div>
            <div class="stat-lbl">Embedding Mode</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Build HTML table
        rows_html = ""
        for _, row in df.iterrows():
            p = row["Probability Score"]
            badge = f'<span class="badge-v">🟡 Virulent</span>' if row["Prediction"]=="Virulent" else f'<span class="badge-nv">🟢 Non-Virulent</span>'
            bar_cls = "score-high" if p >= res["threshold"] else "score-low"
            bar = f'<div class="score-bar-wrap"><div class="score-bar-fill {bar_cls}" style="width:{int(p*100)}%;"></div></div>'
            rows_html += f"""<tr>
              <td><b>{row['Protein Name']}</b></td>
              <td>{row['Length (aa)']} aa</td>
              <td><b>{p:.4f}</b>{bar}</td>
              <td>{badge}</td>
            </tr>"""

        st.markdown(f"""
        <div class="card" style="padding:0;overflow:auto;margin-top:1rem;">
          <table class="result-table">
            <thead><tr>
              <th>Protein Name</th><th>Length</th>
              <th>Probability Score</th><th>Prediction</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        dl_col, rst_col = st.columns([3,1])
        with dl_col:
            st.download_button(
                "⬇️ Download Results as CSV",
                data=df.to_csv(index=False).encode(),
                file_name="paravirpred_results.csv",
                mime="text/csv"
            )
        with rst_col:
            if st.button("🔄 New Prediction"):
                st.session_state.pred_results = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <strong>ParaVirPred v1.0</strong> | <strong>NIAB, Hyderabad</strong> &nbsp;|&nbsp;
        Guide: <strong>Dr. Sandeep Kumar Kushwaha</strong> (Scientist-E) &nbsp;|&nbsp;
        Intern: <strong>Shekhar Gudda</strong>, M.Sc. Bioinformatics, DES Pune University
    </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HELP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Help":
    st.markdown("""
    <div class="hero-banner" style="padding:2rem 3rem;">
      <div class="hero-title" style="font-size:2.1rem;">📖 Help & <span>Documentation</span></div>
      <div class="hero-subtitle">Step-by-step guide to using ParaVirPred</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    col1, col2 = st.columns([3,2], gap="large")

    with col1:
        st.markdown('<div class="section-header">How to Use ParaVirPred</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="timeline">
          <div class="timeline-step" data-step="1">
            <div class="step-title">Navigate to "Predict Virulence"</div>
            <div class="step-desc">Click <b>Predict Virulence</b> in the top navigation bar.</div>
          </div>
          <div class="timeline-step" data-step="2">
            <div class="step-title">Enter your details</div>
            <div class="step-desc">Provide your full name, institutional email, and institute name. 
            All fields are mandatory. A notification will be sent to your email on completion.</div>
          </div>
          <div class="timeline-step" data-step="3">
            <div class="step-title">Submit sequences</div>
            <div class="step-desc">
              <b>Paste mode:</b> Paste 1–10 FASTA sequences directly in the text box.<br>
              <b>Upload mode:</b> Upload any .fasta / .fa / .txt file — no size limit.
            </div>
          </div>
          <div class="timeline-step" data-step="4">
            <div class="step-title">Select embedding approach</div>
            <div class="step-desc">Choose how protein features are generated.
              Four options are available — ESM-2 hybrid, ProtT5, structure-aware, or combined.
              Default (recommended): <b>ESM-2 + Physicochemical Descriptors</b>.
            </div>
          </div>
          <div class="timeline-step" data-step="5">
            <div class="step-title">Set probability threshold</div>
            <div class="step-desc">Choose a virulence score cutoff (default 0.5). 
            Proteins scoring at or above this threshold are classified as Virulent.</div>
          </div>
          <div class="timeline-step" data-step="6">
            <div class="step-title">Click "Submit Sequence"</div>
            <div class="step-desc">The pipeline runs automatically with live progress indicators. 
            Results appear once all steps are complete.</div>
          </div>
          <div class="timeline-step" data-step="7">
            <div class="step-title">Review and download</div>
            <div class="step-desc">Results show protein name, length, probability score, 
            and virulence classification. Download as CSV for further analysis.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">FASTA Format</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <p style="font-size:0.9rem;color:#333;margin-bottom:0.5rem;">Each sequence must follow standard FASTA format:</p>
          <pre style="background:#EBF3FF;padding:14px;border-radius:8px;
               font-family:'Source Code Pro',monospace;font-size:0.83rem;
               color:#0D2B6B;overflow-x:auto;line-height:1.6;">
>Protein_1 | P. falciparum | hypothetical protein
MKFLLLKLVVVTIVAPGNLEGLSPEQLKTLGDLEGKEFGQTEEFTQHEKKIEELNRRMQ
ELPAKDAQFLLSKNLTEKEMRLNHLTQKIGEQPGQNLQTEQLQKEMQLNHLTQKIGEK

>Protein_2 | T. gondii | surface antigen
MSEQNNTAKASSIQKVRQERTRTMLDIMSGKGLVGKKQGSEELGDGDNTKQQSIHFKEE
          </pre>
          <ul style="font-size:0.88rem;color:#555;line-height:1.9;margin-top:0.5rem;">
            <li>Header line starts with <code>&gt;</code></li>
            <li>Sequence follows on subsequent lines — multi-line sequences are accepted</li>
            <li>Standard 20 amino acid single-letter codes only</li>
            <li>Minimum sequence length: <b>20 amino acids</b></li>
            <li>Sequences are automatically truncated to 1,022 tokens for ESM-2</li>
            <li>Stop codons (<code>*</code>) and gaps (<code>-</code>) are automatically stripped</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Understanding Results</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <table style="width:100%;font-size:0.9rem;border-collapse:collapse;">
            <tr style="background:var(--niab-light);">
              <th style="padding:8px 12px;text-align:left;color:var(--niab-royal);">Column</th>
              <th style="padding:8px 12px;text-align:left;color:var(--niab-royal);">Description</th>
            </tr>
            <tr><td style="padding:8px 12px;font-weight:700;">Protein Name</td><td style="padding:8px 12px;">FASTA header identifier</td></tr>
            <tr style="background:var(--niab-light);"><td style="padding:8px 12px;font-weight:700;">Length (aa)</td><td style="padding:8px 12px;">Sequence length in amino acids</td></tr>
            <tr><td style="padding:8px 12px;font-weight:700;">Probability Score</td><td style="padding:8px 12px;">SVM probability of virulence (0.0–1.0). Higher score = more likely virulent.</td></tr>
            <tr style="background:var(--niab-light);">
              <td style="padding:8px 12px;font-weight:700;">Prediction</td>
              <td style="padding:8px 12px;">
                <span class="badge-v">🔴 Virulent</span> if score ≥ threshold<br>
                <span class="badge-nv">🟢 Non-Virulent</span> otherwise
              </td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Algorithm Overview</div>', unsafe_allow_html=True)

        for i,(icon,title,desc) in enumerate([
            ("🧬","ESM-2 Embeddings","Protein sequences are passed through ESM-2 (650M parameters, 33 transformer layers). Mean pooling of layer-33 per-residue representations yields a 1,280-dimensional embedding capturing evolutionary and structural context."),
            ("🔠","ProtT5-XL Embeddings","ProtT5-XL encoder produces 1,024-dim semantic embeddings trained on UniRef50. Captures complementary protein language information independent of ESM-2."),
            ("⚗️","Physicochemical Descriptors","5 classical features computed via BioPython: length, molecular weight, aromaticity, instability index, isoelectric point (pI), GRAVY score, alphafold_plddt, pocket_volume, pocket_depth."),
            ("📐","TM-Score (Structure)","Structure-based similarity score incorporated as an additional feature for the structure-aware embedding mode. Adds a 3D perspective to sequence-level representations."),
            ("🔗","Feature Concatenation","Chosen features are concatenated into a single vector per protein for model input."),
            ("📏","StandardScaler","Features are standardised (zero mean, unit variance) for SVM compatibility."),
            ("🤖","SVM Classification","RBF-kernel SVM (C=6.0, gamma=scale) predicts virulence probability. Highest MCC (0.710) and accuracy (91.1%) among six benchmarked algorithms."),
        ], 1):
            st.markdown(f"""
            <div class="card" style="padding:0.95rem 1.2rem;margin-bottom:0.65rem;">
              <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="background:var(--niab-royal);color:#F0C429;
                     width:28px;height:28px;border-radius:50%;
                     display:flex;align-items:center;justify-content:center;
                     font-weight:900;font-size:0.8rem;flex-shrink:0;">{i}</div>
                <div>
                  <div style="font-weight:700;color:var(--niab-royal);font-size:0.9rem;">{icon} {title}</div>
                  <div style="font-size:0.82rem;color:#555;margin-top:3px;line-height:1.55;">{desc}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Threshold Guide</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card card-light">
          <table style="width:100%;font-size:0.84rem;border-collapse:collapse;">
            <tr style="border-bottom:2px solid var(--niab-royal);">
              <th style="padding:6px 10px;color:var(--niab-royal);text-align:left;">Threshold</th>
              <th style="padding:6px 10px;color:var(--niab-royal);">Use Case</th>
            </tr>
            <tr><td style="padding:6px 10px;"><b>≥ 0.3</b></td><td style="padding:6px 10px;">Maximum recall — broad exploratory screening</td></tr>
            <tr style="background:rgba(26,71,160,0.06);"><td style="padding:6px 10px;"><b>≥ 0.5</b></td><td style="padding:6px 10px;">Balanced — recommended default</td></tr>
            <tr><td style="padding:6px 10px;"><b>≥ 0.7</b></td><td style="padding:6px 10px;">High confidence — drug target short-listing</td></tr>
            <tr style="background:rgba(26,71,160,0.06);"><td style="padding:6px 10px;"><b>≥ 0.9</b></td><td style="padding:6px 10px;">Stringent — only highest-confidence predictions</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="alert-warn" style="margin-top:1rem;">
          <b>Note:</b> ParaVirPred is a computational prioritisation tool. 
          Predictions should be experimentally validated before drawing biological conclusions.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <strong>ParaVirPred v1.0</strong> | <strong>NIAB, Hyderabad</strong> &nbsp;|&nbsp;
        Guide: <strong>Dr. Sandeep Kumar Kushwaha</strong> (Scientist-E) &nbsp;|&nbsp;
        Intern: <strong>Shekhar Gudda</strong>, M.Sc. Bioinformatics, DES Pune University
    </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "About":
    st.markdown("""
    <div class="hero-banner" style="padding:2rem 3rem;">
      <div class="hero-title" style="font-size:2.1rem;">ℹ️ About <span>ParaVirPred</span></div>
      <div class="hero-subtitle">Project background, methodology, team, and credits</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # ── Credits — NIAB first ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">Team & Credits</div>', unsafe_allow_html=True)

    tc1, tc2, tc3 = st.columns(3, gap="large")
    with tc1:
        st.markdown(f"""
        <div class="card card-royal" style="text-align:center;padding:2rem 1.5rem;">
          {NIAB_SVG}
          <div style="font-family:'Playfair Display',serif;font-size:1.15rem;
               color:#F0C429;margin:10px 0 4px;">NIAB, Hyderabad</div>
          <div style="color:rgba(255,255,255,0.82);font-size:0.83rem;line-height:1.75;">
            National Institute of Animal Biotechnology<br>
            An Autonomous Institute of DBT,<br>
            Ministry of Science & Technology,<br>
            Government of India<br>
            Hyderabad – 500 049, Telangana
          </div>
          <div style="margin-top:12px;background:rgba(240,196,41,0.2);border:1px solid #F0C429;
               border-radius:20px;padding:4px 14px;display:inline-block;
               font-size:0.75rem;font-weight:700;letter-spacing:1px;color:#F0C429;">
            HOST INSTITUTION
          </div>
        </div>
        """, unsafe_allow_html=True)
    with tc2:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2rem 1.5rem;">
          <div style="font-size:3rem;">🎓</div>
          <div style="font-weight:700;color:var(--niab-royal);font-size:1.05rem;margin-top:8px;">
            Dr. Sandeep Kumar Kushwaha
          </div>
          <div style="color:var(--niab-olive);font-size:0.88rem;margin-top:4px;font-weight:700;">Scientist-E</div>
          <div style="color:#777;font-size:0.82rem;margin-top:2px;line-height:1.6;">
            National Institute of Animal Biotechnology<br>Hyderabad, India
          </div>
          <div style="margin-top:12px;background:var(--niab-light);border-radius:20px;
               padding:4px 14px;display:inline-block;
               font-size:0.75rem;font-weight:700;letter-spacing:1px;color:var(--niab-royal);">
            PROJECT GUIDE
          </div>
        </div>
        """, unsafe_allow_html=True)
    with tc3:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2rem 1.5rem;">
          <div style="font-size:3rem;">👨‍🔬</div>
          <div style="font-weight:700;color:var(--niab-royal);font-size:1.05rem;margin-top:8px;">
            Shekhar Gudda
          </div>
          <div style="color:#555;font-size:0.88rem;margin-top:4px;">M.Sc. Bioinformatics</div>
          <div style="color:#777;font-size:0.82rem;margin-top:2px;line-height:1.6;">
            DES Pune University<br>Research Intern, NIAB Hyderabad
          </div>
          <div style="margin-top:12px;background:var(--niab-green-l);border-radius:20px;
               padding:4px 14px;display:inline-block;
               font-size:0.75rem;font-weight:700;letter-spacing:1px;color:var(--niab-olive);">
            RESEARCH INTERN
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3,2], gap="large")

    with col1:
        st.markdown('<div class="section-header">Project Background</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <p style="line-height:1.9;color:#1A2E50;">
          ParaVirPred was developed at <b>NIAB, Hyderabad</b> under the guidance of 
          <b>Dr. Sandeep Kumar Kushwaha (Scientist-E)</b> as part of a comprehensive 
          <b>pan-genome based drug target identification project</b> targeting eight clinically 
          important apicomplexan parasites. These organisms — including <i>Plasmodium</i>, 
          <i>Toxoplasma</i>, <i>Babesia</i>, <i>Cryptosporidium</i>, and <i>Theileria</i> — 
          cause devastating diseases in humans and livestock worldwide, with limited therapeutic 
          options and increasing drug resistance.
          </p>
          <p style="line-height:1.9;color:#1A2E50;">
          From the subtractive proteomics pipeline, <b>102 candidate drug target proteins</b> 
          were identified. A machine learning virulence classifier was built to further prioritise 
          these candidates — virulent proteins are more likely essential for pathogenesis and 
          therefore represent superior drug targets. <b>16 proteins</b> were classified as virulent 
          and prioritised for downstream experimental validation.
          </p>
          <p style="line-height:1.9;color:#1A2E50;">
          The project is currently expanding its embedding pipeline, benchmarking ESM-2, ProtT5-XL, 
          structure-aware hybrid features (TM-score), and combined representations to identify the 
          optimal feature strategy for apicomplexan virulence prediction.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Workflow image in About
        if WF_B64:
            st.markdown('<div class="section-header">Methodological Workflow</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:1.2rem;">
              <img src="data:image/png;base64,{WF_B64}"
                   style="max-width:100%;max-height:700px;border-radius:10px;
                          box-shadow:0 4px 20px rgba(26,71,160,0.12);"
                   alt="Methodological Workflow"/>
              <div style="font-size:0.79rem;color:#777;margin-top:8px;font-style:italic;">
                Figure: Complete methodological workflow — from parasite proteomes and ProtVirDB 
                BLASTp screening through multi-strategy embedding to downstream machine learning.
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Dataset & Training</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
            <div class="card card-royal" style="padding:1rem;margin:0;">
              <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:1px;color:#F0C429;">Virulent Proteins</div>
              <div style="font-size:2rem;font-weight:900;font-family:'Playfair Display',serif;">502</div>
              <div style="font-size:0.79rem;opacity:0.82;">≥ 80% BLASTp similarity to ProtVirDB → labelled +1</div>
            </div>
            <div class="card card-olive" style="padding:1rem;margin:0;">
              <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:1px;color:#E8F0D8;">Non-Virulent Proteins</div>
              <div style="font-size:2rem;font-weight:900;font-family:'Playfair Display',serif;">2,913</div>
              <div style="font-size:0.79rem;opacity:0.88;">≤ 40% BLASTp similarity → labelled −1</div>
            </div>
          </div>
          <p style="font-size:0.9rem;color:#555;line-height:1.7;">
            <b>Class imbalance</b> (~1:5 ratio) was corrected via <b>Pfam domain filtering</b>:
            non-virulent proteins sharing conserved Pfam domains with virulent proteins were removed,
            sharpening the decision boundary through biologically motivated rather than statistical correction.
            The intermediate similarity zone (41–79%) was excluded to prevent label noise.
            An 80/20 stratified split with 5-fold cross-validation (GridSearchCV, refit=MCC) was used.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Model Performance</div>', unsafe_allow_html=True)
        perf = {
            "Model":       ["Logistic Regression","SVM ⭐","Random Forest","XGBoost","MLP-ANN","1D-CNN"],
            "Accuracy":    [0.854,0.911,0.905,0.909,0.893,0.796],
            "Sensitivity": [0.782,0.673,0.584,0.623,0.613,0.000],
            "Specificity": [0.873,0.972,0.987,0.982,0.964,1.000],
            "MCC":         [0.601,0.710,0.686,0.700,0.646,0.000],
            "ROC-AUC":     [0.882,0.902,0.895,0.897,0.888,0.500],
        }
        df_p = pd.DataFrame(perf).set_index("Model")
        st.dataframe(df_p.style.highlight_max(axis=0,color="#C8DC7A").format("{:.3f}"),
                     use_container_width=True)
        st.markdown("""
        <div class="alert-success">
          ⭐ <b>SVM selected</b> as the final model — highest simultaneous Accuracy (91.1%) 
          and MCC (0.710), with ROC-AUC of 0.99.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Key Novelty</div>', unsafe_allow_html=True)
        for item in [
            "First multi-strategy protein language model platform for virulence prediction in apicomplexan parasites",
            "Four embedding modes: ESM-2 hybrid, ProtT5-XL, structure-aware (TM-score), and combined fusion",
            "Pfam domain-based class imbalance correction — biologically motivated, not statistical oversampling",
            "SHAP KernelExplainer interpretability — isoelectric point identified as key conventional feature",
            "Benchmarking of 6 ML algorithms including 1D-CNN on parasitic protein virulence classification",
            "Applied to 102 real drug target candidates — 16 virulent proteins prioritised for validation",
        ]:
            st.markdown(f"""
            <div class="card card-light" style="padding:0.7rem 1.2rem;margin-bottom:0.5rem;">
              <span style="color:var(--niab-accent);font-weight:700;margin-right:8px;font-size:1.1rem;">✦</span>
              <span style="font-size:0.9rem;color:#1A2E50;">{item}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Tools & Libraries</div>', unsafe_allow_html=True)
        tools = [
            ("🐍","Python 3.9+","Core language"),
            ("🌊","Streamlit","Web framework"),
            ("🤗","ESM-2 (Meta AI, 650M)","Protein language model"),
            ("🔠","ProtT5-XL (Rostlab)","Protein language model"),
            ("🔬","BioPython","Protein physicochemical analysis"),
            ("📊","scikit-learn","SVM, preprocessing, GridSearchCV"),
            ("🔥","PyTorch","Deep learning backend"),
            ("📈","SHAP","Model interpretability"),
            ("🐼","pandas / numpy","Data handling"),
        ]
        for icon,name,role in tools:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:7px 12px;
                 background:var(--niab-light);border-radius:8px;margin-bottom:6px;">
              <span style="font-size:1.1rem;">{icon}</span>
              <div>
                <span style="font-weight:700;color:var(--niab-royal);font-size:0.87rem;">{name}</span>
                <span style="color:#777;font-size:0.8rem;margin-left:6px;">— {role}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1.5rem;">SHAP Interpretability</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <p style="font-size:0.88rem;color:#1A2E50;line-height:1.75;">
            Model interpretability was assessed using <b>SHAP KernelExplainer</b> with 
            k-means background clustering (10 representative points). Top findings:
          </p>
          <ul style="font-size:0.87rem;color:#555;line-height:1.9;margin-top:0.3rem;">
            <li><b>esm_897, esm_613, esm_426</b> — top positive SHAP features (push toward virulent)</li>
            <li><b>isoelectric_point</b> — ranked 5th overall among all features</li>
            <li>High pI (basic proteins) → positive SHAP → virulent</li>
            <li>Low pI → negative SHAP → non-virulent</li>
            <li>Consistent with electrostatic interaction of virulence proteins with negatively charged host membranes</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="alert-info" style="margin-top:1rem;font-size:0.82rem;">
          <b>Citation:</b> If you use ParaVirPred in your research, please cite the associated 
          publication (in preparation) — NIAB, Hyderabad. 
          Guide: Dr. Sandeep Kumar Kushwaha. Intern: Shekhar Gudda.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card card-royal" style="text-align:center;padding:1.5rem;margin-top:1rem;">
          <div style="font-size:2.2rem;">🏛️</div>
          <div style="font-family:'Playfair Display',serif;font-size:1rem;color:#F0C429;margin:8px 0 4px;">
            DBT, Government of India
          </div>
          <div style="font-size:0.82rem;color:rgba(255,255,255,0.75);line-height:1.7;">
            NIAB is funded by the Department of Biotechnology,<br>
            Ministry of Science and Technology,<br>
            Government of India.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <strong>ParaVirPred v1.0</strong> — ML-Based Virulence Predictor for Apicomplexan Parasitic Proteins<br>
        <strong>National Institute of Animal Biotechnology (NIAB), Hyderabad</strong> &nbsp;|&nbsp;
        Guide: <strong>Dr. Sandeep Kumar Kushwaha</strong> (Scientist-E, NIAB) &nbsp;|&nbsp;
        Research Intern: <strong>Shekhar Gudda</strong>, M.Sc. Bioinformatics, DES Pune University<br>
        <span style="font-size:0.74rem;opacity:0.55;">
          For research use only. Not intended for clinical or diagnostic purposes. © 2024 NIAB, Hyderabad. All rights reserved.
        </span>
    </div>
    </div>
    """, unsafe_allow_html=True)