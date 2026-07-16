import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests

# 1. Page Configuration (MUST BE FIRST)
st.set_page_config(
    page_title="The Archimedean", 
    page_icon="🏛️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- THE DYNAMIC PAYWALL ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 2px;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Premium Mathematical Workspace</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🔒 Enter your personal License Key to access the engine.")
        
        # Link to buy a new key (Replace with your actual Gumroad link)
        st.markdown("<a href='https://your-gumroad-store.gumroad.com/l/archimedean' target='_blank'><button style='width: 100%; padding: 10px; background-color: #5b5b5b; color: white; border: none; border-radius: 5px; cursor: pointer;'>💳 Purchase a Personal License Key</button></a>", unsafe_allow_html=True)
        st.markdown(" ")
        
        user_key = st.text_input("Enter License Key:", type="password", placeholder="XXXX-XXXX-XXXX-XXXX")
        
        if st.button("Unlock Engine", use_container_width=True):
            if user_key:
                with st.spinner("Verifying license..."):
                    try:
                        # Contact Gumroad to verify the specific key
                        payload = {
                            "product_permalink": st.secrets["gumroad_product_permalink"],
                            "license_key": user_key
                        }
                        response = requests.post("https://api.gumroad.com/v2/licenses/verify", data=payload)
                        data = response.json()
                        
                        # Check if the key is valid AND the subscription is active
                        if data.get("success") and not data.get("purchase", {}).get("subscription_cancelled_at"):
                            st.session_state.authenticated = True
                            st.rerun() # Unlocks the app!
                        else:
                            st.error("❌ Invalid, expired, or canceled license key.")
                    except Exception as e:
                        st.error("Error connecting to verification server. Please verify your Streamlit Secrets.")
            else:
                st.warning("Please enter a key.")
                
    st.stop() # Stops the rest of the app from loading
# --- END PAYWALL ---

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
    st.metric(label="Solutions Executed", value=st.session_state.problems_solved)
    st.metric(label="System Integrity", value="100%")
    
    st.markdown("---")
    st.caption('"Give me a place to stand, and a lever long enough, and I will move the world." - Archimedes')

# 3. Main Workspace Header
st.title("🏛️ The Archimedean Interface")
st.markdown("---")

# 4. Interface Tabs 
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Visual Solver", "💬 Formula Assistant", "📚 Reference Library", "🕒 Solution Archive"])

# --- TAB 1: THE CORE SOLVER ---
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
                output_container.warning("⚠️ Parameters required to execute solution.")
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
                            "title": user_problem[:40] + "..." if user_problem else "Visual Diagram Solution",
                            "solution": full_text
                        })
                        
                    except Exception as e:
                        output_container.error(f"Critical Fault: {e}")
        else:
            output_container.info("Awaiting parameters...")

# --- TAB 2: FORMULA ASSISTANT ---
with tab2:
    st.subheader("Query the Oracle")
    st.markdown("Ask for specific formulas, conceptual explanations, or general mathematical theory.")
    
    chat_container = st.container(border=True, height=500)
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    if prompt := st.chat_input("e.g., What is the steady-flow energy equation? or Explain nodal analysis..."):
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    model = genai.GenerativeModel('gemini-3.5-flash')
                    
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
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    
                except Exception as e:
                    message_placeholder.error(f"Connection Error: {e}")
                    full_response = "Error retrieving data."
                    
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

# --- TAB 4: SOLUTION ARCHIVE ---
with tab4:
    st.subheader("Session History log")
    if not st.session_state.history:
        st.caption("No solutions executed in current session.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Solution #{len(st.session_state.history) - idx} | {item['title']}"):
                st.markdown(item['solution'])
