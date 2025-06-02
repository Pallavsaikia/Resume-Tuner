from crewai.project import CrewBase
from crewai.llm import LLM
from crewai.agent import Agent
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import json

@CrewBase
class ResumeTuningCrew:
    def __init__(self, llm: LLM):
        self.llm = llm
    
    @agent
    def resume_analyst_agent(self):
        return Agent(
            role="Resume Tuner",
            goal="Tune the given resume to the given Job description so that its easy to pass auto ATS filter and HRs",
            backstory="""You are an expert resume analyst with over 10 years of experience in recruitment
            and career coaching. You have a keen eye for identifying what makes a resume stand out and
            what might hold it back. You understand current hiring trends and ATS systems.
            You MUST respond with valid JSON structure matching the input resume format.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
       
    @agent
    def verifier_agent(self):
        return Agent(
            role="Resume Verifier",
            goal="Verify if the tuned resume matches the job requirements and provide feedback",
            backstory="""You are an expert resume analyst with over 10 years of experience in recruitment
            and career coaching. You have a keen eye for identifying what makes a resume stand out and
            what might hold it back. You understand current hiring trends and ATS systems.
            Your job is to verify if the tuned resume is relevant and provides constructive feedback.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
   
    @task
    def job_matching_task(self):
        return Task(
            description="""Compare the resume against the target job description and create an optimized version.
           
            Resume Data: {resume}
            Job Description: {job_description}
            User Comment: {comment}
            GIVE more importance to users comment
            
            INSTRUCTIONS:
            1. Create a tuned resume in the EXACT SAME JSON structure as the input resume
            2. Focus on skills that match the job description
            3. Remove or de-emphasize irrelevant skills
            4. Tune work experience descriptions to align with the JD requirements
            5. Humanize the text while keeping it professional
            6. Don't fabricate experience but optimize skill presentation
            7. Categorize skills into: languages, frameworks, cloud, tools, etc.
            8. Format work experience as bullet points. 
            9. Update objective/summary to match job requirements
            10. Need a header for  the first experience summarizing the work done in a single line add skills used if required.
            11.If work done in an experience is already less.Dont trim it.
            CRITICAL: Your response must be ONLY valid JSON, no additional text or explanations.""",
            expected_output="""Valid JSON object containing the tuned resume with:
            - Updated objective/summary aligned with job requirements
            - Optimized skills section categorized appropriately
            - Work experience with bullet points tuned for the target role
            - Same structure as input resume
            - No additional text, only JSON""",
            agent=self.resume_analyst_agent()
        )
    
    @task
    def resume_verifier_task(self):
        return Task(
            description="""Review the tuned resume and provide verification feedback.
           
            Job Description: {job_description}
            User Comment: {comment}
            
            INSTRUCTIONS:
            1. Analyze the tuned resume from the previous task
            2. Check alignment with job requirements
            3. Verify skills relevance and categorization
            4. Ensure work experience is properly optimized
            5. If satisfied with the tuning, respond with: "VERIFICATION_COMPLETE"
            6. If improvements needed, provide specific feedback for the resume tuner
            7. Work Experiences description should be different bullets(items in array) in array 
            Eg:
            "responsibilities": [
                "<work done 1>",
                "<work done 2>",
            ],
            Want all responsibility in description section only
            """,
            expected_output="""Either 'VERIFICATION_COMPLETE' if the resume is well-tuned, 
            or specific suggestions for improvement focusing on job alignment and ATS optimization.""",
            agent=self.verifier_agent(),
            context=[self.job_matching_task()]
        )
    
    @crew
    def crew(self):
        return Crew(
            agents=[
                self.resume_analyst_agent(),
                self.verifier_agent()
            ],
            tasks=[
                self.job_matching_task(),
                self.resume_verifier_task()
            ],
            process=Process.sequential,
            verbose=True
        )
    
    def get_tuned_resume_json(self, resume_data, job_description, comment=""):
        """
        Execute the crew and return the tuned resume as JSON
        """
        try:
            # Execute the crew
            result = self.crew().kickoff(inputs={
                'resume': resume_data,
                'job_description': job_description,
                'comment': comment
            })
            
            # The first task output should contain the JSON resume
            tuned_resume_output = result.tasks_output[0].raw
            
            # Try to parse as JSON to validate
            try:
                tuned_resume_json = json.loads(tuned_resume_output)
                return tuned_resume_json
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON from the output
                import re
                json_match = re.search(r'\{.*\}', tuned_resume_output, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in the output")
                    
        except Exception as e:
            print(f"Error getting tuned resume JSON: {e}")
            return None

# Usage example:
"""
# Initialize the crew
llm = LLM(model="your_model_here")  # Replace with your LLM configuration
crew = ResumeTuningCrew(llm)

# Your resume data (as JSON/dict)
resume_data = {
    "personal_info": {...},
    "objective": "...",
    "skills": {...},
    "experience": [...],
    # ... rest of your resume structure
}

job_description = "Your target job description here..."
user_comment = "Focus on technical skills and leadership experience"

# Get the tuned resume as JSON
tuned_resume = crew.get_tuned_resume_json(resume_data, job_description, user_comment)

if tuned_resume:
    print("Tuned Resume JSON:")
    print(json.dumps(tuned_resume, indent=2))
else:
    print("Failed to generate tuned resume JSON")
"""