from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import fitz
import re
import pandas as pd

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_pdf_text(uploaded_file):
    uploaded_file.seek(0)
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def input_pdf_setup(uploaded_file):
    uploaded_file.seek(0)
    if uploaded_file is not None:
        poppler_path = r'C:\Users\HP\poppler\Release-25.07.0-0\poppler-25.07.0\Library\bin'
        images = pdf2image.convert_from_bytes(
            uploaded_file.read(),
            poppler_path=poppler_path
        )
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


def get_gemini_response_text(input_prompt, resume_text, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, resume_text, job_description])
    return response.text


def get_gemini_response_image(input_prompt, pdf_content, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, pdf_content[0], job_description])
    return response.text


st.set_page_config(page_title="ScoreFilter")
st.header("Resume-Optimizer")
input_text = st.text_area("Job Description: ", key="input")

uploaded_files = st.file_uploader("Upload resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"{len(uploaded_files)} resumes uploaded successfully!")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")
submit_improve = st.button("Suggest Improvements")
submit_rank = st.button("Rank All Resumes")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description.
  Please share your professional evaluation on whether the candidate's profile aligns with the role.
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt_improve = """
You are an expert career coach and senior technical recruiter. Your main task is to provide actionable advice to improve a resume based on a specific job description.

Based on the provided resume text and the job description, please provide the following:

1.  **Overall Summary:** A short, encouraging summary of how the resume can be better tailored for this job.
2.  **Key Missing Skills:** A bulleted list of important skills or technologies mentioned in the job description that are missing from the resume.
3.  **Actionable Suggestions for Improvement:** A numbered list of specific, concrete suggestions. For each suggestion, explain *why* it's important and give an example of *how* the user could rephrase a sentence or add a bullet point. For instance, instead of just saying 'add Python', suggest 'In your project about the analysis dashboard, you should mention the specific Python libraries you used, like Pandas and Matplotlib, to showcase your technical depth.'
"""

if submit1:
    if uploaded_files:
        st.info("Processing the first uploaded resume...")
        first_file = uploaded_files[0]
        pdf_content = input_pdf_setup(first_file)
        response = get_gemini_response_image(input_prompt1, pdf_content, input_text)
        st.subheader("The Response for " + first_file.name)
        st.write(response)
    else:
        st.write("Please upload at least one resume.")

elif submit3:
    if uploaded_files:
        st.info("Processing the first uploaded resume...")
        first_file = uploaded_files[0]
        pdf_content = input_pdf_setup(first_file)
        response = get_gemini_response_image(input_prompt3, pdf_content, input_text)
        st.subheader("The Response for " + first_file.name)
        st.write(response)
    else:
        st.write("Please upload at least one resume.")

elif submit_improve:
    if uploaded_files:
        st.info("Processing the first uploaded resume...")
        first_file = uploaded_files[0]
        resume_text = get_pdf_text(first_file)
        response = get_gemini_response_text(input_prompt_improve, resume_text, input_text)
        st.subheader("Suggestions for " + first_file.name)
        st.write(response)
    else:
        st.write("Please upload at least one resume.")

elif submit_rank:
    if uploaded_files:
        all_results = []
        st.write("Processing and ranking all resumes... Please wait.")
        progress_bar = st.progress(0)

        for i, uploaded_file in enumerate(uploaded_files):
            try:
                resume_text = get_pdf_text(uploaded_file)
                
                response_text = get_gemini_response_text(input_prompt3, resume_text, input_text)

                match = re.search(r'(\d+)\s*%', response_text)
                score = int(match.group(1)) if match else 0

                all_results.append({
                    "Resume Filename": uploaded_file.name,
                    "Match Score (%)": score,
                    "AI Summary": response_text
                })

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
                all_results.append({
                    "Resume Filename": uploaded_file.name,
                    "Match Score (%)": 0,
                    "AI Summary": "Error processing this file."
                })

            progress_bar.progress((i + 1) / len(uploaded_files))

        ranked_resumes = sorted(all_results, key=lambda x: x["Match Score (%)"], reverse=True)

        st.subheader("Ranked Resume Results")
        df = pd.DataFrame(ranked_resumes)
        df.index = df.index + 1
        st.dataframe(df)

    else:
        st.write("Please upload at least one resume to rank.")