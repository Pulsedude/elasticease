import yaml

def read():
    """Read configuration file
    """
    try:
        with open("./config.yaml", "r") as file:
            configuration = yaml.safe_load(file)
        return configuration
    except Exception as e:
        return (False, e)
    
def write(data: dict):
    """Write config settings data back to configuration
    """
    try:
        with open("./config.yaml", "w") as file:
            yaml.safe_dump(data, file, default_flow_style=False)
    except Exception as e:
        return (False, e)
    