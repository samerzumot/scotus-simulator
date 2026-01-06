/**
 * SCOTUS Strategic Engine - Frontend Application
 * Adversarial appellate-strategy system for Supreme Court practitioners
 */

// ========================================
// Configuration & State
// ========================================

const API_BASE = 'http://localhost:5000/api';

const AppState = {
    currentAnalysis: null,
    currentCaseId: null,
    inputTier: null,
    posture: null,
    selectedJustice: null,
    chatHistory: [],
    uploadedFiles: []
};

// Justice profiles for simulation
const JUSTICES = {
    roberts: {
        name: 'Chief Justice Roberts',
        focus: 'Institutionalism & Narrow Rulings',
        style: 'Seeks incremental, consensus-building decisions'
    },
    thomas: {
        name: 'Justice Thomas',
        focus: 'Originalism & Constitutional Text',
        style: 'Questions structural precedents; emphasizes original meaning'
    },
    alito: {
        name: 'Justice Alito',
        focus: 'Textual Analysis & Practical Consequences',
        style: 'Probes real-world impacts and statutory interpretation'
    },
    sotomayor: {
        name: 'Justice Sotomayor',
        focus: 'Civil Rights & Practical Impact',
        style: 'Focuses on effects on marginalized communities'
    },
    kagan: {
        name: 'Justice Kagan',
        focus: 'Pragmatic Interpretation & Workability',
        style: 'Tests practical implementation of legal rules'
    },
    gorsuch: {
        name: 'Justice Gorsuch',
        focus: 'Textualism & Separation of Powers',
        style: 'Strict adherence to statutory text and constitutional structure'
    },
    kavanaugh: {
        name: 'Justice Kavanaugh',
        focus: 'Precedent & Moderate Application',
        style: 'Weighs stare decisis carefully; seeks middle-ground'
    },
    barrett: {
        name: 'Justice Barrett',
        focus: 'Originalism & Doctrinal Clarity',
        style: 'Precise doctrinal questions; historical analysis'
    },
    jackson: {
        name: 'Justice Jackson',
        focus: 'Historical Context & Equity',
        style: 'Emphasizes historical background and fairness'
    }
};

// Sample cases for quick start
const SAMPLE_CASES = {
    'louisiana': {
        title: 'Louisiana v. Callais',
        docket: '24-109',
        posture: 'merits',
        text: `PETITION FOR WRIT OF CERTIORARI

Louisiana v. Callais (consolidated with Robinson v. Callais)
No. 24-109, No. 24-110
Supreme Court of the United States

QUESTIONS PRESENTED

1. Whether the intentional creation of a second majority-minority congressional district to remedy a likely Voting Rights Act violation violates the Fourteenth or Fifteenth Amendments to the United States Constitution.

2. Whether the district court erred in finding that race predominated in the Louisiana legislature's enactment of SB 8, the challenged redistricting plan.

3. Whether the district court erred in finding that SB 8 fails strict scrutiny.

4. Whether the district court erred in subjecting SB 8 to the preconditions specified in Thornburg v. Gingles, 478 U.S. 30 (1986).

STATEMENT OF THE CASE

Following the 2020 Census, Louisiana redrew its congressional districts. Black voters constitute approximately one-third of Louisiana's population. The initial 2022 map created only one majority-Black congressional district out of six total seats.

Civil rights organizations and Black voters challenged the map under Section 2 of the Voting Rights Act, alleging vote dilution. The district court found a likely Section 2 violation and ordered Louisiana to create a remedial map with a second majority-Black district.

In January 2024, Louisiana enacted SB 8, creating two majority-Black congressional districts (Districts 2 and 6). Non-African American voters (the Callais plaintiffs) then challenged SB 8 as unconstitutional racial gerrymandering under Shaw v. Reno, 509 U.S. 630 (1993), and Miller v. Johnson, 515 U.S. 900 (1995).

A three-judge district court struck down SB 8, finding that race was the predominant factor in drawing the new districts and that the State failed to demonstrate a compelling interest because it had not proven an actual Section 2 violation.

ARGUMENT

The core tension in this case is between compliance with the Voting Rights Act and the Equal Protection Clause's prohibition on racial gerrymandering. Under Shaw v. Reno and its progeny, race-conscious redistricting triggers strict scrutiny. The State argues compliance with Section 2 of the VRA constitutes a compelling governmental interest.

However, as this Court held in Cooper v. Harris, 581 U.S. 285 (2017), even good-faith efforts to comply with the VRA cannot justify racial sorting if a race-neutral alternative would suffice. The question is whether preemptive VRA compliance—before a final adjudication of liability—can ever satisfy strict scrutiny.

This case also implicates the ongoing vitality of Thornburg v. Gingles and the relationship between Allen v. Milligan, 599 U.S. 1 (2023), which reaffirmed the Gingles framework, and constitutional limits on race-conscious remedies.

CONCLUSION

The judgment of the district court should be reversed.`
    },
    'trump-tariffs': {
        title: 'Trump v. V.O.S. Selections',
        docket: '24-892',
        posture: 'merits',
        text: `PETITION FOR WRIT OF CERTIORARI

Trump v. V.O.S. Selections, Inc. (consolidated with Learning Resources v. Trump)
No. 24-892
Supreme Court of the United States

QUESTIONS PRESENTED

1. Whether the International Emergency Economic Powers Act (IEEPA) of 1977, 50 U.S.C. § 1701 et seq., authorizes the President to impose tariffs on imported goods.

2. If IEEPA authorizes presidential tariffs, whether such delegation of taxing authority violates the nondelegation doctrine under Article I, Section 8 of the Constitution.

STATEMENT OF THE CASE

In 2025, President Trump invoked the International Emergency Economic Powers Act to declare a national emergency based on the United States trade deficit with various nations. Pursuant to this declaration, the President imposed sweeping tariffs on imported goods from multiple countries, including tariffs ranging from 10% to 145% on products from China, the European Union, and other trading partners.

Multiple importers challenged the tariffs, arguing that IEEPA does not authorize the President to impose tariffs—a power constitutionally vested in Congress under the Import-Export Clause and the Taxing Power. The challengers also argued that even if IEEPA could be read to permit tariffs, such a broad delegation of Congress's taxing authority would violate the nondelegation doctrine.

The district court granted a preliminary injunction. The Court of Appeals for the Federal Circuit affirmed, holding that IEEPA's grant of authority to "regulate" commerce does not encompass the power to impose tariffs, which are taxes historically requiring explicit congressional authorization.

ARGUMENT

I. IEEPA's Text Does Not Authorize Tariffs

IEEPA authorizes the President, upon declaring a national emergency, to "regulate" and "prohibit" various transactions. 50 U.S.C. § 1702(a)(1)(B). However, tariffs are not mere regulations—they are taxes imposed on imports. The Constitution explicitly grants Congress the power "To lay and collect Taxes, Duties, Imposts and Excises." U.S. Const. art. I, § 8, cl. 1.

As this Court explained in Youngstown Sheet & Tube Co. v. Sawyer, 343 U.S. 579 (1952), presidential power must derive from an act of Congress or the Constitution itself. No statute has ever been understood to delegate wholesale tariff authority to the Executive.

II. If IEEPA Authorizes Tariffs, It Violates the Nondelegation Doctrine

Even if IEEPA could be construed to authorize tariffs, such a delegation would lack the "intelligible principle" required under the nondelegation doctrine. See Gundy v. United States, 139 S. Ct. 2116 (2019). The power to tax imports at any rate, on any goods, from any country, based solely on a presidential emergency declaration, would represent the most sweeping delegation of legislative authority in American history.

CONCLUSION

The judgment of the Court of Appeals should be affirmed.`
    },
    'ftc-removal': {
        title: 'Trump v. Slaughter',
        docket: '24-631',
        posture: 'merits',
        text: `PETITION FOR WRIT OF CERTIORARI

Trump v. Slaughter
No. 24-631
Supreme Court of the United States

QUESTIONS PRESENTED

1. Whether the statutory removal protections for members of the Federal Trade Commission, which permit removal only for "inefficiency, neglect of duty, or malfeasance in office," violate the separation of powers.

2. Whether Humphrey's Executor v. United States, 295 U.S. 602 (1935), should be overruled or limited to permit presidential removal of FTC commissioners at will.

STATEMENT OF THE CASE

The Federal Trade Commission Act provides that FTC commissioners may be removed by the President only for "inefficiency, neglect of duty, or malfeasance in office." 15 U.S.C. § 41. This for-cause removal protection was upheld in Humphrey's Executor v. United States, 295 U.S. 602 (1935).

In 2025, President Trump dismissed two FTC commissioners, citing policy disagreements over antitrust enforcement priorities. The dismissed commissioners filed suit, arguing their removal violated the statutory for-cause protection.

The district court granted injunctive relief, reinstating the commissioners. The Court of Appeals for the D.C. Circuit affirmed, holding that Humphrey's Executor remains binding precedent and that the FTC's multi-member, bipartisan structure distinguishes it from the single-director agencies addressed in Seila Law LLC v. CFPB, 591 U.S. ___ (2020).

ARGUMENT

I. The Unitary Executive Requires At-Will Removal

Article II vests "the executive Power" in the President alone. U.S. Const. art. II, § 1. This Court has repeatedly affirmed that the President must have control over those who exercise executive power. See Myers v. United States, 272 U.S. 52 (1926); Seila Law LLC v. CFPB, 591 U.S. ___ (2020).

Humphrey's Executor carved out an exception for "quasi-legislative" and "quasi-judicial" agencies. But this Court has since rejected the premise that Article II permits congressional creation of a "headless fourth branch." Free Enterprise Fund v. PCAOB, 561 U.S. 477, 483 (2010).

II. Humphrey's Executor Should Be Overruled

Humphrey's Executor rested on distinctions between "purely executive" officers and those exercising "quasi-legislative" functions—distinctions this Court has since questioned. See Morrison v. Olson, 487 U.S. 654 (1988) (Scalia, J., dissenting). Modern separation-of-powers analysis focuses on whether removal restrictions "impede the President's ability to perform his constitutional duty." Seila Law, 591 U.S. at ___.

The FTC exercises substantial executive power, including enforcement discretion in antitrust and consumer protection matters. Shielding commissioners from presidential control undermines democratic accountability for federal policy.

III. Multi-Member Structure Does Not Save Humphrey's Executor

Respondents argue that the FTC's multi-member structure provides sufficient accountability. But the constitutional infirmity lies in removal restrictions, not headcount. A multi-member body with for-cause protection is constitutionally indistinguishable from a single director with identical protections.

CONCLUSION

The judgment of the Court of Appeals should be reversed, and Humphrey's Executor should be overruled.`
    },
    'williams-reed': {
        title: 'Williams v. Reed',
        docket: '23-191',
        posture: 'merits',
        text: `PETITION FOR WRIT OF CERTIORARI

Williams v. Reed
No. 23-191
Supreme Court of the United States

QUESTIONS PRESENTED

Whether exhaustion of state administrative remedies is required to bring claims under 42 U.S.C. § 1983 in state court.

STATEMENT OF THE CASE

Petitioners are unemployed workers in Alabama who experienced significant delays in the processing of their unemployment benefits claims. They filed suit in state court under 42 U.S.C. § 1983, alleging that the Alabama Department of Labor's delays violated their due process rights.

The Secretary of Labor moved to dismiss, arguing that the claimants failed to satisfy Alabama's administrative-exhaustion requirement. The Alabama Supreme Court affirmed the dismissal, holding that § 1983 does not preempt state exhaustion requirements.

This created a "catch-22" for the petitioners: they could not sue to expedite the administrative process without first completing the very process that was being unlawfully delayed.

ARGUMENT

I. Section 1983 Does Not Require Exhaustion

As this Court established in Patsy v. Board of Regents of Florida (1982), "exhaustion of state administrative remedies is not a prerequisite to an action under § 1983." This rule applies equally in state and federal courts. States cannot impose additional procedural hurdles that nullify federal rights.

II. State Rules Cannot Immunize Federal Violations

Under Felder v. Casey (1988), a state law that immunizes government conduct otherwise subject to suit under § 1983 is preempted by federal law. Alabama's exhaustion requirement effectively immunizes state officials from § 1983 claims challenging administrative delays.

CONCLUSION

The judgment of the Supreme Court of Alabama should be reversed.`
    }
};


// ========================================
// DOM Elements
// ========================================

const elements = {
    // Buttons
    uploadCaseBtn: document.getElementById('uploadCaseBtn'),
    newAnalysisBtn: document.getElementById('newAnalysisBtn'),
    welcomeUploadBtn: document.getElementById('welcomeUploadBtn'),
    pasteTextBtn: document.getElementById('pasteTextBtn'),
    fullBenchBtn: document.getElementById('fullBenchBtn'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    cancelBtn: document.getElementById('cancelBtn'),
    closeModalBtn: document.getElementById('closeModalBtn'),
    browseBtn: document.getElementById('browseBtn'),
    sendChatBtn: document.getElementById('sendChatBtn'),
    minimizeChatBtn: document.getElementById('minimizeChatBtn'),

    // Panels
    welcomeState: document.getElementById('welcomeState'),
    analysisResults: document.getElementById('analysisResults'),
    chatPanel: document.getElementById('chatPanel'),

    // Modal
    uploadModal: document.getElementById('uploadModal'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingStatus: document.getElementById('loadingStatus'),

    // Dashboard Metrics
    inputTier: document.getElementById('inputTier'),
    posture: document.getElementById('posture'),
    riskLevel: document.getElementById('riskLevel'),
    digRisk: document.getElementById('digRisk'),
    primaryObstacle: document.getElementById('primaryObstacle'),
    rewriteDirective: document.getElementById('rewriteDirective'),

    // Form Elements
    caseTitle: document.getElementById('caseTitle'),
    caseText: document.getElementById('caseText'),
    postureSel: document.getElementById('postureSel'),
    docketNumber: document.getElementById('docketNumber'),
    fileInput: document.getElementById('fileInput'),
    uploadZone: document.getElementById('uploadZone'),
    uploadedFiles: document.getElementById('uploadedFiles'),
    filesList: document.getElementById('filesList'),

    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    pasteTab: document.getElementById('pasteTab'),
    uploadTab: document.getElementById('uploadTab'),
    docketTab: document.getElementById('docketTab'),

    // Results
    precedentList: document.getElementById('precedentList'),
    trapsList: document.getElementById('trapsList'),
    riskTable: document.getElementById('riskTable'),
    justiceQuestions: document.getElementById('justiceQuestions'),
    justiceGrid: document.getElementById('justiceGrid'),

    // Chat
    chatMessages: document.getElementById('chatMessages'),
    chatInput: document.getElementById('chatInput'),
    chatToggleBtn: document.getElementById('chatToggleBtn'),

    // Brief Viewer
    briefViewer: document.getElementById('briefViewer'),
    briefTitle: document.getElementById('briefTitle'),
    briefContent: document.getElementById('briefContent'),
    briefContentWrapper: document.getElementById('briefContentWrapper'),
    briefAnnotations: document.getElementById('briefAnnotations'),
    annotationList: document.getElementById('annotationList'),
    toggleEditBtn: document.getElementById('toggleEditBtn'),
    collapseBriefBtn: document.getElementById('collapseBriefBtn')
};

// ========================================
// Event Listeners
// ========================================

function initializeEventListeners() {
    // Modal triggers
    elements.uploadCaseBtn.addEventListener('click', openModal);
    elements.welcomeUploadBtn.addEventListener('click', openModal);
    elements.pasteTextBtn.addEventListener('click', () => {
        openModal();
        switchTab('paste');
    });
    elements.closeModalBtn.addEventListener('click', closeModal);
    elements.cancelBtn.addEventListener('click', closeModal);

    // New Analysis
    elements.newAnalysisBtn.addEventListener('click', resetAnalysis);

    // Tab switching
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // File upload
    elements.browseBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    elements.uploadZone.addEventListener('dragover', handleDragOver);
    elements.uploadZone.addEventListener('dragleave', handleDragLeave);
    elements.uploadZone.addEventListener('drop', handleDrop);

    // Analysis trigger
    elements.analyzeBtn.addEventListener('click', startAnalysis);

    // Justice simulation
    document.querySelectorAll('.justice-btn').forEach(btn => {
        btn.addEventListener('click', () => simulateJustice(btn.dataset.justice));
    });
    elements.fullBenchBtn.addEventListener('click', simulateFullBench);

    // Chat
    elements.sendChatBtn.addEventListener('click', sendChatMessage);
    elements.chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
    elements.minimizeChatBtn.addEventListener('click', toggleChat);
    elements.chatToggleBtn.addEventListener('click', toggleChat);

    // Close modal on backdrop click
    elements.uploadModal.addEventListener('click', (e) => {
        if (e.target === elements.uploadModal) closeModal();
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

    // Sample case cards
    document.querySelectorAll('.sample-case-card').forEach(card => {
        card.addEventListener('click', () => loadSampleCase(card.dataset.case));
    });

    // Brief viewer actions
    elements.toggleEditBtn.addEventListener('click', toggleEditMode);
    elements.collapseBriefBtn.addEventListener('click', toggleBriefCollapse);
}

// ========================================
// Sample Case Loading
// ========================================

function loadSampleCase(caseId) {
    const sampleCase = SAMPLE_CASES[caseId];
    if (!sampleCase) return;

    AppState.currentCaseId = caseId;

    // Populate form fields
    elements.caseTitle.value = sampleCase.title;
    elements.caseText.value = sampleCase.text;
    elements.postureSel.value = sampleCase.posture;
    elements.docketNumber.value = sampleCase.docket;

    // Start analysis directly
    showLoading(`Loading ${sampleCase.title}...`);

    // Run analysis with slight delay for UX
    setTimeout(async () => {
        try {
            const inputTier = classifyInputTier(sampleCase.text, [], sampleCase.docket);
            AppState.inputTier = inputTier;

            updateLoadingStatus('Analyzing precedent architecture...');
            await delay(600);

            const analysis = await generateAnalysis({
                text: sampleCase.text,
                title: sampleCase.title,
                posture: sampleCase.posture,
                tier: inputTier,
                docket: sampleCase.docket
            });

            AppState.currentAnalysis = analysis;
            AppState.posture = sampleCase.posture;

            updateLoadingStatus('Simulating judicial pressure points...');
            await delay(500);

            renderAnalysisResults(analysis);
            hideLoading();

        } catch (error) {
            console.error('Sample case analysis error:', error);
            hideLoading();
            alert('Failed to analyze sample case. Please try again.');
        }
    }, 300);
}

// ========================================
// Brief Viewer & Annotation Logic
// ========================================

const BRIEF_STATE = {
    isEditing: false,
    isCollapsed: false,
    segments: [],
    selectedSegmentId: null
};

// Feedback data for sample cases
const CASE_FEEDBACK = {
    'louisiana': [
        {
            pattern: /intentional creation of a second majority-minority congressional district/i,
            justice: 'thomas',
            type: 'concern',
            text: 'This framing explicitly admits to racial predominence. Justice Thomas will view this as a per se violation of the 14th Amendment regardless of VRA compliance.',
            rewrite: 'the creation of a district that adheres to traditional districting principles while respecting the voting strength of minority communities as required by federal law.'
        },
        {
            pattern: /compliance with the Voting Rights Act constitutes a compelling governmental interest/i,
            justice: 'barrett',
            type: 'caution',
            text: 'Justice Barrett has questioned whether statutory compliance can ever be a "compelling interest" in the constitutional sense without more specific evidence.',
            rewrite: 'the state\'s specific interest in remedying documented, localized vote dilution that would otherwise trigger liability under Section 2.'
        }
    ],
    'trump-tariffs': [
        {
            pattern: /authorizes presidential tariffs and whether such authority violates the nondelegation doctrine/i,
            justice: 'gorsuch',
            type: 'caution',
            text: 'Justice Gorsuch is a leading proponent of revitalizing the nondelegation doctrine. Use this framing to appeal to his concerns about administrative overreach.',
            rewrite: 'the transfer of the core legislative power to tax imports to the Executive without any clear, intelligible principle from Congress.'
        },
        {
            pattern: /Youngstown Sheet & Tube Co. v. Sawyer, 343 U.S. 579 \(1952\)/i,
            justice: 'kavanaugh',
            type: 'strength',
            text: 'Invoking Youngstown Category 3 is a powerful argument here. Justice Kavanaugh frequently cites Jackson\'s tripartite framework to analyze executive power.',
            rewrite: 'the classic Youngstown framework, where presidential power is at its lowest ebb because it is incompatible with the expressed will of Congress.'
        },
        {
            pattern: /Import-Export Clause and the Taxing Power/i,
            justice: 'alito',
            type: 'caution',
            text: 'Justice Alito will want to see a rigorous textual analysis of whether the power to "regulate" under IEEPA can ever encompass the sovereign power to tax.',
            rewrite: 'the fundamental constitutional distinction between the power to regulate commerce and the exclusive congressional power to lay and collect taxes.'
        }
    ],
    'ftc-removal': [
        {
            pattern: /statutory removal protections for members of the Federal Trade Commission/i,
            justice: 'roberts',
            type: 'caution',
            text: 'Chief Justice Roberts often seeks narrow rulings. He might prefer a decision that limits the FTC\'s power through statutory interpretation rather than a broad constitutional strike on removal protections.',
            rewrite: 'the scope of executive supervisory authority over the Federal Trade Commission\'s enforcement functions.'
        },
        {
            pattern: /Humphrey's Executor v. United States, 295 U.S. 602 \(1935\), should be overruled/i,
            justice: 'alito',
            type: 'concern',
            text: 'Justice Alito has expressed skepticism about "headless" agencies. However, he will be highly focused on the practical consequences of overruling such a long-standing precedent.',
            rewrite: 'the constitutional limits of Humphrey\'s Executor as applied to modern agencies exercising substantial executive power.'
        },
        {
            pattern: /headless fourth branch/i,
            justice: 'gorsuch',
            type: 'strength',
            text: 'This is a strong rhetorical point that resonates with Justice Gorsuch\'s structural constitutionalism. Emphasize that the Constitution provides for only three branches.',
            rewrite: 'an independent agency exercising core executive power outside of the President\'s control.'
        }
    ],
    'williams-reed': [
        {
            pattern: /exhaustion of state administrative remedies is not a prerequisite to an action under § 1983/i,
            justice: 'kavanaugh',
            type: 'strength',
            text: 'Justice Kavanaugh authored the majority opinion here, focusing on the "catch-22" nature of the state rule. Use this to emphasize the practical impossibility of compliance.',
            rewrite: 'the settled rule that § 1983 provides an immediate federal remedy that states cannot obstruct with exhaustion requirements.'
        },
        {
            pattern: /catch-22/i,
            justice: 'kagan',
            type: 'strength',
            text: 'Justice Kagan frequently uses common-sense terminology to highlight logical fallacies in legal arguments. This framing is highly effective for the liberal wing.',
            rewrite: 'an inescapable procedural trap that renders constitutional rights illusory.'
        },
        {
            pattern: /state law that immunizes government conduct/i,
            justice: 'thomas',
            type: 'caution',
            text: 'Justice Thomas dissented, expressing concern about overreading Felder v. Casey. Avoid broad "preemption" claims that might infringe on state court\'s jurisdictional authority.',
            rewrite: 'the specific conflict between Alabama\'s procedural rule and the remedial purpose of the federal civil rights statute.'
        }
    ]
};

function renderBrief(text, caseId = null) {
    if (!text) return;

    BRIEF_STATE.segments = [];
    const container = elements.briefContent;
    container.innerHTML = '';

    // Simple segmentation by lines/sentences
    const sections = text.split('\n\n');

    sections.forEach((section, sIdx) => {
        const sectionEl = document.createElement('div');

        // Detect if it's a title/header
        if (section.toUpperCase() === section && section.length < 100) {
            sectionEl.className = 'section-title';
            sectionEl.textContent = section;
        } else {
            // Split into segments by sentence/keyword for feedback
            const feedbackItems = caseId ? (CASE_FEEDBACK[caseId] || []) : [];
            let processedText = section;

            feedbackItems.forEach((item, fIdx) => {
                const id = `seg-${sIdx}-${fIdx}`;
                const match = processedText.match(item.pattern);

                if (match) {
                    BRIEF_STATE.segments.push({
                        id,
                        original: match[0],
                        feedback: item
                    });

                    const span = `<span class="brief-segment has-feedback ${item.type}" data-id="${id}">${match[0]}</span>`;
                    processedText = processedText.replace(item.pattern, span);
                }
            });

            sectionEl.innerHTML = processedText;
        }

        container.appendChild(sectionEl);
    });

    // Add click listeners to segments
    document.querySelectorAll('.brief-segment').forEach(seg => {
        seg.addEventListener('click', (e) => onSegmentClick(e));
    });

    // Show the viewer
    elements.briefViewer.classList.remove('hidden');
    elements.briefTitle.textContent = elements.caseTitle.value || 'Case Brief';
}

function onSegmentClick(e) {
    if (BRIEF_STATE.isEditing) return;

    const segId = e.target.dataset.id;
    const segment = BRIEF_STATE.segments.find(s => s.id === segId);

    if (!segment) return;

    // Highlight segment
    document.querySelectorAll('.brief-segment').forEach(s => s.classList.remove('highlighted'));
    e.target.classList.add('highlighted');

    BRIEF_STATE.selectedSegmentId = segId;
    showSegmentFeedback(segment);
}

function showSegmentFeedback(segment) {
    const { feedback } = segment;
    const justice = JUSTICES[feedback.justice];

    elements.annotationList.innerHTML = `
        <div class="annotation-card ${feedback.type}">
            <div class="annotation-justice">
                <span class="annotation-justice-name">${justice.name}</span>
                <span class="annotation-type ${feedback.type}">${feedback.type}</span>
            </div>
            <p class="annotation-text">${feedback.text}</p>
            <div class="annotation-rewrite">
                <span class="annotation-rewrite-label">Adversarial Rewrite</span>
                <p class="annotation-rewrite-text">"...${feedback.rewrite}..."</p>
                <button class="btn btn-primary btn-small apply-rewrite-btn" onclick="applyRewrite('${segment.id}')">
                    Apply Edit
                </button>
            </div>
        </div>
    `;

    // Clear hint
    const hint = document.querySelector('.annotation-hint');
    if (hint) hint.style.display = 'none';
}

window.applyRewrite = function (segmentId) {
    const segment = BRIEF_STATE.segments.find(s => s.id === segmentId);
    if (!segment) return;

    const segEl = document.querySelector(`.brief-segment[data-id="${segmentId}"]`);
    if (!segEl) return;

    // Replace in UI
    segEl.textContent = segment.feedback.rewrite;
    segEl.classList.remove('has-feedback', 'critical', 'caution', 'positive');
    segEl.classList.add('positive');

    // Update underlying text in AppState if needed
    // (In a real app, we'd update elements.caseText.value)

    // Show success in chat
    addChatMessage('assistant', `Applied strategic rewrite for: "${segment.original.substring(0, 30)}..."\n\nNew phrasing focuses on: **${segment.feedback.rewrite.substring(0, 50)}...**`);

    // Clear annotations
    elements.annotationList.innerHTML = '';
    const hint = document.querySelector('.annotation-hint');
    if (hint) hint.style.display = 'block';
};

function toggleEditMode() {
    BRIEF_STATE.isEditing = !BRIEF_STATE.isEditing;
    const content = elements.briefContent;

    if (BRIEF_STATE.isEditing) {
        content.contentEditable = 'true';
        content.classList.add('editing');
        elements.toggleEditBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;">
                <polyline points="20 6 9 17 4 12"/>
            </svg>
            Save
        `;
        content.focus();
    } else {
        content.contentEditable = 'false';
        content.classList.remove('editing');
        elements.toggleEditBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            Edit
        `;
        // Sync back to hidden input if needed
        elements.caseText.value = content.innerText;
    }
}

function toggleBriefCollapse() {
    BRIEF_STATE.isCollapsed = !BRIEF_STATE.isCollapsed;
    elements.briefContentWrapper.classList.toggle('collapsed');
    elements.collapseBriefBtn.style.transform = BRIEF_STATE.isCollapsed ? 'rotate(180deg)' : '';
}


// ========================================
// Modal Functions
// ========================================

function openModal() {
    elements.uploadModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    elements.uploadModal.classList.add('hidden');
    document.body.style.overflow = '';
}

function switchTab(tabName) {
    // Update tab buttons
    elements.tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update tab content
    elements.pasteTab.classList.toggle('hidden', tabName !== 'paste');
    elements.uploadTab.classList.toggle('hidden', tabName !== 'upload');
    elements.docketTab.classList.toggle('hidden', tabName !== 'docket');
}

// ========================================
// File Handling
// ========================================

function handleDragOver(e) {
    e.preventDefault();
    elements.uploadZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');

    const files = Array.from(e.dataTransfer.files).filter(f => f.type === 'application/pdf');
    if (files.length > 0) {
        addFiles(files);
    }
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
        addFiles(files);
    }
}

function addFiles(files) {
    AppState.uploadedFiles = [...AppState.uploadedFiles, ...files];
    updateFilesList();
}

function updateFilesList() {
    if (AppState.uploadedFiles.length === 0) {
        elements.uploadedFiles.classList.add('hidden');
        return;
    }

    elements.uploadedFiles.classList.remove('hidden');
    elements.filesList.innerHTML = AppState.uploadedFiles.map((file, i) => `
        <li>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
            </svg>
            ${file.name}
            <button onclick="removeFile(${i})" style="margin-left:auto;background:none;border:none;color:var(--text-tertiary);cursor:pointer;">✕</button>
        </li>
    `).join('');
}

function removeFile(index) {
    AppState.uploadedFiles.splice(index, 1);
    updateFilesList();
}

// ========================================
// Analysis Functions
// ========================================

async function startAnalysis() {
    const caseText = elements.caseText.value.trim();
    const caseTitle = elements.caseTitle.value.trim();
    const posture = elements.postureSel.value;
    const docketNumber = elements.docketNumber.value.trim();

    // Validate input
    if (!caseText && AppState.uploadedFiles.length === 0 && !docketNumber) {
        alert('Please provide case materials, upload a PDF, or enter a docket number.');
        return;
    }

    closeModal();
    showLoading('Classifying input tier...');

    AppState.currentCaseId = null; // New custom analysis

    try {
        // Determine input tier
        const inputTier = classifyInputTier(caseText, AppState.uploadedFiles, docketNumber);
        AppState.inputTier = inputTier;

        updateLoadingStatus('Detecting posture...');
        await delay(500);

        // Detect or use selected posture
        const detectedPosture = posture === 'auto' ? detectPosture(caseText) : posture;
        AppState.posture = detectedPosture;

        updateLoadingStatus('Analyzing precedent architecture...');
        await delay(800);

        // Generate analysis (in production, this would call the backend)
        const analysis = await generateAnalysis({
            text: caseText,
            title: caseTitle,
            posture: detectedPosture,
            tier: inputTier,
            docket: docketNumber
        });

        AppState.currentAnalysis = analysis;

        updateLoadingStatus('Simulating judicial pressure points...');
        await delay(600);

        // Render results
        renderAnalysisResults(analysis);

        hideLoading();

    } catch (error) {
        console.error('Analysis error:', error);
        hideLoading();
        alert('Analysis failed. Please try again.');
    }
}

function classifyInputTier(text, files, docket) {
    // Tier A: Full materials (substantial text or multiple files)
    if (text.length > 5000 || files.length >= 2) {
        return 'A';
    }
    // Tier B: Partial materials
    if (text.length > 500 || files.length === 1) {
        return 'B';
    }
    // Tier C: Minimal (docket only or short text)
    return 'C';
}

function detectPosture(text) {
    const lowerText = text.toLowerCase();

    if (lowerText.includes('petition for writ of certiorari') ||
        lowerText.includes('cert petition') ||
        lowerText.includes('questions presented')) {
        return 'cert';
    }
    if (lowerText.includes('emergency application') ||
        lowerText.includes('stay pending') ||
        lowerText.includes('irreparable harm')) {
        return 'emergency';
    }
    if (lowerText.includes('merits brief') ||
        lowerText.includes('brief for petitioner') ||
        lowerText.includes('brief for respondent')) {
        return 'merits';
    }

    return 'cert'; // Default
}

async function generateAnalysis(input) {
    // Try to call backend API
    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(input)
        });

        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.log('Backend not available, using client-side analysis');
    }

    // Client-side fallback analysis
    return generateClientSideAnalysis(input);
}

function generateClientSideAnalysis(input) {
    const { text, title, posture, tier } = input;

    // Extract key terms for analysis
    const hasVRA = /voting rights act|vra|section 2/i.test(text);
    const hasEqualProtection = /equal protection|14th amendment|fourteenth amendment/i.test(text);
    const hasFirstAmendment = /first amendment|free speech|free exercise/i.test(text);
    const hasSeparationOfPowers = /separation of powers|executive power|removal/i.test(text);
    const hasStanding = /standing|injury in fact|case or controversy/i.test(text);

    // Generate risk assessment based on content
    let riskLevel = 'CAUTION';
    let digRisk = 'Medium';
    let primaryObstacle = 'Incomplete record limits full analysis';
    let rewriteDirective = 'Upload complete petition text for comprehensive evaluation';

    // Build precedent list based on detected issues
    const precedents = [];

    if (hasVRA || hasEqualProtection) {
        precedents.push({
            case: 'Shaw v. Reno, 509 U.S. 630 (1993)',
            url: 'https://supreme.justia.com/cases/federal/us/509/630/',
            relevance: 'Racial gerrymandering violates Equal Protection',
            risk: 'medium'
        });
        precedents.push({
            case: 'Thornburg v. Gingles, 478 U.S. 30 (1986)',
            url: 'https://supreme.justia.com/cases/federal/us/478/30/',
            relevance: 'Section 2 VRA preconditions for vote dilution claims',
            risk: 'high'
        });
        riskLevel = 'CAUTION';
        primaryObstacle = 'Tension between VRA compliance and Equal Protection strict scrutiny';
    }

    if (hasFirstAmendment) {
        precedents.push({
            case: 'Reed v. Town of Gilbert, 576 U.S. 155 (2015)',
            url: 'https://supreme.justia.com/cases/federal/us/576/155/',
            relevance: 'Content-based restrictions subject to strict scrutiny',
            risk: 'medium'
        });
    }

    if (hasSeparationOfPowers) {
        precedents.push({
            case: 'Humphrey\'s Executor v. United States, 295 U.S. 602 (1935)',
            url: 'https://supreme.justia.com/cases/federal/us/295/602/',
            relevance: 'Congressional limits on removal power',
            risk: 'high'
        });
        precedents.push({
            case: 'Seila Law LLC v. CFPB, 591 U.S. ___ (2020)',
            url: 'https://supreme.justia.com/cases/federal/us/591/19-7/',
            relevance: 'Single-director removal restrictions unconstitutional',
            risk: 'medium'
        });
    }

    if (hasStanding) {
        precedents.push({
            case: 'Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992)',
            url: 'https://supreme.justia.com/cases/federal/us/504/555/',
            relevance: 'Article III standing requirements',
            risk: 'high'
        });
    }

    // Default precedents if none detected
    if (precedents.length === 0) {
        precedents.push({
            case: 'Marbury v. Madison, 5 U.S. 137 (1803)',
            url: 'https://supreme.justia.com/cases/federal/us/5/137/',
            relevance: 'Foundational judicial review authority',
            risk: 'low'
        });
    }

    // Generate strategic traps
    const traps = [
        {
            type: 'trap',
            text: 'Conceding jurisdictional or procedural defects while focusing solely on merits arguments'
        },
        {
            type: 'counter',
            text: 'Lead with clean vehicle demonstration; address procedural posture before substantive arguments'
        },
        {
            type: 'trap',
            text: 'Over-relying on circuit split without demonstrating conflict maturity or percolation'
        },
        {
            type: 'counter',
            text: 'Document specific contradictory holdings with parallel fact patterns across circuits'
        }
    ];

    // Generate risk assessment table
    const risks = [
        {
            category: 'Vehicle Integrity',
            level: tier === 'A' ? 'low' : 'medium',
            confidence: tier === 'A' ? 'High' : 'Limited data'
        },
        {
            category: 'Circuit Split Quality',
            level: 'medium',
            confidence: 'Requires verification'
        },
        {
            category: 'Preservation',
            level: 'medium',
            confidence: 'Check record'
        },
        {
            category: 'DIG Risk',
            level: digRisk.toLowerCase(),
            confidence: 'Based on posture'
        }
    ];

    // Generate justice questions based on posture
    const justiceQuestions = generateJusticeQuestions(posture, { hasVRA, hasEqualProtection, hasFirstAmendment, hasSeparationOfPowers });

    return {
        title: title || 'Case Analysis',
        tier,
        posture,
        riskLevel,
        digRisk,
        primaryObstacle,
        rewriteDirective,
        precedents,
        traps,
        risks,
        justiceQuestions
    };
}

function generateJusticeQuestions(posture, issues) {
    const questions = [];

    // Thomas - Originalism
    questions.push({
        justice: 'thomas',
        name: 'Justice Thomas',
        focus: 'Originalism',
        question: issues.hasVRA ?
            'Where in the constitutional text does Congress derive authority to mandate race-conscious districting? Isn\'t Section 2 of the VRA itself constitutionally suspect under the original public meaning of the Fifteenth Amendment?' :
            'What is the original public meaning of the constitutional provision at issue here, and how does that constrain the Court\'s analysis?',
        pressure: 'Challenges modern statutory interpretations against original constitutional framework'
    });

    // Kagan - Pragmatism
    questions.push({
        justice: 'kagan',
        name: 'Justice Kagan',
        focus: 'Workability',
        question: issues.hasVRA ?
            'If we rule for you, what exactly should states do when they face a Section 2 violation? Are you saying they must wait for contempt before drawing remedial maps?' :
            'Walk me through the practical consequences of your rule. How would lower courts and regulated parties actually implement this standard?',
        pressure: 'Forces articulation of workable, real-world legal standard'
    });

    // Barrett - Doctrinal Clarity
    questions.push({
        justice: 'barrett',
        name: 'Justice Barrett',
        focus: 'Doctrine',
        question: issues.hasEqualProtection ?
            'Help me understand the doctrinal framework here. Does compliance with federal law automatically constitute a compelling interest, or must we engage in some additional balancing?' :
            'What is the precise doctrinal rule you want us to announce, and how does it fit within our existing precedential framework?',
        pressure: 'Demands clean legal test that harmonizes with existing doctrine'
    });

    // Jackson - Historical Context
    questions.push({
        justice: 'jackson',
        name: 'Justice Jackson',
        focus: 'History & Context',
        question: issues.hasVRA ?
            'Given the specific history of voter disenfranchisement in this jurisdiction—including documented barriers to Black electoral participation—isn\'t there something dissonant about deploying Equal Protection to prevent majority-Black districts?' :
            'What historical context should inform our interpretation here, and how does your reading account for the purposes of the relevant constitutional or statutory provisions?',
        pressure: 'Invokes purposive/historical analysis to complicate formalist arguments'
    });

    return questions;
}

function renderAnalysisResults(analysis) {
    // Hide welcome, show results
    elements.welcomeState.classList.add('hidden');
    elements.analysisResults.classList.remove('hidden');
    elements.chatPanel.classList.remove('hidden');

    // Render interactive brief
    renderBrief(elements.caseText.value || analysis.text, AppState.currentCaseId);

    // Update dashboard metrics
    elements.inputTier.textContent = analysis.tier;
    elements.inputTier.parentElement.classList.remove('awaiting');

    const postureLabels = {
        cert: 'Cert Petition',
        merits: 'Merits',
        emergency: 'Emergency',
        backtest: 'Backtest'
    };
    elements.posture.textContent = postureLabels[analysis.posture] || analysis.posture;
    elements.posture.parentElement.classList.remove('awaiting');

    // Risk level with color
    const riskEmoji = {
        'CRITICAL': '🔴',
        'CAUTION': '🟡',
        'STRONG': '🟢'
    };
    elements.riskLevel.textContent = `${riskEmoji[analysis.riskLevel] || ''} ${analysis.riskLevel}`;
    elements.riskLevel.className = 'metric-value risk-indicator ' + analysis.riskLevel.toLowerCase();
    elements.riskLevel.parentElement.classList.remove('awaiting');

    elements.digRisk.textContent = analysis.digRisk;
    elements.digRisk.parentElement.classList.remove('awaiting');

    // Primary obstacle
    elements.primaryObstacle.querySelector('p').textContent = analysis.primaryObstacle;
    elements.primaryObstacle.querySelector('p').classList.remove('awaiting-text');

    // Rewrite directive
    elements.rewriteDirective.querySelector('p').textContent = analysis.rewriteDirective;
    elements.rewriteDirective.querySelector('p').classList.remove('awaiting-text');

    // Precedent list
    elements.precedentList.innerHTML = analysis.precedents.map(p => `
        <div class="precedent-item">
            <div>
                <a href="${p.url}" target="_blank" class="precedent-case">${p.case}</a>
                <p class="precedent-relevance">${p.relevance}</p>
            </div>
            <span class="precedent-risk ${p.risk}">${p.risk.toUpperCase()}</span>
        </div>
    `).join('');

    // Strategic traps
    elements.trapsList.innerHTML = analysis.traps.map(t => `
        <div class="trap-item ${t.type}">
            <span class="trap-label">${t.type === 'trap' ? '🔴 TRAP' : '✅ COUNTER'}</span>
            <p class="trap-text">${t.text}</p>
        </div>
    `).join('');

    // Risk table
    elements.riskTable.innerHTML = analysis.risks.map(r => `
        <div class="risk-row">
            <span class="risk-category">${r.category}</span>
            <div class="risk-assessment">
                <span class="risk-badge ${r.level}">${r.level.toUpperCase()}</span>
                <span class="risk-confidence">${r.confidence}</span>
            </div>
        </div>
    `).join('');

    // Justice questions
    elements.justiceQuestions.innerHTML = analysis.justiceQuestions.map(q => `
        <div class="justice-question-card" data-justice="${q.justice}">
            <div class="question-header">
                <span class="question-justice">${q.name}</span>
                <span class="question-focus">${q.focus}</span>
            </div>
            <p class="question-text">"${q.question}"</p>
            <p class="question-pressure"><strong>Pressure:</strong> ${q.pressure}</p>
        </div>
    `).join('');

    // Enable justice buttons
    document.querySelectorAll('.justice-btn').forEach(btn => {
        btn.disabled = false;
    });
    elements.fullBenchBtn.disabled = false;

    // Add welcome message to chat
    addChatMessage('assistant', `Analysis complete for **${analysis.title || 'your case'}**.\n\nInput Tier: **${analysis.tier}** | Posture: **${postureLabels[analysis.posture]}** | Risk: **${analysis.riskLevel}**\n\nYou can now:\n• Challenge any conclusion\n• Ask "what if" hypotheticals\n• Test alternative arguments\n• Click a Justice name to simulate additional pressure points`);
}

function resetAnalysis() {
    // Reset state
    AppState.currentAnalysis = null;
    AppState.inputTier = null;
    AppState.posture = null;
    AppState.chatHistory = [];
    AppState.uploadedFiles = [];

    // Reset UI
    elements.welcomeState.classList.remove('hidden');
    elements.analysisResults.classList.add('hidden');
    elements.briefViewer.classList.add('hidden');
    elements.chatPanel.classList.add('hidden');
    elements.chatToggleBtn.classList.add('hidden');

    // Reset dashboard
    ['inputTier', 'posture', 'riskLevel', 'digRisk'].forEach(id => {
        const el = document.getElementById(id);
        el.textContent = '—';
        el.parentElement.classList.add('awaiting');
    });

    elements.primaryObstacle.querySelector('p').textContent = 'Upload case materials to begin analysis';
    elements.primaryObstacle.querySelector('p').classList.add('awaiting-text');
    elements.rewriteDirective.querySelector('p').textContent = '—';
    elements.rewriteDirective.querySelector('p').classList.add('awaiting-text');

    // Reset form
    elements.caseTitle.value = '';
    elements.caseText.value = '';
    elements.postureSel.value = 'auto';
    elements.docketNumber.value = '';
    elements.filesList.innerHTML = '';
    elements.uploadedFiles.classList.add('hidden');

    // Disable justice buttons
    document.querySelectorAll('.justice-btn').forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('active');
    });
    elements.fullBenchBtn.disabled = true;

    // Clear chat
    elements.chatMessages.innerHTML = '';
}

// ========================================
// Justice Simulation
// ========================================

function simulateJustice(justiceId) {
    if (!AppState.currentAnalysis) return;

    const justice = JUSTICES[justiceId];
    if (!justice) return;

    // Update button states
    document.querySelectorAll('.justice-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.justice === justiceId);
    });

    AppState.selectedJustice = justiceId;

    // Find existing question or generate new one
    const existingQ = AppState.currentAnalysis.justiceQuestions.find(q => q.justice === justiceId);

    if (existingQ) {
        // Scroll to the question card
        const card = document.querySelector(`.justice-question-card[data-justice="${justiceId}"]`);
        if (card) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            card.style.animation = 'pulse 0.5s ease';
            setTimeout(() => card.style.animation = '', 500);
        }
    } else {
        // Generate a new question and add to chat
        const newQuestion = generateAdditionalQuestion(justiceId);
        addChatMessage('assistant', `**${justice.name}** (${justice.focus}):\n\n"${newQuestion}"`);
    }
}

function generateAdditionalQuestion(justiceId) {
    const justice = JUSTICES[justiceId];
    const posture = AppState.posture || 'cert';

    const genericQuestions = {
        roberts: 'How do we write a narrow opinion that resolves this case without creating broader doctrinal disruption? What\'s the minimalist path here?',
        thomas: 'Which of our precedents should we reconsider in light of the original meaning of the Constitution? Are we perpetuating an error?',
        alito: 'What are the real-world practical consequences of your proposed rule? Who wins and who loses if we adopt your interpretation?',
        sotomayor: 'How does your position affect ordinary people—workers, consumers, the accused? Have you considered the on-the-ground impact?',
        kagan: 'Give me a manageable test courts can apply. Your standard sounds fine in theory, but how would it actually work in practice?',
        gorsuch: 'Point me to the statutory text. Where are the words that support your reading? Aren\'t we just legislating from the bench here?',
        kavanaugh: 'How do we respect stare decisis while also recognizing the limits of the prior decision? What\'s the reliance interest?',
        barrett: 'What\'s the original meaning of the relevant text? How does that historical understanding inform our analysis today?',
        jackson: 'What historical context are we overlooking? How does the purpose behind this provision inform our interpretation?'
    };

    return genericQuestions[justiceId] || 'How do you respond to the strongest version of your opponent\'s argument?';
}

function simulateFullBench() {
    if (!AppState.currentAnalysis) return;

    // Add all justice questions to chat
    addChatMessage('assistant', '**Full Bench Simulation**\n\nSimulating pressure points from all nine Justices:');

    Object.keys(JUSTICES).forEach((justiceId, index) => {
        setTimeout(() => {
            const question = generateAdditionalQuestion(justiceId);
            addChatMessage('assistant', `**${JUSTICES[justiceId].name}** (${JUSTICES[justiceId].focus}):\n\n"${question}"`);
        }, index * 300);
    });
}

// ========================================
// Chat Functions
// ========================================

async function sendChatMessage() {
    const message = elements.chatInput.value.trim();
    if (!message) return;

    // Add user message
    addChatMessage('user', message);
    elements.chatInput.value = '';

    // Add to history
    AppState.chatHistory.push({ role: 'user', content: message });

    // Try backend first
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                history: AppState.chatHistory,
                context: AppState.currentAnalysis
            })
        });

        if (response.ok) {
            const data = await response.json();
            addChatMessage('assistant', data.response);
            AppState.chatHistory.push({ role: 'assistant', content: data.response });
            return;
        }
    } catch (e) {
        console.log('Backend chat not available');
    }

    // Client-side fallback response
    const fallbackResponse = generateChatResponse(message);
    addChatMessage('assistant', fallbackResponse);
    AppState.chatHistory.push({ role: 'assistant', content: fallbackResponse });
}

function generateChatResponse(message) {
    const lowerMessage = message.toLowerCase();

    // Pattern matching for common queries
    if (lowerMessage.includes('what if') || lowerMessage.includes('hypothetical')) {
        return 'Interesting hypothetical. To properly evaluate alternative scenarios, I would need to assess:\n\n1. How the changed facts affect the vehicle analysis\n2. Whether the legal standard would apply differently\n3. Impact on Justice-specific concerns\n\nCould you specify which aspect of the case you\'d like to modify?';
    }

    if (lowerMessage.includes('rewrite') || lowerMessage.includes('question presented')) {
        return 'When rewriting Questions Presented, consider:\n\n1. **Front-load the winning facts** — Your client\'s best facts should appear in the question itself\n2. **Signal the standard of review** — Frame to invoke favorable precedent\n3. **Avoid over-breadth** — Narrow questions have better grant rates\n4. **Create asymmetry** — Make your question easier to answer "yes" than opponent\'s\n\nShall I draft alternative framings based on the current case posture?';
    }

    if (lowerMessage.includes('circuit split') || lowerMessage.includes('conflict')) {
        return 'Circuit split quality is critical for cert. The Court looks for:\n\n1. **Direct conflict** — Same legal question, opposite holdings\n2. **Maturity** — Has the issue percolated sufficiently?\n3. **Importance** — Does the split affect substantial federal interests?\n4. **Clean vehicle** — Can this case cleanly resolve the split?\n\nA shallow or manufactured split significantly increases DIG risk.';
    }

    if (lowerMessage.includes('standing') || lowerMessage.includes('jurisdiction')) {
        return 'Jurisdictional and standing defects are **dispositive** — they can end your case before reaching the merits.\n\nKey checkpoints:\n• **Article III standing**: injury, causation, redressability\n• **Statutory exhaustion**: have all required administrative steps been completed?\n• **Finality**: is the lower court judgment truly final?\n• **Mootness**: can the Court still grant effective relief?\n\nAny weakness here should be addressed before cert, not at merits.';
    }

    // Default analytical response
    return 'That\'s a strategic consideration worth examining. Based on the current analysis:\n\n• **Input Tier ' + (AppState.inputTier || 'B') + '** limits definitive conclusions on some procedural aspects\n• The **' + (AppState.posture || 'cert') + ' posture** emphasizes certain institutional concerns\n\nTo provide more specific guidance, could you clarify:\n1. Which party\'s perspective you\'re analyzing from?\n2. What specific doctrinal or strategic concern you want to probe?';
}

function addChatMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;

    // Simple markdown-like formatting
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    messageDiv.innerHTML = formatted;
    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function toggleChat() {
    const isHidden = elements.chatPanel.classList.toggle('hidden');
    // Show floating button when chat is hidden, hide it when chat is visible
    elements.chatToggleBtn.classList.toggle('hidden', !isHidden);
}

// ========================================
// Loading Functions
// ========================================

function showLoading(status) {
    elements.loadingOverlay.classList.remove('hidden');
    elements.loadingStatus.textContent = status;
}

function updateLoadingStatus(status) {
    elements.loadingStatus.textContent = status;
}

function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

// ========================================
// Utilities
// ========================================

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ========================================
// Initialize
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    console.log('SCOTUS Strategic Engine initialized');
});

// Make removeFile available globally for inline onclick
window.removeFile = removeFile;
