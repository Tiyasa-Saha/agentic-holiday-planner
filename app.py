import os
from dotenv import load_dotenv
import gradio as gr
from agents import Runner

from travel_agents.travel_manager import travel_manager_agent
from memory.session_memory import SessionMemory


load_dotenv()

session_memory = SessionMemory()


def chat_with_agent(message, history):
    session_memory.update_from_message(message)

    memory_summary = session_memory.get_memory_summary()

    agent_input = f"""
    User message:
    {message}

    Saved user preferences from this session:
    {memory_summary}

    Use the saved preferences when helpful.
    If you use an assumption or remembered preference, mention it clearly.
    """

    result = Runner.run_sync(travel_manager_agent, agent_input)
    return result.final_output


demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="Agentic Holiday Planner",
    description="Plan trips using a multi-agent PRMA holiday planner.",
)


if __name__ == "__main__":
    demo.launch()