import web , datetime

db = web.database(dbn='sqlite' , db='user.db')


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
    def register(name,mail,pw):
		
		db.insert('users',name=name,password=pw)
        
    def getUser(self,user):

		try:
			data = db.select('users' , where='name=$name' , vars=locals())[0]
		except:
			return True

		return False

   
