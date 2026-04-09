# import json
# import requests

# url = 'https://arronwh-backend.onrender.com/api/v1/service?sortBy=createdAt&limit=10&page=1' 

# response = requests.get(url)

# # print(response.json())

# with open('data/json/service_data.json', 'w', encoding='utf-8') as f:
#     json.dump(response.json(), f, indent=4)

from src.db.db_queries import DbQueries

db = DbQueries()

data = db.GetAllField(collection_name="services", isactive=True, include_field=['heroSection.gallery.url'])
print(list(data))