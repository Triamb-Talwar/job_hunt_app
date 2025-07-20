from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool,ApifyActorsTool
from .tools.send_email import SendEmailTool

@CrewBase
class JobApp():
    """JobApp crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def job_search_agent(self)->Agent:
        return Agent(
            config=self.agents_config['job_search_agent'],
            verbose=True,
            tools=[SerperDevTool(),ApifyActorsTool(actor_name="misceres/indeed-scraper")]
        )
    
    # @agent
    # def resume_tailor_agent(self)->Agent:
    #     return Agent(
    #         config=self.agents_config['resume_tailor_agent'],
    #         verbose=True,
    #         tools=[DirectoryReadTool(directory='job_app\input')]
    #     )
    
    @agent
    def hr_contact_agent(self)->Agent:
        return Agent(
            config=self.agents_config['hr_contact_agent'],
            verbose=True,
            tools=[SerperDevTool(), ApifyActorsTool(actor_name="misceres/indeed-scraper")]
        )
    
    @agent
    def cold_email_agent(self)->Agent:
        return Agent(
            config=self.agents_config['cold_email_agent'],
            verbose=True,
        )
    
    @agent
    def application_submitter_agent(self)->Agent:
        return Agent(
            config=self.agents_config['application_submitter_agent'],
            verbose=True,
            tools=[SendEmailTool()]
        )

    
    @task
    def job_search_task(self)->Task:
        return Task(
            config=self.tasks_config['job_search_task']
        )
    
    # @task
    # def resume_tailoring_task(self)->Task:
    #     return Task(
    #         config=self.tasks_config['resume_tailoring_task']
    #     )
    
    @task
    def hr_contact_lookup_task(self)->Task:
        return Task(
            config=self.tasks_config['hr_contact_lookup_task']
        )
    
    @task
    def cold_email_task(self)->Task:
        return Task(
            config=self.tasks_config['cold_email_task']
        )
    
    @task
    def application_submission_task(self)->Task:
        return Task(
            config=self.tasks_config['application_submission_task']
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the JobApp crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )