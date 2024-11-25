import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import os

def get_course_name_from_google(course_code):
    query = f"KTU {course_code} course name"
    for result in search(query, num_results=5):
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            match = re.search(r"KTU\s+[A-Za-z\s]+", title)
            if match:
                course_name = match.group(0).replace("KTU", "").strip()
                return course_name
        except Exception as e:
            print(f"Failed to retrieve course name from {result}: {e}")
    return None

def format_course_url(course_code, course_name, alt_format=False):
    course_name_formatted = course_name.replace(" ", "-").lower()
    if alt_format:
        # Alternative URL format with separated alphabetic and numeric parts of the course code
        course_code_alpha = re.match(r'[A-Za-z]+', course_code).group()
        course_code_numeric = re.search(r'\d+', course_code).group()
        return f"https://www.ktunotes.in/ktu-{course_code_alpha.lower()}-{course_code_numeric}-{course_name_formatted}-solved-question-papers/"
    else:
        # Original URL format
        return f"https://www.ktunotes.in/ktu-{course_code.lower()}-{course_name_formatted}-solved-question-papers/"

def extract_file_id(drive_url):
    match = re.search(r'(file/d/|id=)([\w-]+)', drive_url)
    if match:
        return match.group(2)
    return None

def download_google_drive_file(file_id, save_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully and saved as {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def download_question_papers(course_code, download_folder):
    course_name = get_course_name_from_google(course_code)
    if course_name is None:
        print(f"Course name for code {course_code} not found.")
        return

    # Try the first URL format
    url = format_course_url(course_code, course_name)
    response = requests.get(url)
    
    # If the first URL format fails, try the alternative format
    if response.status_code != 200:
        print("First URL format failed. Trying alternative format.")
        url = format_course_url(course_code, course_name, alt_format=True)
        response = requests.get(url)

    # Check if either format was successful
    if response.status_code == 200:
        print(f"Formatted URL: {url}")

        # Create a folder for the course code if it doesn't already exist
        course_folder = os.path.join(download_folder, course_code)
        os.makedirs(course_folder, exist_ok=True)

        soup = BeautifulSoup(response.text, 'html.parser')
        question_links = []
        for link in soup.find_all('a', href=True):
            if 'drive.google.com' in link['href']:
                question_links.append(link['href'])
        
        if question_links:
            print("Question papers found:")
            for i, link in enumerate(question_links):
                file_id = extract_file_id(link)
                if file_id:
                    save_location = os.path.join(course_folder, f"{course_code}_{course_name.replace(' ', '_')}_{i+1}.pdf")
                    download_google_drive_file(file_id, save_location)
                else:
                    print(f"Failed to extract file ID from link: {link}")
        else:
            print("No Google Drive question papers found at this URL.")
    else:
        print("Failed to load the webpage with both URL formats. Please check the course code.")

if __name__ == "__main__":
    course_code = input("Enter the course code (e.g., 'MAT203'): ")
    download_folder = r"C:\Users\Kurian Tony Aloor\Downloads\KTU"  # Make sure this folder exists
    download_question_papers(course_code, download_folder)





