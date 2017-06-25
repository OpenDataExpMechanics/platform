import yaml

class configuration:
    
    def __init__(self):
        with open("conf.yaml",'r') as f:
            doc = yaml.load(f)
            self.username= doc["Database"]["User"]
            self.database= doc["Database"]["Database"]
            self.password= doc["Database"]["Password"]
            self.dbType= doc["Database"]["Type"]
            self.host= doc["Database"]["Host"]
