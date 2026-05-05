params = {
    'accepted_parameters': ['temperature', 'streaming'],
    'model_name': 'gpt-4.1-2025-04-14',
    'collections': {
        'products': {
            'exclude_field' : ['images', 'includedImages', 'featureInformation.featureLogo', 'user', 'createdAt', 'updatedAt', '__v']
        },
        'boilercontrollers': {
            'exclude_field' : []
        },
        'extras': {
            'exclude_field' : ['images', 'createdAt', 'updatedAt', '__v']
        },
        # 'services': {
        #     'exclude_field' : ['_id', 'user', 'updatedAt', '__v']
        # }
    }
    
}