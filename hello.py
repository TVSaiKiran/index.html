from flask import Flask,render_template,redirect,url_for,request,session
import mysql.connector
app=Flask(__name__)
app.secret_key="secret_key"
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python")
cursor=conn.cursor(dictionary=True)
@app.route('/')
def home():
    return render_template('index.html')
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        cursor.execute('insert into login(name,email,password) values(%s,%s,%s)',(name,email,password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template("register.html")
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        cursor.execute('select *from login where email=%s and password=%s',(email,password))
        user=cursor.fetchone()
        if user:
            session['user']=user['name']
            return redirect(url_for('endpoint'))
    return render_template('login.html')
@app.route('/endpoint')
def endpoint():
    if 'user' in session:
        return render_template('home.html',content=f"you login successfully {session['user']}")
    else:
        return render_template('login.html',content="you have to check your login details")

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))
if __name__=='__main__':
    app.run(debug=True)

