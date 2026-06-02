import os
from dotenv import load_dotenv
import gradio as gr
from agents import Runner

from travel_agents.travel_manager import travel_manager_agent


load_dotenv()


def chat_with_agent(message, history):
    result = Runner.run_sync(travel_manager_agent, message)
    return result.final_output


demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="Agentic Holiday Planner",
    description="Plan trips using a multi-agent PRMA holiday planner.",
)


if __name__ == "__main__":
    demo.launch()