import web
import model
import md5
web.config.debug = False


urls = (
        '/' , 'Index' ,
        '/login' , 'Login',
        '/register' , 'Register' ,
        '/logout' , 'Logout' ,
        '/data' , 'Data' ,
        '/new' , 'New' ,
        '/delete/(\d+)' , 'Delete' ,
        '/list' , 'List' ,
        '/edit/(\d+)' , 'Edit' ,
        '/show/(\d+)' , 'Show' ,
        )


# Object handling the session of a user
app = web.application(urls, globals())
if web.config.get('_session') is None:
    session = web.session.Session(app,web.session.DiskStore('sessions'),initializer=  {'t_user': '', 't_auth':False,'t_level':0,'t_id':-1})
    web.config._session = session
else: 
    session = web.config._session



### Global variables
t_globals = {
    'datestr': web.datestr,
    'session' : session
}




render = web.template.render('templates',base='base', globals=t_globals)

data = model.model(render,session)

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

	if data.login(form.d.Username,md5.md5(form.d.Password).hexdigest()):
	    return render.index()
	else:
	    return render.login(form,True)
    
##############################################################################
# Register
##############################################################################    
class Register:

    form = web.form.Form(
        web.form.Textbox('Username', web.form.notnull,
            size=30,
            description="User:"),
        web.form.Textbox('EMail', web.form.notnull, web.form.regexp('[^@]+@[^@]+\.[^@]+', 'Must be in form of *@*.*'),
            size=30,
            description="E-Mail:"),
        web.form.Password('Password', web.form.Validator('Must be more at least 8 charcters long', lambda x:int(x)>7),
            description="Password:"),
         web.form.Password('PasswordRepeated',web.form.Validator('Must be more at least 8 charcters long', lambda x:int(x)>7),
            description="Repeat password:"),
        web.form.Button('send'),
        validators = [web.form.Validator("Passwords didn't match.", lambda i: i.Password == i.PasswordRepeated),
			 ],
    )

    def GET(self):
        form = self.form()
        return render.register(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.register(form)
        else:
            res = data.register(form.d.Username,form.d.EMail,form.d.Password)
            if res:
                return render.index()
            else:
                return render.register(form,True)
	   

##############################################################################
# Logout
##############################################################################
class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')
    
##############################################################################
# Delete
##############################################################################
class Delete:
    def POST(self,postID):
        data.deletePost(int(postID))
        raise web.seeother('/data')
    
##############################################################################
# Show data sets of a specific user
##############################################################################
class Data:
    def GET(self):
        posts = data.getPosts()
        return render.data(posts)
    
##############################################################################
# Show data sets
##############################################################################
class List:
    def GET(self):
        posts = data.getAllPosts()
        return render.list(posts)
    
##############################################################################
# Show full data set
##############################################################################
class Show:
    def GET(self,postID):
        posts = data.getPost(int(postID))
        return render.show(posts)
    
##############################################################################
# Insert new data set
##############################################################################
class New:
    
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            size=30,
            description="Title of the data set:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description="Description of the data set:"),
        web.form.Textbox('link', web.form.notnull, 
            size=30,
            description="Link to the data set:"),
        web.form.Button('Post data set')
    )
    
    def GET(self):
        form = self.form()
        return render.new(form)
    
    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        else:
            res = data.new(form.d.title,form.d.content,form.d.link)
            if res:
                raise web.seeother('/data')
            else:
                return render.new(form,True)
    
    
    
if __name__ == "__main__":
    app.run()
