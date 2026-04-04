from openai import OpenAI

class AudioModel:
    def __init__(self, model_name = "gpt-4o-mini-transcribe"):
        self.client = OpenAI()
        self.model_name = model_name
    
    def audio_to_text(self, audio_path, stram=True):
        stream = self.client.audio.transcriptions.create(
                model=self.model_name, 
                file=audio_path, 
                response_format="text",
                stream=True
                )
        return stram