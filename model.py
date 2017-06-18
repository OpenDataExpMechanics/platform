import web , datetime

db = web.database(dbn='sqlite' , db='user.db')


class model():

    def __init__(self,render,session):
        self.render = render
        self.session = session

    def login(self,name, pw):

        

        data = db.select('users' , where='name=$name' , vars=locals())[0]['password']
        print data
        #if pw == pw:
        self.session.t_user = name 
        self.session.t_auth = True
        return self.render.index()

    #def register(name,mail,pw1,pw2):
        
      
