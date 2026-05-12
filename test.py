# from src.config.config_audio_model import OpenAIAudio
# from dotenv import load_dotenv

# load_dotenv()
# model = OpenAIAudio()

path = r"data\files\Battle Symphony (Official Lyric Video) - Linkin Park.mp3"

# text = model.ConvertToText(path)
# print(text)
from src.services.data_processor import DataProcessor

data = DataProcessor.file_reader_route(path)

print(data)