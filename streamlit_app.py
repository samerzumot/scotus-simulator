import streamlit as st
import os
import json
import re
from datetime import datetime
import PyPDF2
from streamlit_extras.add_vertical_space import add_vertical_space

# Set page config
st.set_page_config(
    page_title="SCOTUS Strategic Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .metric-card {
        background-color: #1e2124;
        border: 1px solid #36393e;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #72767d;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    .risk-caution { color: #faa61a; }
    .risk-critical { color: #f04747; }
    .risk-low { color: #43b581; }
    
    .justice-btn {
        width: 100%;
        text-align: left;
        padding: 10px;
        border-radius: 5px;
        background: #2f3136;
        border: 1px solid #36393e;
        color: #dcddde;
        margin-bottom: 5px;
        cursor: pointer;
    }
    
    .brief-viewer {
        background: #ffffff;
        color: #2e3338;
        padding: 30px;
        border-radius: 8px;
        font-family: 'Playfair Display', serif;
        line-height: 1.6;
        border-left: 5px solid #7289da;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# Data & Logic (Ported from backend.py)
# ========================================

JUSTICES = {
    'roberts': {'name': 'Chief Justice Roberts', 'role': 'Chief Justice', 'focus': 'Institutionalism & Narrow Rulings', 'style': 'Seeks incremental, consensus-building decisions', 'keywords': ['institutional', 'narrow', 'minimalist', 'precedent']},
    'thomas': {'name': 'Justice Thomas', 'role': 'Associate', 'focus': 'Originalism & Constitutional Text', 'style': 'Questions structural precedents; emphasizes original meaning', 'keywords': ['original', 'text', 'constitution', 'stare decisis']},
    'alito': {'name': 'Justice Alito', 'role': 'Associate', 'focus': 'Textual Analysis & Practical Consequences', 'style': 'Probes real-world impacts and statutory interpretation', 'keywords': ['practical', 'consequences', 'statutory', 'text']},
    'sotomayor': {'name': 'Justice Sotomayor', 'role': 'Associate', 'focus': 'Civil Rights & Practical Impact', 'style': 'Focuses on effects on marginalized communities', 'keywords': ['rights', 'impact', 'fairness', 'equality']},
    'kagan': {'name': 'Justice Kagan', 'role': 'Associate', 'focus': 'Pragmatic Interpretation & Workability', 'style': 'Tests practical implementation of legal rules', 'keywords': ['workable', 'practical', 'implementation', 'pragmatic']},
    'gorsuch': {'name': 'Justice Gorsuch', 'role': 'Associate', 'focus': 'Textualism & Separation of Powers', 'style': 'Strict adherence to statutory text and constitutional structure', 'keywords': ['text', 'separation', 'powers', 'structure']},
    'kavanaugh': {'name': 'Justice Kavanaugh', 'role': 'Associate', 'focus': 'Precedent & Moderate Application', 'style': 'Weighs stare decisis carefully; seeks middle-ground', 'keywords': ['precedent', 'stare decisis', 'moderate', 'reliance']},
    'barrett': {'name': 'Justice Barrett', 'role': 'Associate', 'focus': 'Originalism & Doctrinal Clarity', 'style': 'Precise doctrinal questions; historical analysis', 'keywords': ['doctrine', 'original', 'historical', 'clarity']},
    'jackson': {'name': 'Justice Jackson', 'role': 'Associate', 'focus': 'Historical Context & Equity', 'style': 'Emphasizes historical background and fairness', 'keywords': ['history', 'context', 'equity', 'purpose']}
}

PRECEDENTS = {
    'voting_rights': [
        {'case': 'Thornburg v. Gingles, 478 U.S. 30 (1986)', 'url': 'https://supreme.justia.com/cases/federal/us/478/30/', 'holding': 'Established Section 2 VRA preconditions for vote dilution claims'},
        {'case': 'Shaw v. Reno, 509 U.S. 630 (1993)', 'url': 'https://supreme.justia.com/cases/federal/us/509/630/', 'holding': 'Racial gerrymandering violates Equal Protection'},
        {'case': 'Allen v. Milligan, 599 U.S. 1 (2023)', 'url': 'https://supreme.justia.com/cases/federal/us/599/1/', 'holding': 'Reaffirmed Gingles framework for Section 2 claims'}
    ],
    'equal_protection': [
        {'case': 'Miller v. Johnson, 515 U.S. 900 (1995)', 'url': 'https://supreme.justia.com/cases/federal/us/515/900/', 'holding': 'Race cannot predominate in redistricting without compelling justification'},
        {'case': 'Cooper v. Harris, 581 U.S. 285 (2017)', 'url': 'https://supreme.justia.com/cases/federal/us/581/285/', 'holding': 'Good-faith VRA compliance cannot save unnecessary racial sorting'}
    ]
}

SAMPLE_CASES = {
    'Louisiana v. Callais': {
        'docket': '24-109', 'posture': 'merits',
        'text': """PETITION FOR WRIT OF CERTIORARI... Questions Presented: 1. Whether the intentional creation of a second majority-minority congressional district to remedy a likely Voting Rights Act violation violates the Fourteenth or Fifteenth Amendments..."""
    },
    'Trump v. V.O.S. Selections': {
        'docket': '24-892', 'posture': 'merits',
        'text': """PETITION FOR WRIT OF CERTIORARI... Questions Presented: 1. Whether the International Emergency Economic Powers Act (IEEPA) authorizes the President to impose tariffs..."""
    }
}

# Helper functions (Ported from backend.py)
def detect_posture(text):
    lower_text = text.lower()
    if 'petition' in lower_text: return 'cert'
    if 'emergency' in lower_text: return 'emergency'
    if 'merits' in lower_text: return 'merits'
    return 'cert'

def extract_issues(text):
    lower_text = text.lower()
    return {
        'voting_rights': any(kw in lower_text for kw in ['voting rights', 'vra', 'section 2']),
        'equal_protection': any(kw in lower_text for kw in ['equal protection', '14th amendment']),
        'first_amendment': any(kw in lower_text for kw in ['first amendment', 'free speech']),
        'separation_of_powers': any(kw in lower_text for kw in ['separation of powers', 'removal']),
        'standing': any(kw in lower_text for kw in ['standing', 'injury'])
    }

def extract_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error extracting PDF: {e}")
    return text.strip()

def analyze_case(text, title, posture, tier, docket):
    issues = extract_issues(text)
    
    # Generate risk assessment
    risk_level = 'CAUTION'
    if issues.get('standing') or issues.get('separation_of_powers'):
        risk_level = 'CRITICAL'
    elif tier == 'C':
        risk_level = 'CAUTION'
    
    # Find relevant precedents
    relevant = []
    for issue_name, is_present in issues.items():
        if is_present and issue_name in PRECEDENTS:
            relevant.extend(PRECEDENTS[issue_name])
    
    if not relevant:
        relevant.append({'case': 'Marbury v. Madison, 5 U.S. 137 (1803)', 'relevance': 'Foundational judicial review authority'})

    analysis = {
        'title': title or 'Untitled Case',
        'tier': tier,
        'posture': posture,
        'riskLevel': risk_level,
        'digRisk': 'High' if issues.get('standing') or tier == 'C' else 'Medium',
        'primaryObstacle': 'Potential jurisdictional defect identified' if issues.get('standing') else 'Standard appellate risks present',
        'rewriteDirective': 'Address threshold standing issues' if issues.get('standing') else 'Strengthen circuit split documentation',
        'precedents': relevant[:6],
        'issues': issues,
        'docket': docket
    }
    return analysis

# ========================================
# Streamlit UI
# ========================================

# Sidebar
with st.sidebar:
    st.title("⚖️ SCOTUS Strategic Engine")
    st.caption("Adversarial Appellate Strategy System")
    
    add_vertical_space(2)
    
    if st.button("New Analysis", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
        
    add_vertical_space(1)
    
    st.subheader("Executive Dashboard")
    if 'analysis' in st.session_state:
        ans = st.session_state.analysis
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Input Tier**\n### {ans['tier']}")
        with col2:
            st.markdown(f"**Posture**\n### {ans['posture'].upper()}")
            
        risk_color = "red" if ans['riskLevel'] == 'CRITICAL' else "orange"
        st.markdown(f"**Risk Level**\n#### :{risk_color}[{ans['riskLevel']}]")
        st.markdown(f"**DIG Risk**\n#### {ans['digRisk']}")
        
        st.write(f"**Primary Obstacle:** {ans['primaryObstacle']}")
        st.write(f"**Rewrite Directive:** {ans['rewriteDirective']}")
    else:
        st.info("Upload materials to begin analysis")

    add_vertical_space(2)
    st.subheader("Justice Simulation")
    justice_grid = st.container()
    justice_col1, justice_col2 = st.columns(2)
    for i, (jid, info) in enumerate(JUSTICES.items()):
        col = justice_col1 if i % 2 == 0 else justice_col2
        if col.button(f"{info['name'].split()[-1]}", key=jid, use_container_width=True, help=info['role']):
            st.session_state.selected_justice = jid

# Main Area
if 'analysis' not in st.session_state:
    st.title("Welcome to SCOTUS Strategic Engine")
    st.write("Upload a cert petition, merits brief, or emergency application to begin adversarial analysis.")
    
    tab_paste, tab_upload, tab_sample = st.tabs(["Paste Text", "Upload PDF", "Sample Cases"])
    
    with tab_paste:
        case_title = st.text_input("Case Title", placeholder="e.g., Louisiana v. Callais")
        case_text = st.text_area("Case Materials", height=300, placeholder="Paste petition text, questions presented, or lower-court decision...")
        if st.button("Begin Analysis", key="btn_paste", type="primary"):
            if not case_text:
                st.error("Please provide case materials.")
            else:
                posture = detect_posture(case_text)
                st.session_state.analysis = analyze_case(case_text, case_title, posture, "B", "")
                st.session_state.case_text = case_text
                st.rerun()
            
    with tab_upload:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file:
            st.success(f"File '{uploaded_file.name}' uploaded!")
            if st.button("Extract and Analyze", type="primary"):
                with st.spinner("Extracting text and analyzing..."):
                    text = extract_pdf_text(uploaded_file)
                    posture = detect_posture(text)
                    st.session_state.analysis = analyze_case(text, uploaded_file.name, posture, "A", "")
                    st.session_state.case_text = text
                    st.rerun()
                
    with tab_sample:
        cols = st.columns(2)
        for i, (name, data) in enumerate(SAMPLE_CASES.items()):
            col = cols[i % 2]
            with col:
                st.markdown(f"### {name}")
                st.write(f"**Docket:** {data['docket']} | **Posture:** {data['posture'].upper()}")
                if st.button(f"Load {name.split()[0]}", key=f"sample_{i}"):
                    st.session_state.analysis = analyze_case(data['text'], name, data['posture'], "A", data['docket'])
                    st.session_state.case_text = data['text']
                    st.rerun()
else:
    ans = st.session_state.analysis
    st.title(f"Strategic Analysis: {ans['title']}")
    
    col_brief, col_details = st.columns([2, 1])
    
    with col_brief:
        st.subheader("Case Materials")
        st.markdown(f'<div class="brief-viewer">{st.session_state.case_text}</div>', unsafe_allow_html=True)
        
    with col_details:
        st.subheader("Strategy Overview")
        st.markdown(f"**Docket:** `{ans.get('docket', 'N/A')}`")
        st.markdown(f"**Posture:** `{ans['posture'].upper()}`")
        
        add_vertical_space(1)
        st.markdown("#### Relevant Precedents")
        for p in ans['precedents']:
            st.markdown(f"- **{p['case']}**\n  *{p['relevance']}*")
            
        add_vertical_space(1)
        st.markdown("#### Identified Issues")
        for issue, present in ans['issues'].items():
            if present:
                st.markdown(f"✅ {issue.replace('_', ' ').title()}")

    # Justice Detail if selected
    if 'selected_justice' in st.session_state:
        jid = st.session_state.selected_justice
        justice = JUSTICES[jid]
        st.divider()
        st.subheader(f"Judicial Simulation: {justice['name']}")
        
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            st.markdown(f"**Focus:**\n{justice['focus']}")
            st.markdown(f"**Analytical Style:**\n{justice['style']}")
        with col_j2:
            st.markdown("#### Simulated Pressure Point")
            st.warning(f"**Justice {justice['name'].split()[-1]}:** How do you reconcile your request for a broad constitutional ruling with our institutional preference for narrow, incremental decisions? Is there a statutory 'off-ramp' we should consider first?")
            st.info("**Strategic Counter:** Emphasize the unique nature of this case that precludes a narrow ruling, while providing a 'fallback' statutory interpretation that still achieves the core objective.")

    # Chat
    st.divider()
    st.subheader("Interactive Strategy Refinement")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Adversarial analysis complete. How should we iterate on this strategy?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Test a hypothetical or refine an argument..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        response = f"Analyzing '{prompt}' against the current {ans['posture']} posture... \n\nChanging this fact would likely shift Chief Justice Roberts toward a more skeptical view, as it increases the risk of a broad ruling with unintended consequences. You should counter by framing this as a unique outcome limited to these specific facts."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
