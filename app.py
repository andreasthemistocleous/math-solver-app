import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# 1. Page Configuration
st.set_page_config(
    page_title="The Archimedean", 
    page_icon="🏛️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "history" not in st.session_state: st.session_state.history = []
if "problems_solved" not in st.session_state: st.session_state.problems_solved = 0
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# --- QUOTE REPOSITORY ---
quotes = [
    '"Give me a place to stand, and a lever long enough, and I will move the world." - Archimedes',
    '"Mathematics is the queen of the sciences." - Carl Friedrich Gauss',
    '"The book of nature is written in the language of mathematics." - Galileo Galilei',
    '"Pure mathematics is, in its way, the poetry of logical ideas." - Albert Einstein',
    '"There is no royal road to geometry." - Euclid',
    '"What we know is a drop, what we don\'t know is an ocean." - Isaac Newton',
    '"Nature is an infinite sphere of which the center is everywhere and the circumference nowhere." - Blaise Pascal',
    '"Number rules the universe." - Pythagoras',
    '"God used beautiful mathematics in creating the world." - Paul Dirac'
]

# Randomly select two unique quotes
q1, q2 = random.sample(quotes, 2)

# 2. Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 2px;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("⚙️ System Status")
    try:
        genai.configure(api_key=st.secrets["api_key"])
        st.success("🟢 Neural Core: ONLINE")
    except:
        st.error("🔴 Neural Core: OFFLINE")
    st.metric(label="Solutions Executed", value=st.session_state.problems_solved)

# 3. Header with Dynamic Quotes
st.markdown(f"<p style='text-align: center; font-style: italic; color: #555;'>{q1}</p>", unsafe_allow_html=True)
st.title("🏛️ The Archimedean Interface")
st.markdown(f"<p style='text-align: center; font-style: italic; color: #555;'>{q2}</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Visual Solver", "💬 Formula Assistant", "📚 Reference Library", "🕒 Solution Archive"])

with tab1:
    col_input, col_output = st.columns([1, 1.2])
    with col_input:
        uploaded_file = st.file_uploader("Upload Diagram", type=["png", "jpg"])
        user_problem = st.text_area("Constraints/Problem Details:", height=150)
        solve_button = st.button("⚡ Execute Solution", type="primary")
    with col_output:
        output_container = st.container(border=True, height=500)
        if solve_button:
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                response = model.generate_content(["Act as an expert STEM tutor. Solve the following problem step-by-step with LaTeX formatting:", user_problem])
                output_container.markdown(response.text)
                st.session_state.problems_solved += 1
            except Exception as e:
                output_container.error(f"Fault: {e}")

with tab2:
    st.markdown("### 💬 Formula & Theory Oracle")
    chat_container = st.container(border=True, height=450)
    if prompt := st.chat_input("Ask about A-Level/IGCSE Physics or Math concepts..."):
        with chat_container:
            st.chat_message("user").markdown(prompt)
            model = genai.GenerativeModel('gemini-3.5-flash')
            response = model.generate_content(f"Explain this engineering/math concept for an A-level student: {prompt}")
            st.chat_message("assistant").markdown(response.text)

with tab3:
    st.subheader("📚 A-Level/IGCSE Syllabus Formulas")
    search = st.text_input("🔍 Search Formulas (e.g. 'Kinematics', 'Electricity', 'Integration')").lower()
    
    # Comprehensive Syllabus Library
    syllabus = {
        "📐 Pure Math": [("Quadratic", "$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$"), ("Sine Rule", "$\\frac{a}{\\sin A} = \\frac{b}{\\sin B}$"), ("Differentiation", "$\\frac{d}{dx}x^n = nx^{n-1}$")],
        "🚀 Kinematics": [("Displacement", "$s = ut + 0.5at^2$"), ("Velocity Squared", "$v^2 = u^2 + 2as$"), ("Angular Velocity", "$\\omega = 2\\pi f$")],
        "⚙️ Dynamics": [("Newton's 2nd Law", "$\\Sigma F = ma$"), ("Momentum", "$p = mv$"), ("Hooke's Law", "$F = kx$")],
        "🔥 Thermodynamics": [("Ideal Gas", "$pV = nRT$"), ("Specific Heat", "$Q = mc\\Delta T$"), ("Latent Heat", "$Q = mL$")],
        "⚡ Electricity": [("Ohm's Law", "$V = IR$"), ("Power", "$P = IV$"), ("Capacitance", "$C = Q/V$"), ("Series Resistors", "$R_T = \\Sigma R$")],
        "🌊 Waves & Quantum": [("Wave Speed", "$v = f\\lambda$"), ("Photon Energy", "$E = hf$"), ("De Broglie", "$\\lambda = h/p$")]
    }
    
    for cat, items in syllabus.items():
        if search in cat.lower() or any(search in name.lower() for name, _ in items):
            with st.expander(cat, expanded=True):
                for name, eq in items: st.markdown(f"- **{name}:** {eq}")

with tab4:
    st.subheader("🕒 Session History")
    for log in reversed(st.session_state.history):
        st.write(log)
