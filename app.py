import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Set up the Web Page
st.set_page_config(page_title="Engineering Math Solver", page_icon="⚙️")
st.title("⚙️ Engineering Math Solver")
st.write("Upload a picture of your problem or type it out to get a step-by-step solution.")

# 2. Secure API Key Input
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

# 3. User Input Area (Image + Text)
uploaded_file = st.file_uploader("Upload or paste an image of the problem here:", type=["png", "jpg", "jpeg"])
user_problem = st.text_area("Or type additional instructions/context here (optional):", height=100)

# 4. The Solving Logic
if st.button("Solve Problem"):
    if not api_key:
        st.warning("Please enter your API key in the sidebar first.")
    elif not uploaded_file and not user_problem:
        st.warning("Please upload an image or type a problem.")
    else:
        with st.spinner("Analyzing image and calculating step-by-step solution..."):
            try:
                # Configure the AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Build the request package
                contents = [
                    """You are an expert mechanical engineering and advanced mathematics tutor. 
                    Solve the provided problem step-by-step. 
                    1. Define all variables. 
                    2. Show the exact equations used. 
                    3. Provide the final numerical answer. 
                    Format all mathematics using strict LaTeX so it renders perfectly."""
                ]
                
                # Add text if they typed any
                if user_problem:
                    contents.append(f"User text: {user_problem}")
                
                # Add the image if they uploaded one
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Your Problem", use_column_width=True)
                    contents.append(image)
                
                # Call the AI and display the result
                response = model.generate_content(contents)
                st.success("Solution Found!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
