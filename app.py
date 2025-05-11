import streamlit as st
import google.generativeai as genai
import time

# Configure Gemini 
genai.configure(api_key='AIzaSyBFIWQgcwoI6OeNw7du1DC-DAJzIiHEiIk')  # 🔒 Replace with your actual key

# Model selection dropdown
MODEL_OPTIONS = {
    "Gemini 1.5 Pro (Latest)": "gemini-1.5-pro-latest",
    "Gemini Pro": "gemini-pro",
    "Gemini 1.5 Flash": "gemini-1.5-flash-latest"
}

# Set up the page
st.set_page_config(
    page_title="Gemini Text Generator",
    page_icon="✨",
    layout="centered"
)

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        list(MODEL_OPTIONS.keys()),
        index=1  # Default to Gemini Pro
    )
    st.caption("Note: 1.5 models may have higher rate limits")

# Main interface
st.title("✨ Advanced Gemini Text Generator")
model = genai.GenerativeModel(MODEL_OPTIONS[selected_model])

# Text input with session state
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""
    
prompt = st.text_area(
    "Enter your prompt:", 
    height=150,
    value=st.session_state.prompt,
    placeholder="Write a creative story about..."
)

# Generation parameters
with st.expander("Advanced Settings"):
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider(
            "Temperature", 
            0.0, 1.0, 0.7, 0.1,
            help="Controls randomness: Lower = more deterministic"
        )
    with col2:
        max_tokens = st.slider(
            "Max Output Tokens", 
            100, 2000, 1000, 100,
            help="Maximum length of the response"
        )

# Generation with retry logic
if st.button("Generate"):
    if not prompt.strip():
        st.error("Please enter a prompt")
    else:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with st.spinner(f"Generating with {selected_model}..."):
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=temperature,
                            max_output_tokens=max_tokens
                        )
                    )
                
                st.subheader("Generated Text")
                st.markdown(response.text)
                break
                
            except Exception as e:
                if "429" in str(e):
                    wait_time = 20 * (attempt + 1)
                    st.warning(f"Rate limited. Retry {attempt+1}/{max_retries} in {wait_time}s...")
                    time.sleep(wait_time)
                    st.rerun()
                else:
                    st.error(f"Error: {str(e)}")
                    break
        else:
            st.error("Failed after multiple retries. Try again later.")

# ... (rest of your existing UI elements for examples/instructions/footer)