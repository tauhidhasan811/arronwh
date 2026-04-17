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

# from src.tools.database_tools import GetAllData

# data = GetAllData(collection_name='extras')
# print(data)

from collections.abc import AsyncIterable, Iterable
from fastapi import FastAPI
import time
from fastapi.responses import StreamingResponse

message = """
Rick: (stumbles in drunkenly, and turns on the lights) Morty! You gotta come on. You got--... you gotta come with me.
Morty: (rubs his eyes) What, Rick? What's going on?
Rick: I got a surprise for you, Morty.
Morty: It's the middle of the night. What are you talking about?
Rick: (spills alcohol on Morty's bed) Come on, I got a surprise for you. (drags Morty by the ankle) Come on, hurry up. (pulls Morty out of his bed and into the hall)
Morty: Ow! Ow! You're tugging me too hard!
Rick: We gotta go, gotta get outta here, come on. Got a surprise for you Morty.
"""

app = FastAPI()

async def story_generator() -> AsyncIterable[str]:
    for line in message.splitlines():
        time.sleep(1)
        yield line + '\n'

@app.get('/api/get')
async def stream_story():
    return StreamingResponse(story_generator(), media_type='text/plain')
