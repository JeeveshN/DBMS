from flask import Flask,render_template,redirect,url_for,request,flash,session

app = Flask(__name__)

def authorize(u,p):
	return None

@app.route('/')
def index():
	return render_template('index.html',incorrect='True')

@app.route('/login/submit', methods=['POST'])
def loginSub():
	user = request.form['email']
	password = request.form['password']
	auth = authorize(userid,password)
	print auth
	# if auth is not None:
	# 	session.push('user',auth)
	# 	if(auth=='user'):
	# 		return render_template
	# 	else:
	# 		return render_template
	# else:
	# 	return render_template('index.html',incorrect='True')
	return ('OK')
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