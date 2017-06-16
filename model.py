import web , datetime

db = web.database(dbn='sqlite' , db='user.db')


class model():

    def __init__(self,render):
        self.render = render

    def login(self,name, pw):

        data = db.select('users' , where='name=$name' , vars=locals())[0]['password']

        #if pw == pw:
    
        return self.render.index()

    #def register(name,mail,pw1,pw2):
        
      
