import web

urls = ( 
        '/' , 'Index' , 
        '/register' , 'Register'
        )

### Templates
t_globals = {
    'datestr': web.datestr
}

render = web.template.render('templates',base='base', globals=t_globals)

class Index:
    def GET(self):
        return render.index()
    
class Register:
    
    form = web.form.Form(
        web.form.Textbox('Username', web.form.notnull, 
            size=30,
            description="User:"),
        web.form.Textbox('Password', web.form.notnull, 
            description="Password:"),
        web.form.Button('Login'),
    )
    
    def GET(self):
        form = self.form()
        return render.register(form)    

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
