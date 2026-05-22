from agents import Agent
from agents.voice import SingleAgentVoiceWorkflow, VoicePipeline

class ConfigVoiceAgent:
    def __init__(self, model_name="gpt-5.5"):
        self.model_name = model_name

    def openai_voice_agent(self, name="Assistant",
                           instraction: str = None,
                           tools: list | None = None):
        

        agent = Agent(
            name=name,
            model = self.model_name,
            instructions=instraction,
            tools=tools or []

        )

        pipeline = VoicePipeline(
            workflow=SingleAgentVoiceWorkflow(agent=agent)
        )
        return pipeline
    
