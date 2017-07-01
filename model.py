import web , datetime
import configuration as conf
import md5

conf = conf.configuration()


db = web.database(dbn=conf.dbType , db=conf.database, pw=conf.password, user=conf.username,host=conf.host)


class model():

    def __init__(self,render,session):
        self.render = render
        self.session = session

    def login(self,name, pw):

		try:
			data = db.select('users' , where='name=$name' , vars=locals())[0]
		except:
			return False

		if pw == data['password']:
			self.session.t_user = name 
			self.session.t_auth = True
			self.session.t_id = data['id']

		return True
            
    def register(self,name,mail,pw):
		try:
                    db.insert('users',name=name,password=md5.md5(pw).hexdigest(),mail=mail)
                    data = db.select('users' , where='name=$name' , vars=locals())[0]
                except:
                    return False
                
                self.session.t_user = name 
                self.session.t_auth = True
                self.session.t_id = data['id']
                
                return True
        
    def getUser(self,user):

                try:
                    user = dict(name=user)
                    data = db.select('users' , user, where='name=$name' , vars=locals())[0]
                except:
                    return False
		
                if data['name'] == user:
                    return True
                
                return False
            
    def new(self,title,content,link):
		try:
                    db.insert('datasets',title=title,link=link,user=self.session.t_id,content=content)
                except:
                    return False

                return True
            
    def getPosts(self):
         userID = dict(user=self.session.t_id)
         return db.select('datasets', userID, order='id DESC' , where='user=$user')
     
    def getPost(self,postID):
        post = dict(id=postID)
        return db.select('datasets', post, where='id=$id')
    
    def getAllPosts(self):
         return db.select('datasets',  order='id DESC' )
     
    def deletePost(self,ID):
        var = dict(user=self.session.t_id,id=ID)
        db.delete('datasets', where="id=$id AND user=$user", vars=var)
