#-*- coding: utf-8 -*-
#@author: patrick@openexpmechanics.science
import web , datetime
import md5
import math
import os

## Class for the connection to the database
class model():

    ## Constructor
    # @param render Render engine
    # @param session Session of the current user
    # @param conf Configuration
    def __init__(self,render,session, conf):
        ## Render engine
        self.render = render
        ## Session of the current user
        self.session = session
        ## Connector to the databse
        self.db = web.database(dbn=conf.dbType , db=conf.database, pw=conf.password, user=conf.username,host=conf.host)

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
			self.session.t_upload = data['fileupload']

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
    def new(self,title,content,link,tags):
		try:
                    self.db.insert('datasets',title=title,link=link,user=self.session.t_id,content=content,tags=tags)
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
        
        if amount == 0:
            return self.db.select('datasets',  order='id DESC' ) , []
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
        
        res = self.db.query("SELECT file FROM datasets WHERE id=$id AND user=$user",vars=var)[0]
        
        if not res["file"] == "None":
                os.remove(res["file"])
        
        self.db.delete('datasets', where="id=$id AND user=$user", vars=var)
    
    ## Update a dataset
    # @param postID Id of the dataset
    # @param title Title of the dataset
    # @param content Description of the dataset
    # @param link Link to the dataset
    def updatePost(self,postID,title,content,link,tags):
        self.db.update('datasets', where="id=$postID", vars=locals(),
        title=title, content=content,link=link,tags=tags)
    
    ## Search data sets for tags and title
    # @param title Text which is contained in the title of the data set
    # @param tags Text which is contained in the tags of a data set
    # @return All data sets containing these attributes
    def search(self,title,tags):
        
        if len(tags) == 0:
            title = "%" + str(title) + "%"
            return self.db.query("SELECT * FROM datasets WHERE title LIKE $title ORDER BY id ",vars={'title':title})
        if len(title) == 0:
            tags.replace(",","|")
            return self.db.query("SELECT * FROM datasets WHERE tags REGEXP $tags ORDER BY id ",vars={'tags':tags})
        else:
            title = "%" + str(title) + "%"
            tags.replace(",","|")
            return self.db.query("SELECT * FROM datasets WHERE tags REGEXP $tags OR title LIKE $title ORDER BY id ",vars={'tags':tags,'title':title})
    
    ## Get all tags 
    # @ return All available tags
    def tags(self):
        
        tags = []
        
        res = self.db.select('datasets' , what='tags')
        
        for r in res:
            tmp = str(r['tags']).split(',')
            for t in tmp:
                tags.append(t)
                
        tags.append('All')
        return sorted(list(set(tags)))
    
    ## Get all data sets with the provided tag
    # @param name Name of the tag
    # @return All datasets containing this tag
    def getPostsByTag(self,name):
        name = "%" + str(name) + "%"
        return self.db.query("SELECT * FROM datasets WHERE tags LIKE $name ORDER BY id ",vars={'name':name})
    
    ## Add a file to an existing data set
    # @param title Title of the dataset
    # @param filename Path to the file and name of the file
    def addFile(self,title,filename):
        
        self.db.query("Update datasets SET file=$filename WHERE title=$title AND user=$user",vars={'filename':filename,'title':title,'user':self.session.t_id})

    ## Get post of a specific user which have no files
    # @return All posts without files
    def getPostsWithoutFiles(self):
        
        return self.db.query("Select title FROM datasets WHERE user=$user AND file LIKE 'None'",vars={'user':self.session.t_id})
    
    
    ## Get all post with files from a specific user
    # @return All datasets of a specific user with files
    def getFiles(self):
        return self.db.query("SELECT id,title FROM datasets WHERE file NOT LIKE 'None' AND user=$user ORDER BY id ",vars={'user':self.session.t_id})
    
    ## Delte the file of the dataset with id
    # @param postID Id of the dataset
    def deleteFile(self,postID):
        
        res = self.db.query("SELECT file FROM datasets WHERE user=$user AND id=$id ",vars={'id':postID,'user':self.session.t_id})[0]
        
        os.remove(res["file"])
        
        self.db.query("Update datasets SET file='None' WHERE user=$user AND id=$id",vars={'id':postID,'user':self.session.t_id})
        
        
