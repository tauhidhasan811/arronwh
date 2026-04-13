from langchain_core.tools import tool
from src.hyper_parameters import params
from src.db.db_queries import DbQueries

# @tool
def GetAllData(collection_name):
    """Extract data like three collection where one cluster name is products wherehave boilder fileds are " _id, payablePrice 
    secound one is controllers where there are boiler controllers
    third one is extras where there are extra items"""

    
    db = DbQueries()
    collection_info = params['collections'][collection_name]
    exclude_field = collection_info['exclude_field']
    exclude = {}
    for f in exclude_field:
        exclude.update({f:0})
    
    payload = {'collection_name': collection_name,
               'exclude_field': exclude}
    # print(payload)

    data = db.GetAllField(**payload)
    return data

def GetSelectedData(collection_name, **kwargs):
    """Extract data like three collection where one cluster name is products wherehave boilder fileds are " _id, payablePrice 
    secound one is controllers where there are boiler controllers
    third one is extras where there are extra items"""

    
    db = DbQueries()
    collection_info = params['collections'][collection_name]
    exclude_field = collection_info['exclude_field']
    exclude = {}
    for f in exclude_field:
        exclude.update({f:0})
    
    payload = {'collection_name': collection_name,
               'exclude_field': exclude}
    payload.update(kwargs)
    print(payload)

    data = db.GetDataByFilter(**payload)
    return data


