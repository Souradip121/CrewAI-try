from crewai_tools import ScrapeWebsiteTool, FileWriterTool, TXTSearchTool
import requests

# Initialize the tool, potentially passing the session
tool = ScrapeWebsiteTool(website_url='https://en.wikipedia.org/wiki/Pok%C3%A9mon')  

# Extract the text
text = tool.run()
print(text)

# Initialize the tool
file_writer_tool = FileWriterTool()

# Write content to a file in a specified directory
result = file_writer_tool._run(filename='pokemon.txt', content = text, directory = '', overwrite=True)
print(result)

import os
from crewai_tools import TXTSearchTool

os.environ['OPENAI_API_KEY'] = ''

# Initialize the tool with a specific text file, so the agent can search within the given text file's content
tool = TXTSearchTool(txt='pokemon.txt')

from crewai import Agent, Task, Crew

context = tool.run('What is the origin of Pokemon')

pokemon_fan = Agent(
    role='Educator',
    goal=f'Based on the context provided, answer the question - What is the origin? Context - {context}',
    backstory='You are a pokemon nerd',
    verbose=True,
    allow_delegation=False,
    tools=[tool]
)

test_task = Task(
    description="Understand the topic and give the correct response",
    tools=[tool],
    agent=pokemon_fan,
    expected_output='Give a correct response'
)

crew = Crew(
    agents=[pokemon_fan],
    tasks=[test_task]
)

output = crew.kickoff()