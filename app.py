import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration & Custom Theme Hints
st.set_page_config(
    page_title="OmniSolve AI", 
    page_icon="⚡", 
    layout="centered"
)

# App Header with a clean, modern subtitle
st.markdown("<h1 style='text-align: center;'>⚡ OmniSolve AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 1.2rem;'>Advanced Engineering & Mathematics Visual Solver</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. Configure the AI using Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["api_key"])
except Exception:
    st.error("🔒 Configuration Profile Needed: Please set 'api_key' in your Streamlit Secrets.")

# 3. Clean Workspace Layout
st.subheader("📋 Step 1: Input Your Problem")

# Modern drag-and-drop / upload zone
uploaded_file = st.file_uploader(
    "Drop an image, screenshot, or photo of the problem here", 
    type=["png", "jpg", "jpeg"]
)

# Context or text box inside an expander to save screen space
with st.expander("✏️ Add optional text or specific instructions"):
    user_problem = st.text_area(
        "Type any extra context, specific constraints, or clarify variables here:", 
        height=100,
        placeholder="e.g., Use gravity g = 9.81 m/s^2 or evaluate using Green's Theorem..."
    )

st.markdown(" ") # Spacer

# 4. Action Section
if st.button("🚀 Generate Step-by-Step Solution", use_container_width=True):
    if not uploaded_file and not user_problem:
        st.info("💡 Please upload an image or type a problem to begin.")
    else:
        st.markdown("---")
        st.subheader("✨ Step 2: Live AI Analysis")
        
        # Display the uploaded image immediately in a clean frame
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Problem Blueprint", use_column_width=True)
        
        # Create a premium styled container for the streaming output
        output_container = st.container(border=True)
        output_placeholder = output_container.empty()
        
        with st.spinner("Analyzing parameters and computing solution..."):
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                
                contents = [
                    """You are an elite mechanical engineering and advanced mathematics professor. 
                    Solve the provided problem step-by-step with absolute precision.
                    
                    Structure your answer perfectly using markdown:
                    - Use clear headings (##) for each step (e.g., Given Parameters, Governing Equations, Step-by-Step Derivation, Final Verification).
                    - Highlight final key values.
                    - Format all complex math/science equations using strict LaTeX formatting.
                    """
                ]
                
                if user_problem:
                    contents.append(f"User request: {user_problem}")
                if uploaded_file is not None:
                    contents.append(image)
                
                # Stream the content
                response = model.generate_content(contents, stream=True)
                
                full_text = ""
                for chunk in response:
                    full_text += chunk.text
                    # Dynamically render into the framed container
                    output_placeholder.markdown(full_text)
                    
            except Exception as e:
                st.error(f"Execution Error: {e}")
