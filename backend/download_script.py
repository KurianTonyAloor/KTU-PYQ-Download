import requests
from bs4 import BeautifulSoup
import re

def format_course_url(course_code):
    # Format the URL based on the course code
    url1 = f"https://www.ktunotes.in/ktu-{course_code.lower()}-solved-question-papers/"
    url2 = f"https://www.ktunotes.in/ktu-{course_code[:3].lower()}-{course_code[3:]}-solved-question-papers/"
    return [url1, url2]

def download_question_papers(course_code):
    # Try both URL formats
    question_paper_links = []
    for url in format_course_url(course_code):
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                if 'drive' in link['href']:  # Filter for Google Drive links
                    question_paper_links.append(link['href'])
            if question_paper_links:
                break

    return question_paper_links
