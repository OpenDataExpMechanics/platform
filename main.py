import web

urls = ( 
        '/' , 'Index'
        )

### Templates
t_globals = {
    'datestr': web.datestr
}

render = web.template.render('templates',base='base', globals=t_globals)

class Index:
    def GET(self):
        return render.index()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
