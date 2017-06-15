import web , datetime

db = web.database(dbn='sqlite' , db='user.db')


class model():

    def __init__(self,session,render):
        self.session = session
        self.render = render

    def login(self,name, pw):



        pw = db.select('users' , where='name=$name' , vars=locals())[0]['password']

        if pw == pw:
            self.session.loggedin = True
            self.session.username = name
        return self.render.index()

    #def register(name,mail,pw1,pw2):
        
      
