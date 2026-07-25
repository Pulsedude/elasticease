import re

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
    """Create a JSON (dict) document from given string (text) to insert into elasticsearch index
    """
    document = {}
    last_key = ""
    for i, letter in enumerate(text.split()):
        cleaned_letter = re.sub(r'[^a-zA-Z0-9]', '', letter)

        if (i + 1) % 2 == 0:
            document[last_key] = cleaned_letter if not cleaned_letter.isdigit() else int(
                cleaned_letter)

        else:
            document[cleaned_letter] = ""
            last_key = cleaned_letter if not cleaned_letter.isdigit() else int(cleaned_letter)
    return document
