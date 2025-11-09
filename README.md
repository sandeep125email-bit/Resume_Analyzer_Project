🧠 AI Resume Analyzer (Flask Project)

🚀 A smart web app built with Python (Flask) that compares your Resume with a Job Description and gives a Match Score based on skills, helping job seekers identify gaps before applying!

🔍 Features

✅ Upload files in PDF, DOCX, or TXT format
✅ Extracts text automatically from uploaded files
✅ Detects technical and soft skills
✅ Displays:

Match Score (%)

Common Skills

Missing Skills
✅ Generates a downloadable PDF report
✅ Simple and clean web interface built using HTML + CSS

🛠️ Tech Stack
Category	Technologies
💻 Backend	Python, Flask
📄 File Processing	PyPDF2, python-docx
🧾 Report Generation	ReportLab
🎨 Frontend	HTML, CSS
⚙️ Version Control	Git, GitHub
📂 Project Structure
Resume_Analyzer_Project/
│
├── app.py
├── requirements.txt
│
├── templates/
│   ├── index.html
│   └── result.html
│
└── static/
    └── style.css

⚙️ Setup Instructions (Run Locally)
# Clone this repository
git clone https://github.com/sandeep125email-bit/Resume_Analyzer_Project.git

# Navigate to the folder
cd Resume_Analyzer_Project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py


Then open your browser and go to 👉 http://127.0.0.1:5000

🧾 Sample Output
1️⃣ Upload Page

Upload your Resume (PDF/DOCX/TXT) and Job Description, then click “Analyze Match”

2️⃣ Result Page

Match Score: 75%

Common Skills: Python, Flask, SQL

Missing Skills: React, Communication

3️⃣ Download Report

Generate a detailed PDF report of your results

💡 Future Enhancements

🔹 Add NLP-based keyword extraction
🔹 Display a bar graph for Match Score
🔹 Support cloud deployment on Render or PythonAnywhere
🔹 Include job title and summary matching

👨‍💻 Developer

Kanchanpally Sandeep
🎓 B.Tech Student | 💻 AI & Web Development Enthusiast

📧 Email: sandeep.125.email@gmail.com

🔗 LinkedIn

🐙 GitHub

🏷️ Hashtags

#Python #Flask #MachineLearning #DataScience #WebDevelopment #AI #ResumeAnalyzer #FlaskProject #GitHub #OpenSource

✅ Example Commit Message for README Upload

Once you paste this file, open your VS Code terminal and run:

git add README.md
git commit -m "Added professional README for Resume Analyzer project"
git push