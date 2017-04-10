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
	return render_template('admin/addshow.html')

@app.route('/remshow')
def rem_show():
	return render_template('admin/remshow.html')

@app.route('/addhall')
def add_hall():
<<<<<<< HEAD
	return render_template('admin/addhall.html')

@app.route('/remhall')
def rem_hall():
	return render_template('admin/remhall.html')
=======
	db.add_hall('Audi 5', 10, 15, 25)
	return ('Add Hall')

@app.route('/remhall')
def rem_hall():
	db.delete_hall(8)
	return ('Remove Show')
>>>>>>> cb9197858084b0e7ffffb2315c7e2b73a558755a

@app.route('/test')
def test():
	return db.get_halls()

@app.route('/addmovie')
def add_movie():
	return render_template('admin/addmovie.html')

@app.route('/remmovie')
def rem_movie():
	return render_template('admin/remmovie.html')

# @app.route('/addshow/submit',methods=['POST'])
# def add_show_sub():

# @app.route('/remshow/submit',methods=['POST'])
# def rem_show_sub():

@app.route('/addhall/submit',methods=['POST'])
def add_hall_sub():
	hname = request.form['hname']
	n_p = request.form['num_platinum']
	n_g = request.form['num_gold']
	n_s = request.form['num_silver']
	db.add_hall(hname,n_p,n_g,n_s)
	return redirect('admin')

# @app.route('/remhall/submit',methods=['POST'])
# def rem_hallSub():

@app.route('/addmovie/submit',methods=['POST'])
def add_movieSub():
	title = request.form['mname']
	rating = request.form['mrating']
	desc = request.form['desc']
	img = request.form['image']
	lang = request.form['lang']
	genre = request.form['genre']
	db.add_movies(title, desc, rating, lang, img)
	return redirect('admin')

# @app.route('/remmovie/submit',methods=['POST'])
# def rem_movieSub():

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