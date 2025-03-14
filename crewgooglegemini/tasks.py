from crewai import Task
from tools import search_tool, web_scraper_tool, file_read_tool
from agents import job_analysis_agent, technical_interviewer, behavioral_interviewer, master_agent, researcher_agent
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
    
# 1️⃣ Job Analysis Task (Uses File First, Falls Back to Web Search)
job_analysis_task = Task(
    description=(
        "Retrieve job details for {position} at {company}. **If a reference job description file is provided, extract and summarize its contents.**\n"
        "If no file is available, conduct **in-depth research** to generate a structured job analysis using external sources.\n\n"

        "### 📝 **Step 1: Read from Job Description File (If Available)**\n"
        "   - Extract **job responsibilities, qualifications, skills, and expectations** from the provided file.\n"
        "   - Summarize the key insights and pass them to the next agents for personalized question generation.\n\n"

        "### 🔍 **Step 2: Conduct Web Research (If No File Provided)**\n"
        "   - **Company Overview & Culture:**\n"
        "     - Provide a **brief history** of {company}, including mission, vision, and key achievements.\n"
        "     - Highlight **core values, work culture, and hiring philosophy** for interview alignment.\n\n"

        "   - **Industry Trends & Market Position:**\n"
        "     - Analyze {company}'s **market presence, competitors, and recent developments**.\n"
        "     - Identify key industry trends and how they impact {position} within {company}.\n\n"

        "   - **Job Role Breakdown:**\n"
        "     - Provide a **detailed breakdown** of {position} responsibilities.\n"
        "     - Identify the **key skills, tools, and methodologies** required for success in this role.\n\n"

        "   - **Common Interview Process at {company}:**\n"
        "     - Outline the **standard interview stages** (phone screen, technical rounds, system design, etc.).\n"
        "     - Provide insights on **what interviewers look for** and how to prepare accordingly.\n\n"

        "   - **Required Skills & Learning Resources:**\n"
        "     - List the **top technical and soft skills** required for the role.\n"
        "     - Suggest **study materials, online courses, and company blogs** that help in preparation.\n\n"

        "   - **Insider Tips & Recent Hiring Patterns:**\n"
        "     - If available, summarize insights from **Glassdoor reviews, employee testimonials, and interview experiences**.\n"
        "     - Include common **hiring trends** at {company}, such as preferred candidate backgrounds and qualities.\n"
    ),
    expected_output=(
        "A **comprehensive job analysis report** for {position} at {company}, covering:\n"
        "- 📄 Job details extracted from a provided file (if available)\n"
        "- 🌍 Company Overview & Culture\n"
        "- 📊 Industry Trends & Market Position\n"
        "- 📌 Detailed Job Role Breakdown\n"
        "- 🎯 Interview Process Overview\n"
        "- 📚 Required Skills & Learning Resources\n"
        "- 🔥 Insider Tips & Recent Hiring Patterns\n"
    ),
    tools=[file_read_tool, search_tool, web_scraper_tool],  # ✅ Prioritizes File First, Then Web Search
    agent=job_analysis_agent
)


# 2️⃣ Technical Interview Task (Generating Questions & Answers)
generate_technical_questions_task = Task(
    description=(
        "Conduct an in-depth technical interview preparation for {position} at {company}. "
        "Follow these steps:\n\n"
        "1️⃣ **Identify Key Skills**: Analyze {position} job descriptions and industry requirements "
        "to determine the most relevant technical skills.\n\n"
        "2️⃣ **Generate Questions by Category**: Formulate **at least 20 technical questions** "
        "covering different skill areas:\n"
        "   - **Coding Challenges** (5+ questions)\n"
        "   - **Data Structures & Algorithms** (5+ questions)\n"
        "   - **System Design** (5+ questions)\n"
        "   - **Debugging & Optimization** (2-3 questions)\n"
        "   - **Databases & Query Optimization** (2-3 questions)\n\n"
        "3️⃣ **Provide Detailed Answers**: Each question should have a clear, well-structured answer "
        "including explanations, best practices, and example code where applicable.\n\n"
        "4️⃣ **Ensure Depth & Relevance**: Ensure the questions align with industry standards "
        "and the specific role’s job requirements.\n\n"
        "5️⃣ **Format the Output**: Structure the output into sections for clarity.\n\n"
        "This will create a **comprehensive technical interview guide** for {position} at {company}."
    ),
    expected_output="A structured document containing **at least 20 technical interview questions**, "
                    "grouped by skill categories, each with a **detailed answer and explanation** "
                    "for {position} at {company}.",
    tools=[file_read_tool, search_tool, web_scraper_tool],
    agent=technical_interviewer,
    output_file="Interview_prep/Technical_Q_A.md"
)


# 3️⃣ Behavioral Interview Task (Generating Questions & Model Answers)
generate_behavioral_questions_task = Task(
        description=(
        "Retrieve and generate a **comprehensive** list of **20 behavioral interview questions** "
        "tailored for {position} at {company}. Follow these structured steps:\n\n"

        "1️⃣ **Analyze the Role:** Identify the core competencies required for {position} at {company}, such as leadership, teamwork, adaptability, and problem-solving.\n"
        "2️⃣ **Company Insights:** If available, use {company}'s leadership principles, values, or culture to craft company-specific questions. If unavailable, rely on general behavioral frameworks.\n"
        "3️⃣ **Identify Key Behavioral Themes:** Ensure that the questions align with critical behavioral skills, including:\n"
        "   - Leadership & Ownership\n"
        "   - Communication & Conflict Resolution\n"
        "   - Problem-Solving & Decision Making\n"
        "   - Teamwork & Collaboration\n"
        "   - Adaptability & Handling Ambiguity\n"
        "   - Work Ethic & Time Management\n"
        "   - Innovation & Continuous Learning\n"
        "4️⃣ **STAR Method Integration:** Structure each question to encourage STAR method responses (Situation, Task, Action, Result).\n"
        "5️⃣ **Conversational & Engaging Format:** Frame responses in a **paragraph format** with a natural, conversational tone to simulate a real interview experience.\n"
        "6️⃣ **Include Ideal Responses:** Provide model answers based on industry best practices, demonstrating how an ideal candidate should answer.\n"
    ),
    expected_output=(
        "A **detailed list of 20 behavioral interview questions** for {position} at {company}, "
        "each with an ideal STAR-based response formatted in a **conversational and paragraph-style tone**."
    ),
    tools=[file_read_tool, search_tool,web_scraper_tool],  # No tool needed since we only need LLM output
    agent=behavioral_interviewer,
    output_file="Interview_prep/Behavioral_Q_A.md"
)

research_interview_prep_task = Task(
    description=(
        "Conduct extensive research to find the best resources available online for {position} at {company}. "
        "This should include study materials, interview guides, practice questions, real interview experiences, "
        "and insights from platforms like LinkedIn, Medium, Dev.to, Glassdoor, GitHub discussions, LeetCode, and InterviewBit.\n\n"
        
        "**Steps to follow:**\n"
        "1️⃣ Find **official** company resources, including blogs, job postings, and interview guides.\n"
        "2️⃣ Gather **LinkedIn posts/articles** from professionals discussing interview experiences at {company}.\n"
        "3️⃣ Research **GitHub discussions** and repositories with relevant projects for {position}.\n"
        "4️⃣ Extract **Glassdoor interview reviews** to get insight into past interview patterns at {company}.\n"
        "5️⃣ Search **technical blogs and Medium articles** that provide deep insights and real-life problem-solving.\n"
        "6️⃣ Retrieve **LeetCode, InterviewBit, and HackerRank questions** specifically tagged for {company} and {position}.\n"
        "7️⃣ Look for **Reddit discussions** where candidates have shared their interview journey.\n"
        "8️⃣ Fetch **any YouTube video links** where former candidates share interview insights.\n"
        "9️⃣ Verify all links to ensure they are **current and relevant**.\n"
        "🔟 Compile at least **50 high-quality links** covering all topics relevant to {position}.\n"
    ),
    expected_output=(
        "A **structured collection** of at least **50 links** containing **interview preparation resources** "
        "for {position} at {company}. The links should be grouped by source (LinkedIn, GitHub, Blogs, Glassdoor, etc.) "
        "and include a brief summary of what each resource contains."
    ),
    tools=[file_read_tool, search_tool, web_scraper_tool],
    agent=researcher_agent,
    output_file="Interview_prep/Resources_and_Material_to_Prepare_for_Interview.md"
)

# 4️⃣ Final Report Task (Master Evaluator)
generate_final_report_task = Task(
    description=(
        "Summarize all gathered **interview preparation material** into a structured, well-organized **final report** "
        "for {position} at {company}. Ensure it includes essential details and useful recommendations. "
        "Follow these structured steps to enhance its effectiveness:\n\n"

        "1️⃣ **Company & Role Analysis:** Provide a summary of {company}, its culture, values, and industry focus, "
        "along with key insights into the **responsibilities, required skills, and expectations** for {position}.\n\n"

        "2️⃣ **Technical Interview Preparation:**\n"
        "   - Present a **comprehensive list** of **10-15 technical interview questions** relevant to {position}.\n"
        "   - Include **detailed solutions and explanations** for each question.\n"
        "   - Highlight key concepts, best practices, and common mistakes to avoid.\n\n"

        "3️⃣ **Behavioral Interview Preparation:**\n"
        "   - Provide a **detailed list of 15-20 behavioral interview questions** tailored for {position} at {company}.\n"
        "   - Ensure questions are designed for **STAR method (Situation, Task, Action, Result) responses**.\n"
        "   - Offer **ideal answers** in a conversational tone, demonstrating best practices.\n\n"

        "4️⃣ **Industry-Specific Study Resources:**\n"
        "   - Compile a list of **handpicked study resources**, including online courses, books, and documentation.\n"
        "   - Include **official documentation links** (if applicable) for technical topics.\n"
        "   - Provide **relevant interview preparation links**, such as **Glassdoor**, LeetCode, and company career blogs.\n\n"

        "5️⃣ **System Design & Case Studies (If Applicable):**\n"
        "   - If {position} involves system design (e.g., Software Engineer, Data Architect), include **common system design problems**.\n"
        "   - Provide **best practices, solution frameworks, and sample high-level architectures**.\n\n"

        "6️⃣ **Final Preparation Checklist:**\n"
        "   - Summarize the **top 5-10 key takeaways** for the candidate.\n"
        "   - Provide a **step-by-step plan** to follow before the interview (mock interviews, practice problems, resume tips, etc.).\n\n"

        "7️⃣ **Personalized Recommendations:**\n"
        "   - If possible, suggest a **personalized preparation plan** based on the company’s interview style.\n"
        "   - Include common pitfalls and strategies for excelling in interviews at {company}.\n"
    ),
    expected_output=(
        "A **comprehensive interview preparation report** for {position} at {company}, including:\n"
        "- Company & Job Insights\n"
        "- Technical & Behavioral Interview Questions (with answers)\n"
        "- Industry-Specific Study Resources & Recommended Links\n"
        "- System Design & Case Studies (if applicable)\n"
        "- A Final Preparation Checklist & Personalized Strategies\n"
    ),
    tools=[file_read_tool, search_tool],
    agent=master_agent,
    async_execution=False,
    output_file="Interview_prep/Interview_Prep_guide.md"
)

# List of all tasks
all_tasks = [
    job_analysis_task,
    generate_technical_questions_task,
    generate_behavioral_questions_task,
    research_interview_prep_task,
    generate_final_report_task
]
