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