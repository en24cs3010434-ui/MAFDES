import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from modules.reports import generate_pdf_report

st.set_page_config(
    page_title="MAFDES | Expert Diagnostics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN SYSTEM --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {
    --bg:#17191d;
    --panel:#24272d;
    --panel2:#30343b;
    --line:#454b54;
    --cyan:#c5cbd3;
    --blue:#89939f;
    --muted:#aeb5be;
 }
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
    background: #17191d !important;
    color: #f1f2f4 !important;
 }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#292d34,#17191d) !important;
    border-right: 1px solid #454b54;
 }
[data-testid="stSidebar"] * { color:#eaf3ff; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1500px; }
h1,h2,h3 { color:#f2f7ff !important; letter-spacing:-.03em; }
p, label, .stMarkdown { color:#d4e1f0; }
[data-testid="stMetric"] {
    background: linear-gradient(145deg,#363b43,#25292f) !important;
    border: 1px solid #626a75 !important;
    padding: 18px 20px;
    border-radius: 16px;
}
[data-testid="stMetricLabel"] {
    color:#aeb5be !important;
}
[data-testid="stMetricValue"] {
    color:#ffffff !important;
}
div.stButton > button,
div.stDownloadButton > button {
    border:1px solid #aeb5be;
    border-radius:10px;
    background:linear-gradient(100deg,#59616c,#89939f);
    color:white;
    font-weight:700;
    padding:.62rem 1.1rem;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color:#c5cbd3;
    color:white;
    background:#737d89;
}
div[data-testid="stVerticalBlockBorderWrapper"] { border-color:#29425e !important; border-radius:16px; background:rgba(16,31,51,.72); }
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div { background:#142943; border-color:#34516f; }
.stRadio label, .stCheckbox label { color:#e5f0fc !important; }
hr { border-color:#29425e !important; }
.small-muted { color:#91a5bd; font-size:.88rem; }
.eyebrow {
    color:#c5cbd3;
    font-size:.76rem;
    font-weight:800;
    letter-spacing:.16em;
    text-transform:uppercase;
}

.pill {
    display:inline-block;
    border:1px solid #747d88;
    background:#343941;
    color:#e1e5ea;
    padding:5px 10px;
    border-radius:99px;
    font-size:.75rem;
    font-weight:700;
}
.hero {
    padding:28px 30px;
    border:1px solid #727b87;
    border-radius:20px;
    background:linear-gradient(115deg,#414750,#25292f);
    box-shadow:0 18px 55px rgba(0,0,0,.22);
}
.hero h1 { font-size:2.35rem; margin:.3rem 0 .45rem 0; }
.hero p { color:#b8cbe0; margin:0; }
.section-head { margin-top:1.4rem; margin-bottom:.6rem; }
</style>
""", unsafe_allow_html=True)

# -------------------- BACKGROUND IMAGE --------------------
bg_path = Path(__file__).parent / "assets" / "mafdes_background.png"

if bg_path.exists():
    with open(bg_path, "rb") as image_file:
        bg_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(15,17,21,.55), rgba(15,17,21,.72)),
                url("data:image/png;base64,{bg_image}")
                center/cover fixed no-repeat !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("Aircraft background image not found!")

# -------------------- DEMO LOGIN GATE --------------------

if "ma fdes_user" not in st.session_state:
    st.session_state["ma fdes_user"] = ""

if not st.session_state["ma fdes_user"]:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    .login-wrap {
        text-align: center;
        max-width: 820px;
        margin: 4vh auto 0 auto;
        padding: 42px 46px;
        border: 1px solid #747d88;
        border-radius: 24px;
        background: linear-gradient(135deg,#393e46,#202329);
        box-shadow: 0 24px 80px rgba(0,0,0,.4);
    }
    .login-mark {
    font-size: 3rem;
}

.login-kicker {
    color: #c5cbd3;
    font-size: .85rem;
    letter-spacing: 4px;
}

.login-title {
    color: white;
    font-size: 2.5rem !important;
    font-weight: 800;
    line-height: 1.3;
    margin: 20px 0;
    text-align: center;
}

.login-sub {
    color: #c5cbd3;
    font-size: 1rem;
}

.login-tag {
    display: inline-block;
    color: #e1e5ea;
    border: 1px solid #89939f;
    border-radius: 20px;
    padding: 7px 14px;
    margin: 5px;
}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrap">
        <div class="login-mark">✈️</div>
        <div class="login-kicker">MAFDES / SECURE DEMO ACCESS</div>
        <div class="login-title">
            MILITARY AIRCRAFT FAULT<br>
            DIAGNOSIS EXPERT SYSTEM
        </div>
        <div class="login-sub">
            Knowledge-based expert system · Explainable reasoning · Academic simulation environment
        </div>
        <span class="login-tag">● SIMULATION MODE</span>
        <span class="login-tag">EXPERT SYSTEM CONSOLE</span>
    </div>
    """, unsafe_allow_html=True)

    _, login_col, _ = st.columns([1, 1.2, 1])

    with login_col:
        with st.form("ma fdes_login_form"):
            st.subheader("Operator Login")
            login_name = st.text_input("Operator name")
            access_key = st.text_input("Demo access key", type="password")
            submitted = st.form_submit_button(
                "ENTER COMMAND CENTER",
                 type="secondary",                use_container_width=True
            )

        if submitted:
            if login_name.strip() and access_key == "MAFDES2026":
                st.session_state["ma fdes_user"] = login_name.strip()
                st.rerun()
            elif not login_name.strip():
                st.warning("Please enter an operator name.")
            else:
                st.error("Incorrect demo access key. Please try again.")

        st.caption("Demo access key: MAFDES2026")
        st.info("Educational simulation only.")

    st.stop()

# -------------------- KNOWLEDGE BASE (FICTIONAL EDUCATIONAL RULES) --------------------
RULES = [
    ("Engine", ["High temperature", "High vibration"], "Engine anomaly", .90, "Both simulated temperature and vibration observations are abnormal."),
    ("Engine", ["Low oil pressure", "High temperature"], "Lubrication-related anomaly", .85, "Low oil pressure and high temperature are reported in the simulation."),
    ("Engine", ["High vibration"], "Vibration anomaly", .75, "An abnormal vibration indicator is selected in the simulation."),
    ("Engine", ["Low performance indication", "High temperature"], "Engine performance anomaly", .80, "Performance and temperature indicators are selected."),
    ("Hydraulic", ["Low hydraulic pressure", "Leakage indication"], "Possible hydraulic leakage", .90, "Low pressure and a leakage indicator are both selected."),
    ("Hydraulic", ["Low hydraulic pressure"], "Hydraulic pressure anomaly", .75, "A low-pressure indicator is selected."),
    ("Hydraulic", ["Abnormal actuator response", "Low hydraulic pressure"], "Hydraulic response anomaly", .85, "Response and pressure indicators are both selected."),
    ("Electrical", ["Voltage fluctuation", "Electrical warning"], "Electrical system anomaly", .90, "Voltage fluctuation and warning indicators are selected."),
    ("Electrical", ["Low voltage", "Power interruption"], "Power supply anomaly", .90, "Low-voltage and interruption indicators are selected."),
    ("Electrical", ["Electrical warning"], "Electrical warning requires investigation", .70, "An electrical warning indicator is selected."),
    ("Avionics", ["Display failure", "Sensor disagreement"], "Avionics anomaly", .90, "Display and sensor indicators disagree in the simulation."),
    ("Avionics", ["Communication failure", "Communication warning"], "Communication subsystem anomaly", .85, "Communication indicators are selected."),
    ("Avionics", ["Navigation display abnormal", "Sensor disagreement"], "Navigation data anomaly", .85, "Navigation display and sensor indicators disagree."),
    ("Landing Gear", ["Gear position mismatch", "Gear warning"], "Landing gear indication anomaly", .90, "Position mismatch and warning indicators are selected."),
    ("Landing Gear", ["Position sensor invalid", "Gear position mismatch"], "Position sensor anomaly", .85, "Invalid position and mismatch indicators are selected."),
    ("Landing Gear", ["Gear warning"], "Landing gear status requires investigation", .70, "A gear warning indicator is selected."),
    ("Environmental Control", ["High cabin temperature", "Cooling failure"], "Cooling subsystem anomaly", .90, "Cabin temperature and cooling indicators are selected."),
    ("Environmental Control", ["Abnormal airflow", "High cabin temperature"], "Environmental control anomaly", .85, "Airflow and temperature indicators are selected."),
    ("Environmental Control", ["Cooling warning"], "Cooling system requires investigation", .70, "A cooling warning indicator is selected.")
]
SYMPTOMS = {
    "Engine":["High temperature","High vibration","Low oil pressure","Low performance indication"],
    "Hydraulic":["Low hydraulic pressure","Leakage indication","Abnormal actuator response"],
    "Electrical":["Voltage fluctuation","Electrical warning","Low voltage","Power interruption"],
    "Avionics":["Display failure","Sensor disagreement","Communication failure","Communication warning","Navigation display abnormal"],
    "Landing Gear":["Gear position mismatch","Gear warning","Position sensor invalid"],
    "Environmental Control":["High cabin temperature","Cooling failure","Abnormal airflow","Cooling warning"]
}
SYSTEM_ICONS = {"Engine":"⚙️","Hydraulic":"💧","Electrical":"⚡","Avionics":"📡","Landing Gear":"🛬","Environmental Control":"🌡️"}

def forward_chaining(system, facts):
    results=[]
    for category, conditions, conclusion, cf, explanation in RULES:
        if category == system and all(c in facts for c in conditions):
            score=min(facts[c] for c in conditions)*cf
            results.append({"Fault":conclusion,"Rule":conditions,"Confidence":round(score*100,1),
                            "Explanation":explanation,"Rule CF":cf})
    return results

def backward_chaining(system, goal, facts):
    for category, conditions, conclusion, cf, explanation in RULES:
        if category == system and conclusion == goal:
            missing=[c for c in conditions if c not in facts]
            return (not missing), conditions, cf, explanation, missing
    return None, [], 0, "No matching rule found.", []

# -------------------- HISTORY --------------------
DB_PATH = Path(__file__).parent / "database" / "ma fdes_history.db"
DB_PATH.parent.mkdir(exist_ok=True)
def init_history():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS runs(
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT,
            subsystem TEXT, method TEXT, symptoms TEXT, findings TEXT)""")
def save_history(report, method):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO runs(created_at,subsystem,method,symptoms,findings) VALUES(?,?,?,?,?)",
            (report["time"],report["system"],method,json.dumps(report["symptoms"]),
             json.dumps([r["Fault"] for r in report["results"]])))
def read_history():
    with sqlite3.connect(DB_PATH) as con:
        return con.execute("SELECT id,created_at,subsystem,method,symptoms,findings FROM runs ORDER BY id DESC").fetchall()
init_history()

st.markdown("""
<style>
.stApp {
    color: #f1f2f4 !important;
}
h1, h2, h3 {
    color: #f1f2f4 !important;
}

/* DASHBOARD CHARCOAL + SILVER THEME */

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#292d34,#1b1e23) !important;
    border-right:1px solid #555c66;
}

[data-testid="stSidebar"] h2 {
    color:#ffffff !important;
}

[data-testid="stMetric"] {
    background:linear-gradient(145deg,#363b43,#25292f) !important;
    border:1px solid #626a75 !important;
}

.hero {
    background:linear-gradient(120deg,#414750,#25292f) !important;
    border:1px solid #727b87 !important;
}

.hero h1 {
    color:#ffffff !important;
}

.hero p {
    color:#d0d5dc !important;
}

.eyebrow {
    color:#c5cbd3 !important;
}

.pill {
    background:#343941 !important;
    border:1px solid #747d88 !important;
    color:#e1e5ea !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:#25292f !important;
    border:1px solid #555c66 !important;
}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background:#30343b !important;
    border-color:#747d88 !important;
}

div.stButton > button,
div.stDownloadButton > button {
    background:linear-gradient(100deg,#59616c,#89939f) !important;
    border:1px solid #aeb5be !important;
    color:#ffffff !important;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background:linear-gradient(100deg,#737d89,#aeb5be) !important;
}

hr {
    border-color:#555c66 !important;
}

</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("<div style='font-size:2.2rem'>✈️</div><h2 style='margin:0'>MAFDES</h2><div class='small-muted'>MILITARY AIRCRAFT FAULT DIAGNOSIS<br>EXPERT SYSTEM</div>",unsafe_allow_html=True)
    st.divider()
    page=st.radio("WORKSPACE",["Command Dashboard","Fault Diagnosis","Knowledge Base","Diagnosis History","About Project"],label_visibility="visible")
    st.divider()
    st.markdown("<span class='pill'>● SIMULATION MODE</span>",unsafe_allow_html=True)
    st.markdown(f"<p class='small-muted'>MAFDES v2.0<br>Academic AI Expert System<br>Operator: {st.session_state['ma fdes_user']}</p>",unsafe_allow_html=True)
    if st.button("↪ Log out", use_container_width=True):
        st.session_state["ma fdes_user"] = ""
        st.rerun()

# -------------------- DASHBOARD --------------------
if page == "Command Dashboard":
    st.markdown("""<div class="hero">
    <div class="eyebrow">MAFDES / EXPERT SYSTEM CONSOLE</div>
    <h1>Aircraft Diagnostic Command Center</h1>
    <p>Knowledge-based reasoning • Rule evaluation • Explainable simulation results</p>
    <div style="margin-top:18px"><span class="pill">● SYSTEM READY</span> &nbsp; <span class="pill">ACADEMIC SIMULATION</span></div>
    </div>""",unsafe_allow_html=True)
    st.write("")
    history=read_history()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Subsystem Models","06","Configured")
    c2.metric("Knowledge Rules",f"{len(RULES):02d}","IF–THEN rules")
    c3.metric("Inference Methods","02","Forward / Backward")
    c4.metric("Saved Simulations",len(history),"Local history")
    # -------------------- SIMULATED FLEET OVERVIEW --------------------
    st.markdown(
        "<div class='section-head'><div class='eyebrow'>FLEET MONITOR</div><h2>Simulated Fleet Overview</h2></div>",
        unsafe_allow_html=True
    )

    fleet = pd.DataFrame({
        "Aircraft ID": ["MAF-01", "MAF-02", "MAF-03", "MAF-04", "MAF-05", "MAF-06"],
        "Category": ["Training", "Transport", "Training", "Support", "Transport", "Support"],
        "Simulation Status": ["Active", "Standby", "Active", "Standby", "Under Review", "Active"]
    })

    f1, f2, f3 = st.columns(3)
    f1.metric("Total Simulated Aircraft", len(fleet))
    f2.metric("Active", int((fleet["Simulation Status"] == "Active").sum()))
    f3.metric("Standby", int((fleet["Simulation Status"] == "Standby").sum()))
    fleet_filter = st.selectbox(
        "Filter Aircraft by Status",
        ["All", "Active", "Standby", "Under Review"]
    )

    if fleet_filter == "All":
        filtered_fleet = fleet
    else:
        filtered_fleet = fleet[
            fleet["Simulation Status"] == fleet_filter
        ] 

    fc1, fc2 = st.columns([1, 1])

    with fc1:
        st.markdown("#### Fleet Status Distribution")
        status_counts = filtered_fleet["Simulation Status"].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            hole=0.55
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with fc2:
        st.markdown("#### Simulated Fleet Registry")
        st.dataframe(filtered_fleet, use_container_width=True, hide_index=True)

    st.markdown("#### Aircraft Category Analytics")

    category_counts = filtered_fleet["Category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Aircraft Count"]

    category_chart = px.bar(
        category_counts,
        x="Category",
        y="Aircraft Count",
        text="Aircraft Count",
        title="Simulated Aircraft by Category"
    )

    category_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        category_chart,
        use_container_width=True,
        key="category_analytics_chart"
    )  


    st.caption("All fleet records are fictional demonstration data.")

    st.markdown("<div class='section-head'><div class='eyebrow'>SYSTEM OVERVIEW</div><h2>Subsystem Modules</h2></div>",unsafe_allow_html=True)
    cols=st.columns(3)
    for i,(name,symptoms) in enumerate(SYMPTOMS.items()):
        with cols[i%3]:
            with st.container(border=True):
                st.markdown(f"### {SYSTEM_ICONS[name]} {name}")
                st.markdown(f"<div class='small-muted'>{len(symptoms)} simulated observation indicators</div>",unsafe_allow_html=True)
                st.progress((len(symptoms)+1)/6)
    st.markdown("<div class='section-head'><div class='eyebrow'>CAPABILITIES</div><h2>Reasoning & Explainability</h2></div>",unsafe_allow_html=True)
    x,y,z=st.columns(3)
    with x:
        with st.container(border=True):
            st.subheader("🔗 Forward Chaining")
            st.caption("Evidence-driven rule evaluation from selected observations.")
    with y:
        with st.container(border=True):
            st.subheader("🎯 Backward Chaining")
            st.caption("Goal-based verification of a selected simulated finding.")
    with z:
        with st.container(border=True):
            st.subheader("📊 Certainty Estimate")
            st.caption("Illustrative rule confidence with visible explanation.")
    st.info("Academic simulation only. This prototype is not approved for real aircraft inspection, maintenance or operational decisions.")

# -------------------- DIAGNOSIS --------------------
elif page == "Fault Diagnosis":
    st.markdown("<div class='eyebrow'>ANALYSIS WORKSPACE</div><h1>Fault Diagnosis</h1><p class='small-muted'>Select a simulated subsystem and observations to evaluate the knowledge rules.</p>",unsafe_allow_html=True)
    left,right=st.columns([1.2,.8],gap="large")
    with left:
        with st.container(border=True):
            system=st.selectbox("01  Select subsystem",list(SYMPTOMS.keys()),format_func=lambda s:f"{SYSTEM_ICONS[s]}  {s}")
            selected=st.multiselect("02  Select simulated observations",SYMPTOMS[system],placeholder="Choose one or more observations")
            confidence=st.slider("03  Confidence in entered observations",50,100,100,step=5)
            method=st.radio("04  Reasoning method",["Forward Chaining","Backward Chaining"],horizontal=True)
            goal=None
            if method=="Backward Chaining":
                goals=[r[2] for r in RULES if r[0]==system]
                goal=st.selectbox("Select a suspected finding to verify",goals)
            run=st.button("▶  RUN DIAGNOSTIC SIMULATION",type="primary",use_container_width=True)
    with right:
        with st.container(border=True):
            st.markdown("### 🧭 Simulation Protocol")
            st.markdown("**01 / INPUT**  Select a subsystem and observation indicators.")
            st.markdown("**02 / INFERENCE**  Evaluate the matching IF–THEN rules.")
            st.markdown("**03 / EXPLANATION**  Review activated conditions and confidence.")
            st.divider()
            st.markdown("### 📌 Model Scope")
            st.caption("All indicators and rules are fictional, simplified teaching examples. They do not represent real aircraft maintenance procedures.")
    if run:
        if not selected:
            st.warning("Select at least one observation before running the simulation.")
        else:
            facts={s:confidence/100 for s in selected}
            now=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            if method=="Forward Chaining":
                results=forward_chaining(system,facts)
                if results:
                    report={"system":system,"symptoms":selected,"results":results,"time":now}
                    st.session_state["last_report"]=report
                    save_history(report,method)
                    st.markdown("<div class='section-head'><div class='eyebrow'>OUTPUT / 01</div><h2>Diagnostic Results</h2></div>",unsafe_allow_html=True)
                    for r in results:
                        with st.container(border=True):
                            a,b=st.columns([3,1])
                            a.markdown(f"### ⚠️ {r['Fault']}")
                            b.metric("Illustrative confidence",f"{r['Confidence']:.1f}%")
                            st.progress(min(int(r["Confidence"]),100))
                            st.markdown("**Activated conditions**")
                            st.write("  •  "+"   |   ".join(r["Rule"]))
                            st.markdown("**Rule explanation**")
                            st.write(r["Explanation"])
                    st.caption("Confidence is an illustrative rule-based score, not a verified probability of aircraft failure.")
                else:
                    st.session_state.pop("last_report",None)
                    st.warning("No configured rule matched these observations. The simulation result is inconclusive.")
            else:
                verified,conditions,cf,explanation,missing=backward_chaining(system,goal,facts)
                st.markdown("<div class='section-head'><div class='eyebrow'>OUTPUT / 01</div><h2>Goal Verification</h2></div>",unsafe_allow_html=True)
                if verified:
                    score=cf*confidence
                    st.success(f"Evidence supports the simulated finding: {goal}")
                    st.metric("Illustrative confidence",f"{score:.1f}%")
                    st.write("**Required conditions:** "+"  •  ".join(conditions))
                    st.write("**Explanation:** "+explanation)
                else:
                    st.warning(f"The selected evidence does not establish: {goal}")
                    st.write("**Missing observations:** "+", ".join(missing))
    if "last_report" in st.session_state:
        report=st.session_state["last_report"]
        st.divider()
        st.markdown("### 📄 Export simulation report")
        st.caption("Download a PDF summary of the latest forward-chaining simulation.")
        pdf=generate_pdf_report(report)
        st.download_button("⬇  DOWNLOAD PDF REPORT",data=pdf,file_name="MAFDES_Simulation_Report.pdf",mime="application/pdf",type="primary")

# -------------------- KNOWLEDGE BASE --------------------
elif page=="Knowledge Base":
    st.markdown("<div class='eyebrow'>RULE LIBRARY</div><h1>Knowledge Base</h1><p class='small-muted'>Inspectable IF–THEN production rules used by the academic simulation.</p>",unsafe_allow_html=True)
    chosen=st.selectbox("Filter subsystem",["All"]+list(SYMPTOMS.keys()))
    rows=[r for r in RULES if chosen=="All" or r[0]==chosen]
    a,b=st.columns(2)
    a.metric("Visible rules",len(rows))
    b.metric("Subsystems",len(SYMPTOMS) if chosen=="All" else 1)
    for i,(category,conditions,conclusion,cf,explanation) in enumerate(rows,1):
        with st.expander(f"RULE {i:02d}  ·  {category}  →  {conclusion}"):
            st.markdown("**IF**  "+" AND ".join(conditions))
            st.markdown("**THEN**  "+conclusion)
            st.progress(int(cf*100))
            st.caption(f"Illustrative rule confidence: {cf*100:.0f}%")
            st.write(explanation)

# -------------------- HISTORY --------------------
elif page=="Diagnosis History":
    st.markdown("<div class='eyebrow'>ACTIVITY LOG</div><h1>Diagnosis History</h1><p class='small-muted'>Previously saved forward-chaining simulation runs on this device.</p>",unsafe_allow_html=True)
    records=read_history()
    if records:
        df=pd.DataFrame(records,columns=["ID","Timestamp","Subsystem","Method","Observations","Findings"])
        df["Observations"]=df["Observations"].apply(lambda x:", ".join(json.loads(x)))
        df["Findings"]=df["Findings"].apply(lambda x:", ".join(json.loads(x)))
        st.metric("Saved simulation runs",len(df))
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("⬇  EXPORT HISTORY CSV",df.to_csv(index=False).encode("utf-8"),"MAFDES_History.csv","text/csv")
    else:
        st.info("No saved simulation runs yet. Run a forward-chaining simulation to create the first history entry.")

# -------------------- ABOUT --------------------
elif page=="About Project":
    st.markdown("<div class='eyebrow'>PROJECT DOCUMENTATION</div><h1>About MAFDES</h1>",unsafe_allow_html=True)
    st.markdown("""### Military Aircraft Fault Diagnosis Expert System
MAFDES is an academic Artificial Intelligence project demonstrating how a knowledge-based expert system can represent facts, evaluate IF–THEN rules and explain simulated findings.""")
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.subheader("Core AI concepts")
            st.write("• Knowledge representation\n\n• Production rules\n\n• Forward chaining\n\n• Backward chaining\n\n• Certainty-factor estimates\n\n• Explanation facility")
    with b:
        with st.container(border=True):
            st.subheader("Technology stack")
            st.write("• Python\n\n• Streamlit\n\n• Pandas & Plotly\n\n• SQLite\n\n• ReportLab PDF generation")
    st.warning("Safety boundary: MAFDES is a fictional educational simulation. It must not be used for real aircraft inspection, maintenance, flight-safety or operational decisions.")

st.markdown("<hr><div style='text-align:center;color:#8298b2;font-size:.78rem'>MAFDES v2.0  •  KNOWLEDGE-BASED EXPERT SYSTEM  •  EDUCATIONAL SIMULATION ONLY</div>",unsafe_allow_html=True)
