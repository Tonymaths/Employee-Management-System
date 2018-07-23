#importing libraries
from flask import Flask,render_template,request,url_for,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import exc
from functools import wraps
import os,re


app = Flask(__name__)
#app configuration 
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1/mind2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='ryeze'
app.config['MAX_CONTENT_LENGHT']= 6* 1024 *1024
app.config['UPLOAD_FOLDER']='C:\\Users\TONY EZEMBAMALU\Downloads\lectures\programming projects\mind2\static\my_pix'
ALLOWED_EXTENTIONS= set(['txt','jpg','pdf'])

db =SQLAlchemy(app)

#blog content db column
class Tony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(80),  unique=True )
    content = db.Column(db.String(400) , unique=True)
    #comment = db.Column(db.String(70), unique=True)
    date_posted=db.Column(db.DateTime())

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment= db.Column(db.String(400) , unique=True)
    date_posted2=db.Column(db.DateTime())


#registration db table
class reg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user =db.Column(db.String(20) ,unique=False, nullable=False)
    email = db.Column(db.String(50) , unique=True, nullable=False)
    password=db.Column(db.String(15), nullable=False)
    date_reg=db.Column(db.DateTime())


@app.route('/')
def index():
    result=Tony.query.order_by(Tony.date_posted.desc()).all()
    posts = Comments.query.filter_by(id=comment).all()

    return render_template('index.html', result=result, post=posts)


@app.route('/contact', methods=['GET','POST'])
def contact():
 if request.method=='POST':

    title=request.form['title1']
    content=request.form['content1']
    if title=='':
        error='PLEASE ENTER TITLE FIELD'
        return render_template('sign2.html', error=error)
    elif content == '':
        error = 'PLEASE ENTER CONTENT FIELD'
        return render_template('contact.html',error=error )

    else:
       flash(' REQUEST SUCCESSFULLY SENT ')
    #return '<h1> title:{} contents:{}</h1>'.format(title,content)
# adding values to db, similar to execute function in msql
       me=Tony(title=title,content=content,date_posted=datetime.now())
       db.session.add(me)
       #db.session.commit()
       return redirect(url_for('contact'))
 return render_template('contact.html')




#handling login/out with session
@app.route('/sign', methods=['GET','POST'])
def sign():
  if request.method== 'POST':
    login_email=request.form['email']
    login_password=request.form['pass']
    reg_email=reg.query.filter_by(email=login_email).first()
    if reg_email is None:
        session['logged_in']=False
        error='INVALID LOGIN'
        return render_template('sign.html', error=error)
    else:
       actual_password=reg_email.password
       if actual_password==login_password:
        session['logged_in']=True
        session['username']=reg_email.user
        return redirect(url_for('sign2'))
       else:
           error='PASSWORD MISMATCH'
           return render_template('sign.html', error=error)
  return render_template('sign.html')



"""def is_logged_in(f):
  @wraps(f)
  def wrap(*args, **kwargs):
      if 'is_logged_in' in session:
          return f(*args, **kwargs)
      else:
          flash('NOT AUTHORIZED ', 'danger')
          redirect(url_for(sign))
  return wrap"""

@app.route('/logout')
def logout():
    session.clear()
    flash('YOU ARE NOW LOGGED OUT', 'success')
    return redirect(url_for('sign'))

#REGISTRATION PROCESS
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
     user_name=request.form['username']
     email=request.form['email']
     password=request.form['password']
     confirm_password=request.form['confirm']
     reg_email = reg.query.filter_by(email=email).first()
     reg_user = reg.query.filter_by(user=user_name).first()
     pattern=r'[^@]+@[^@]+\.[^@]+'
     email_pattern=re.match(pattern, email)

     if password=='' or confirm_password=='' or email=='' or user_name=='':
         error = 'PLEASE ENTER ALL FIELDS'
         return render_template('register.html', error=error)
     if email_pattern is None:
         error = 'PLEASE ENTER A VALID EMAIL ADDRESS'
         return render_template('register.html', error=error)
     if len(password) < 5:
         error = 'PLEASE ENTER MINIMUM 5 CHARACTERS FOR PASSWORD '
         return render_template('register.html', error=error)

     if reg_email is not None:
         error = 'EMAIL ADDRESS ALREADY TAKEN, IF PREVIOUSLY REGISTERED, PLEASE SIGN IN'
         return render_template('register.html', error=error)
     if reg_user is not None:
         error = 'USER NAME ALREADY TAKEN, TRY SOMETHING MORE UNIQUE'
         return render_template('register.html', error=error)

     elif password!=confirm_password:
         error='PASSWORD DO NOT MATCH'
         return render_template('register.html', error=error)

     else:
         #commit reg details to db
         span=reg(user=user_name, email=email, password=password, date_reg=datetime.now())
         try:
          db.session.add(span)
          db.session.commit()
         except exc.IntegrityError:
             db.session().rollback()
         flash('SUCCESSFULL REGISTRATION, YOU CAN NOW LOG IN')

     return render_template('register.html')
    return render_template('register.html')



#@app.route('/comment')
#def comment():

# return render_template('comment.html')

@app.route('/comment/<int:post_id>/')
def comment(post_id):
    posts=Comments.query.filter_by(id=post_id).one()
    return render_template('comment.html', post=posts)


#single article route
@app.route('/comment_process', methods=['GET','POST'] )
#@is_logged_in
def comment_process():
  if request.method == 'POST':
    comment = request.form['comment']
    #comment_title=Tony.query.filter_by(title=comment.title)
    if comment == '':
      error = 'PLEASE ENTER A COMMENT'
      return render_template('comment.html', error=error)
    else:
        commentv=Comments(comment=comment,  date_posted2=datetime.now())
        try:
          db.session.add(commentv)
          db.session.commit()

        except exc.IntegrityError:
            db.session().rollback()
        return render_template('comment.html')
  return render_template('comment.html')



# making comment and creating posts
@app.route('/sign2')
#@is_logged_in
def sign2():
    #post=Tony.query.filter_by(Tony.content).one()
    return render_template('sign2.html')


@app.route('/process', methods=['GET','POST'])
def process():
 if request.method=='POST':

# nb 'title' etc has already been mention in the html file
    title=request.form['title']
    content=request.form['content']
    if title=='':
        error='PLEASE ENTER TITLE FIELD'
        return render_template('sign2.html', error=error)
    elif content == '':
        error = 'PLEASE ENTER CONTENT FIELD'
        return render_template('sign2.html',error=error )

    else:
       flash(' ONE NEW RECORD FOUND ')
    #return '<h1> title:{} contents:{}</h1>'.format(title,content)
# adding values to db, similar to execute function in msql
       me=Tony(title=title,content=content,date_posted=datetime.now())
       db.session.add(me)
       db.session.commit()
       return redirect(url_for('home'))

 return render_template('sign.html')
#The file upload route

@app.route('/uploads')
def uploads():
    return render_template('uploads.html')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENTIONS


@app.route('/upload_process', methods=['GET','POST'])
def upload_process():
 if request.method=='POST':


    my_upload=request.files['file']

    if 'my_upload' is None:
        error='PLEASE SELECT A FILE'
        return render_template('uploads.html', error=error)

    if not allowed_file(my_upload.filename):
        error = 'FILE FORMAT NOT SUPPORTED IN MASSAPP '
        return render_template('uploads.html', error=error)

    if my_upload and allowed_file(my_upload.filename):

        my_upload.save(os.path.join(app.config['UPLOAD_FOLDER'],my_upload.filename))
        flash(' UPLOAD SENT SUCCESSFULLY, ')
        return redirect(url_for('uploads', filename=my_upload.filename))



if __name__ == '__main__':
    app.run(debug='true')
