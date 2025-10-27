import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

# Configure Gemini API
genai.configure(api_key="Your_Gemini_API_Key_Here")

model = genai.GenerativeModel("gemini-2.5-flash")


# Function to read PDF
def read_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to read TXT
def read_txt(file):
    return file.read().decode("utf-8")

# Streamlit interface
st.title("File-based QnA Bot")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        file_text = read_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        file_text = read_txt(uploaded_file)
    else:
        st.error("Unsupported file type")
        file_text = ""
    
    user_question = st.text_input("Ask a question about the uploaded file")

    if user_question:
        # Role / system prompt
        system_prompt = (
            "You are a helpful document assistant. "
            "Answer the user's question ONLY based on the file content provided. "
            "If the answer is not in the file, respond honestly that you don't know."
        )

        # Full prompt
        prompt = f"{system_prompt}\n\nFile Content:\n{file_text}\n\nUser Question: {user_question}"

        try:
            response = model.generate_content(prompt)
            ai_message = response.text or "(No text returned)"
        except Exception as e:
            ai_message = f"Error: {str(e)}"

        st.write("Answer:")
        st.write(ai_message)
