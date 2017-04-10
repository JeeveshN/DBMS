from flask import Flask,render_template,redirect,url_for,request,flash,session
from db_queries import Database
import re

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
	halls=db.get_halls()
	movies = db.get_movies()
	days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	return render_template('admin/addshow.html',halls=halls,movies=movies,days=days)

@app.route('/remshow')
def rem_show():
	return render_template('admin/remshow.html')

@app.route('/addhall')
def add_hall():
	return render_template('admin/addhall.html')

@app.route('/remhall')
def rem_hall():
	halls = db.get_halls()
	return render_template('admin/remhall.html', halls=halls)

@app.route('/addmovie')
def add_movie():
	return render_template('admin/addmovie.html')

@app.route('/remmovie')
def rem_movie():
	movies = db.get_movies()
	return render_template('admin/remmovie.html', movies=movies)

@app.route('/addshow/submit',methods=['POST'])
def add_show_sub():
	hid = request.form['hall']
	mid = request.form['movie']
	time = request.form['time']
	time = re.sub('T'," ",time)
	time = time+":00"
	db.add_show(int(hid),int(mid),time)
	return redirect('admin')

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

@app.route('/remhall/submit',methods=['POST'])
def rem_hall_sub():
	bid = request.form['del']
	print(bid)
	if bid:
		db.delete_hall(bid)
	return redirect('admin')

@app.route('/addmovie/submit',methods=['POST'])
def add_movie_sub():
	title = request.form['mname']
	rating = request.form['mrating']
	desc = request.form['desc']
	img = request.form['image']
	lang = request.form['lang']
	genre = request.form['genre']
	db.add_movie(title, desc, rating, lang, img, genre)
	return redirect('admin')

# @app.route('/remmovie/submit',methods=['POST'])
# def rem_movie_sub():

@app.route('/viewmovie')
def view_movie():
	return render_template('user/viewmovie.html',movie=movie)

# @app.route('/bookmovie')
# def book_movie():
# 	return render_template('user/bookmovie.html')

@app.route('/searchmovie')
def search_movie():
	return render_template('user/searchmovie.html')

@app.route('/allmovies')
def all_movie():
	movies = db.get_movies()
	return render_template('user/allmovie.html',movies=movies)

@app.route('/bookmovie/submit',methods=['POST'])
def book_movie_sub():
	return render_template('user/bookmovie.html')

@app.route('/searchmovie/submit',methods=['POST'])
def search_movie_sub():
	movie = request.form['mname']
	print(movie)
	res = db.get_movie_search(movie)
	if res:
		return render_template('user/viewmovie.html',movie=res)
	return render_template('user/searchmovie.html')
# @app.route('/logout')
# def logout():
# 	session.pop('user',None)
# 	return redirect(url_for('logged_in'))


if __name__ == '__main__':
	app.run(debug=True)
