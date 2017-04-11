from flask import Flask,render_template,redirect,url_for,request,flash,session
from db_queries import Database
import re,json

app = Flask(__name__)
app.secret_key = 'DBMS'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'project1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db = Database(app)

<<<<<<< HEAD
=======
def chech_admin():
    if 'admin' in session:
        return True
    return False

def check_user():
    if 'user' in session:
        return True
    return False

>>>>>>> 0665118d7706bd40232eec3706078a6553b6c5c5
@app.route('/')
@app.route('/index')
def index():
     if check_user():
        return render_template('user.html')
     return render_template('index.html')

@app.route('/login/submit', methods=['POST'])
def loginSub():
    userid = request.form['email']
    password = request.form['password']
    if db.auth_user(userid,password) is None:
        return redirect('/')
    else:
        auth,uid = db.auth_user(userid,password)
        if auth=='User':
            session['user']=uid
            return render_template('user.html')
        else:
            session['admin']=uid
            return redirect('admin')


@app.route('/admin')
def admin():
    if chech_admin():
        return render_template('admin.html')
    else:
        return render_template('index.html')

@app.route('/user')
def user():
    if check_user():
        return render_template('user.html')
    else:
        return redirect('/')

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

@app.route('/show_halls')
def show_halls():
    halls = db.get_halls()
    return render_template('admin/halls.html',halls=halls)

@app.route('/show_hall_movies',methods=['POST'])
def show_hall_movies():
    if request.form['hall']=='All':
        shows=db.get_movies()
        return render_template('/admin/all_shows.html',shows=shows)
    else:
        hid = int(request.form['hall'])
        shows = db.get_shows_of_hall(hid)
        return render_template('/admin/all_shows.html',shows=shows)

@app.route('/remshow/submit',methods=['POST'])
def rem_show_sub():
    hid = int(request.form['hid'])
    mid = int(request.form['mid'])
    time = request.form['time']
    print hid,mid,time
    if hid and mid and time:
        print "Sdfdf"
        db.delete_show(hid,mid,time)
    return redirect('admin')

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
    desc = re.sub("\'","",desc)
    desc = re.sub("\"","",desc)
    img = request.form['img']
    lang = request.form['lang']
    genre = request.form['genre']
    db.add_movie(title, desc, rating, lang, img, genre)
    return redirect('admin')

@app.route('/remmovie/submit',methods=['POST'])
def rem_movie_sub():
    mid = request.form['movie']
    db.delete_movie(mid)
    return redirect('admin')

@app.route('/viewmovie')
def view_movie():
    return render_template('user/viewmovie.html',movie=movie)

@app.route('/bookmovie/<mid>')
def book_movie(mid):
    movie = db.get_movie(mid)[0]
    shows = db.get_shows_of_movie(mid)
    return render_template('user/bookmovie.html',movie=movie,shows=shows)

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

@app.route('/getseats',methods=['POST'])
def getseats():
    res = request.form['hall']
    res = res.split(',')
    mid = res[0]
    hall = res[1]
    time = res[2]
    res = db.get_seats(mid,hall,time)
    return render_template('user/seats.html',res=res)

@app.route('/payment',methods=['POST'])
def pay():
    seats = request.form['del']
    seats = seats.split(',')
    seat_list = [ int(x) for x in seats ]
    res = request.form['res']
    res = eval(res)
    uid = session['user']
    price = {}
    price['Platinum'] = 250
    price['Silver'] = 150
    price['Gold'] = 200
    np = 0
    ng = 0
    ns = 0
    cost = 0
    a = 0
    for x in seat_list:
        a = price[res['seat_type'][x]]
        if a == 250:
            np+=1
        elif a==200:
            ng+=1
        else:
            ns+=1
        cost += a
    j = {'mid':res['mid'],'hid':res['hid'],'time':res['time'],'uid':uid,'seat_list':seat_list,'cost':cost,'num':[np,ng,ns]}
    return render_template('user/pay.html',res=j)
    # success = db.book(res['mid'], res['hid'], res['time'], uid, seat_list)

@app.route('/payment/success',methods=['POST'])
def pay_sub():
    res = request.form['res']
    res = eval(res)
    success = db.book(res['mid'], res['hid'], res['time'], res['uid'], res['seat_list'])
    return (success)

@app.route('/logout_admin')
def logout_admin():
    session.pop('admin',None)
    return redirect('/')

@app.route('/logout_user')
def logout_user():
    session.pop('user',None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
