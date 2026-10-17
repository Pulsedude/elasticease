def remove_commas(text: str) -> str:
    for i in text:
        if i == "\'" or i == "\"":
            text = text.replace(i, "")
    return text


def url_validator(url: str) -> str:
    """Validate a url whether is is starts with required protocols or not
    """
    if not url.startswith(("http://", "https://")):
        return (False, "[!] URL must starts with http:// or https://\n")
    return True


def create_document(text: str) -> dict:
    """Create a JSON (dict) proper valid document from given string (text) 
    """
    keys, values = [], []
    text_list = text.split()
    
    i, n = 0, len(text_list)
    
    while i < n:
        pair = [remove_commas(i) for i in text_list[i].split("=")]
        
        if len(pair) == 1:
            values[-1] += f" {pair[0]}"
        else:
            keys.append(pair[0])
            values.append(pair[1])
            
        i += 1
    
    document = {}
    i, j, n, m = 0, 0, len(keys), len(values)
    
    while i < n and j < m:
        key, value = keys[i], values[j]
        document[key] = value
        i += 1
        j += 1
    
    return document
    

def create_mappings(text: str) -> dict:
    """Create a JSON based (dict) valid mapping document from given string (text) 
    """
    mappings = {}
    properties = {}
     
    text_list = text.split()    
    i, n = 0, len(text_list)
    
    while i < n:
        pair = [remove_commas(i) for i in text_list[i].split("=")]
        
        properties[pair[0]] = {
            "type": pair[1]
        }
        i += 1
    
    mappings["mappings"] = {"properties": properties}
    return mappings 


    