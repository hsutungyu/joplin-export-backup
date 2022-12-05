import requests

def getAll(url: str, params: dict) -> dict:
    """a helper function to retrieve result from a paginated Joplin API endpoint

    Args:
        url (str): the API endpoint that you want to call
        params (dict): the GET params you want to pass on
        if the key "page" is not found within params then it's default to start from the first page

    Returns:
        list: a list that stores the result from all pages in JSON format, i.e., result[0] stores the result from the first page
    """
    if "page" not in params:
        params["page"] = 1
    
    result = list()

    while True:
        response = requests.get(url, params=params)
        responseJSON = response.json()
        
        if "has_more" not in responseJSON:
            raise KeyError("The API endpoint that you call is not paginated. Call the correct method to retrieve one result.")
            
        result.append(responseJSON["items"])
        
        if not responseJSON["has_more"]:
            break
        else:
            params["page"] += 1
        
    return result
