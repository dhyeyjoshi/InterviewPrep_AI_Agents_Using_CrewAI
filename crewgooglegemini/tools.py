import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, FileReadTool
import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool  # ✅ Required for CrewAI tools

# Load environment variables
load_dotenv()

# Set API keys
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

# ✅ Web Search Tool (Serper.dev)
search_tool = SerperDevTool()  # Fetches interview questions & study materials
# ✅ Automatically Find the JD.md File in Ref_Job_posting Directory
job_description_folder = "./Ref_Job_posting/"
jd_filename = None

# Search for a job description file inside the folder
if os.path.exists(job_description_folder):
    for file in os.listdir(job_description_folder):
        if file.lower().startswith("jd") and file.lower().endswith((".md", ".txt")):
            jd_filename = os.path.join(job_description_folder, file)
            break

# ✅ Initialize File Read Tool (If File Exists)
if jd_filename:
    print(f"📂 Job description file found: {jd_filename}")
    file_read_tool = FileReadTool(
        file_path=jd_filename,
        description=f'Reads the job description example file: {jd_filename}'
    )
else:
    print("⚠️ No job description file found. Proceeding without it.")
    file_read_tool = None 

def web_scraper(url: str) -> dict:
    """Scrapes detailed content from a webpage including headings, metadata, links, and structured text."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching the webpage: {e}"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract Title and Meta Description
    title = soup.title.string.strip() if soup.title else "No title found"
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_description["content"].strip() if meta_description else "No meta description found"

    # Extract Headings
    headings = {f"H{i}": [h.get_text(strip=True) for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

    # Extract all links (internal and external)
    links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]

    # Extract Tables (Convert table data into structured format)
    tables = []
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(cells)
        tables.append(rows)

    # Extract Main Text Content
    for script in soup(["script", "style"]):  # Remove JS and CSS
        script.extract()

    text = soup.get_text(separator="\n").strip()

    # Limit text output to 4000 characters for readability
    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "links": links[:20],  # Limit to first 20 links
        "tables": tables[:3],  # Limit to first 3 tables
        "text_content": text[:4000]  # Limit to 4000 characters
    }

# ✅ Convert Advanced Web Scraper Function into a CrewAI-Compatible Tool
web_scraper_tool = Tool(
    
    name="Advanced Web Scraper",
    func=web_scraper,
    description="Scrapes a webpage and extracts structured data including headings, metadata, links, tables, and main content."
)