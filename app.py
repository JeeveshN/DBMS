from flask import Flask,render_template,redirect,url_for,request,flash,session


app = Flask(__name__)

@app.route('/')
@app.route('/logged_in',method=['POST','GET'])
def logged_in():

	if 'user' in session:
		return render_template('')
	if request.method == 'POST':
		""" Implement user login functionality """


	return render_template('login.html')

@app.route('/change_show',method=['POST'])
def change_show():


@app.route('/change_movie',method=['POST'])
def change_movie():

@app.route('/all_movies')
def all_movies():

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect(url_for('logged_in'))






if __name__ == '__main__':
	app.run(debug=True)