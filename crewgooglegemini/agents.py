from crewai import Agent
from tools import search_tool, web_scraper_tool, file_read_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# Initialize Google Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 1️⃣ Job Analysis Agent
job_analysis_agent = Agent(
    role="Job Analyst",
    goal="Fetch job description details for {company} and {position} using the provided reference file. "
         "If the file is available, extract job details directly and pass them to the next agent. "
         "Otherwise, research the role online using trusted sources.",
    backstory="An expert in analyzing job descriptions, extracting key details, and structuring role-specific insights.",
    tools=[file_read_tool, search_tool, web_scraper_tool],  # ✅ Uses File Read Tool first
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=True
)

# 2️⃣ Technical Interviewer Agent
technical_interviewer = Agent(
    role="Senior Technical Interviewer",
    goal="Retrieve and generate a list of easy to hard-level technical interview questions and answers for {position} at {company}, along with expertly crafted ideal responses.",
    backstory="A seasoned technical expert with years of industry experience, adept at crafting and evaluating challenging interview questions to assess candidates' problem-solving skills, technical depth, and real-world expertise.",
    tools=[file_read_tool,search_tool, web_scraper_tool],
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=True,
)

# 3️⃣ Behavioral Interviewer Agent
behavioral_interviewer = Agent(
    role="Senior Behavioral Interviewer",
    goal="Retrieve and generate a list of behavioral interview questions tailored for {position} at {company}, "
         "along with expertly crafted ideal responses based on industry best practices and the STAR method. "
         "If external data cannot be retrieved, generate questions purely based on the provided job role context.",
    backstory="A skilled HR professional with a keen eye for talent, dedicated to assessing candidates, "
              "providing insightful feedback, and fostering professional growth.",
    tools=[file_read_tool,search_tool,web_scraper_tool],  # Remove web_scraper_tool if unnecessary
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=True,
)

researcher_agent = Agent(
    role="Interview Preparation Researcher",
    goal="Find and compile a **comprehensive set of resources** to prepare for an interview at {company} for {position}.",
    backstory=(
        "An expert researcher with years of experience in sourcing the best learning materials, interview guides, "
        "and resources from various platforms, ensuring candidates are well-prepared."
    ),
    tools=[file_read_tool,search_tool,web_scraper_tool],
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=True
)

# 4️⃣ Master Evaluator Agent (Final Report Generator)
master_agent = Agent(
    role="Master Evaluator",
    goal="Summarize and compile a structured final interview report, including company information, a list of technical questions given by Senior Technical Interviewer above, also a list of behavioral questions given by Senior Behavioral Interviewer, with ideal answers, and an overall candidate evaluation.",
    backstory="An AI-driven evaluator responsible for structuring interview data into a detailed final report, ensuring clarity and valuable insights for candidate preparation.",
    tools=[file_read_tool,search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# List of all agents
all_agents = [job_analysis_agent, technical_interviewer, behavioral_interviewer,researcher_agent, master_agent]
