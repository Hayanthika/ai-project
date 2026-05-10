from flask import Flask, render_template, request
import os
import PyPDF2
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jobs = pd.read_csv("jobs.csv")

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Analyze Resume
@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read PDF
        text = ""

        with open(filepath, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            for page in reader.pages:
                text += page.extract_text()

        text = text.lower()

        matched_jobs = []

        for index, row in jobs.iterrows():

            skills = row['Skills'].lower().split(',')

            score = 0

            for skill in skills:
                if skill.strip() in text:
                    score += 1

            matched_jobs.append((row['Job Role'], score))

        matched_jobs.sort(key=lambda x: x[1], reverse=True)

        result = matched_jobs[:3]

        return f"""
        <h2>Top Recommended Jobs</h2>

        <ul>
            <li>{result[0]}</li>
            <li>{result[1]}</li>
            <li>{result[2]}</li>
        </ul>

        <a href="/">Go Back</a>
        """

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)