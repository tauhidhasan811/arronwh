"""from openai import OpenAI

class AudioModel:
    def __init__(self, model_name = "whisper-1"):
        self.client = OpenAI()
        self.model_name = model_name
    
    # def audio_to_text(self, audio_path, stram=True):
    #     stream = self.client.audio.transcriptions.create(
    #             model=self.model_name, 
    #             file=audio_path, 
    #             response_format="text",
    #             stream=True
    #             )
    #     return stram
    # def audio_to_text(self, audio_path: str):
    #     with open(audio_path, "rb") as audio_file:
    #         response = self.client.audio.transcriptions.create(
    #             model=self.model_name,
    #             file=audio_file,
    #             response_format="text"
    #         )
    #     return response


    # def audio_to_text(self, audio_path: str):
    #     with open(audio_path, "rb") as audio_file:
    #         response = self.client.audio.transcriptions.create(
    #             model=self.model_name,
    #             file=audio_file
    #         )
    #     return response.text
    def audio_to_text(self, audio_path):

        # with open(audio_path, "rb") as audio_file:
        #     result = self.client.audio.transcriptions.create(
        #         model=self.model_name,
        #         file=audio_file,
        #         response_format="verbose_json"
        #     )
        #     # print(result.segments.text)

        # return result
        with open(audio_path, 'rb') as audio_file:
            result = self.client.audio.transcriptions.create(
                model=self.model_name,
                file=audio_file
            )
        return result.text"""

# from openai import OpenAI

# class AudioModel:
#     def __init__(self, model_name="gpt-4o-mini-transcribe"):
#         self.client = OpenAI()
#         self.model_name = model_name

#     def audio_to_text_stream(self, audio_path: str):
#         with open(audio_path, "rb") as audio_file:
#             stream = self.client.audio.transcriptions.create(
#                 model=self.model_name,
#                 file=audio_file,
#                 response_format="text",
#                 stream=True,
#             )
#             for event in stream:
#                 yield event


from openai import OpenAI

class OpenAIAudio:
    def __init__(self, model_name = "whisper-1"):
        self.client = OpenAI()
        self.model = model_name

    def ConvertToText(self, audio_path):
        """
        audion_file = open(audio_path, 'rb')
        result = self.client.audio.transcriptions.create(
            model=self.model,
            file=audion_file
        )
        """

        with open(audio_path, 'rb') as audion_file:
            result = self.client.audio.transcriptions.create(
                model=self.model,
                file=audion_file
            )
        return result.text