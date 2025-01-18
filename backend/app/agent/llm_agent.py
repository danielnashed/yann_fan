from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, FunctionMessage, messages_to_dict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from pathlib import Path
from typing import Annotated, Dict
from typing_extensions import TypedDict
from .prompts import Prompts
import os
from pydantic import BaseModel

class TavilySearchAPIWrapper(BaseModel):
    tavily_api_key: str

# from .tools.save_off_resume import SaveResumeTool

load_dotenv(Path(__file__).parent.parent / '.env')
tavily_api_key = os.getenv('TAVILY_API_KEY')
groq_api_key = os.getenv("GROQ_API_KEY")


class State(TypedDict):
    messages: Annotated[list, add_messages]


class ChatAgent:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.graph = self._build_graph(user_id)

    def _build_graph(self, user_id: int):
        llm = ChatGroq(
                model="llama-3.2-1b-preview",
                temperature=0.0,
                max_retries=2,
                api_key=groq_api_key,
            )
        tools = [
            # TavilySearchResults(max_results=4,
            #                     api_wrapper=TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)),
            # WebScraperTool(),
            # PDFParserTool(),
        ]

        prompts = Prompts()
        system_message = SystemMessage(prompts.store['system'])
        agent = create_react_agent(llm, tools, state_modifier=system_message)

        graph_builder = StateGraph(State)
        graph_builder.add_node("agent", agent)
        graph_builder.set_entry_point("agent")
        return graph_builder.compile()

    def process_user_message(self, message: str, state: State = {"messages": []}) -> Dict:
        """
        Process a message from the user and return the response

        :param message: The message to process
        :param state: The state of the agent (e.g., previous messages in the conversation), or None to start a new conversation
        :param system_message: The system message to use for the conversation

        :return: The response from the agent and the updated graph state
        """

        state["messages"] = add_messages(state["messages"], HumanMessage(message))
        result = self.graph.invoke(state)
        response = result["messages"][-1].content
        state["messages"] = result["messages"]

        return {
            "response": response,
            "state": state,
        }

    def serialize_state(self, state: State) -> Dict:
        """
        Serialize the state of the agent into a dictionary

        :param state: The state of the agent

        :return: The serialized state of the agent
        """

        if "messages" not in state:
            return {
                "messages": []
            }

        return {
            "messages": messages_to_dict(state["messages"])
        }

    def deserialize_state(self, serialized_state: Dict) -> State:
        """
        Deserialize the state of the agent from a dictionary

        :param serialized_state: The serialized state of the agent

        :return: The state of the agent
        """

        if "messages" not in serialized_state:
            return {
                "messages": []
            }

        messages = []
        for msg in serialized_state["messages"]:
            if msg["type"] == "human":
                message = HumanMessage(**msg["data"])
            elif msg["type"] == "ai":
                message = AIMessage(**msg["data"])
            elif msg["type"] == "system":
                message = SystemMessage(**msg["data"])
            elif msg["type"] == "tool":
                message = ToolMessage(**msg["data"])
            elif msg["type"] == "function":
                message = FunctionMessage(**msg["data"])
            else:
                raise ValueError(f"Unknown message type: {msg['type']}")
            messages.append(message)
        return {
            "messages": messages
        }
    

# For debugging/presentation purposes
# Run from backend/ directory like `python -m app.agent.llm_agent`
if __name__ == "__main__":

    agent = ChatAgent(user_id=1)
    print('created agent...')

    # Send the message to the agent and process the response
    prompt = 'Hello World!'
    response = agent.process_user_message(prompt)
    print('got back a response...')

    # Print the response and the updated state
    print("Agent Response:", response["response"])
    print("Updated State:", agent.serialize_state(response["state"]))