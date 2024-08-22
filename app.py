from flask import Flask, request, render_template
import PyPDF2
import openai
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv()

# Get the API key from the environment
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_questions(text):
    """Generate questions from text using OpenAI's GPT model."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate questions from the following text:\n\n{text}",
        max_tokens=150,
        n=5,  # Generate 5 questions
        stop=None
    )
    questions = response.choices[0].text.strip().split('\n')
    return questions

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/generate', methods=['POST'])
def generate():
    file = request.files['file']
    text = extract_text_from_pdf(file)
    questions = generate_questions(text)
    return render_template('results.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
