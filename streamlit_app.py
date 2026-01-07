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
    /* 1. Base Reset & Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    
    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #111827;
        --bg-tertiary: #1a2234;
        --bg-card: rgba(26, 34, 52, 0.8);
        --gold-primary: #c9a227;
        --gold-light: #e8c547;
        --gold-dark: #a07d1c;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-tertiary: #64748b;
        --border-subtle: rgba(148, 163, 184, 0.1);
        --font-serif: 'Playfair Display', Georgia, serif;
        --font-sans: 'Inter', sans-serif;
    }

    /* Aggressive Streamlit Overrides */
    [data-testid="stAppViewContainer"] {
        background: var(--bg-primary) !important;
        background-image: 
            radial-gradient(ellipse at 20% 0%, rgba(30, 58, 95, 0.3) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 100%, rgba(201, 162, 39, 0.1) 0%, transparent 50%) !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(17, 24, 39, 0.95) !important;
        border-right: 1px solid var(--border-subtle) !important;
        width: 320px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
        visibility: hidden !important;
    }

    /* 2. Custom Header */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(17, 24, 39, 0.95);
        border-bottom: 1px solid var(--border-subtle);
        width: 100%;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .header-logo {
        width: 40px;
        height: 40px;
        color: var(--gold-primary);
    }

    .brand-text h1 {
        font-size: 1.25rem;
        margin: 0;
        color: var(--text-primary);
        font-family: var(--font-serif);
        font-weight: 600;
    }

    .brand-text .tagline {
        font-size: 0.75rem;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* 3. Sidebar Cards */
    .sidebar-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
    }

    .sidebar-card-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    .sidebar-card-title svg {
        width: 16px;
        height: 16px;
        color: var(--gold-primary);
    }

    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin-bottom: 1.25rem;
    }

    .metric-box {
        background: var(--bg-secondary);
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        border: 1px solid var(--border-subtle);
    }

    .metric-label {
        display: block;
        font-size: 0.65rem;
        color: var(--text-tertiary);
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .awaiting { opacity: 0.5; }

    /* Justice Grid */
    .justice-btn-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        margin-bottom: 1rem;
    }

    /* 4. Landing Page / Welcome State */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 4rem 2rem;
        text-align: center;
        max-width: 1100px;
        margin: 0 auto;
    }

    .welcome-hero-icon {
        width: 80px;
        height: 80px;
        color: var(--gold-primary);
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }

    .welcome-title {
        font-family: var(--font-serif);
        font-size: 2.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .welcome-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        max-width: 600px;
        margin-bottom: 3rem;
    }

    /* Action Buttons (Streamlit Overrides) */
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--gold-primary), var(--gold-dark)) !important;
        border: none !important;
        color: var(--bg-primary) !important;
        box-shadow: 0 4px 15px rgba(201, 162, 39, 0.2) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--gold-light), var(--gold-primary)) !important;
        transform: translateY(-2px) !important;
    }

    /* Tiers Container */
    .tiers-wrapper {
        display: flex;
        gap: 1.5rem;
        padding: 1.5rem;
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        margin-top: 2rem;
        width: 100%;
        max-width: 900px;
        justify-content: center;
    }

    .tier-card {
        text-align: left;
        flex: 1;
    }

    .tier-badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--gold-primary);
        background: rgba(201, 162, 39, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }

    .tier-text {
        font-size: 0.8rem;
        color: var(--text-tertiary);
        line-height: 1.4;
    }

    /* Sample Cases Grid */
    .sample-section-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        color: var(--text-secondary);
        margin-top: 4rem;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .case-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: left;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
    }

    .case-card:hover {
        border-color: var(--gold-primary);
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3), 0 0 20px rgba(201, 162, 39, 0.1);
    }

    .case-badge {
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        font-size: 0.65rem;
        font-weight: 700;
        color: var(--gold-primary);
        background: rgba(201, 162, 39, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }

    .case-docket {
        font-size: 0.75rem;
        color: var(--gold-primary);
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .case-name {
        font-family: var(--font-serif);
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }

    .case-issue {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* Result Indicators */
    .indicator-high { color: #ef4444 !important; }
    .indicator-medium { color: #f59e0b !important; }
    .indicator-low { color: #22c55e !important; }

    /* Hide Streamlit Footer & Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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

def render_sidebar_dashboard(ans=None):
    with st.sidebar:
        # 1. Executive Dashboard Card
        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>
                </svg>
                Executive Dashboard
            </div>
            <div class="metric-grid">
                <div class="metric-box {'awaiting' if not ans else ''}">
                    <span class="metric-label">Input Tier</span>
                    <span class="metric-value">{ans["tier"] if ans else "—"}</span>
                </div>
                <div class="metric-box {'awaiting' if not ans else ''}">
                    <span class="metric-label">Posture</span>
                    <span class="metric-value">{ans["posture"].upper() if ans else "—"}</span>
                </div>
                <div class="metric-box {'awaiting' if not ans else ''}">
                    <span class="metric-label">Risk Level</span>
                    <span class="metric-value {('indicator-high' if ans['riskLevel'] == 'CRITICAL' else 'indicator-medium') if ans else ''}">{ans["riskLevel"] if ans else "—"}</span>
                </div>
                <div class="metric-box {'awaiting' if not ans else ''}">
                    <span class="metric-label">DIG Risk</span>
                    <span class="metric-value">{ans["digRisk"] if ans else "—"}</span>
                </div>
            </div>
            <div style="margin-bottom: 1rem;">
                <span class="metric-label">Primary Obstacle</span>
                <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0;">{ans['primaryObstacle'] if ans else "Upload case materials to begin analysis"}</p>
            </div>
            <div>
                <span class="metric-label">Rewrite Directive</span>
                <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0;">{ans['rewriteDirective'] if ans else "—"}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Justice Simulation Card
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/>
                </svg>
                Justice Simulation
            </div>
        """, unsafe_allow_html=True)
        
        justice_ids = list(JUSTICES.keys())
        cols = st.columns(3)
        for i, jid in enumerate(justice_ids):
            col = cols[i % 3]
            name_parts = JUSTICES[jid]['name'].split()
            last_name = name_parts[-1]
            role = "C.J." if jid == 'roberts' else "Associate"
            
            # Using st.button with specific key to avoid conflicts
            if col.button(f"**{last_name}**\n{role}", key=f"side_{jid}", use_container_width=True, disabled=not ans, help=JUSTICES[jid]['focus']):
                st.session_state.selected_justice = jid
        
        st.markdown("""
        <div style="margin-top: 1rem;"></div>
        """, unsafe_allow_html=True)
        st.button(" Simulate Full Bench", key="sim_bench", use_container_width=True, disabled=not ans, icon="🏛️")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_custom_header():
    # Use a container for the header to match the sticking behavior
    st.markdown("""
    <div class="header-container">
        <div class="header-brand">
            <div class="header-logo">
                <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 4L4 12V28L20 36L36 28V12L20 4Z" stroke="currentColor" stroke-width="2" />
                    <path d="M20 4V36M4 12L36 28M36 12L4 28" stroke="currentColor" stroke-width="1.5" opacity="0.5" />
                    <circle cx="20" cy="20" r="6" fill="currentColor" />
                </svg>
            </div>
            <div class="brand-text">
                <h1>SCOTUS Strategic Engine</h1>
                <span class="tagline">Adversarial Appellate Strategy System</span>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; align-items: center;">
    """, unsafe_allow_html=True)
    
    # We use st.columns *inside* the header area by absolute positioning or just matching layout
    # Since Streamlit won't let us put st.button easily inside HTML, we match the look
    dummy_col, h_btn1, h_btn2 = st.columns([10, 2, 2])
    with h_btn1:
        if st.button("New Analysis", key="h_new", use_container_width=True, icon="➕"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with h_btn2:
        if st.button("Upload Case", key="h_up", type="primary", use_container_width=True, icon="📤"):
            if 'analysis' in st.session_state:
                del st.session_state['analysis']
            st.session_state.show_uploader = True
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_welcome_screen():
    render_custom_header()
    
    # 1. Welcome State / Hero
    st.markdown("""
    <div class="welcome-screen">
        <div class="welcome-hero-icon">
            <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M40 10L10 25V55L40 70L70 55V25L40 10Z" stroke="currentColor" stroke-width="2" />
                <path d="M40 10V70M10 25L70 55M70 25L10 55" stroke="currentColor" stroke-width="1" opacity="0.3" />
                <circle cx="40" cy="40" r="12" stroke="currentColor" stroke-width="2" />
                <circle cx="40" cy="40" r="4" fill="currentColor" />
            </svg>
        </div>
        <h1 class="welcome-title">SCOTUS Strategic Engine</h1>
        <p class="welcome-subtitle">Upload a cert petition, merits brief, or emergency application to begin adversarial analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Buttons - centered
    _, col_cta1, col_cta2, _ = st.columns([1, 1.5, 1.5, 1])
    with col_cta1:
        if st.button("🚀 Upload Case Materials", key="welcome_up", use_container_width=True, type="primary"):
            st.session_state.show_uploader = True
            st.session_state.show_paster = False
    with col_cta2:
        if st.button("📝 Paste Text", key="welcome_paste", use_container_width=True):
            st.session_state.show_paster = True
            st.session_state.show_uploader = False

    # Modal-like input area (Centered)
    if st.session_state.get('show_uploader'):
        _, u_col, _ = st.columns([1, 2, 1])
        with u_col:
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            u_file = st.file_uploader("Upload Case materials", type="pdf", label_visibility="collapsed")
            if u_file:
                if st.button("Begin Analysis", key="up_btn", use_container_width=True, type="primary"):
                    with st.spinner("Analyzing..."):
                        text = extract_pdf_text(u_file)
                        posture = detect_posture(text)
                        st.session_state.analysis = analyze_case_logic(text, u_file.name, posture, "")
                        st.session_state.case_text = text
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    if st.session_state.get('show_paster'):
        _, p_col, _ = st.columns([0.5, 3, 0.5])
        with p_col:
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            c_title = st.text_input("Case Title", placeholder="e.g., Louisiana v. Callais")
            c_text = st.text_area("Case Materials", height=300, placeholder="Paste text here...")
            if st.button("Begin Analysis", key="paste_btn", use_container_width=True, type="primary"):
                if c_text:
                    posture = detect_posture(c_text)
                    st.session_state.analysis = analyze_case_logic(c_text, c_title or "Untitled", posture, "")
                    st.session_state.case_text = c_text
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # 3. Input Tiers
    st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%;">
        <div class="tiers-wrapper">
            <div class="tier-card">
                <span class="tier-badge">Tier A</span>
                <p class="tier-text">Full petition + Questions Presented + lower-court decision</p>
            </div>
            <div class="tier-card">
                <span class="tier-badge">Tier B</span>
                <p class="tier-text">Summaries, excerpts, docket information</p>
            </div>
            <div class="tier-card">
                <span class="tier-badge">Tier C</span>
                <p class="tier-text">Case name or docket number only</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Sample Cases
    st.markdown("""
    <div class="sample-section-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        </svg>
        Or Start with a Sample Case
    </div>
    """, unsafe_allow_html=True)
    
    sample_items = list(SAMPLE_CASES.items())
    row1 = st.columns(2)
    row2 = st.columns(2)
    all_cols = row1 + row2
    
    for i, (name, data) in enumerate(sample_items):
        with all_cols[i]:
            st.markdown(f"""
            <div class="case-card">
                <div class="case-badge">{data['posture']}</div>
                <div class="case-docket">{data['docket']}</div>
                <div class="case-name">{name}</div>
                <div class="case-issue">{data['issue']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Begin Analysis", key=f"btn_samp_{i}", use_container_width=True):
                st.session_state.analysis = analyze_case_logic(data['text'], name, data['posture'], data['docket'])
                st.session_state.case_text = data['text']
                st.rerun()

def render_analysis_dashboard():
    ans = st.session_state.analysis
    render_custom_header()
    render_sidebar_dashboard(ans)
    
    st.markdown(f"""
    <div style="padding: 2rem 3rem;">
        <h2 style="font-family: var(--font-serif); font-size: 2.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 2rem;">Strategic Analysis: {ans['title']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        # 1. Brief Viewer
        st.markdown(f"""
        <div class="sidebar-card" style="margin: 0; margin-bottom: 2rem;">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
                </svg>
                Case Materials / Brief Viewer
            </div>
            <div style="font-size: 0.95rem; line-height: 1.6; color: var(--text-secondary); max-height: 500px; overflow-y: auto; background: var(--bg-secondary); padding: 1.5rem; border-radius: 8px;">
                {st.session_state.get('case_text', '').replace('\n', '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Strategy Overview
        st.markdown(f"""
        <div class="sidebar-card" style="margin: 0;">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                Strategic Traps & Counters
            </div>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div style="padding: 1rem; background: rgba(239, 68, 68, 0.05); border-left: 3px solid #ef4444; border-radius: 4px;">
                    <span style="font-size: 0.7rem; font-weight: 700; color: #ef4444; text-transform: uppercase;">Primary Trap</span>
                    <p style="font-size: 0.9rem; color: var(--text-primary); margin: 0.25rem 0;">{ans['traps'][0] if ans['traps'] else 'N/A'}</p>
                </div>
                <div style="padding: 1rem; background: rgba(34, 197, 94, 0.05); border-left: 3px solid #22c55e; border-radius: 4px;">
                    <span style="font-size: 0.7rem; font-weight: 700; color: #22c55e; text-transform: uppercase;">Counter-Strategy</span>
                    <p style="font-size: 0.9rem; color: var(--text-primary); margin: 0.25rem 0;">{ans['traps'][1] if len(ans['traps']) > 1 else 'N/A'}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # 3. Precedents
        st.markdown(f"""
        <div class="sidebar-card" style="margin: 0; margin-bottom: 2rem;">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
                Precedent Architecture
            </div>
        """, unsafe_allow_html=True)
        for p in ans['precedents']:
            st.markdown(f"""
            <div style="padding: 0.75rem; background: var(--bg-secondary); border-radius: 6px; border-left: 3px solid var(--gold-primary); margin-bottom: 0.5rem;">
                <div style="font-size: 0.85rem; font-weight: 600; color: var(--gold-light);">{p}</div>
                <div style="font-size: 0.75rem; color: var(--text-tertiary);">Relevance: Direct · Reliability: High</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 4. Strategic Risk Matrix
        st.markdown("""
        <div class="sidebar-card" style="margin: 0;">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                Strategic Risk Matrix
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        """, unsafe_allow_html=True)
        for cat, risk in ans['risks'].items():
            color = "#ef4444" if risk == "High" else "#f59e0b" if risk == "Medium" else "#22c55e"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--bg-secondary); border-radius: 6px;">
                <span style="font-size: 0.85rem; color: var(--text-primary);">{cat}</span>
                <span style="font-size: 0.75rem; font-weight: 700; color: {color};">{risk.upper()}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    
    # 5. Justice Spotlight
    st.markdown("""
    <div style="padding: 0 3rem;">
        <div class="sidebar-card" style="margin: 0;">
            <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                Justice-Aware Question Simulation
            </div>
    """, unsafe_allow_html=True)
    
    j_sel = st.session_state.get('selected_justice', 'roberts')
    j_data = JUSTICES[j_sel]
    
    j_col1, j_col2 = st.columns([1, 2])
    with j_col1:
        st.markdown(f"""
        <div style="padding: 1.5rem; background: var(--bg-secondary); border-radius: 8px; border-top: 4px solid var(--gold-primary);">
            <div style="font-size: 1.25rem; font-family: var(--font-serif); font-weight: 600; color: var(--gold-primary);">{j_data['name']}</div>
            <div style="font-size: 0.8rem; color: var(--text-tertiary); margin-bottom: 1rem;">{j_data['role']}</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">{j_data['style']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with j_col2:
        st.markdown(f"""
        <div style="padding: 1.5rem; background: var(--navy-primary); border-radius: 8px; border-left: 4px solid var(--gold-primary);">
            <div style="font-size: 0.7rem; font-weight: 700; color: var(--gold-primary); text-transform: uppercase; margin-bottom: 0.5rem;">Predictive Oral Argument Question</div>
            <p style="font-size: 1rem; color: var(--text-primary); font-style: italic; font-family: var(--font-serif); margin-bottom: 1rem;">
                "{ans['questions'].get(j_sel, "How does the proposed rule reconcile with the principles of constitutional structure and historical practice in this domain?")}"
            </p>
            <div style="font-size: 0.8rem; color: var(--text-tertiary);">
                <strong style="color: #f59e0b;">Strategic Pressure:</strong> This line of questioning tests the doctrinal limits of your argument's proposed framework.
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # 6. Follow-up Chat
    st.markdown("""
    <div style="padding: 2rem 3rem;">
        <h3 style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-primary); margin-bottom: 1.5rem;">Interactive Strategy Refinement</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Analysis complete. How should we iterate on this adversarial strategy?"}]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Ask a follow-up or test a hypothetical..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simple response logic for the demo
        response = "Analyzing follow-up... \n\nThis shift likely moves Chief Justice Roberts toward a more skeptical position, as it increases 'vehicle risk' for a broad decision. You should counter by framing this as a unique outcome limited to these specific facts."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ========================================
# Main Execution
# ========================================

def main():
    if 'analysis' not in st.session_state:
        render_sidebar_dashboard(None)
        render_welcome_screen()
    else:
        render_analysis_dashboard()

if __name__ == "__main__":
    main()
