import web
import model

web.config.debug = True


urls = (
        '/' , 'Index' ,
        '/login' , 'Login',
        '/register' , 'Register'
        )

### Templates
t_globals = {
    'datestr': web.datestr
}

#render = web.template.render('templates',base='base', globals=t_globals)

# Object handling the session of a user
app = web.application(urls, locals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0,'user':'anonymous','loggedin':False})

render = web.template.render('templates',base='base', globals=t_globals)

data = model.model(session,render)

class Index:
    def GET(self):
        return render.index()

##############################################################################
# Login as existing user
##############################################################################
class Login:

    form = web.form.Form(
        web.form.Textbox('Username', web.form.notnull,
            size=30,
            description="User:"),
        web.form.Password('Password', web.form.notnull,
            description="Password:"),
        web.form.Button('Login'),
    )

    def GET(self):
        form = self.form()
        return render.login(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.login(form)
        data.login(form.d.Username,form.d.Password)
        raise web.seeother('/')
    
##############################################################################
# Register
##############################################################################    
class Register:

    form = web.form.Form(
        web.form.Textbox('Username', web.form.notnull,
            size=30,
            description="User:"),
        web.form.Textbox('EMail', web.form.notnull,
            size=30,
            description="E-Mail:"),
        web.form.Password('Password', web.form.notnull,
            description="Password:"),
         web.form.Password('PasswordRepeated', web.form.notnull,
            description="Repet password:"),
        web.form.Button('send'),
    )

    def GET(self):
        form = self.form()
        return render.register(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.register(form)
        #data.login(form.d.Username,form.d.Password)
        raise web.seeother('/')
    

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
