import streamlit as st
import google.generativeai as genai
import random

# 1. Page Configuration
st.set_page_config(page_title="The Archimedean | Premium", page_icon="🏛️", layout="wide")

# Initialize Session State
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "problems_solved" not in st.session_state: st.session_state.problems_solved = 0

# --- AUTHENTICATION GATE (The Landing Page) ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>ARCHIMEDEAN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Login")
            user_input = st.text_input("Enter Access Password", type="password")
            if st.button("Unlock Engine", use_container_width=True, type="primary"):
                # Compare input against your secret password
                if user_input == st.secrets["access_password"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
            
            st.markdown("---")
            st.caption("Don't have access? [Buy here](https://your-gumroad-link.com)")
    st.stop()

# --- MAIN APP (Rest of your app code below) ---
# [Keep the rest of your app code here exactly as it was]
