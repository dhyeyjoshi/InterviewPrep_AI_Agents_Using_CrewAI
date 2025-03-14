from crewai import Crew, Process
from agents import all_agents
from tasks import all_tasks
import os
from dotenv import load_dotenv

load_dotenv()

# Get user input for company and position
company = input("Enter the company you are interviewing with: ").strip()
position = input("Enter the job position: ").strip()

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# Display Interview Process Start
print(f"\n🚀 Preparing your mock interview for {position} at {company}...\n")

# Ensure company and position values are passed into all tasks
for task in all_tasks:
    task.description = task.description.format(company=company, position=position)
    task.expected_output = task.expected_output.format(company=company, position=position)

# Assemble the Crew
interview_prep_crew = Crew(
    agents=all_agents,
    tasks=all_tasks,
    process=Process.sequential,
    verbose=True,
    planning=True
)

# Start Interview Process
if __name__ == "__main__":
    try:
        interview_prep_crew.kickoff()
    except Exception as e:
        print(f"\n❌ Error encountered: {str(e)}")
