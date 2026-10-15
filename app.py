
import streamlit as st

st.set_page_config(
    page_title="PathPilot",
    page_icon="🧭",
    layout="centered"
)

st.title("🧭 PathPilot")
st.subheader("MCP Workshop Learning Path Generator")
st.write("Create your personal learning roadmap in seconds!")

name = st.text_input("Your name")
goal = st.selectbox(
    "What do you want to learn?",
    ["Python", "AI / Machine Learning", "Cloud / AWS",
     "Web Development", "Cybersecurity", "IoT"]
)
level = st.selectbox(
    "Your current level",
    ["Beginner", "Intermediate", "Advanced"]
)
weeks = st.slider("Learning duration (weeks)", 2, 12, 4)
hours = st.slider("Study hours per week", 2, 20, 6)

if st.button("Generate My Learning Path"):
    st.success(f"Learning path created for {name or 'Learner'}!")
    st.markdown(f"### 🎯 Goal: {goal}")
    st.write(f"**Current level:** {level}")
    st.write(f"**Duration:** {weeks} weeks")
    st.write(f"**Study time:** {hours} hours/week")

    st.markdown("### 📚 Your roadmap")
    topics = {
        "Python": ["Variables and data types", "Conditions and loops",
                   "Functions and collections", "Build a Python mini-project"],
        "AI / Machine Learning": ["AI and ML fundamentals",
                   "Python for data", "Basic ML models",
                   "Build a prediction mini-project"],
        "Cloud / AWS": ["Cloud computing basics", "Core cloud services",
                   "Deployment and security", "Deploy a demo project"],
        "Web Development": ["HTML and CSS", "JavaScript basics",
                   "Interactive applications", "Publish a portfolio"],
        "Cybersecurity": ["Security fundamentals", "Networking basics",
                   "Defensive security", "Safe practice lab"],
        "IoT": ["Sensors and devices", "Connectivity basics",
                   "Collect and display data", "Build an IoT demo"]
    }
    selected_topics = topics[goal]
    for week in range(weeks):
        topic = selected_topics[week % len(selected_topics)]
        st.write(f"**Week {week + 1}:** {topic}")

    st.info("Tip: Divide your weekly study time between learning, practice, and revision.")
  streamlit>=1.36,<2.0
