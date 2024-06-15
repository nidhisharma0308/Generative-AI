import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from google.api_core.exceptions import ResourceExhausted

# Load environment variables
load_dotenv()

# Configure Google API key for Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(input_text)
        return response.text
    except ResourceExhausted as e:
        return "Quota exceeded. Please try again later."

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit application
st.title("MCQ Generator")
st.text("Generate Multiple Choice Questions from PDF content")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf", help="Please upload the PDF")
num_questions = st.number_input("Number of questions", min_value=1, max_value=20, value=5)
difficulty_level = st.selectbox("Difficulty level", options=["easy", "medium", "hard"])

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        input_prompt = {
            "prompt": f'''
            You are an expert multiple choice question maker. You will read the given PDF content and make {num_questions} {difficulty_level} level multiple choice questions.
            PDF content: {pdf_text}
            ''',
            "template": {
                "1": {
                    "mcq": "multiple choice question",
                    "options": {
                        "a": "choice here",
                        "b": "choice here",
                        "c": "choice here",
                        "d": "choice here"
                    },
                    "correct": "correct answer"
                }
                # The remaining questions will follow the same format
            }
        }
        
        
        input_prompt_str = json.dumps(input_prompt)
        
        response = get_gemini_response(input_prompt_str)
        st.subheader("Generated MCQs")
        st.text(response)
