from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import NonRetryableError, agent, import_functions, log

with import_functions():
    from src.functions.llm_chat import LlmChatInput, Message, llm_chat
import json

def parse_json_to_dict(json_str: str) -> dict:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentChat:
    def __init__(self) -> None:
        self.end = False
        system_prompt = """
    Respond STRICTLY in English

    Provide a direct, concise, and objective fact-check for the following statement:

    statement: 
    speaker: 
    Respond with a valid JSON object containing the following fields:

    {
      "rating": One of the following: True, Partly true, False, Unverifiable,
      "confidence": A number between 0 and 1 indicating your confidence,
      "explanation": "Provide a clear explanation in one concise sentence",
      "evidence": "Cite specific evidence with numbers, facts, and direct source names",
      "sources": [
        {
          "name": "Source name",
          "url": "Source URL if available",
          "credibility_score": 0.0
        }
      ]
    }

    Rating criteria:
    - True: The statement is accurate and verifiable.
    - Partly true: The statement contains some truth but also inaccuracies.
    - False: The statement is inaccurate and verifiably false.
    - Unverifiable: There isn't enough information to determine accuracy.

    Be direct, precise, and objective. Focus on verifiable facts rather than opinions. Provide concrete evidence.
    """
        self.messages = [
            Message(role="system", content=system_prompt)
        ]

    @agent.event
    async def messages(self, messages_event: MessagesEvent):
        log.info(f"Received messages: {messages_event.messages}")
        #self.messages.extend(messages_event.messages)

        log.info(f"Calling llm_chat with messages: {self.messages}")
        try:
            assistant_message = await agent.step(
                function=llm_chat,
                function_input=LlmChatInput(messages=self.messages+messages_event.messages),
                start_to_close_timeout=timedelta(seconds=120),
            )
        except Exception as e:
            error_message = f"Error during llm_chat: {e}"
            raise NonRetryableError(error_message) from e
        else:
            #self.messages.append(assistant_message)
            return assistant_message["content"]

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, function_input: dict) -> None:
        log.info("AgentChat function_input", function_input=function_input)
        await agent.condition(lambda: self.end)
