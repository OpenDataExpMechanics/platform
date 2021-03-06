#!/usr/bin/env python
#-*- coding: utf-8 -*-
#@author: patrick@openexpmechanics.science
import web
import model
import md5, os
import cgi
import configuration as conf
import magic
import shutil
import uuid

web.config.debug = False

urls = (
        '/' , 'Index' ,
        '/login' , 'Login',
        '/register' , 'Register' ,
        '/logout' , 'Logout' ,
        '/data' , 'Data' ,
        '/new' , 'New' ,
        '/delete/(\d+)' , 'Delete' ,
        '/list/(\d+,\d+)' , 'List' ,
        '/edit/(\d+)' , 'Edit' ,
        '/show/(\d+)' , 'Show' ,
        '/deleteFile/(\d+)' , 'DeleteFile' ,
        '/search' , 'Search' ,
        '/files' , 'Files' ,
        '/tags/(.*)' , 'Tags' ,
        '/assets/(.*)' , 'images'
        )


# Object handling the session of a user
app = web.application(urls, globals())
if web.config.get('_session') is None:
    session = web.session.Session(app,web.session.DiskStore('sessions'),initializer=  {'t_user': '', 't_auth':False,'t_upload':False,'t_id':-1})
    web.config._session = session
else:
    session = web.config._session



### Global variables
t_globals = {
    'datestr': web.datestr,
    'session' : session
}

## Render engine
render = web.template.render('templates',base='base', globals=t_globals)

## Configuration loaded from the yaml file
conf = conf.configuration()
cgi.maxlen = conf.size

## Connector to the database
data = model.model(render,session,conf)

##############################################################################
# Main page of the website
##############################################################################
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
        web.form.Password('Password', web.form.Validator('Must be more at least 8 characters long', lambda x:len(x)>7),
            description="Password:"),
         web.form.Password('PasswordRepeated',web.form.Validator('Must be more at least 8 characters long', lambda x:len(x)>7),
            description="Repeat password:"),
        web.form.Button('send'),
        validators = [
	    web.form.Validator("Passwords didn't match.", lambda i:i.Password==i.PasswordRepeated),
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
            if res == 0:
                return render.index()
            else:
                return render.register(form,res)


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
    def GET(self,postID):
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
    
    form = web.form.Form( 
     web.form.Dropdown('posts', ['All','5','15','50','100'], description="Posts per page"),
     web.form.Button('show'))
    
    def GET(self,values):
        form = self.form()
        res = values.split(',')
        amount = int(res[0])
        if amount == 0:
             form.posts.value = 'All'
        else:
             form.posts.value = amount
        result , pages  = data.getRangePosts(amount,int(res[1])-1)
        return render.list(result,form,pages,amount)
    
    def POST(self,page):
        form = self.form()
        amount = 0
        formData = web.input()
        selected = formData['posts']
        form.posts.value = selected
        if selected == "All":
            amount = 0
        else:
            amount = int(selected)
        result , pages  = data.getRangePosts(amount,int(0))
        return render.list(result,form,pages,amount)

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
            description="Description of the data set:"),
        web.form.Textbox('link', web.form.notnull,
            size=30,
            description="Link to the data set:"),
        web.form.Textbox('tags',  web.form.notnull, size=30 ,description="Tags (separated with ,):"),
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
            res = data.new(form.d.title,form.d.content,form.d.link,form.d.tags)
            if res:
                raise web.seeother('/data')
            else:
                return render.new(form,True)

##############################################################################
# Edit data set
##############################################################################
class Edit:
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=30,
            description="Title of the data set:"),
        web.form.Textarea('content', web.form.notnull,
            rows=10, cols=80,
            description="Description of the data set:"),
        web.form.Textbox('link', web.form.notnull,
            size=30,
            description="Link to the data set:"),
        web.form.Textbox('tags',  web.form.notnull, size=30 ,description="Tags (separated with ,):"),
        web.form.Button('Save changes')
    )

    def GET(self,postID):
        posts = data.getPost(int(postID))[0]
        form = self.form()
        form.fill(posts)
        return render.edit(posts,form)

    def POST(self,postID):
        posts = data.getPost(int(postID))[0]
        form = self.form()
        form.fill(posts)
        if not form.validates():
            return render.edit(posts, form)
        data.updatePost(int(postID),form.d.title,form.d.content,
            form.d.link,form.d.tags)
        posts = data.getPosts()
        return render.data(posts)

##############################################################################
# Search data sets
##############################################################################
class Search:
    
    form = web.form.Form(
         web.form.Textbox('title', web.form.notnull,
            size=30,
            description="Title contains:"),
         web.form.Textbox('tags', web.form.notnull,
            size=30,
            description="Tags contains (separated by ,):"),
         web.form.Button('Search'))
    
    def GET(self):
         form = self.form()
         return render.search(form, [])
     
    def POST(self):
         form = self.form()
         formData = web.input()
         posts = data.search(formData['title'],formData['tags'])
         return render.search(form,posts)
     
##############################################################################
# Search data sets
##############################################################################
class Tags:
    
    def GET(self,name):
        
        tags = data.tags()
        print name
        if name == "All":
            print 'All'
            posts = data.getAllPosts()
        elif len(name) > 0:
            print 'tag'
            posts = data.getPostsByTag(name)
        else:
            posts = []
        return render.tags(tags,posts)
    
##############################################################################
# Search data sets
##############################################################################
class Files:
        
    def GET(self):
        
        res = data.getPostsWithoutFiles()
        
        title = []
        for r in res:
            title.append(r.title)
        
        filedata = data.getFiles()
        
        return render.files(title,filedata,0)
    
    def POST(self):
        
        res = data.getPostsWithoutFiles()
        
        filedata = data.getFiles()
        
        title = []
        for r in res:
            title.append(r.title)
        
        # Check for the maximal file size
        try:
            i = web.input(myfile={})
        except ValueError:
            return render.files(title,filedata,1)
        
        # Check for the mime time
        fileType = magic.from_buffer(i['myfile'].file.read(), mime=True)
        
        if fileType not in conf.types:
            return render.files(title,2)
        
        filedir = str(conf.path) + "/" + str(uuid.uuid1()) + ".zip"
      
        fout = open(filedir,'w')
        fout.write(i['myfile'].file.read())
        fout.close()
        
        data.addFile(i["title"],filedir)
        
        return render.files(title,filedata,0)
        
##############################################################################
# Delete a file
##############################################################################
class DeleteFile:
    
    def GET(self,postId):
        
        res = data.getPostsWithoutFiles()
        
        title = []
        for r in res:
            title.append(r.title)
            
        filedata = data.getFiles()
            
        data.deleteFile(int(postId))
        
        return render.files(title,filedata,0)

##############################################################################
# Serve images
##############################################################################
class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"image/png",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "ico":"image/x-icon",
            "svg":"image/svg" }

        if name in os.listdir('assets'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('assets/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

if __name__ == "__main__":
    app.run()
