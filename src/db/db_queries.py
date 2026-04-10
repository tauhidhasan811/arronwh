from src.config.config_db import GetDataBase
class DbQueries:
    def __init__(self):
        self.db = GetDataBase()

    def GetAllField(self, collection_name, include_field: list = [],
                    exclude_field: list = []):
        
        collection = self.db[collection_name]
        if include_field:
            include = {'_id': 0}
            for f in include_field:
                include.update({f:1})
            data = collection.find({}, include)
            return data
        
        elif exclude_field:
            exclude = {'_id': 0}
            for f in exclude_field:
                exclude.update({f:0})
            data = collection.find({}, exclude)
            return data
        
        data = collection.find({})
        return data
    
    # def Get