import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="The Archimedean", 
    page_icon="📐", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize session states
if "history" not in st.session_state:
    st.session_state.history = []
if "problems_solved" not in st.session_state:
    st.session_state.problems_solved = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 2. Left Sidebar - The Archimedean Identity
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 2px;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-style: italic; font-size: 0.95rem;'>Absolute Mathematical Truth</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("⚙️ System Status")
    try:
        genai.configure(api_key=st.secrets["api_key"])
        st.success("🟢 Neural Core: ONLINE")
        st.caption("Engine: gemini-3.5-flash")
    except Exception:
        st.error("🔴 Neural Core: OFFLINE")
        st.caption("Missing API Key in Secrets")
    
    st.markdown("---")
    st.subheader("📊 Session Telemetry")
    st.metric(label="Theorems Proven", value=st.session_state.problems_solved)
    st.metric(label="System Integrity", value="100%")
    
    st.markdown("---")
    st.caption('"Give me a place to stand, and a lever long enough, and I will move the world." - Archimedes')

# 3. Main Workspace Header
st.title("📐 The Archimedean Interface")
st.markdown("---")

# 4. Interface Tabs (Added the new Assistant Tab)
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Visual Solver", "💬 Formula Assistant", "📚 Reference Library", "🕒 Theorem Archive"])

# --- TAB 1: THE CORE SOLVER (For specific, heavy problems) ---
with tab1:
    col_input, col_output = st.columns([1, 1.2]) 
    
    with col_input:
        st.subheader("Define Parameters")
        uploaded_file = st.file_uploader(
            "Upload System Diagram or Equation", 
            type=["png", "jpg", "jpeg"]
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Visual Data Registered", use_column_width=True)

        user_problem = st.text_area(
            "Set System Constraints & Variables:", 
            height=120,
            placeholder="e.g., Define boundaries for integration, or detail physical forces..."
        )
        solve_button = st.button("⚡ Execute Solution", use_container_width=True, type="primary")

    with col_output:
        st.subheader("Terminal Output")
        output_container = st.container(border=True, height=600) 
        
        if solve_button:
            if not uploaded_file and not user_problem:
                output_container.warning("⚠️ Parameters required to execute proof.")
            else:
                output_placeholder = output_container.empty()
                with st.spinner("Synthesizing mathematical truth..."):
                    try:
                        model = genai.GenerativeModel('gemini-3.5-flash')
                        contents = [
                            """You are the Archimedean computational engine. Solve the provided STEM problem step-by-step.
                            1. Define Initial States & Variables.
                            2. State Governing Equations.
                            3. Show mathematical derivations using strict LaTeX.
                            4. Highlight the final numerical truth.
                            """
                        ]
                        
                        if user_problem: contents.append(f"Constraints: {user_problem}")
                        if uploaded_file is not None: contents.append(image)
                        
                        response = model.generate_content(contents, stream=True)
                        full_text = ""
                        for chunk in response:
                            full_text += chunk.text
                            output_placeholder.markdown(full_text)
                        
                        st.session_state.problems_solved += 1
                        st.session_state.history.append({
                            "title": user_problem[:40] + "..." if user_problem else "Visual Diagram Proof",
                            "solution": full_text
                        })
                        
                    except Exception as e:
                        output_container.error(f"Critical Fault: {e}")
        else:
            output_container.info("Awaiting parameters...")

# --- TAB 2: FORMULA ASSISTANT (New Feature!) ---
with tab2:
    st.subheader("Query the Oracle")
    st.markdown("Ask for specific formulas, conceptual explanations, or general mathematical theory.")
    
    # Create a nice framed container for the chat history
    chat_container = st.container(border=True, height=500)
    
    with chat_container:
        # Render existing chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    # The Chat Input Box
    if prompt := st.chat_input("e.g., What is the steady-flow energy equation? or Explain nodal analysis..."):
        # Display user message immediately
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        # Save user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Generate and stream AI response
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    
                    # Custom system prompt for the chat assistant
                    chat_prompt = f"""
                    You are a highly advanced engineering and mathematics assistant.
                    Answer the following query clearly and concisely.
                    If asked for a formula, provide it using clean LaTeX formatting.
                    Provide brief, practical engineering context where applicable.
                    User Query: {prompt}
                    """
                    
                    response = model.generate_content(chat_prompt, stream=True)
                    for chunk in response:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌") # The ▌ adds a cool typing cursor effect
                    message_placeholder.markdown(full_response)
                    
                except Exception as e:
                    message_placeholder.error(f"Connection Error: {e}")
                    full_response = "Error retrieving data."
                    
        # Save AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# --- TAB 3: REFERENCE LIBRARY ---
with tab3:
    st.subheader("Fundamental Constants")
    st.markdown("Immutable truths for verifying physical simulations.")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("🔥 Thermodynamics"):
            st.markdown("- **Specific Heat (Water):** $4.184 \\text{ kJ/kg\\cdot K}$")
            st.markdown("- **Gas Constant (R):** $8.314 \\text{ J/mol\\cdot K}$")
    with col2:
        with st.expander("⚙️ Mechanics"):
            st.markdown("- **Gravity (g):** $9.81 \\text{ m/s}^2$")
            st.markdown("- **Newton's Second Law:** $\\Sigma F = m \\cdot a$")
    with col3:
        with st.expander("⚡ Circuitry"):
            st.markdown("- **Ohm's Law:** $V = I \\cdot R$")
            st.markdown("- **KCL:** $\\Sigma I_{in} = \\Sigma I_{out}$")

# --- TAB 4: THEOREM ARCHIVE ---
with tab4:
    st.subheader("Session History log")
    if not st.session_state.history:
        st.caption("No proofs executed in current session.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Proof #{len(st.session_state.history) - idx} | {item['title']}"):
                st.markdown(item['solution'])
