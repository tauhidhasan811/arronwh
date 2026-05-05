from src.services.data_processor import DataProcessor

path = r'data\files\YoloHeat Company Guide.docx'

chunk = DataProcessor.create_chunk(path)

data = "hi !! how are you??"

ebd = DataProcessor.embedde_sentence(data)
print(ebd.shape)
# print(chunk)