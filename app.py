from flask import Flask,render_template,redirect,url_for,request,flash,session
from db_queries import Database

app = Flask(__name__)
app.secret_key = 'DBMS'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ms101234321'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db = Database(app)

def authorize(u,p):
	return None


@app.route('/')
@app.route('/index')
def index():
	# if 'user' in session:
	# 	if session['user'] == 'User':
	# 		return redirect('user')
	# 	else:
	# 		return redirect('admin')
	return render_template('index.html')

@app.route('/login/submit', methods=['POST'])
def loginSub():
	userid = request.form['email']
	password = request.form['password']
	auth = db.auth_user(userid,password)
	print(auth)
	if auth is not None:
		session['user']=auth
		if auth=='User':
			return('User')
		else:
			return redirect('admin')
	else:
		return redirect('')

@app.route('/admin')
def admin():
	# if not 'user' in session:
	# 	return redirect('')
	# elif session['user'] is not 'Admin':
	# 	return redirect('')
	return render_template('admin.html')

@app.route('/user')
def user():
	# if not 'user' in session:
	# 	return redirect('')
	# elif session['user'] is not 'User':
	# 	return redirect('')
	return render_template('user.html')

@app.route('/addshow')
def add_show():
	return ('Add Show')

@app.route('/remshow')
def rem_show():
	return ('Remove Show')

@app.route('/addhall')
def add_hall():
	db.add_hall('Audi 5', 10, 15, 25)
	return ('Add Hall')

@app.route('/remhall')
def rem_hall():
	db.delete_hall(8)
	return ('Remove Show')

@app.route('/test')
def test():
	return db.get_halls()

@app.route('/addmovie')
def add_movie():
	return ('Add Movie')

@app.route('/remmovie')
def rem_movie():
	return ('Remove Movie')
# @app.route('/change_show',method=['POST'])
# def change_show():


# @app.route('/change_movie',method=['POST'])
# def change_movie():

# @app.route('/all_movies')
# def all_movies():

# @app.route('/logout')
# def logout():
# 	session.pop('user',None)
# 	return redirect(url_for('logged_in'))






if __name__ == '__main__':
	app.run(debug=True)