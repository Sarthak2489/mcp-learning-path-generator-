

import streamlit as st
from datetime import date
import json
from google import genai

st.set_page_config(
    page_title="PathPilot",
    page_icon="🧭",
    layout="wide"
)

st.markdown("""
<style>
.block-container {max-width:1100px;padding-top:2rem}
.hero {
 padding:28px;border-radius:22px;color:white;
 background:linear-gradient(120deg,#171d3b,#6257e8);
}
.hero h1 {font-size:2.7rem}
.hero p {color:#eeeaff}
.pill {
 display:inline-block;background:#f0efff;color:#4b42b8;
 padding:5px 12px;border-radius:30px;margin:3px;
}
div[data-testid="stMetric"] {
 border:1px solid #e5e7f0;border-radius:14px;padding:12px
}
</style>
""", unsafe_allow_html=True)

def generate_ai_roadmap(plan):
    """Generate a personalized learning roadmap with Gemini."""
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Create a practical learning roadmap for a student.

        Learning goal: {plan["goal"]}
        Current level: {plan["level"]}
        Main goal: {plan["focus"]}
        Duration: {plan["weeks"]} weeks
        Study hours per week: {plan["hours"]}

        Return ONLY valid JSON with this structure:
        {{
          "weeks": [
            {{
              "title": "Week topic",
              "learn": "Topics to learn",
              "build": "Practical task"
            }}
          ]
        }}

        Include exactly {plan["weeks"]} weekly entries.
        Keep the plan beginner-friendly and practical.
        Do not include markdown fences.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = json.loads(response.text)
        return result["weeks"]

    except Exception:
        return None
        
TRACKS = {
    "Python": [
        ("Python basics", "Variables, data types and input/output",
         "Create a marks calculator"),
        ("Conditions and loops", "if/else, loops, strings and lists",
         "Build a quiz application"),
        ("Functions and files", "Functions, exceptions and file handling",
         "Create a contact book"),
        ("Portfolio project", "Testing, debugging and documentation",
         "Publish a Python project on GitHub")
    ],
    "AI / Machine Learning": [
        ("AI fundamentals", "AI, ML and real-world use cases",
         "Compare three AI applications"),
        ("Python for data", "Collections, CSV and data cleaning",
         "Clean a sample dataset"),
        ("Machine learning", "Features, labels and train/test split",
         "Train a beginner model"),
        ("AI mini-project", "Evaluation and documentation",
         "Create a small prediction demo")
    ],
    "Cloud / AWS": [
        ("Cloud fundamentals", "IaaS, PaaS, SaaS and cloud architecture",
         "Draw a cloud architecture"),
        ("Core services", "Compute, storage and databases",
         "Design a sample cloud app"),
        ("Deployment", "Git, environment variables and logs",
         "Deploy a demo application"),
        ("Security and costs", "Permissions, monitoring and budgets",
         "Write a cloud security checklist")
    ],
    "Web Development": [
        ("HTML and CSS", "Web pages, forms and responsive design",
         "Build a profile page"),
        ("JavaScript", "Functions, arrays and events",
         "Create a to-do list"),
        ("Interactive apps", "Forms, validation and application state",
         "Build a study tracker"),
        ("Portfolio", "Testing, hosting and documentation",
         "Publish a portfolio website")
    ],
    "Cybersecurity": [
        ("Security basics", "CIA triad, threats and risk",
         "Create a security glossary"),
        ("Networking", "IP, DNS, HTTP and ports",
         "Draw a network diagram"),
        ("Defensive security", "MFA, patching and permissions",
         "Create a security checklist"),
        ("Safe practice", "Authorized labs and reporting",
         "Write a defensive lab report")
    ],
    "IoT": [
        ("IoT foundations", "Sensors, actuators and microcontrollers",
         "Draw a smart-room diagram"),
        ("Connectivity", "Wi-Fi, MQTT concepts and telemetry",
         "Design a sensor data flow"),
        ("Dashboard", "Display and interpret sensor readings",
         "Build a simulated sensor dashboard"),
        ("IoT mini-project", "Testing, security and documentation",
         "Publish an IoT project report")
    ]
}

st.markdown("""
<div class="hero">
  <div>YOUR PERSONAL LEARNING COMPANION</div>
  <h1>🧭 PathPilot</h1>
  <p>Learn with a plan. Build real projects. Track your progress.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.subheader("Create your learning path")

with st.form("learning_form"):
    name = st.text_input("Your name", placeholder="e.g. Sarthak")
    goal = st.selectbox("What do you want to learn?", list(TRACKS))
    level = st.selectbox(
        "Your current level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    focus = st.selectbox(
        "Main goal",
        ["College project", "Internship preparation",
         "Build portfolio", "Explore a new skill"]
    )
    weeks = st.slider("Learning duration (weeks)", 2, 12, 4)
    hours = st.slider("Study hours per week", 2, 20, 6)
    submit = st.form_submit_button(
        "✨ Generate my learning path",
        use_container_width=True
    )

if submit:
    st.session_state.plan = {
        "name": name.strip() or "Learner",
        "goal": goal,
        "level": level,
        "focus": focus,
        "weeks": weeks,
        "hours": hours,
        "date": date.today().isoformat()
    }

if "plan" in st.session_state:
    p = st.session_state.plan
    track = TRACKS[p["goal"]]

    st.divider()
    st.subheader(f"🎯 Your learning path, {p['name']}")
    st.markdown(
        f'<span class="pill">{p["goal"]}</span>'
        f'<span class="pill">{p["level"]}</span>'
        f'<span class="pill">{p["focus"]}</span>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)
    a.metric("Duration", f'{p["weeks"]} weeks')
    b.metric("Weekly study", f'{p["hours"]} hours')
    c.metric("Total planned", f'{p["weeks"] * p["hours"]} hours')

    st.write("### 📚 Weekly roadmap")
    completed = 0
    checklist = []

    for i in range(p["weeks"]):
        title, topics, task = track[i % len(track)]
        with st.expander(f"Week {i + 1}: {title}",
                         expanded=(i == 0)):
            st.write("**Learn:**", topics)
            st.write("**Build:**", task)
            st.write("**Suggested routine:** Learn, practise, then review.")
            done = st.checkbox(
                f"Complete Week {i + 1}",
                key=f'{p["date"]}_{p["goal"]}_{i}'
            )
            checklist.append(done)
            completed += int(done)

    progress = completed / p["weeks"]
    st.progress(progress, text=f"Progress: {completed}/{p['weeks']} weeks")

    report = [
        f'# PathPilot Learning Plan — {p["goal"]}',
        f'- Learner: {p["name"]}',
        f'- Level: {p["level"]}',
        f'- Main goal: {p["focus"]}',
        f'- Duration: {p["weeks"]} weeks',
        f'- Study time: {p["hours"]} hours per week',
        ""
    ]

    for i in range(p["weeks"]):
        title, topics, task = track[i % len(track)]
        report.extend([
            f'## Week {i + 1}: {title}',
            f'Learn: {topics}',
            f'Build: {task}',
            ""
        ])

    st.download_button(
        "⬇️ Download roadmap",
        data="\n".join(report),
        file_name="pathpilot_roadmap.md",
        mime="text/markdown",
        use_container_width=True
    )

st.divider()
with st.expander("About this project"):
    st.write(
        "PathPilot is a Streamlit learning planner. "
        "Its standard roadmap uses predefined learning tracks "
        "and works without a paid AI API."
    )
    st.write(
        "Actual MCP integration requires an MCP client/server "
        "connection and appropriate testing."
    )
