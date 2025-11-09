from flask import Flask, render_template, request, send_file
import PyPDF2
import re
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document

app = Flask(__name__)

SKILLS = ["Python", "Flask", "Django", "Machine Learning", "Deep Learning",
          "HTML", "CSS", "JavaScript", "SQL", "Pandas", "Numpy", "NLP",
          "Java", "C++", "React", "Data Science", "AI", "Communication", "Leadership"]

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def analyze_text_for_skills(text):
    return [s for s in SKILLS if re.search(rf"\b{s}\b", text, re.IGNORECASE)]

def calculate_match(resume_skills, jd_skills):
    common = set(resume_skills) & set(jd_skills)
    if not jd_skills:
        return 0, []
    score = round(len(common) / len(jd_skills) * 100, 2)
    return score, list(common)

latest = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global latest
    resume = request.files.get('resume')
    jd = request.files.get('jobdesc')

    if not resume or not jd:
        return "Please upload both files", 400

    os.makedirs("uploads", exist_ok=True)
    resume_path = os.path.join("uploads", resume.filename)
    jd_path = os.path.join("uploads", jd.filename)
    resume.save(resume_path)
    jd.save(jd_path)

    if resume.filename.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume.filename.lower().endswith(".docx"):
        resume_text = extract_text_from_docx(resume_path)
    else:
        resume_text = extract_text_from_txt(resume_path)

    if jd.filename.lower().endswith(".pdf"):
        jd_text = extract_text_from_pdf(jd_path)
    elif jd.filename.lower().endswith(".docx"):
        jd_text = extract_text_from_docx(jd_path)
    else:
        jd_text = extract_text_from_txt(jd_path)

    resume_skills = analyze_text_for_skills(resume_text)
    jd_skills = analyze_text_for_skills(jd_text)
    match_score, common_skills = calculate_match(resume_skills, jd_skills)
    missing = [s for s in jd_skills if s not in common_skills]

    latest = {
        "match_score": match_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "common_skills": common_skills,
        "missing_skills": missing
    }

    return render_template('result.html', **latest)

@app.route('/download_report')
def download_report():
    if not latest:
        return "No results yet", 400
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(150, 750, "AI Resume Analyzer Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, f"Match Score: {latest['match_score']}%")
    y = 700
    pdf.drawString(50, y, "Common Skills:")
    y -= 20
    for s in latest["common_skills"]:
        pdf.drawString(70, y, f"- {s}")
        y -= 15
    y -= 10
    pdf.drawString(50, y, "Missing Skills:")
    y -= 20
    for s in latest["missing_skills"]:
        pdf.drawString(70, y, f"- {s}")
        y -= 15
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Resume_Report.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
