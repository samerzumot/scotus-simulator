import streamlit as st
import os
import json
import re
from datetime import datetime
import PyPDF2
from streamlit_extras.add_vertical_space import add_vertical_space

# ========================================
# Page Configuration
# ========================================
st.set_page_config(
    page_title="SCOTUS Strategic Engine | Appellate Strategy System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    
    :root {
        --bg-primary: #0a0e1a;
        --gold-primary: #c9a227;
        --gold-light: #e8c547;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border-subtle: rgba(148, 163, 184, 0.1);
    }

    .stApp {
        background: #0a0e1a;
        background-image: 
            radial-gradient(ellipse at 20% 0%, rgba(30, 58, 95, 0.3) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 100%, rgba(201, 162, 39, 0.1) 0%, transparent 50%);
        color: #f8fafc;
    }

    /* Typography */
    h1, h2, h3, .section-title {
        font-family: 'Playfair Display', serif !important;
    }
    
    body {
        font-family: 'Inter', sans-serif;
    }

    /* Cards */
    .css-1r6p8d1, .stMarkdownContainer {
        color: #f8fafc;
    }
    
    .metric-card {
        background: rgba(26, 34, 52, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    
    .metric-label {
        font-size: 0.7rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background: rgba(17, 24, 39, 0.95);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }

    /* Brief Viewer */
    .brief-viewer {
        background: #ffffff;
        color: #2e3338;
        padding: 40px;
        border-radius: 12px;
        font-family: 'Playfair Display', serif;
        line-height: 1.7;
        border-left: 8px solid #c9a227;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-height: 600px;
        overflow-y: auto;
        font-size: 1.1rem;
    }
    
    .brief-segment {
        cursor: pointer;
        padding: 2px 4px;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    
    .brief-segment:hover {
        background: rgba(201, 162, 39, 0.2);
    }
    
    .brief-segment.critical {
        background: rgba(239, 64, 64, 0.15);
        border-bottom: 2px solid #ef4444;
    }
    
    .brief-segment.caution {
        background: rgba(245, 158, 11, 0.15);
        border-bottom: 2px solid #f59e0b;
    }

    /* Sample Case Cards */
    .sample-card {
        background: rgba(26, 34, 52, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }
    
    .sample-card:hover {
        border-color: #c9a227;
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(201, 162, 39, 0.15);
    }

    /* Result Indicators */
    .indicator-high { color: #ef4444; font-weight: 700; }
    .indicator-medium { color: #f59e0b; font-weight: 700; }
    .indicator-low { color: #22c55e; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ========================================
# Data Definitions (Ported from app.js / backend.py)
# ========================================

JUSTICES = {
    'roberts': {'name': 'Chief Justice Roberts', 'role': 'Chief Justice', 'focus': 'Institutionalism & Narrow Rulings', 'style': 'Seeks incremental, consensus-building decisions', 'id': 'roberts'},
    'thomas': {'name': 'Justice Thomas', 'role': 'Associate', 'focus': 'Originalism & Constitutional Text', 'style': 'Questions structural precedents; emphasizes original meaning', 'id': 'thomas'},
    'alito': {'name': 'Justice Alito', 'role': 'Associate', 'focus': 'Textual Analysis & Practical Consequences', 'style': 'Probes real-world impacts and statutory interpretation', 'id': 'alito'},
    'sotomayor': {'name': 'Justice Sotomayor', 'role': 'Associate', 'focus': 'Civil Rights & Practical Impact', 'style': 'Focuses on effects on marginalized communities', 'id': 'sotomayor'},
    'kagan': {'name': 'Justice Kagan', 'role': 'Associate', 'focus': 'Pragmatic Interpretation & Workability', 'style': 'Tests practical implementation of legal rules', 'id': 'kagan'},
    'gorsuch': {'name': 'Justice Gorsuch', 'role': 'Associate', 'focus': 'Textualism & Separation of Powers', 'style': 'Strict adherence to statutory text and constitutional structure', 'id': 'gorsuch'},
    'kavanaugh': {'name': 'Justice Kavanaugh', 'role': 'Associate', 'focus': 'Precedent & Moderate Application', 'style': 'Weighs stare decisis carefully; seeks middle-ground', 'id': 'kavanaugh'},
    'barrett': {'name': 'Justice Barrett', 'role': 'Associate', 'focus': 'Originalism & Doctrinal Clarity', 'style': 'Precise doctrinal questions; historical analysis', 'id': 'barrett'},
    'jackson': {'name': 'Justice Jackson', 'role': 'Associate', 'focus': 'Historical Context & Equity', 'style': 'Emphasizes historical background and fairness', 'id': 'jackson'}
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
    ],
    'first_amendment': [
        {'case': 'Reed v. Town of Gilbert, 576 U.S. 155 (2015)', 'url': 'https://supreme.justia.com/cases/federal/us/576/155/', 'holding': 'Content-based speech restrictions subject to strict scrutiny'},
        {'case': 'New York Times Co. v. Sullivan, 376 U.S. 254 (1964)', 'url': 'https://supreme.justia.com/cases/federal/us/376/254/', 'holding': 'Actual malice standard for defamation of public figures'}
    ],
    'separation_of_powers': [
        {'case': "Humphrey's Executor v. United States, 295 U.S. 602 (1935)", 'url': 'https://supreme.justia.com/cases/federal/us/295/602/', 'holding': 'Congress may limit presidential removal of certain officers'},
        {'case': 'Seila Law LLC v. CFPB, 591 U.S. ___ (2020)', 'url': 'https://supreme.justia.com/cases/federal/us/591/19-7/', 'holding': 'Single-director removal restrictions unconstitutional'}
    ],
    'standing': [
        {'case': 'Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992)', 'url': 'https://supreme.justia.com/cases/federal/us/504/555/', 'holding': 'Article III standing requires injury, causation, redressability'},
        {'case': 'TransUnion LLC v. Ramirez, 594 U.S. ___ (2021)', 'url': 'https://supreme.justia.com/cases/federal/us/594/20-297/', 'holding': 'Statutory violations alone insufficient for Article III standing'}
    ]
}

SAMPLE_CASES = {
    'Louisiana v. Callais': {
        'docket': '24-109', 'posture': 'merits', 'issue': 'VRA Section 2 · Racial Gerrymandering',
        'text': """PETITION FOR WRIT OF CERTIORARI... Questions Presented: 1. Whether the intentional creation of a second majority-minority congressional district to remedy a likely Voting Rights Act violation violates the Fourteenth or Fifteenth Amendments... 2. Whether the district court erred in finding that race predominated..."""
    },
    'Trump v. V.O.S. Selections': {
        'docket': '24-892', 'posture': 'merits', 'issue': 'IEEPA · Tariffs · Nondelegation',
        'text': """PETITION FOR WRIT OF CERTIORARI... Questions Presented: 1. Whether the International Emergency Economic Powers Act (IEEPA) authorizes the President to impose tariffs... 2. Whether such delegation of taxing authority violates the nondelegation doctrine..."""
    },
    'Trump v. Slaughter': {
        'docket': '24-631', 'posture': 'merits', 'issue': 'Removal Power · Separation of Powers',
        'text': """PETITION FOR WRIT OF CERTIORARI... Questions Presented: 1. Whether statutory removal protections for FTC commissioners violate the separation of powers... 2. Whether Humphrey's Executor should be overruled..."""
    },
    'Williams v. Reed': {
        'docket': '23-191', 'posture': 'merits', 'issue': 'Section 1983 · Due Process · Exhaustion',
        'text': """PETITION FOR WRIT OF CERTIORARI... Questions Presented: 1. Whether exhaustion of state administrative remedies is required to bring claims under 42 U.S.C. § 1983 in state court..."""
    }
}

# ========================================
# Helper Functions
# ========================================

def detect_posture(text):
    lower_text = text.lower()
    if 'petition for writ' in lower_text or 'cert petition' in lower_text: return 'cert'
    if 'emergency application' in lower_text or 'stay pending' in lower_text: return 'emergency'
    if 'merits brief' in lower_text or 'brief for petitioner' in lower_text: return 'merits'
    if 'oral argument transcript' in lower_text: return 'backtest'
    return 'cert'

def extract_issues(text):
    lower_text = text.lower()
    return {
        'voting_rights': any(kw in lower_text for kw in ['voting rights', 'vra', 'section 2', 'dilution']),
        'equal_protection': any(kw in lower_text for kw in ['equal protection', '14th amendment', 'discrimination']),
        'first_amendment': any(kw in lower_text for kw in ['first amendment', 'free speech', 'free exercise', 'establishment clause']),
        'separation_of_powers': any(kw in lower_text for kw in ['separation of powers', 'removal', 'nondelegation', 'executive power']),
        'standing': any(kw in lower_text for kw in ['standing', 'injury in fact', 'mootness', 'case or controversy']),
        'due_process': any(kw in lower_text for kw in ['due process', 'procedural', 'substantive due process']),
        'commerce_clause': any(kw in lower_text for kw in ['commerce clause', 'interstate commerce', 'dormant commerce']),
        'preemption': any(kw in lower_text for kw in ['preemption', 'supremacy clause', 'federal preemption'])
    }

def analyze_case_logic(text, title, posture, docket):
    issues = extract_issues(text)
    
    # Tier Classification
    text_len = len(text)
    if text_len > 10000: tier = "A"
    elif text_len > 1000: tier = "B"
    else: tier = "C"

    # Risk Assessment
    high_risk_issues = ['standing', 'separation_of_powers']
    has_high_risk = any(issues.get(issue) for issue in high_risk_issues)
    
    if tier == "C":
        risk_level = "CAUTION"
        primary_obstacle = "Insufficient materials for complete analysis"
        rewrite = "Upload full petition and lower court decision for comprehensive evaluation"
        dig_risk = "High"
    elif has_high_risk:
        risk_level = "CRITICAL"
        primary_obstacle = "Potential jurisdictional or structural defect identified"
        rewrite = "Address threshold issues before merits arguments"
        dig_risk = "Medium"
    else:
        risk_level = "CAUTION"
        primary_obstacle = "Standard appellate risks present; vehicle quality uncertain"
        rewrite = "Strengthen circuit split documentation and vehicle presentation"
        dig_risk = "Low"

    # Risks detailed
    risks = [
        {'category': 'Vehicle Integrity', 'level': 'low' if tier == 'A' else 'medium', 'confidence': 'High' if tier == 'A' else 'Limited data'},
        {'category': 'Circuit Split', 'level': 'medium', 'confidence': 'Requires verification'},
        {'category': 'Preservation', 'level': 'medium' if tier != 'A' else 'low', 'confidence': 'Check full record'},
        {'category': 'Mootness Risk', 'level': 'low' if posture != 'emergency' else 'high', 'confidence': 'Based on posture'}
    ]

    # Precedents
    relevant_prec = []
    for issue, present in issues.items():
        if present and issue in PRECEDENTS:
            relevant_prec.extend(PRECEDENTS[issue])
    if not relevant_prec:
        relevant_prec.append({'case': 'Marbury v. Madison, 5 U.S. 137 (1803)', 'holding': 'Foundational judicial review authority'})

    # Traps & Counters
    traps = []
    if issues.get('standing'):
        traps.append({'trap': 'Addressing merits extensively while leaving standing vulnerable', 'counter': 'Lead with concrete injury demonstration'})
    if issues.get('voting_rights') and issues.get('equal_protection'):
        traps.append({'trap': 'Conceding race predominated while relying on VRA compliance', 'counter': 'Contest predomination; argue traditional criteria'})
    
    if not traps:
        traps.append({'trap': 'Over-relying on circuit split maturity', 'counter': 'Document specific contradictory holdings'})

    return {
        'title': title, 'tier': tier, 'posture': posture, 'docket': docket,
        'riskLevel': risk_level, 'primaryObstacle': primary_obstacle, 
        'rewriteDirective': rewrite, 'digRisk': dig_risk,
        'precedents': relevant_prec[:6], 'issues': issues, 'traps': traps[:4],
        'risks': risks
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

# ========================================
# Streamlit UI Components
# ========================================

def render_sidebar_dashboard(ans):
    with st.sidebar:
        add_vertical_space(1)
        st.markdown("### Executive Dashboard")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Input Tier</div><div class="metric-value">{ans["tier"]}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card"><div class="metric-label">DIG Risk</div><div class="metric-value">{ans["digRisk"]}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Posture</div><div class="metric-value">{ans["posture"].upper()}</div></div>', unsafe_allow_html=True)
            risk_class = "indicator-high" if ans["riskLevel"] == "CRITICAL" else "indicator-medium"
            st.markdown(f'<div class="metric-card"><div class="metric-label">Risk Level</div><div class="metric-value {risk_class}">{ans["riskLevel"]}</div></div>', unsafe_allow_html=True)
        
        st.markdown(f"**Primary Obstacle:**\n{ans['primaryObstacle']}")
        st.markdown(f"**Rewrite Directive:**\n{ans['rewriteDirective']}")
        
        add_vertical_space(1)
        st.divider()
        st.markdown("### Justice Simulation")
        
        justice_ids = list(JUSTICES.keys())
        cols = st.columns(3)
        for i, jid in enumerate(justice_ids):
            col = cols[i % 3]
            if col.button(JUSTICES[jid]['name'].split()[-1], key=f"side_{jid}", use_container_width=True):
                st.session_state.selected_justice = jid

def render_welcome_screen():
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>SCOTUS Strategic Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.8rem;'>Adversarial Appellate Strategy System</p>", unsafe_allow_html=True)
    add_vertical_space(2)
    
    tab_paste, tab_upload, tab_sample = st.tabs(["Paste Text", "Upload PDF", "Sample Cases"])
    
    with tab_paste:
        case_title = st.text_input("Case Title", placeholder="e.g., Louisiana v. Callais")
        case_text = st.text_area("Case Materials", height=300, placeholder="Paste petition text, questions presented, or lower-court decision...")
        if st.button("Begin Analysis", key="btn_paste", type="primary"):
            if not case_text: st.error("Please provide case materials.")
            else:
                posture = detect_posture(case_text)
                st.session_state.analysis = analyze_case_logic(case_text, case_title or "Untitled", posture, "")
                st.session_state.case_text = case_text
                st.rerun()
                
    with tab_upload:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file:
            if st.button("Extract and Analyze", type="primary"):
                with st.spinner("Analyzing case materials..."):
                    text = extract_pdf_text(uploaded_file)
                    posture = detect_posture(text)
                    st.session_state.analysis = analyze_case_logic(text, uploaded_file.name, posture, "")
                    st.session_state.case_text = text
                    st.rerun()
                    
    with tab_sample:
        st.markdown("### Select a Landmark Case")
        cols = st.columns(2)
        for i, (name, data) in enumerate(SAMPLE_CASES.items()):
            col = cols[i % 2]
            with col:
                st.markdown(f"""
                <div class="sample-card">
                    <span style='font-size: 0.7rem; color: #c9a227; font-weight: 700;'>{data['docket']}</span>
                    <h4 style='margin: 5px 0;'>{name}</h4>
                    <p style='font-size: 0.8rem; color: #94a3b8;'>{data['issue']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Analyze {name.split()[-1]}", key=f"btn_sample_{i}"):
                    st.session_state.analysis = analyze_case_logic(data['text'], name, data['posture'], data['docket'])
                    st.session_state.case_text = data['text']
                    st.rerun()

def render_analysis_dashboard():
    ans = st.session_state.analysis
    render_sidebar_dashboard(ans)
    
    st.markdown(f"## Strategic Analysis: {ans['title']}")
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### Case Materials")
        st.markdown(f'<div class="brief-viewer">{st.session_state.case_text}</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown("### Strategy Overview")
        with st.container():
            st.markdown("#### Relevant Precedents")
            for prec in ans['precedents']:
                st.markdown(f"**{prec['case']}**")
                st.markdown(f"<span style='font-size: 0.85rem; color: #94a3b8; font-style: italic;'>{prec['holding']}</span>", unsafe_allow_html=True)
            
            add_vertical_space(1)
            st.markdown("#### Strategic Traps & Counters")
            for t in ans['traps']:
                st.warning(f"**Trap:** {t['trap']}")
                st.success(f"**Counter:** {t['counter']}")
            
            add_vertical_space(1)
            st.markdown("#### Identified Issues")
            for issue, present in ans['issues'].items():
                if present:
                    st.markdown(f"✅ {issue.replace('_', ' ').title()}")
            
            add_vertical_space(1)
            st.markdown("#### Strategic Risk Matrix")
            for r in ans['risks']:
                color = "#22c55e" if r['level'] == 'low' else "#f59e0b" if r['level'] == 'medium' else "#ef4444"
                st.markdown(f"""
                <div style='margin-bottom: 8px;'>
                    <div style='display: flex; justify-content: space-between; font-size: 0.8rem;'>
                        <span>{r['category']}</span>
                        <span style='color: {color}; font-weight: 700;'>{r['level'].upper()}</span>
                    </div>
                    <div style='font-size: 0.7rem; color: #94a3b8;'>{r['confidence']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Justice Spotlight
    if 'selected_justice' in st.session_state:
        jid = st.session_state.selected_justice
        j = JUSTICES[jid]
        st.divider()
        st.markdown(f"### Judicial Spotlight: {j['name']}")
        
        j_col1, j_col2 = st.columns([1, 2])
        with j_col1:
            st.markdown(f"**Focus:**\n{j['focus']}")
            st.markdown(f"**Style:**\n{j['style']}")
        with j_col2:
            st.markdown("#### Simulated Pressure Point")
            
            # Detailed templates for each justice
            question_templates = {
                'thomas': {
                    'voting_rights': "Where in the constitutional text does Congress derive authority to mandate race-conscious districting? Isn't Section 2 of the VRA itself constitutionally suspect under the original public meaning of the Fifteenth Amendment?",
                    'separation_of_powers': "What is the original understanding of 'executive Power' in Article II? Doesn't the removal restriction here conflict with the Constitution's vesting of that power in the President?",
                    'default': "What is the original public meaning of the constitutional provision at issue, and how does that constrain our analysis?"
                },
                'kagan': {
                    'voting_rights': "If we rule for you, what exactly should states do when facing a Section 2 violation? Must they wait for contempt before drawing remedial maps?",
                    'standing': "Walk me through how your proposed standing rule would work in practice. What cases does it let in, and what does it keep out?",
                    'default': "Give me a workable test. How would lower courts actually apply this standard?"
                },
                'barrett': {
                    'voting_rights': "Does VRA compliance automatically constitute a compelling interest, or must we engage in additional balancing? What's the doctrinal framework?",
                    'first_amendment': "What level of scrutiny applies here, and what's the precise test? I want clean doctrine.",
                    'default': "Help me understand the doctrinal rule you want us to announce and how it fits existing precedent."
                },
                'jackson': {
                    'voting_rights': "Given the specific history of voter disenfranchisement in this jurisdiction, isn't there something dissonant about using Equal Protection to prevent majority-Black districts?",
                    'equal_protection': "What historical context should inform our interpretation? How does the purpose behind this provision guide us?",
                    'default': "What historical background are we overlooking that should inform our reading here?"
                },
                'roberts': {
                    'default': "Is there a narrow way to decide this case without reaching the broader constitutional question you're pressing?"
                },
                'alito': {
                    'default': "What are the real-world consequences of your proposed rule? Who wins and who loses?"
                },
                'sotomayor': {
                    'default': "How does your position affect ordinary people? Have you considered the on-the-ground impact?"
                },
                'gorsuch': {
                    'default': "Point me to the statutory text. Where are the words that support your reading?"
                },
                'kavanaugh': {
                    'default': "What about stare decisis? What reliance interests would we disrupt by ruling your way?"
                }
            }
            
            # Find appropriate question
            templates = question_templates.get(jid, {'default': "How do you respond to the strongest version of your opponent's argument?"})
            question = templates.get('default', "")
            for issue, present in ans['issues'].items():
                if present and issue in templates:
                    question = templates[issue]
                    break
            
            st.markdown(f"**{j['name']}:** *\"{question}\"*")
            
            # Strategic Counter Mapping
            pressures = {
                'thomas': 'Challenges modern interpretations against original constitutional framework',
                'kagan': 'Forces articulation of workable, real-world legal standard',
                'barrett': 'Demands clean legal test that harmonizes with existing doctrine',
                'jackson': 'Invokes purposive/historical analysis to destabilize formalist arguments',
                'roberts': 'Seeks narrow resolution; tests for minimalist off-ramps',
                'alito': 'Probes practical consequences and implementation difficulties',
                'sotomayor': 'Emphasizes human impact and fairness concerns',
                'gorsuch': 'Insists on textual grounding for every proposition',
                'kavanaugh': 'Weighs reliance interests and precedential stability'
            }
            
            st.info(f"** Pressure Point:** {pressures.get(jid, 'Tests the logical limits of the argument')}")
            st.success("**Strategic Counter:** Emphasize the unique nature of this record that makes a narrow ruling impossible, while providing a clear limiting principle for the proposed rule.")

    # Chat Footer
    st.divider()
    st.markdown("### Interactive Strategy Refinement")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Analysis complete. How should we iterate on this adversarial strategy?"}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Ask a follow-up or test a hypothetical..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Contextual response logic from backend.py
        lower_prompt = prompt.lower()
        if 'what if' in lower_prompt or 'hypothetical' in lower_prompt:
            response = """**Hypothetical Analysis Framework**
To evaluate alternative scenarios, I assess:
1. **Vehicle Impact** — How do changed facts affect jurisdictional posture?
2. **Standard Shift** — Does the legal test apply differently?
3. **Justice Alignment** — Which Justices become more/less sympathetic?
Specify which aspect you'd like to modify for targeted analysis."""
        elif 'rewrite' in lower_prompt or 'question presented' in lower_prompt:
            response = """**Questions Presented: Strategic Drafting**
Key principles:
1. **Front-load winning facts** — Your best facts should appear in the question نفسه
2. **Signal favorable review** — Frame to invoke your preferred precedent
3. **Avoid over-breadth** — Narrow questions have higher grant rates
4. **Create asymmetry** — Make "yes" easier than opponent's "no"."""
        elif 'circuit split' in lower_prompt or 'conflict' in lower_prompt:
            response = """**Circuit Split Analysis**
The Court evaluates split quality on:
1. **Directness** — Same legal question, opposite holdings
2. **Maturity** — Sufficient percolation across circuits
3. **Importance** — Substantial federal interests affected
4. **Vehicle** — Can this case cleanly resolve the split?"""
        elif 'standing' in lower_prompt or 'jurisdiction' in lower_prompt:
            response = """**Jurisdictional Checklist**
Standing/jurisdiction defects are **dispositive**:
• **Article III Standing**: injury-in-fact, causation, redressability  
• **Statutory Exhaustion**: all administrative steps completed?  
• **Finality**: lower court judgment truly final?  
• **Mootness**: can Court grant effective relief?"""
        else:
            response = f"Analyzing '{prompt}' against {ans['posture']} posture... \n\nThis shift likely moves Chief Justice Roberts toward a more skeptical position, as it increases 'vehicle risk' for a broad decision. You should counter by framing this as a unique outcome limited to these specific facts."
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ========================================
# Main Execution
# ========================================

# Reset functionality
if st.sidebar.button("New Analysis", use_container_width=True):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

if 'analysis' not in st.session_state:
    render_welcome_screen()
else:
    render_analysis_dashboard()
