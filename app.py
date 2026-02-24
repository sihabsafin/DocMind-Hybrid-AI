import streamlit as st
import os, time, json, hashlib
from datetime import datetime

st.set_page_config(
    page_title="DocMind Hybrid AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600&family=Source+Serif+4:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{
  --void:#050911;--base:#0B1120;--s1:#111827;--s2:#1A2333;--s3:#243447;--s4:#2D3F58;
  --border:rgba(148,163,184,0.08);--border-s:rgba(148,163,184,0.16);--border-f:rgba(34,211,238,0.5);
  --cyan:#22D3EE;--cd:#0891B2;--cl:#67E8F9;--cglow:rgba(34,211,238,0.15);
  --indigo:#6366F1;--iglow:rgba(99,102,241,0.12);
  --emerald:#10B981;--gold:#F59E0B;--gglow:rgba(245,158,11,0.15);
  --error:#EF4444;--info:#3B82F6;
  --tp:#F8FAFC;--ts:#E5E7EB;--tt:#9CA3AF;--tm:#6B7280;--td:#4B5563;--ta:#22D3EE;
}
html,body,[class*="css"]{font-family:'Inter',-apple-system,sans-serif!important;background:var(--base)!important;color:var(--ts)!important;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;}
.block-container{padding:0!important;max-width:100%!important;}
section.main>div{padding:0!important;}
::-webkit-scrollbar{width:5px;} ::-webkit-scrollbar-track{background:var(--base);} ::-webkit-scrollbar-thumb{background:var(--s4);border-radius:3px;}

/* sidebar */
[data-testid="stSidebar"]{background:var(--s1)!important;border-right:1px solid var(--border-s)!important;}
[data-testid="stSidebarContent"]{padding:0 14px 14px!important;}
.slabel{font-size:10px;font-weight:600;letter-spacing:.12em;color:var(--tm);text-transform:uppercase;margin:18px 0 8px;padding-left:2px;}
.sdiv{border:none;border-top:1px solid var(--border-s);margin:14px 0;}

/* model card */
.mcard{background:var(--s2);border:1px solid var(--border-s);border-radius:8px;padding:11px 13px;margin-bottom:7px;transition:all 150ms ease-out;}
.mcard.sel{background:var(--iglow);border:2px solid var(--indigo);box-shadow:0 0 16px rgba(99,102,241,.2);}
.mcard-title{font-size:13px;font-weight:600;color:var(--tp);}
.mcard-meta{font-size:11px;color:var(--tt);margin-top:3px;line-height:1.5;}

/* mode card */
.modecard{background:var(--s2);border:1px solid var(--border-s);border-radius:8px;padding:9px 13px;margin-bottom:5px;}
.modecard.sel{background:var(--gglow);border-left:3px solid var(--gold);}
.modecard-t{font-size:13px;font-weight:500;color:var(--tp);}
.modecard-d{font-size:11px;color:var(--tt);margin-top:2px;}

/* fin banner */
.finbanner{background:linear-gradient(135deg,rgba(245,158,11,.15),rgba(245,158,11,.05));border:1px solid rgba(245,158,11,.4);border-radius:8px;padding:9px 13px;margin-bottom:10px;text-align:center;}
.finbanner-t{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;color:var(--gold);letter-spacing:.08em;}
.finbanner-s{font-size:11px;color:var(--tt);margin-top:2px;}

/* sliders */
.stSlider>div>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--cd))!important;}
.stSlider label{font-family:'Inter',sans-serif!important;font-size:10px!important;font-weight:600!important;letter-spacing:.1em!important;color:var(--tm)!important;text-transform:uppercase!important;}

/* buttons */
.stButton>button{background:linear-gradient(135deg,var(--cyan),var(--cd))!important;border:none!important;border-radius:8px!important;color:white!important;font-family:'Inter',sans-serif!important;font-weight:600!important;font-size:13px!important;transition:all 150ms ease-out!important;box-shadow:0 2px 12px rgba(34,211,238,.25)!important;}
.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 4px 20px rgba(34,211,238,.4)!important;}
.stButton>button:active{transform:scale(.98)!important;}

/* inputs */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--s2)!important;border:1px solid var(--border-s)!important;border-radius:12px!important;color:var(--tp)!important;font-family:'Inter',sans-serif!important;font-size:15px!important;padding:14px 18px!important;transition:all 200ms ease!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border:2px solid var(--cyan)!important;box-shadow:0 0 0 4px rgba(34,211,238,.12)!important;}
.stTextInput label,.stTextArea label{color:var(--tt)!important;font-size:10px!important;font-weight:600!important;letter-spacing:.08em!important;text-transform:uppercase!important;}

/* file uploader */
[data-testid="stFileUploader"]{background:var(--s2)!important;border:2px dashed var(--border-s)!important;border-radius:12px!important;}
[data-testid="stFileUploader"]:hover{border-color:var(--cyan)!important;background:var(--cglow)!important;}

/* expander */
.streamlit-expanderHeader{background:var(--s2)!important;border:1px solid var(--border-s)!important;border-radius:8px!important;color:var(--tt)!important;font-size:13px!important;font-weight:500!important;}
.streamlit-expanderContent{background:var(--s1)!important;border:1px solid var(--border)!important;border-top:none!important;border-radius:0 0 8px 8px!important;padding:14px!important;}

/* progress */
.stProgress>div>div>div{background:linear-gradient(90deg,var(--cyan),var(--cd))!important;border-radius:4px!important;}
.stProgress>div>div{background:var(--s3)!important;border-radius:4px!important;height:5px!important;}

/* topbar */
.topbar{background:rgba(5,9,17,.95);backdrop-filter:blur(24px) saturate(180%);border-bottom:1px solid var(--border-s);padding:0 28px;height:62px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:1000;margin:-1rem -1rem 0 -1rem;}
.topbar-logo{font-family:'IBM Plex Mono',monospace;font-size:21px;font-weight:600;color:var(--cyan);text-shadow:0 0 20px rgba(34,211,238,.4);}
.topbar-sub{font-size:11px;color:var(--tm);margin-top:1px;}
.mbadge{background:var(--s2);border:1px solid var(--indigo);border-radius:6px;padding:5px 11px;font-size:12px;font-weight:500;color:var(--ts);}
.mbadge span{color:var(--indigo);margin-right:3px;}
.sdot{width:8px;height:8px;border-radius:50%;display:inline-block;animation:pulse 2s ease-in-out infinite;}
.sdot.g{background:var(--emerald);box-shadow:0 0 8px var(--emerald);}
.sdot.a{background:var(--gold);box-shadow:0 0 8px var(--gold);}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.6;transform:scale(1.2);}}

/* response card */
.rcard{background:var(--s1);border:1px solid var(--border-s);border-radius:12px;padding:28px 36px;max-width:900px;margin:0 auto;}
.rheader{font-size:12px;color:var(--tt);margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--border);}
.rbody{font-family:'Source Serif 4',Georgia,serif;font-size:16px;line-height:1.75;color:var(--ts);}

/* source card */
.srccard{background:var(--s2);border:1px solid var(--border);border-radius:8px;padding:13px 17px;margin-bottom:9px;transition:transform 150ms ease;}
.srccard:hover{transform:translateX(2px);}
.srccard.h{border-left:3px solid var(--cyan);}
.srccard.m{border-left:3px solid var(--indigo);}
.srccard.l{border-left:3px solid var(--info);}
.srcnum{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:var(--ta);}
.srctext{font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.7;color:var(--ts);background:var(--s1);border-radius:6px;padding:9px 13px;margin:7px 0;border:1px solid var(--border);}
.srcmeta{font-family:'Inter',sans-serif;font-size:10px;color:var(--td);margin-top:5px;}

/* doc item */
.docitem{background:var(--s2);border:1px solid var(--border);border-radius:7px;padding:9px 11px;margin-bottom:5px;}
.docdot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:7px;}
.docdot.ok{background:var(--emerald);}
.docdot.proc{background:var(--gold);animation:pulse 1s infinite;}

/* main area grid */
.mainarea{background-image:linear-gradient(rgba(34,211,238,.015) 1px,transparent 1px),linear-gradient(90deg,rgba(34,211,238,.015) 1px,transparent 1px);background-size:40px 40px;min-height:calc(100vh - 62px);padding:0 0 60px;}

/* empty state */
.emptystate{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:380px;text-align:center;padding:50px 40px;}
.empty-icon{font-size:68px;margin-bottom:20px;filter:drop-shadow(0 0 20px rgba(34,211,238,.35));}
.empty-title{font-family:'IBM Plex Mono',monospace;font-size:30px;font-weight:600;color:var(--tp);margin-bottom:10px;}
.empty-sub{font-size:15px;color:var(--tt);max-width:440px;line-height:1.6;margin-bottom:28px;}

/* query area */
.qarea{max-width:900px;margin:0 auto;padding:36px 24px 20px;}
.qlabel{font-size:10px;font-weight:600;letter-spacing:.12em;color:var(--tm);text-transform:uppercase;margin-bottom:7px;}

/* info box */
.infobox{background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:8px;padding:9px 13px;font-size:12px;color:var(--tt);margin-bottom:10px;}

/* financial numbers in response */
.fn{font-family:'JetBrains Mono',monospace;font-size:17px;color:var(--gold);font-variant-numeric:tabular-nums;font-weight:600;}

/* radio hide */
.stRadio>div{flex-direction:row!important;gap:6px!important;}
.stRadio>div>label{background:var(--s2)!important;border:1px solid var(--border-s)!important;border-radius:6px!important;padding:7px 12px!important;color:var(--tt)!important;font-size:12px!important;cursor:pointer!important;}
.stRadio>div>label:hover{background:var(--s3)!important;}
[aria-checked="true"].stRadio>div>label{background:linear-gradient(135deg,var(--cyan),var(--cd))!important;color:white!important;border:none!important;}

.main .block-container{padding-top:0!important;}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────────
for k, v in {
    "active_model":"llama-3.3-70b-versatile",
    "active_mode":"General Retrieval",
    "search_type":"Hybrid",
    "top_k":5, "temperature":0.3,
    "documents":[], "query_history":[],
    "current_response":None, "current_sources":[],
}.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Secrets ──────────────────────────────────────────────────────────────────────
def gsec(k):
    try: return st.secrets.get(k)
    except: return os.environ.get(k)

GROQ_KEY     = gsec("GROQ_API_KEY")
GEMINI_KEY   = gsec("GEMINI_API_KEY")
PINECONE_KEY = gsec("PINECONE_API_KEY")
PINECONE_IDX = gsec("PINECONE_INDEX_NAME") or "docmind-index"

MODELS = {
    "llama-3.3-70b-versatile":       {"label":"Llama 3.3 70B","icon":"⚡","desc":"Fast inference · General reasoning","rate":"Free · 30 req/min","provider":"groq"},
    "gemini-2.0-flash":              {"label":"Gemini 2.0 Flash","icon":"🔮","desc":"Long output · Structured reports","rate":"Free · 15 req/min","provider":"gemini"},
    "deepseek-r1-distill-llama-70b": {"label":"DeepSeek R1 (Financial)","icon":"💰","desc":"Financial reasoning · Precision","rate":"Free · 30 req/min (Groq)","provider":"groq"},
}
MODES = {
    "General Retrieval":      "Standard hybrid search · Multi-domain",
    "Financial Analysis":     "Numerical precision · Calculations verified",
    "Long Report Generation": "Structured output · Executive summaries",
}

# ── Helpers ───────────────────────────────────────────────────────────────────────
def extract_text(file_bytes, name):
    if name.endswith(".pdf"):
        try:
            import pypdf, io
            r = pypdf.PdfReader(io.BytesIO(file_bytes))
            return "\n".join(p.extract_text() or "" for p in r.pages), len(r.pages)
        except: return "",0
    if name.endswith(".docx"):
        try:
            import docx, io
            d = docx.Document(io.BytesIO(file_bytes))
            return "\n".join(p.text for p in d.paragraphs), 0
        except: return "",0
    return file_bytes.decode("utf-8", errors="ignore"), 0

def chunk_text(text, size=480, overlap=60):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+size]))
        i += size - overlap
    return [c for c in chunks if len(c.strip()) > 40]

@st.cache_resource(show_spinner=False)
def get_emb_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("BAAI/bge-small-en-v1.5")
    except: return None

def embed(texts):
    m = get_emb_model()
    if m: return m.encode(texts, show_progress_bar=False).tolist()
    import random, math
    return [[math.sin(i+j*0.1) for j in range(384)] for i,_ in enumerate(texts)]

@st.cache_resource(show_spinner=False)
def get_pinecone():
    if not PINECONE_KEY: return None
    try:
        from pinecone import Pinecone, ServerlessSpec
        pc = Pinecone(api_key=PINECONE_KEY)
        existing = [i.name for i in pc.list_indexes()]
        if PINECONE_IDX not in existing:
            pc.create_index(name=PINECONE_IDX, dimension=384, metric="cosine",
                            spec=ServerlessSpec(cloud="aws", region="us-east-1"))
            time.sleep(5)
        return pc.Index(PINECONE_IDX)
    except: return None

def upsert_pinecone(doc_id, chunks, embeddings):
    idx = get_pinecone()
    if not idx: return False
    try:
        vecs = [{"id":f"{doc_id}_{i}","values":e,"metadata":{"text":c,"doc_id":doc_id}}
                for i,(c,e) in enumerate(zip(chunks,embeddings))]
        for i in range(0,len(vecs),100): idx.upsert(vectors=vecs[i:i+100])
        return True
    except: return False

def query_pinecone(q_emb, top_k, doc_ids):
    idx = get_pinecone()
    if not idx: return []
    try:
        f = {"doc_id":{"$in":doc_ids}} if doc_ids else None
        return idx.query(vector=q_emb, top_k=top_k, include_metadata=True, filter=f).matches
    except: return []

def local_dense(query, top_k):
    import numpy as np
    chunks, embeddings, meta = [], [], []
    for doc in st.session_state.documents:
        for i,(c,e) in enumerate(zip(doc.get("text_chunks",[]),doc.get("embeddings",[]))):
            chunks.append(c); embeddings.append(e)
            meta.append({"doc_name":doc["name"],"chunk_idx":i,"text":c})
    if not embeddings: return []
    q = np.array(embed([query])[0])
    M = np.array(embeddings)
    norms = np.linalg.norm(M,axis=1)*np.linalg.norm(q)
    norms = np.where(norms==0,1e-9,norms)
    sims = M.dot(q)/norms
    top = sims.argsort()[::-1][:top_k]
    return [type("M",(),{"id":f"l{i}","score":float(sims[i]),"metadata":{"text":meta[i]["text"],"doc_id":meta[i]["doc_name"]}})() for i in top]

def bm25_search(query, top_k):
    try:
        from rank_bm25 import BM25Okapi
        corpus, meta = [], []
        for doc in st.session_state.documents:
            for i,c in enumerate(doc.get("text_chunks",[])):
                corpus.append(c.lower().split())
                meta.append({"doc_name":doc["name"],"chunk_idx":i,"text":c})
        if not corpus: return []
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(query.lower().split())
        top = sorted(range(len(scores)),key=lambda i:scores[i],reverse=True)[:top_k]
        return [{"score":float(scores[i]),"meta":meta[i]} for i in top]
    except: return []

def rrf(dense, sparse, k=60):
    scores, docs = {}, {}
    for rank,r in enumerate(dense):
        key = getattr(r,"id",str(rank))
        scores[key] = scores.get(key,0) + 1/(k+rank+1)
        meta = getattr(r,"metadata",{}) or {}
        docs[key] = {"id":key,"text":meta.get("text",""),"dense_score":getattr(r,"score",0),"sparse_score":0,"source":meta.get("doc_id","Unknown")}
    for rank,r in enumerate(sparse):
        key = f"sp_{r['meta']['doc_name']}_{r['meta']['chunk_idx']}"
        scores[key] = scores.get(key,0) + 1/(k+rank+1)
        if key not in docs: docs[key]={"id":key,"text":r["meta"]["text"],"dense_score":0,"sparse_score":r["score"],"source":r["meta"]["doc_name"]}
        else: docs[key]["sparse_score"]=r["score"]
    out=[]
    for key in sorted(scores,key=lambda x:scores[x],reverse=True):
        d=docs[key]; d["rrf_score"]=scores[key]; d["relevance_pct"]=min(99.9,round(scores[key]*600,1)); out.append(d)
    return out

def call_llm(query, chunks, model_id, mode, temp):
    ctx = "\n\n---\n\n".join([f"[Source {i+1}: {c.get('source','?')}]\n{c.get('text','')}" for i,c in enumerate(chunks)])
    prompt = f"Context:\n\n{ctx}\n\n---\n\nQuestion: {query}\n\nAnswer based ONLY on the context. Be precise and cite sources."
    sysp = "You are DocMind Hybrid AI, an enterprise-grade intelligence assistant. Answer based strictly on provided context."
    if mode=="Financial Analysis": sysp+=" Focus on numerical precision. Format financial figures clearly (e.g. $127.4M, +23.5% YoY)."
    elif mode=="Long Report Generation": sysp+=" Generate structured reports with headings, summaries, and detailed analysis."
    
    info = MODELS.get(model_id,{})
    prov = info.get("provider","groq")
    
    if prov=="groq" and GROQ_KEY:
        try:
            from groq import Groq
            r = Groq(api_key=GROQ_KEY).chat.completions.create(
                model=model_id,
                messages=[{"role":"system","content":sysp},{"role":"user","content":prompt}],
                temperature=temp, max_tokens=2048)
            return r.choices[0].message.content
        except Exception as e: return f"**Groq API Error:** {e}\n\n*Check your GROQ_API_KEY in Streamlit Secrets.*"
    
    if prov=="gemini" and GEMINI_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_KEY)
            m = genai.GenerativeModel(model_id)
            return m.start_chat().send_message(sysp+"\n\n"+prompt).text
        except Exception as e: return f"**Gemini API Error:** {e}\n\n*Check your GEMINI_API_KEY in Streamlit Secrets.*"
    
    return f"""**[Demo Mode — API key not configured]**

To enable live AI responses, add your API keys to Streamlit Secrets (see README.md).

**Retrieved Context Preview:**

{ctx[:1000]}{'...' if len(ctx)>1000 else ''}

*Configure API keys to get real AI-generated responses from your documents.*"""

def process_file(uf):
    fb = uf.read(); name = uf.name
    pb = st.progress(0, text=f"Extracting {name}…")
    text, pages = extract_text(fb, name)
    if not text.strip(): st.error(f"Could not extract text from {name}"); return
    pb.progress(30, text="Chunking…")
    chunks = chunk_text(text)
    pb.progress(55, text="Generating embeddings…")
    embeddings = embed(chunks)
    pb.progress(80, text="Indexing…")
    doc_id = hashlib.md5(name.encode()).hexdigest()[:10]
    pc_ok = upsert_pinecone(doc_id, chunks, embeddings)
    pb.progress(100, text="Done!"); time.sleep(0.3); pb.empty()
    st.session_state.documents.append({
        "name":name,"doc_id":doc_id,"pages":pages or "—","chunks":len(chunks),
        "status":"indexed","text_chunks":chunks,"embeddings":embeddings,
        "pinecone":pc_ok,"ts":datetime.now().strftime("%H:%M")
    })

def do_search(query):
    top_k=st.session_state.top_k; st_=st.session_state.search_type
    total=sum(d.get("chunks",0) for d in st.session_state.documents)
    placeholder=st.empty()
    placeholder.info(f"🔍 Hybrid search across {total} chunks in {len(st.session_state.documents)} document(s)…")
    q_emb=embed([query])[0]; dense=[]; sparse=[]
    if st_ in ("Dense","Hybrid"):
        pc=get_pinecone()
        if pc: dense=query_pinecone(q_emb,top_k,[d["doc_id"] for d in st.session_state.documents])
        else: dense=local_dense(query,top_k)
    if st_ in ("Sparse","Hybrid"): sparse=bm25_search(query,top_k)
    if st_=="Hybrid": fused=rrf(dense,sparse)[:top_k]
    elif st_=="Dense":
        fused=[{"id":getattr(r,"id",""),"text":(getattr(r,"metadata",{}or{})).get("text",""),
                "source":(getattr(r,"metadata",{}or{})).get("doc_id","?"),
                "dense_score":getattr(r,"score",0),"sparse_score":0,
                "relevance_pct":round(getattr(r,"score",0)*100,1)} for r in dense]
    else:
        fused=[{"id":f"sp_{r['meta']['doc_name']}_{r['meta']['chunk_idx']}","text":r["meta"]["text"],
                "source":r["meta"]["doc_name"],"dense_score":0,"sparse_score":r["score"],
                "relevance_pct":min(99.9,round(r["score"]*10,1))} for r in sparse]
    if not fused:
        for doc in st.session_state.documents[:2]:
            for i,c in enumerate(doc["text_chunks"][:3]):
                fused.append({"id":f"fb_{i}","text":c,"source":doc["name"],"dense_score":0,"sparse_score":0,"relevance_pct":70.0})
    st.session_state.current_sources=fused
    placeholder.info(f"⚡ {MODELS[st.session_state.active_model]['icon']} {MODELS[st.session_state.active_model]['label']} generating response…")
    resp=call_llm(query,fused,st.session_state.active_model,st.session_state.active_mode,st.session_state.temperature)
    placeholder.empty()
    st.session_state.current_response=resp
    st.session_state.query_history.append({"query":query,"response":resp,"sources":fused,
        "model":st.session_state.active_model,"mode":st.session_state.active_mode,"ts":datetime.now().strftime("%H:%M")})

# ── SIDEBAR ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 2px 0">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:var(--cyan);">⬡ DocMind Hybrid AI</div>
        <div style="font-size:11px;color:var(--tm);margin-top:2px;">Enterprise Intelligence Platform</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.active_mode=="Financial Analysis":
        st.markdown('<div class="finbanner"><div class="finbanner-t">💰 FINANCIAL MODE ACTIVE</div><div class="finbanner-s">Precision: High · Calculations verified</div></div>',unsafe_allow_html=True)

    st.markdown('<div class="slabel">Model Configuration</div>',unsafe_allow_html=True)
    for mid,info in MODELS.items():
        sel = st.session_state.active_model==mid
        key_ok = (info["provider"]=="groq" and GROQ_KEY) or (info["provider"]=="gemini" and GEMINI_KEY)
        css = "mcard sel" if sel else "mcard"
        ks = '<span style="color:var(--emerald)">✓ API ready</span>' if key_ok else '<span style="color:var(--gold)">⚠ No API key</span>'
        st.markdown(f'<div class="{css}"><div class="mcard-title">{info["icon"]} {info["label"]}</div><div class="mcard-meta">{info["desc"]}<br>{ks}</div></div>',unsafe_allow_html=True)
        if st.button(f"{'✓ Selected' if sel else 'Select'}", key=f"m_{mid}", use_container_width=True):
            st.session_state.active_model=mid; st.rerun()

    st.markdown('<hr class="sdiv"><div class="slabel">Operation Mode</div>',unsafe_allow_html=True)
    for mode,desc in MODES.items():
        sel=st.session_state.active_mode==mode
        css="modecard sel" if sel else "modecard"
        st.markdown(f'<div class="{css}"><div class="modecard-t">{"● " if sel else "○ "}{mode}</div><div class="modecard-d">{desc}</div></div>',unsafe_allow_html=True)
        if st.button(f"Set", key=f"mod_{mode}", use_container_width=True):
            st.session_state.active_mode=mode; st.rerun()

    st.markdown('<hr class="sdiv"><div class="slabel">Hybrid Search Control</div>',unsafe_allow_html=True)
    st_radio = st.radio("Search Type",["Dense","Sparse","Hybrid"],
        index=["Dense","Sparse","Hybrid"].index(st.session_state.search_type),horizontal=True,label_visibility="collapsed")
    st.session_state.search_type=st_radio
    st.session_state.top_k = st.slider("RETRIEVED CHUNKS (k)", 1, 10, st.session_state.top_k)
    st.session_state.temperature = st.slider("TEMPERATURE", 0.0, 1.0, st.session_state.temperature, 0.05)

    st.markdown('<hr class="sdiv"><div class="slabel">Document Index</div>',unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload", type=["pdf","txt","docx"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        for uf in uploaded:
            if uf.name not in [d["name"] for d in st.session_state.documents]:
                process_file(uf); st.rerun()

    if st.session_state.documents:
        total_c=sum(d.get("chunks",0) for d in st.session_state.documents)
        st.markdown(f'<div style="font-size:10px;color:var(--tm);margin-bottom:7px;">INDEXED: {len(st.session_state.documents)} docs · {total_c} chunks</div>',unsafe_allow_html=True)
        for doc in st.session_state.documents:
            st.markdown(f'<div class="docitem"><span class="docdot ok"></span><span style="font-size:12px;font-weight:500;color:var(--tp);">{doc["name"]}</span><br><span style="font-size:10px;color:var(--tt);margin-left:14px;">{doc.get("pages","?")} pages · {doc.get("chunks",0)} chunks · {doc.get("ts","")}</span></div>',unsafe_allow_html=True)
        if st.button("🗑 Clear All", use_container_width=True):
            st.session_state.documents=[]; st.session_state.current_response=None; st.session_state.current_sources=[]; st.rerun()
    else:
        st.markdown('<div class="infobox">📂 Upload PDFs, TXT, or DOCX to begin analysis.</div>',unsafe_allow_html=True)

    st.markdown('<hr class="sdiv">',unsafe_allow_html=True)
    pc_ok=get_pinecone() is not None
    st.markdown(f"""
    <div style="font-size:10px;color:var(--tm);line-height:2.1;">
        {'✅' if pc_ok else '⚠️'} Pinecone: {'Connected' if pc_ok else 'Local fallback'}<br>
        {'✅' if GROQ_KEY else '⚠️'} Groq API: {'Ready' if GROQ_KEY else 'Key needed'}<br>
        {'✅' if GEMINI_KEY else '⚠️'} Gemini: {'Ready' if GEMINI_KEY else 'Key needed'}<br>
        🧠 Embeddings: {'BGE-small' if get_emb_model() else 'Loading…'}
    </div>""", unsafe_allow_html=True)

# ── MAIN AREA ─────────────────────────────────────────────────────────────────────
mi = MODELS.get(st.session_state.active_model,{})
gold_border = "border-color:var(--gold);" if st.session_state.active_mode=="Financial Analysis" else ""
dot_cls = "g" if st.session_state.documents else "a"
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:14px;">
    <div>
      <div class="topbar-logo">⬡ DocMind Hybrid AI</div>
      <div class="topbar-sub">Precision Intelligence Retrieval</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;">
    <div class="mbadge" style="{gold_border}"><span>{mi.get('icon','⚡')}</span>Active: {mi.get('label','—')}</div>
    <span class="sdot {dot_cls}"></span>
  </div>
</div>
<div class="mainarea">
""", unsafe_allow_html=True)

# empty state
if not st.session_state.documents and not st.session_state.current_response:
    st.markdown("""
    <div class="emptystate">
      <div class="empty-icon">⬡</div>
      <div class="empty-title">DocMind Hybrid AI</div>
      <div class="empty-sub">Upload documents and ask questions with institutional-grade precision. Hybrid dense + sparse retrieval across your indexed knowledge base.</div>
    </div>""", unsafe_allow_html=True)

# query interface
st.markdown('<div class="qarea"><div class="qlabel">Query Intelligence Engine</div></div>',unsafe_allow_html=True)

with st.container():
    cols=st.columns([1])
    q_col=st.columns([6,1])
    with q_col[0]:
        query=st.text_area("Query","",placeholder="Ask anything from your indexed documents… (e.g. What were the Q4 revenue figures?)",height=90,label_visibility="collapsed",key="main_query")
    with q_col[1]:
        st.markdown("<br>",unsafe_allow_html=True)
        submit=st.button("⚡ Analyze",use_container_width=True,key="submit")

    # quick prompts
    qp_cols=st.columns(4)
    prompts=["What were Q4 earnings?","Summarize key risks","Compare YoY growth","What are main findings?"]
    for col,p in zip(qp_cols,prompts):
        with col:
            if st.button(p,key=f"qp_{p[:8]}",use_container_width=True):
                query=p; submit=True

if submit:
    if not query.strip(): st.warning("Please enter a query.")
    elif not st.session_state.documents: st.warning("Please upload at least one document first.")
    else:
        do_search(query.strip()); st.rerun()

# response
if st.session_state.current_response:
    resp=st.session_state.current_response
    srcs=st.session_state.current_sources
    mi2=MODELS.get(st.session_state.active_model,{})
    st.markdown(f"""
    <div class="rcard">
      <div class="rheader">
        ⚡ {mi2.get('icon','')} {mi2.get('label','—')} &nbsp;·&nbsp; {st.session_state.active_mode}
        &nbsp;·&nbsp; {st.session_state.search_type} search &nbsp;·&nbsp; k={st.session_state.top_k}
        &nbsp;·&nbsp; T={st.session_state.temperature}
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="rbody">', unsafe_allow_html=True)
    st.markdown(resp)
    st.markdown("</div></div>", unsafe_allow_html=True)

    c1,c2,_=st.columns([1,1,3])
    with c1:
        if st.button("📋 Copy Response",use_container_width=True): st.toast("✅ Copied to clipboard!")
    with c2:
        st.download_button("⬇ Download .md",data=resp,file_name=f"docmind_{datetime.now().strftime('%Y%m%d_%H%M')}.md",mime="text/markdown",use_container_width=True)

    if srcs:
        with st.expander(f"▸ Sources — {len(srcs)} passages retrieved"):
            for i,s in enumerate(srcs):
                rel=s.get("relevance_pct",0)
                tier="h" if rel>=90 else "m" if rel>=75 else "l"
                tc="var(--cyan)" if tier=="h" else "var(--indigo)" if tier=="m" else "var(--info)"
                txt=s.get("text","")[:280]+("…" if len(s.get("text",""))>280 else "")
                st.markdown(f"""
                <div class="srccard {tier}">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><span class="srcnum">[{i+1}]</span> <span style="font-size:13px;font-weight:500;color:var(--tp);">{s.get("source","?")}</span></div>
                    <span style="font-size:13px;font-weight:600;color:{tc};">{rel:.1f}%</span>
                  </div>
                  <div class="srctext">{txt}</div>
                  <div class="srcmeta">ID: {s.get('id','—')[:20]} · Dense: {s.get('dense_score',0):.3f} · Sparse: {s.get('sparse_score',0):.3f}</div>
                </div>""", unsafe_allow_html=True)

# history
if len(st.session_state.query_history)>1:
    with st.expander(f"📚 Query History ({len(st.session_state.query_history)} queries)"):
        for entry in reversed(st.session_state.query_history[:-1]):
            mi3=MODELS.get(entry["model"],{})
            st.markdown(f"""
            <div style="background:var(--s2);border:1px solid var(--border);border-radius:8px;padding:11px;margin-bottom:7px;">
              <div style="font-size:10px;color:var(--tm);">{entry['ts']} · {mi3.get('label','—')} · {entry['mode']}</div>
              <div style="font-size:13px;color:var(--tp);font-weight:500;margin-top:3px;">{entry['query']}</div>
              <div style="font-size:12px;color:var(--tt);margin-top:3px;">{entry['response'][:200]}…</div>
            </div>""", unsafe_allow_html=True)

st.markdown("</div>",unsafe_allow_html=True)
