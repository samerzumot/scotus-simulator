"""
SCOTUS Strategic Engine - Backend API Server
Flask-based API for case analysis and justice simulation
"""

import os
import json
import re
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Optional PDF support
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("PyPDF2 not installed. PDF upload will be disabled.")

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ========================================
# Configuration
# ========================================

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Justice profiles for simulation
JUSTICES = {
    'roberts': {
        'name': 'Chief Justice Roberts',
        'focus': 'Institutionalism & Narrow Rulings',
        'style': 'Seeks incremental, consensus-building decisions',
        'keywords': ['institutional', 'narrow', 'minimalist', 'precedent']
    },
    'thomas': {
        'name': 'Justice Thomas',
        'focus': 'Originalism & Constitutional Text',
        'style': 'Questions structural precedents; emphasizes original meaning',
        'keywords': ['original', 'text', 'constitution', 'stare decisis']
    },
    'alito': {
        'name': 'Justice Alito',
        'focus': 'Textual Analysis & Practical Consequences',
        'style': 'Probes real-world impacts and statutory interpretation',
        'keywords': ['practical', 'consequences', 'statutory', 'text']
    },
    'sotomayor': {
        'name': 'Justice Sotomayor',
        'focus': 'Civil Rights & Practical Impact',
        'style': 'Focuses on effects on marginalized communities',
        'keywords': ['rights', 'impact', 'fairness', 'equality']
    },
    'kagan': {
        'name': 'Justice Kagan',
        'focus': 'Pragmatic Interpretation & Workability',
        'style': 'Tests practical implementation of legal rules',
        'keywords': ['workable', 'practical', 'implementation', 'pragmatic']
    },
    'gorsuch': {
        'name': 'Justice Gorsuch',
        'focus': 'Textualism & Separation of Powers',
        'style': 'Strict adherence to statutory text and constitutional structure',
        'keywords': ['text', 'separation', 'powers', 'structure']
    },
    'kavanaugh': {
        'name': 'Justice Kavanaugh',
        'focus': 'Precedent & Moderate Application',
        'style': 'Weighs stare decisis carefully; seeks middle-ground',
        'keywords': ['precedent', 'stare decisis', 'moderate', 'reliance']
    },
    'barrett': {
        'name': 'Justice Barrett',
        'focus': 'Originalism & Doctrinal Clarity',
        'style': 'Precise doctrinal questions; historical analysis',
        'keywords': ['doctrine', 'original', 'historical', 'clarity']
    },
    'jackson': {
        'name': 'Justice Jackson',
        'focus': 'Historical Context & Equity',
        'style': 'Emphasizes historical background and fairness',
        'keywords': ['history', 'context', 'equity', 'purpose']
    }
}

# Precedent database (subset for demonstration)
PRECEDENTS = {
    'voting_rights': [
        {
            'case': 'Thornburg v. Gingles, 478 U.S. 30 (1986)',
            'url': 'https://supreme.justia.com/cases/federal/us/478/30/',
            'holding': 'Established Section 2 VRA preconditions for vote dilution claims',
            'keywords': ['vra', 'voting rights', 'section 2', 'dilution']
        },
        {
            'case': 'Shaw v. Reno, 509 U.S. 630 (1993)',
            'url': 'https://supreme.justia.com/cases/federal/us/509/630/',
            'holding': 'Racial gerrymandering violates Equal Protection',
            'keywords': ['gerrymandering', 'equal protection', 'race', 'redistricting']
        },
        {
            'case': 'Allen v. Milligan, 599 U.S. 1 (2023)',
            'url': 'https://supreme.justia.com/cases/federal/us/599/1/',
            'holding': 'Reaffirmed Gingles framework for Section 2 claims',
            'keywords': ['vra', 'gingles', 'section 2', 'alabama']
        }
    ],
    'equal_protection': [
        {
            'case': 'Miller v. Johnson, 515 U.S. 900 (1995)',
            'url': 'https://supreme.justia.com/cases/federal/us/515/900/',
            'holding': 'Race cannot predominate in redistricting without compelling justification',
            'keywords': ['race', 'predominate', 'strict scrutiny', 'redistricting']
        },
        {
            'case': 'Cooper v. Harris, 581 U.S. 285 (2017)',
            'url': 'https://supreme.justia.com/cases/federal/us/581/285/',
            'holding': 'Good-faith VRA compliance cannot save unnecessary racial sorting',
            'keywords': ['vra', 'racial sorting', 'narrow tailoring']
        }
    ],
    'first_amendment': [
        {
            'case': 'Reed v. Town of Gilbert, 576 U.S. 155 (2015)',
            'url': 'https://supreme.justia.com/cases/federal/us/576/155/',
            'holding': 'Content-based speech restrictions subject to strict scrutiny',
            'keywords': ['content', 'speech', 'strict scrutiny', 'signs']
        },
        {
            'case': 'New York Times Co. v. Sullivan, 376 U.S. 254 (1964)',
            'url': 'https://supreme.justia.com/cases/federal/us/376/254/',
            'holding': 'Actual malice standard for defamation of public figures',
            'keywords': ['defamation', 'malice', 'press', 'public figure']
        }
    ],
    'separation_of_powers': [
        {
            'case': 'Humphrey\'s Executor v. United States, 295 U.S. 602 (1935)',
            'url': 'https://supreme.justia.com/cases/federal/us/295/602/',
            'holding': 'Congress may limit presidential removal of certain officers',
            'keywords': ['removal', 'executive', 'independent agency']
        },
        {
            'case': 'Seila Law LLC v. CFPB, 591 U.S. ___ (2020)',
            'url': 'https://supreme.justia.com/cases/federal/us/591/19-7/',
            'holding': 'Single-director removal restrictions unconstitutional',
            'keywords': ['cfpb', 'removal', 'single director', 'unconstitutional']
        }
    ],
    'standing': [
        {
            'case': 'Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992)',
            'url': 'https://supreme.justia.com/cases/federal/us/504/555/',
            'holding': 'Article III standing requires injury, causation, redressability',
            'keywords': ['standing', 'injury', 'causation', 'redressability']
        },
        {
            'case': 'TransUnion LLC v. Ramirez, 594 U.S. ___ (2021)',
            'url': 'https://supreme.justia.com/cases/federal/us/594/20-297/',
            'holding': 'Statutory violations alone insufficient for Article III standing',
            'keywords': ['standing', 'statutory', 'concrete harm']
        }
    ]
}


# ========================================
# Routes
# ========================================

@app.route('/')
def serve_index():
    """Serve the main application"""
    return send_from_directory('.', 'index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_case():
    """
    Main analysis endpoint
    Accepts case text and returns full strategic analysis
    """
    data = request.json
    
    text = data.get('text', '')
    title = data.get('title', 'Untitled Case')
    posture = data.get('posture', 'auto')
    tier = data.get('tier', 'B')
    docket = data.get('docket', '')
    
    # Detect posture if auto
    if posture == 'auto':
        posture = detect_posture(text)
    
    # Classify input tier
    tier = classify_tier(text, docket)
    
    # Extract legal issues
    issues = extract_issues(text)
    
    # Find relevant precedents
    precedents = find_precedents(issues)
    
    # Generate risk assessment
    risk_assessment = assess_risk(text, issues, tier, posture)
    
    # Generate strategic traps
    traps = generate_traps(issues, posture)
    
    # Generate justice questions
    justice_questions = generate_justice_questions(issues, posture)
    
    # Build response
    response = {
        'title': title,
        'tier': tier,
        'posture': posture,
        'riskLevel': risk_assessment['level'],
        'digRisk': risk_assessment['dig_risk'],
        'primaryObstacle': risk_assessment['primary_obstacle'],
        'rewriteDirective': risk_assessment['rewrite_directive'],
        'precedents': precedents,
        'traps': traps,
        'risks': risk_assessment['risks'],
        'justiceQuestions': justice_questions,
        'issues': issues,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return jsonify(response)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle PDF upload and extract text
    """
    if not PDF_SUPPORT:
        return jsonify({'error': 'PDF support not available. Install PyPDF2.'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400
    
    try:
        # Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Extract text
        text = extract_pdf_text(filepath)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'filename': file.filename,
            'text': text,
            'length': len(text)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulate', methods=['POST'])
def simulate_justice():
    """
    Generate a simulated question from a specific Justice
    """
    data = request.json
    justice_id = data.get('justice', 'thomas')
    context = data.get('context', {})
    
    if justice_id not in JUSTICES:
        return jsonify({'error': 'Unknown justice'}), 400
    
    justice = JUSTICES[justice_id]
    issues = context.get('issues', {})
    posture = context.get('posture', 'cert')
    
    question = generate_single_question(justice_id, justice, issues, posture)
    
    return jsonify({
        'justice': justice_id,
        'name': justice['name'],
        'focus': justice['focus'],
        'question': question['question'],
        'pressure': question['pressure']
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle interactive chat follow-ups
    """
    data = request.json
    message = data.get('message', '')
    history = data.get('history', [])
    context = data.get('context', {})
    
    response = generate_chat_response(message, history, context)
    
    return jsonify({'response': response})


# ========================================
# Analysis Functions
# ========================================

def detect_posture(text: str) -> str:
    """Detect case posture from text content"""
    lower_text = text.lower()
    
    if 'petition for writ of certiorari' in lower_text or 'cert petition' in lower_text:
        return 'cert'
    if 'emergency application' in lower_text or 'stay pending' in lower_text:
        return 'emergency'
    if 'merits brief' in lower_text or 'brief for petitioner' in lower_text:
        return 'merits'
    if 'oral argument transcript' in lower_text:
        return 'backtest'
    
    return 'cert'


def classify_tier(text: str, docket: str) -> str:
    """Classify input tier based on available materials"""
    text_len = len(text)
    
    if text_len > 10000:
        return 'A'
    elif text_len > 1000 or text:
        return 'B'
    elif docket:
        return 'C'
    return 'C'


def extract_issues(text: str) -> dict:
    """Extract legal issues from case text"""
    lower_text = text.lower()
    
    issues = {
        'voting_rights': any(kw in lower_text for kw in ['voting rights', 'vra', 'section 2', 'vote dilution']),
        'equal_protection': any(kw in lower_text for kw in ['equal protection', '14th amendment', 'fourteenth amendment', 'discrimination']),
        'first_amendment': any(kw in lower_text for kw in ['first amendment', 'free speech', 'free exercise', 'establishment clause']),
        'separation_of_powers': any(kw in lower_text for kw in ['separation of powers', 'executive power', 'removal', 'nondelegation']),
        'standing': any(kw in lower_text for kw in ['standing', 'injury in fact', 'case or controversy', 'mootness']),
        'due_process': any(kw in lower_text for kw in ['due process', 'procedural', 'substantive due process']),
        'commerce_clause': any(kw in lower_text for kw in ['commerce clause', 'interstate commerce', 'dormant commerce']),
        'preemption': any(kw in lower_text for kw in ['preemption', 'supremacy clause', 'federal preemption'])
    }
    
    return issues


def find_precedents(issues: dict) -> list:
    """Find relevant precedents based on identified issues"""
    relevant = []
    
    for issue_name, is_present in issues.items():
        if is_present and issue_name in PRECEDENTS:
            for prec in PRECEDENTS[issue_name]:
                relevant.append({
                    'case': prec['case'],
                    'url': prec['url'],
                    'relevance': prec['holding'],
                    'risk': 'medium'  # Could be refined based on context
                })
    
    # Default precedents if none found
    if not relevant:
        relevant.append({
            'case': 'Marbury v. Madison, 5 U.S. 137 (1803)',
            'url': 'https://supreme.justia.com/cases/federal/us/5/137/',
            'relevance': 'Foundational judicial review authority',
            'risk': 'low'
        })
    
    return relevant[:6]  # Limit to 6 most relevant


def assess_risk(text: str, issues: dict, tier: str, posture: str) -> dict:
    """Generate comprehensive risk assessment"""
    
    # Determine overall risk level
    high_risk_issues = ['standing', 'separation_of_powers']
    has_high_risk = any(issues.get(issue) for issue in high_risk_issues)
    
    if tier == 'C':
        risk_level = 'CAUTION'
        primary_obstacle = 'Insufficient materials for complete analysis'
        rewrite = 'Upload full petition and lower court decision for comprehensive evaluation'
    elif has_high_risk:
        risk_level = 'CRITICAL'
        primary_obstacle = 'Potential jurisdictional or structural defect identified'
        rewrite = 'Address threshold issues before merits arguments'
    else:
        risk_level = 'CAUTION'
        primary_obstacle = 'Standard appellate risks present; vehicle quality uncertain'
        rewrite = 'Strengthen circuit split documentation and vehicle presentation'
    
    # Individual risk categories
    risks = [
        {
            'category': 'Vehicle Integrity',
            'level': 'low' if tier == 'A' else 'medium',
            'confidence': 'High' if tier == 'A' else 'Limited data'
        },
        {
            'category': 'Circuit Split Quality',
            'level': 'medium',
            'confidence': 'Requires external verification'
        },
        {
            'category': 'Preservation',
            'level': 'medium' if tier != 'A' else 'low',
            'confidence': 'Check full record'
        },
        {
            'category': 'Mootness Risk',
            'level': 'low' if posture != 'emergency' else 'high',
            'confidence': 'Based on posture'
        }
    ]
    
    # DIG risk
    dig_risk = 'Medium'
    if tier == 'C' or issues.get('standing'):
        dig_risk = 'High'
    elif tier == 'A' and not has_high_risk:
        dig_risk = 'Low'
    
    return {
        'level': risk_level,
        'dig_risk': dig_risk,
        'primary_obstacle': primary_obstacle,
        'rewrite_directive': rewrite,
        'risks': risks
    }


def generate_traps(issues: dict, posture: str) -> list:
    """Generate strategic traps and counters"""
    traps = []
    
    if issues.get('standing'):
        traps.append({
            'type': 'trap',
            'text': 'Addressing merits extensively while leaving standing vulnerable to attack'
        })
        traps.append({
            'type': 'counter',
            'text': 'Lead with concrete, particularized injury demonstration before reaching merits'
        })
    
    if issues.get('voting_rights') and issues.get('equal_protection'):
        traps.append({
            'type': 'trap',
            'text': 'Conceding that race "predominated" while relying solely on VRA compliance as compelling interest'
        })
        traps.append({
            'type': 'counter',
            'text': 'Contest predomination finding; argue traditional redistricting criteria drove map design'
        })
    
    # Default traps
    if len(traps) < 2:
        traps.extend([
            {
                'type': 'trap',
                'text': 'Over-relying on circuit split without demonstrating conflict maturity'
            },
            {
                'type': 'counter',
                'text': 'Document specific contradictory holdings with parallel fact patterns'
            }
        ])
    
    return traps[:4]  # Limit to 4


def generate_justice_questions(issues: dict, posture: str) -> list:
    """Generate simulated questions from selected Justices"""
    questions = []
    
    # Select 4 Justices with distinct analytical approaches
    selected_justices = ['thomas', 'kagan', 'barrett', 'jackson']
    
    for justice_id in selected_justices:
        justice = JUSTICES[justice_id]
        q = generate_single_question(justice_id, justice, issues, posture)
        questions.append(q)
    
    return questions


def generate_single_question(justice_id: str, justice: dict, issues: dict, posture: str) -> dict:
    """Generate a single Justice's question based on context"""
    
    question_templates = {
        'thomas': {
            'voting_rights': 'Where in the constitutional text does Congress derive authority to mandate race-conscious districting? Isn\'t Section 2 of the VRA itself constitutionally suspect under the original public meaning of the Fifteenth Amendment?',
            'separation_of_powers': 'What is the original understanding of "executive Power" in Article II? Doesn\'t the removal restriction here conflict with the Constitution\'s vesting of that power in the President?',
            'default': 'What is the original public meaning of the constitutional provision at issue, and how does that constrain our analysis?'
        },
        'kagan': {
            'voting_rights': 'If we rule for you, what exactly should states do when facing a Section 2 violation? Must they wait for contempt before drawing remedial maps?',
            'standing': 'Walk me through how your proposed standing rule would work in practice. What cases does it let in, and what does it keep out?',
            'default': 'Give me a workable test. How would lower courts actually apply this standard?'
        },
        'barrett': {
            'voting_rights': 'Does VRA compliance automatically constitute a compelling interest, or must we engage in additional balancing? What\'s the doctrinal framework?',
            'first_amendment': 'What level of scrutiny applies here, and what\'s the precise test? I want clean doctrine.',
            'default': 'Help me understand the doctrinal rule you want us to announce and how it fits existing precedent.'
        },
        'jackson': {
            'voting_rights': 'Given the specific history of voter disenfranchisement in this jurisdiction, isn\'t there something dissonant about using Equal Protection to prevent majority-Black districts?',
            'equal_protection': 'What historical context should inform our interpretation? How does the purpose behind this provision guide us?',
            'default': 'What historical background are we overlooking that should inform our reading here?'
        },
        'roberts': {
            'default': 'Is there a narrow way to decide this case without reaching the broader constitutional question you\'re pressing?'
        },
        'alito': {
            'default': 'What are the real-world consequences of your proposed rule? Who wins and who loses?'
        },
        'sotomayor': {
            'default': 'How does your position affect ordinary people? Have you considered the on-the-ground impact?'
        },
        'gorsuch': {
            'default': 'Point me to the statutory text. Where are the words that support your reading?'
        },
        'kavanaugh': {
            'default': 'What about stare decisis? What reliance interests would we disrupt by ruling your way?'
        }
    }
    
    # Find appropriate question
    templates = question_templates.get(justice_id, {'default': 'How do you respond to the strongest version of your opponent\'s argument?'})
    
    question_text = templates.get('default', '')
    for issue, is_present in issues.items():
        if is_present and issue in templates:
            question_text = templates[issue]
            break
    
    # Pressure description
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
    
    return {
        'justice': justice_id,
        'name': justice['name'],
        'focus': justice['focus'],
        'question': question_text,
        'pressure': pressures.get(justice_id, 'Tests the logical limits of the argument')
    }


def generate_chat_response(message: str, history: list, context: dict) -> str:
    """Generate contextual chat response"""
    lower_message = message.lower()
    
    if 'what if' in lower_message or 'hypothetical' in lower_message:
        return '''**Hypothetical Analysis Framework**

To evaluate alternative scenarios, I assess:

1. **Vehicle Impact** — How do changed facts affect jurisdictional posture?
2. **Standard Shift** — Does the legal test apply differently?
3. **Justice Alignment** — Which Justices become more/less sympathetic?

Specify which aspect you'd like to modify for targeted analysis.'''
    
    if 'rewrite' in lower_message or 'question presented' in lower_message:
        return '''**Questions Presented: Strategic Drafting**

Key principles:

1. **Front-load winning facts** — Your best facts should appear in the question itself
2. **Signal favorable review** — Frame to invoke your preferred precedent
3. **Avoid over-breadth** — Narrow questions have higher grant rates
4. **Create asymmetry** — Make "yes" easier than opponent's "no"

Want me to draft alternative framings based on current case posture?'''
    
    if 'circuit split' in lower_message or 'conflict' in lower_message:
        return '''**Circuit Split Analysis**

The Court evaluates split quality on:

1. **Directness** — Same legal question, opposite holdings
2. **Maturity** — Sufficient percolation across circuits
3. **Importance** — Substantial federal interests affected
4. **Vehicle** — Can this case cleanly resolve the split?

Shallow or manufactured splits dramatically increase DIG risk.'''
    
    if 'standing' in lower_message or 'jurisdiction' in lower_message:
        return '''**Jurisdictional Checklist**

Standing/jurisdiction defects are **dispositive**:

• **Article III Standing**: injury-in-fact, causation, redressability  
• **Statutory Exhaustion**: all administrative steps completed?  
• **Finality**: lower court judgment truly final?  
• **Mootness**: can Court grant effective relief?

Any weakness here must be addressed before cert, not at merits.'''
    
    # Default response
    tier = context.get('tier', 'B')
    posture = context.get('posture', 'cert')
    
    return f'''That's worth examining. Based on current analysis:

• **Input Tier {tier}** limits definitive conclusions on some procedural aspects
• **{posture.title()} posture** emphasizes particular institutional concerns

For more specific guidance, clarify:
1. Which party's perspective are you analyzing?
2. What specific doctrinal or strategic concern to probe?'''


def extract_pdf_text(filepath: str) -> str:
    """Extract text content from PDF file"""
    if not PDF_SUPPORT:
        return ""
    
    text = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return text.strip()


# ========================================
# Main Entry Point
# ========================================

if __name__ == '__main__':
    print("=" * 50)
    print("SCOTUS Strategic Engine - Backend Server")
    print("=" * 50)
    print(f"PDF Support: {'Enabled' if PDF_SUPPORT else 'Disabled (install PyPDF2)'}")
    print("Starting server on http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
