import web , datetime
import configuration as conf
import md5

conf = conf.configuration()


db = web.database(dbn=conf.dbType , db=conf.database, pw=conf.password, user=conf.username,host="marvin")


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

		return True
            
    def register(self,name,mail,pw):
		try:
                    db.insert('users',name=name,password=md5.md5(pw).hexdigest(),mail=mail)
                except:
                    return False
                
                self.session.t_user = name 
                self.session.t_auth = True
                
                return True
        
    def getUser(self,user):

                try:
                    data = db.select('users' , where='name=$name' , vars=locals())[0]
                except:
                    return False
		
                if data['name'] == user:
                    return True
                
                return False

   
