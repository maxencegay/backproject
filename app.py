from datetime import timedelta

from unittest import result
from flask import *
import pymongo
import re 
import bcrypt

app = Flask(__name__)
app.secret_key = '1234'
app.permanent_session_lifetime = timedelta(days=1)


client = pymongo.MongoClient("mongodb+srv://maxence:maxou1812@cluster0.0zjke.mongodb.net/")

users=client.project2.users
tweets = client.project2.tweets


@app.route('/signup',methods = ['GET','POST'])
def signup() :
    
    if request.method == 'POST' :
        
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password') 

        
          

    
  
        if (re.search(r"^[\w.+-]+@[\w]+.[a-z]", email)):
            
            if(len(name)>3) and not(re.search(' ',name)) :
                
                if users.find_one({'email' : email}) is None : 
                    if users.find_one({'name' : name}) is None : 
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        password = hashed_password.decode('utf-8')
                        users.insert_one({"name": name, "email": email, "password": password})
                        return render_template('login.html')            

                        
                    else :
                        return render_template('signup.html',errorname = 'Name is not valid',)           
                
                else :                    
                    return render_template('signup.html',errorname = 'email is not valid or is already taken',)     
            
            else :
                return render_template('signup.html',errorname = 'Name is not valid',) 
            
        else :
            return render_template('signup.html', errorpassword='Password is not valid',)

    else :    
        return render_template("signup.html") 


@app.route('/login',methods = ['GET','POST'])
def login() :
    if request.method == 'POST' :        
        name = request.form.get('name')
        password = request.form.get('password')

        res = users.find_one({"name": name}) 



        if users.find_one({"name": name}) : 
            
            if bcrypt.checkpw(password.encode('utf-8'), res['password'].encode('utf-8')) :
                session["user"]= name
                return redirect('home')
            else :
                return render_template("login.html", errorpassword="Incorrect password",)

        else : 
            return render_template("login.html", errorname="Name is incorrect",)




    else : 
        return render_template("login.html") 


@app.route('/home',methods = ['GET','POST'])
def home() :
    if request.method == 'POST' :

        tweet = request.form.get('tweet')
        print(tweet)
        return render_template("home.html")

    else : 
        print(tweet)
        return render_template("home.html")


    

    



@app.route('/',methods = ['GET','POST'])
def index() : 
    return redirect('signup')


if __name__ == "__main__" : 
    app.run(debug=True)
