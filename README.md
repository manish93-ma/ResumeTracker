# Resume Ranker 🎯  

An **AI-powered Applicant Tracking System (ATS)** using **Google Gemini** to analyze, score, and rank resumes against job descriptions.  

## 🚀 Key Features  

- 🔄 **Batch Processing & Ranking** – Upload and rank multiple resumes against a single job description.  
- 🤖 **AI-Powered Scoring** – Get a percentage match score to quickly identify top candidates.  
- 📝 **Actionable Feedback** – AI-generated resume improvement suggestions tailored for the role.  
- 🎨 **Simple Web Interface** – Clean and user-friendly design built with **Streamlit**.  

---

## 🛠 Tech Stack  

- **Frontend / UI**: Streamlit  
- **AI Model**: Google Gemini  
- **Backend / Processing**: Python, Pandas, PyMuPDF, pdf2image  
- **Environment Management**: python-dotenv  

---

## ⚡ Quick Start  

Run the project locally by following these steps:  

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-username/resume-ranker.git
cd resume-ranker
2️⃣ Create requirements.txt
streamlit
google-generativeai
python-dotenv
PyMuPDF
pandas
pdf2image
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Set Up API Key
Create a .env file in the root directory and add your API key:

env
GEMINI_API_KEY="YOUR_API_KEY_HERE"


bash
Copy code
streamlit run app.py
