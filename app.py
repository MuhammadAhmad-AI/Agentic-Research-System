import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import time

# Environment loading
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- UI Setup ---
st.set_page_config(
    page_title="Agentic Research AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }

        /* Title styling */
        .main-title {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }

        .sub-title {
            text-align: center;
            color: #94a3b8;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        /* Card box */
        .result-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem 2rem;
            margin-top: 1rem;
            backdrop-filter: blur(10px);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e1b4b, #312e81);
            border-right: 1px solid rgba(255,255,255,0.1);
        }

        /* Button */
        .stButton > button {
            background: linear-gradient(90deg, #7c3aed, #2563eb);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            width: 100%;
            transition: 0.3s;
        }

        .stButton > button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.6);
        }

        /* Input field */
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            padding: 0.6rem 1rem;
        }

        /* Divider */
        hr {
            border-color: rgba(255,255,255,0.1);
        }

        /* Metric cards */
        .metric-box {
            background: rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 👨‍💻 Developer")
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:4rem;'>🧑‍🎓</div>
        <h3 style='color:#a78bfa; margin:0.5rem 0;'>Muhammad Ahmad</h3>
        <p style='color:#94a3b8; font-size:0.85rem;'>AI Researcher & Expert</p>
        <p style='color:#60a5fa; font-size:0.85rem;'>IUB — 6th Semester</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### ⚙️ Model Settings")
    model_choice = st.selectbox(
        "Select Groq Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
        index=0
    )
    temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.3, 0.05)

    st.markdown("---")
    st.markdown("### 📊 About This App")
    st.markdown("""
    <p style='color:#94a3b8; font-size:0.85rem;'>
    This AI-powered research assistant uses <b>CrewAI</b> multi-agent framework
    with <b>Groq</b> LLMs to generate detailed research reports on any topic.
    </p>
    """, unsafe_allow_html=True)

# --- Main Header ---
st.markdown('<p class="main-title">🤖 Agentic Research Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Powered by CrewAI · Groq LLMs · Multi-Agent Intelligence</p>', unsafe_allow_html=True)
st.markdown("---")

# --- Stats Row ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class='metric-box'>
        <div style='font-size:1.8rem'>🧠</div>
        <div style='color:#a78bfa; font-weight:700'>Multi-Agent</div>
        <div style='color:#94a3b8; font-size:0.8rem'>CrewAI Framework</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class='metric-box'>
        <div style='font-size:1.8rem'>⚡</div>
        <div style='color:#60a5fa; font-weight:700'>Ultra Fast</div>
        <div style='color:#94a3b8; font-size:0.8rem'>Groq Inference</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class='metric-box'>
        <div style='font-size:1.8rem'>📄</div>
        <div style='color:#34d399; font-weight:700'>5 Key Findings</div>
        <div style='color:#94a3b8; font-size:0.8rem'>Structured Report</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Input ---
topic = st.text_input(
    "🔍 Enter Research Topic:",
    placeholder="e.g. Artificial Intelligence in 2026"
)

st.markdown("<br>", unsafe_allow_html=True)
generate = st.button("🚀 Generate Research Report")

# --- Logic ---
if generate:
    if not api_key:
        st.error("❌ API Key missing! Please check your .env file.")
    elif not topic.strip():
        st.warning("⚠️ Please enter a research topic first.")
    else:
        try:
            with st.status("🤖 AI Agents are working...", expanded=True) as status:
                st.write("🧠 Initializing LLM...")
                time.sleep(0.5)

                # ✅ FIXED: CrewAI native LLM - no ChatGroq object needed
                os.environ["GROQ_API_KEY"] = api_key
                llm = LLM(
                    model=f"groq/{model_choice}",
                    temperature=temperature
                )

                st.write("👨‍🔬 Spawning Research Agent...")
                time.sleep(0.3)

                researcher = Agent(
                    role='Senior Research Analyst',
                    goal=f'Find comprehensive and detailed insights about: {topic}',
                    backstory=(
                        "You are a world-class research analyst with deep expertise in "
                        "technology, science, and emerging trends. You produce clear, "
                        "structured, and insightful reports."
                    ),
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                st.write("📋 Defining Research Task...")
                time.sleep(0.3)

                research_task = Task(
                    description=(
                        f"Conduct a thorough research on: '{topic}'.\n"
                        "Cover the latest trends, breakthroughs, challenges, and future outlook.\n"
                        "Structure your findings clearly."
                    ),
                    expected_output=(
                        "A well-structured research report with:\n"
                        "1. Overview\n"
                        "2. 5 Key Findings\n"
                        "3. Challenges\n"
                        "4. Future Outlook\n"
                        "5. Conclusion"
                    ),
                    agent=researcher
                )

                st.write("⚙️ Running CrewAI Pipeline...")

                crew = Crew(
                    agents=[researcher],
                    tasks=[research_task],
                    process=Process.sequential
                )

                result = str(crew.kickoff())
                status.update(label="✅ Research Complete!", state="complete")

            # --- Result Display ---
            st.markdown("---")
            st.markdown("### 📄 Research Report")
            st.markdown(f"""
            <div class='result-card'>
                {result.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Download button
            st.download_button(
                label="⬇️ Download Report",
                data=result,
                file_name=f"research_{topic[:30].replace(' ', '_')}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
            st.info("💡 Tip: Make sure your GROQ_API_KEY is valid and crewai/langchain-groq are up to date.")

# --- Footer ---
st.markdown("---")
st.markdown("""
<p style='text-align:center; color:#64748b; font-size:0.85rem;'>
    Developed with ❤️ by <b style='color:#a78bfa;'>Muhammad Ahmad</b> · IUB 6th Semester · Powered by CrewAI & Groq
</p>
""", unsafe_allow_html=True)