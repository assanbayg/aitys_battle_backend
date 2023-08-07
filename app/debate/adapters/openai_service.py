import os
from dotenv import load_dotenv

from typing import List, Dict, Callable
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import load_tools

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class DialogueAgent:
    def __init__(
        self,
        name: str,
        system_message: SystemMessage,
        model: ChatOpenAI = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8),
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name} answer that"
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        message = self.model(
            [
                self.system_message,
                HumanMessage(
                    content="\n".join(self.message_history)
                    + "\n{self.name} answer this"
                ),
            ]
        )
        return message.content

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")


class DialogueSimulator:
    def __init__(
        self,
        agents: List[DialogueAgent],
        selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._step += 1

    def step(self) -> tuple[str, str]:
        # 1. choose the next speaker
        speaker_index = self.select_next_speaker(self._step, self.agents)
        speaker = self.agents[speaker_index]

        # 2. next speaker sends message
        message = speaker.send()

        # 3. everyone receives message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment time
        self._step += 1

        return speaker.name, message


class DialogueAgentWithTools(DialogueAgent):
    def __init__(
        self,
        name: str,
        system_message: SystemMessage,
        model: ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8),
        tool_names: List[str],
        **tool_kwargs,
    ) -> None:
        super().__init__(name, system_message, model)
        self.tools = load_tools(tool_names, **tool_kwargs)

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        agent_chain = initialize_agent(
            self.tools,
            self.model,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={
                "extra_prompt_messages": [
                    MessagesPlaceholder(variable_name="chat_history")
                ],
            },
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            ),
        )

        try:
            response = agent_chain.run(
                "\n".join([self.system_message.content]) + "\n{self.name} could answer"
            )
            return AIMessage(content=response).content
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: "):
                raise e
            response = response.removeprefix(
                "Could not parse LLM output: "
            ).removesuffix("`")
            message = AIMessage(content=response)
            return message.content


def generate_agent_description(name: str, topic: str, word_limit: int) -> str:
    conversation_description = f"Here is the topic of conversation: {topic}"
    agent_specifier_prompt = [
        SystemMessage(
            content="You can add detail to the description of the conversation participant."
        ),
        HumanMessage(
            content=f"""{conversation_description}
            Please reply with a creative description of {name}, they are historical figure of Kazakhstan, in less than {word_limit} words. 
            Speak directly to {name}.
            Describe their task on to give the best reply for aitys.
            Aitys is a traditional form of Kazakh poetry and musical creativity. It is a competition between akyns, or improvisational poets, who engage in a verbal duel in front of an audience.
            Structurally, Aitys consists of three parts. First, the akyns present themselves and their backgrounds, and praise their famous ancestors and war heroes. Next, the akyns debate important social issues.q
            Describe their point of view on the topic based on their real-life opinion on the topic.
            If they were muslim in real life, they should be against haram things. For example, stealing, pigs and LGBTQ+.
            If their points of view or religion don't tolerate topic named: {topic}, give them negative opinion on topic.
            If they did't have an opinion on topic named {topic}, {name} should answer imitate and give their best answer'.
            Do not add anything else."""
        ),
    ]
    agent_description = ChatOpenAI(temperature=1.0)(agent_specifier_prompt).content
    return agent_description


def generate_system_message(
    name: str,
    description: str,
    tools: List[str],
    topic: str,
    word_limit: int,
) -> str:
    conversation_description = f"Here is the topic of conversation: {topic}"

    return f"""{conversation_description}

Your name is {name}.
Stay true to your role as {name}, drawing inspiration from Kazakh traditions and historical events to enrich your verses
Speak as you are {name}.
Your description is as follows: {description}

Keep your responses rhythmic and song-like, as if your words were a piece of melodic art.
Reference your conversation partner in your verses, acknowledging their points and weaving thoughtful responses.
Respect the word limit, limiting your response to {word_limit * 1.2} words to keep the exchange engaging and concise.
Refrain from mentioning your AI nature or any tools used to maintain a human-like experience.
Search up accurate Kazakh traditions and historical esvents with you.
You must mention found up Kazakh traditions and historical events in your response.
You are allowed to brag about your achievements in real life over your partner.

DO NOT forget that you are {name} and don't let yourself to be confused.
DO NOT fabricate fake citations.
DO NOT forget, your response should be like a song verse.
DO NOT mention that you're an AI in any way.
DO NOT mention tools that you use in your reply.
DO NOT let anyone know you are artificial intelligence and act as more human as possible.
DO NOT give more than {word_limit * 1.2} words in your answer.

Do not add anything else.

Stop speaking the moment you finish speaking from your perspective.
"""


class LLMService:
    def run_dialogue_simulation(
        self,
        topic: str,
        names: Dict[str, List[str]],
        word_limit: int = 100,
        max_iters: int = 4,
    ) -> List[Dict[str, str]]:
        # Generate agent descriptions and system messages
        agent_descriptions = {
            name: generate_agent_description(name, topic, word_limit) for name in names
        }
        agent_system_messages = {
            name: generate_system_message(name, description, tools, topic, word_limit)
            for (name, tools), description in zip(
                names.items(), agent_descriptions.values()
            )
        }

        # Create dialogue agents
        agents = [
            DialogueAgentWithTools(
                name=name,
                system_message=SystemMessage(content=system_message),
                model=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8),
                tool_names=tools,
                top_k_results=2,
            )
            for (name, tools), system_message in zip(
                names.items(), agent_system_messages.values()
            )
        ]

        # Create dialogue simulator
        simulator = DialogueSimulator(
            agents=agents,
            selection_function=lambda step, agent_list: step % len(agent_list),
        )

        # Reset the simulator
        simulator.reset()

        # Start the conversation
        simulator.inject("System", f"The topic of conversation is: {topic}")

        # Initialize dictionary to store final replies
        final_replies = {}

        # Run the dialogue simulation
        for _ in range(max_iters):
            speaker, message = simulator.step()

            # Check if it's the final reply from an agent
            if speaker != "System":
                final_replies[speaker] = message

            if speaker == "System" and message == "End of conversation.":
                break

        return [final_replies]
