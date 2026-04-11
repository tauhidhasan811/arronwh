# import json
# import requests

# url = 'https://arronwh-backend.onrender.com/api/v1/service?sortBy=createdAt&limit=10&page=1' 

# response = requests.get(url)

# # print(response.json())

# with open('data/json/service_data.json', 'w', encoding='utf-8') as f:
#     json.dump(response.json(), f, indent=4)

# from src.db.db_queries import DbQueries
# from src.hyper_parameters import params

# db = DbQueries()

# # data = db.GetAllField(collection_name="products", exclude_field=['_id', 'user', 'images', 'featureInformation.featureLogo', 'includedImages', 'createdAt', 'updatedAt', 'boilerInstallationGuide.image', '__v'])

# # print(list(data))
# exclude = {}
# exclude_field = params['collections']['products']['exclude_field']
# for f in exclude_field:
#     exclude.update({f:0})
# data = db.GetDataByFilter('products',exclude_data=exclude, _id = '69d86b535fbdf0e7994ac679', payablePrice = 950)
# print(list(data))

from src.tools.database_tools import GetAllData

data = GetAllData(collection_name='products', _id = '69d86b535fbdf0e7994ac679', payablePrice = 950)

print(data)