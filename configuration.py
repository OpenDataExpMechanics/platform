#-*- coding: utf-8 -*-
#@author: patrick@openexpmechanics.science
import yaml

## Class to load the configuration from the yaml file
class configuration:
    
    ## Constructor
    def __init__(self):
        with open("conf.yaml",'r') as f:
            doc = yaml.load(f)
            ## Username for the connection
            self.username= doc["Database"]["User"]
            ## Database 
            self.database= doc["Database"]["Database"]
            ## Password
            self.password= doc["Database"]["Password"]
            ## Type of database (mysql or postgres)
            self.dbType= doc["Database"]["Type"]
            ## Host of the database
            self.host= doc["Database"]["Host"]
            ## Max file size for upload
            self.size = doc["File"]["Max"]
            ## Path for storing uploaded data
            self.path = doc["File"]["Path"]
            ## Allowed file types for upload
            self.types = doc["File"]["Types"].split(',')
