def get_api():
    """Get the API key from the api.txt file"""
    content = None
    with open('src/configuration/api.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content