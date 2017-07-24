#-*- coding: utf-8 -*-
#@author: patrick@openexpmechanics.science
import web , datetime
import configuration as conf
import md5
import math

## Class for the connection to the database
class model():

    ## Constructor
    # @param render Render engine
    # @param session Session of the current user
    def __init__(self,render,session):
        ## Render engine
        self.render = render
        ## Session of the current user
        self.session = session
        ## Configuration loaded from the yaml file
        self.conf = conf.configuration()
        ## Connector to the databse
        self.db = web.database(dbn=self.conf.dbType , db=self.conf.database, pw=self.conf.password, user=self.conf.username,host=self.conf.host)

    ## Login
    # @param name Username
    # @param pw Password
    # @return Login was succesfull 
    def login(self,name, pw):

		try:
			data = self.db.select('users' , where='name=$name' , vars=locals())[0]
		except:
			return False

		if pw == data['password']:
			self.session.t_user = name 
			self.session.t_auth = True
			self.session.t_id = data['id']

		return True
    
    ## Register
    # @param name Username
    # @param mail Mailadress of the user
    # @param pw Password
    # @return Registration succesfull
    def register(self,name,mail,pw):
        
		try:
                    
                    if self.getUser(name) == True:
                        return 2
                    
                    self.db.insert('users',name=name,password=md5.md5(pw).hexdigest(),mail=mail)
                    data = self.db.select('users' , where='name=$name' , vars=locals())[0]
                except:
                    return 1
                
                self.session.t_user = name 
                self.session.t_auth = True
                self.session.t_id = data['id']
                
                return 0
            
    ## Check if username exists
    # @param user Username to validate
    # @return User exists
    def getUser(self,user):

                data = self.db.query("SELECT count(*) as count FROM users WHERE name=$name LIMIT 1", vars={'name':user})[0]
              
                if data['count'] == 1:
                    return True
                else:
                    return False
         
    ## Add new dataset
    # @param title Title of the dataset
    # @param content Description of the dataset
    # @param link Link to the dataset
    # @return Dataset inserted
    def new(self,title,content,link):
		try:
                    self.db.insert('datasets',title=title,link=link,user=self.session.t_id,content=content)
                except:
                    return False

                return True
    
    ## Get all posts for a specific user
    # @return All datasets of the user
    def getPosts(self):
         userID = dict(user=self.session.t_id)
         return self.db.select('datasets', userID, order='id DESC' , where='user=$user')
    
    ## Get the dataset corresponding to an id
    # @param postID Id of the post
    # @return Dataset corresponding to postID
    def getPost(self,postID):
        post = dict(id=postID)
        return self.db.select('datasets', post, where='id=$id')
    
    ## Get all posts
    # @return All datasets
    def getAllPosts(self):
        return self.db.select('datasets',  order='id DESC' )
     
    ## Get a range of posts
    # @return Range datasets
    def getRangePosts(self,amount,page):
        
        if amount == -1:
            return self.db.select('datasets',  order='id DESC' )
        else:
            data = self.db.query("SELECT count(*) as count FROM datasets")[0]
            count = data['count']
            length = int(math.ceil(float(count) / float(amount)))
            pages = []
            for i in range(1,length+1):
                pages.append(i)
            return self.db.query("SELECT * FROM datasets ORDER BY id DESC LIMIT $first,$last",vars={'first':page*amount,'last':amount}) , pages
            
    ## Delete a post by id
    # @param postID Id of the dataset to delete
    def deletePost(self,postID):
        var = dict(user=self.session.t_id,id=postID)
        self.db.delete('datasets', where="id=$id AND user=$user", vars=var)
    
    ## Update a dataset
    # @param postID Id of the dataset
    # @param title Title of the dataset
    # @param content Description of the dataset
    # @param link Link to the dataset
    def updatePost(self,postID,title,content,link):
        self.db.update('datasets', where="id=$postID", vars=locals(),
        title=title, content=content,link=link)
