"""
This file is where you will implement your agent.
The `root_agent` is used to evaluate your agent's performance.
"""

from google.adk.agents import llm_agent

from my_agent.tools import read_image, read_pdf

root_agent = llm_agent.Agent(
    model="gemini-2.5-flash-lite",
    name="agent",
    description="A helpful assistant that can read PDFs and analyze images.",
    instruction="""You answer questions concisely.

CRITICAL RULES about files:
- When a .pdf path appears anywhere in the message, you MUST call read_pdf with that exact path. Do not skip this.
- When an image path (.png, .jpg, .jpeg, .gif, .webp) appears anywhere in the message, you MUST call read_image with that exact path and the full question. Do not skip this.
- NEVER say you cannot access a file — always call the appropriate tool instead.
- NEVER invent file paths. Only use paths explicitly given in the message.
- If no file is provided, answer from your knowledge.
- Be brief. End with exactly: ANSWER: <your answer>""",
    tools=[read_pdf, read_image],
    sub_agents=[],
)
