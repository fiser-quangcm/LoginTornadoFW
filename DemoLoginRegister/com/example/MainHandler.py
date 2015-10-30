'''
Created on 29-Oct-2015

@author: sf4u
'''
import tornado.ioloop
import tornado.web
import torndb


class DBHandler(tornado.web.RequestHandler):
    def get(self):
        db = torndb.Connection(
            host="localhost", database="Users",
            user="root", password="q135773751")
        rows = db.query("select id,username,password from Users")
        db.close()
        top = "<html><body><b>List Acc</b><br /><br />"
        table = "<table border=\"1\"><col width=\"50\" /><col width=\"200\" />"
        for row in rows:
            table += "<tr><td>" + str(row["id"]) + "</td><td>" +str(row["username"]) + "</td><td>" + str(row["password"]) + "</td></tr>"
        bottom = "</body></html>"
        self.write(top+table+bottom)
        
        if db == None:
            self.write("Error connect")
            return None
        if rows == None :
            self.write("Empty Acc")
class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Register.html")
        
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        
        db = torndb.Connection(
        host="localhost", database="Users",
        user="root", password="q135773751")
        rows = db.query("select username,password from Users")
        
        
        for row in rows:
            if (str(row["username"]) == username):
                self.write("Username exists!!")
                db.close()
                return None
        
        db.query("insert into Users(username,password) values ('"+ username + "','" + password + "')" )
        db.close()
class LoginHandler(tornado.web.RequestHandler):
        def get(self):
            self.render("Login.html")
            

        def post(self):
            username = self.get_argument('username')
            password = self.get_argument('password')
            
            db = torndb.Connection(
            host="localhost", database="Users",
            user="root", password="q135773751")
            rows = db.query("select username,password from Users")
            db.close()
            
            for row in rows:
                if (str(row["username"]) == username and str(row["password"]) == password):
                    self.redirect("/")
                    return None
            self.redirect("login")    
               
            
class IndexHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello World")
                            
application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/accessAcc", DBHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()