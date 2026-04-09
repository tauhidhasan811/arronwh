from src.config.config_db import GetDataBase
class DbQueries:
    def __init__(self):
        self.db = GetDataBase()

    def GetAllField(self, collection_name, isactive: bool = True, include_field: list = [],
                    exclude_field: list = []):
        
        collection = self.db[collection_name]
        if include_field:
            include = {}
            for f in include_field:
                include.update({f:1})
            data = collection.find({'isActive': isactive}, include)
            return data
        
        elif exclude_field:
            exclude = {}
            for f in exclude_field:
                exclude.update({f:0})
            data = collection.find({'isActive': isactive}, exclude)
            return data
        
        data = collection.find({'isActive': isactive})
        return data
    
    # def Get