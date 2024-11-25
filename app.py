from flask import Flask, render_template, request, jsonify
import os
from backend.download_script import download_question_papers

app = Flask(__name__)

# Ensure the downloads directory exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    course_code = data.get("course_code")
    
    # Call the function to scrape and download papers
    question_paper_links = download_question_papers(course_code)
    
    if question_paper_links:
        return jsonify(question_paper_links), 200
    else:
        return jsonify({"error": "No question papers found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
