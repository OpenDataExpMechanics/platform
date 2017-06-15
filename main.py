import web
import model

web.config.debug = False



urls = (
        '/' , 'Index' ,
        '/register' , 'Register'
        )

### Templates
t_globals = {
    'datestr': web.datestr
}

render = web.template.render('templates',base='base', globals=t_globals)

# Object handling the session of a user
app = web.application(urls, locals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0,'user':'anonymous','loggedin':False})


data = model.model(session,render)

class Index:
    def GET(self):
        return render.index()

class Register:

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
        return render.register(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.register(form)
        data.login(form.d.Username,form.d.Password)
        raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
