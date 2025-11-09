from flask import Flask, render_template, request, send_file
import PyPDF2
import re
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document  # to read Word files

app = Flask(__name__)

# List of technical & soft skills
SKILLS = ["Python", "Flask", "Django", "Machine Learning", "Deep Learning",
          "HTML", "CSS", "JavaScript", "SQL", "Pandas", "Numpy", "NLP",
          "Java", "C++", "React", "Data Science", "AI", "Communication", "Leadership"]

def extract_text_from_pdf(file_path):
    """Extract text from PDF files"""
    text = ""
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

def extract_text_from_docx(file_path):
    """Extract text from Word (.docx) files"""
    try:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text_from_txt(file_path):
    """Extract text from plain text (.txt) files"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading TXT: {e}"

def analyze_text_for_skills(text):
    """Find known skills in the given text"""
    found_skills = [skill for skill in SKILLS if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]
    return found_skills

def calculate_match_score(resume_skills, jd_skills):
    """Compare skills between resume and job description"""
    common = set(resume_skills).intersection(set(jd_skills))
    if len(jd_skills) == 0:
        return 0, []
    score = round((len(common) / len(jd_skills)) * 100, 2)
    return score, list(common)

latest_result = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global latest_result

    if 'resume' not in request.files or 'jobdesc' not in request.files:
        return "Please upload both Resume and Job Description files.", 400

    resume_file = request.files['resume']
    jd_file = request.files['jobdesc']

    if resume_file.filename == '' or jd_file.filename == '':
        return "Please select both files.", 400

    os.makedirs('uploads', exist_ok=True)
    resume_path = os.path.join('uploads', resume_file.filename)
    jd_path = os.path.join('uploads', jd_file.filename)
    resume_file.save(resume_path)
    jd_file.save(jd_path)

    # --- Extract text from Resume ---
    if resume_file.filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_file.filename.lower().endswith('.docx'):
        resume_text = extract_text_from_docx(resume_path)
    elif resume_file.filename.lower().endswith('.txt'):
        resume_text = extract_text_from_txt(resume_path)
    else:
        resume_text = extract_text_from_txt(resume_path)

    # --- Extract text from Job Description ---
    if jd_file.filename.lower().endswith('.pdf'):
        jd_text = extract_text_from_pdf(jd_path)
    elif jd_file.filename.lower().endswith('.docx'):
        jd_text = extract_text_from_docx(jd_path)
    elif jd_file.filename.lower().endswith('.txt'):
        jd_text = extract_text_from_txt(jd_path)
    else:
        jd_text = extract_text_from_txt(jd_path)

    # --- Analyze Skills ---
    resume_skills = analyze_text_for_skills(resume_text)
    jd_skills = analyze_text_for_skills(jd_text)

    match_score, common_skills = calculate_match_score(resume_skills, jd_skills)
    missing_skills = [skill for skill in jd_skills if skill not in common_skills]

    latest_result = {
        "match_score": match_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "common_skills": common_skills,
        "missing_skills": missing_skills
    }

    return render_template('result.html', **latest_result)


@app.route('/download_report')
def download_report():
    """Generate a PDF report of the results"""
    if not latest_result:
        return "No analysis found. Please analyze a resume first.", 400

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("AI Resume Analyzer Report")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(150, 750, "AI Resume Analyzer Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, f"Match Score: {latest_result['match_score']}%")

    y = 700
    pdf.drawString(50, y, "Common Skills:")
    y -= 20
    for skill in latest_result["common_skills"]:
        pdf.drawString(70, y, f"- {skill}")
        y -= 15

    y -= 10
    pdf.drawString(50, y, "Missing Skills:")
    y -= 20
    for skill in latest_result["missing_skills"]:
        pdf.drawString(70, y, f"- {skill}")
        y -= 15

    y -= 10
    pdf.drawString(50, y, "All Resume Skills:")
    y -= 20
    for skill in latest_result["resume_skills"]:
        pdf.drawString(70, y, f"- {skill}")
        y -= 15
        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="Resume_Report.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
