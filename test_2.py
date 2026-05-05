from src.services.data_processor import DataProcessor

path = r"data\files\YoloHeat Company Guide.docx"

data = DataProcessor.read_docx(path)

print(len(data))