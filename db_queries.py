from flaskext.mysql import MySQL
from datetime import datetime, timedelta

class Database():

	def __init__(self, app):
		sql = MySQL()
		sql.init_app(app)
		self.conn = sql.connect()
		self.cursor = self.conn.cursor()

	# Done
	def auth_user(self, id, pwd):
		self.cursor.execute("SELECT type FROM user WHERE email='%s' AND pass='%s'" % (id, pwd))
		res = self.cursor.fetchall()
		try:
			type = res[0][0]
		except:
			return None
		return type

	# Done
	def get_halls(self):
		self.cursor.execute("select * from hall")
		res = self.cursor.fetchall()
		print(type(res))
		json = []
		for hid, h_name, n_seats in res:
			x = {
				"hid": hid,
				"h_name": h_name,
				"n_seats": n_seats 
			}
			json.append(x)
		return json

	# Done
	def add_hall(self, h_name, platinum, gold, silver):
		i = 1
		self.cursor.execute("INSERT INTO hall(h_name) VALUES('%s')" % h_name)
		hid = self.cursor.lastrowid
		for _ in range(platinum*10):
			self.cursor.execute("INSERT INTO has_seats(hid,sid,type) VALUES(%d, %d, 'Platinum')" % (hid, i))
			i += 1
		for _ in range(gold*10):
			self.cursor.execute("INSERT INTO has_seats(hid,sid,type) VALUES(%d, %d, 'Gold')" % (hid, i))
			i += 1
		for _ in range(silver*10):
			self.cursor.execute("INSERT INTO has_seats(hid,sid,type) VALUES(%d, %d, 'Silver')" % (hid, i))
			i += 1
		self.conn.commit()

	# Done
	def delete_hall(self, hid):
		hid = str(hid)
		self.cursor.execute("DELETE FROM hall WHERE hid=%s" % (hid))
		self.conn.commit()

	# Done
	def get_movies(self):
		self.cursor.execute("select * from movie")
		res = self.cursor.fetchall()
		json = []
		for (mid, title, rating, descr, img, lang) in res:
			self.cursor.execute("SELECT genre FROM movie_genre WHERE mid = %d"%mid)
			genres = self.cursor.fetchall()
			g = []
			for x in list(genres):
				g.append(x[0])
			x = {
				"mid": mid,
				"title": title,
				"rating": rating,
				"descr": descr,
				"img": img,
				"lang": lang,
				"genre": g
			}
			json.append(x)
		return str(json)

	# Done
	def get_movie_search(self, name):
		self.cursor.execute("SELECT * FROM movie WHERE title='%s'" % name)
		res = self.cursor.fetchall()
		json = []
		for (mid, title, rating, descr, img, lang) in res:
			self.cursor.execute("SELECT genre FROM movie_genre WHERE mid = %d"%mid)
			genres = self.cursor.fetchall()
			g = []
			for x in list(genres):
				g.append(x[0])
			x = {
				"mid": mid,
				"title": title,
				"rating": rating,
				"descr": descr,
				"img": img,
				"lang": lang,
				"genre": g
			}
			json.append(x)
		return json

	# Done
	def add_movie(self, title, descr, rating, lang, img, genre):
		query = "INSERT INTO movie(title, rating, descr, img, lang) VALUES('%s', '%s', '%s', '%s', '%s')" % (title, rating, descr, img, lang)
		print(query)
		self.cursor.execute(query)
		pk = self.cursor.lastrowid
		for g in genre.split(','):
			g = g.strip()
			self.cursor.execute("INSERT INTO movie_genre VALUES(%d, '%s')" % (pk, g))
		self.conn.commit()

	# Done
	def delete_movie(self, mid):
		mid = str(mid)
		self.cursor.execute("DELETE FROM movie WHERE mid=%s" % (mid))
		self.conn.commit()


	# Done
	def get_shows(self):
		self.cursor.execute("SELECT * FROM hall NATURAL JOIN shows NATURAL JOIN movie")
		res = self.cursor.fetchall()
		json = []
		for (hid,mid,h_name,n_seats,time,avail,title,rating,descr,img,lang) in res:
			x = {
				"mid": mid,
				"hid": hid,
				"h_name": h_name,
				"n_seats": n_seats,
				"time": time,
				"avail": avail,
				"title": title,
				"rating": rating,
				"descr": descr,
				"img": img,
				"lang":lang
			}
			json.append(x)
		return json

	# Done
	def add_show(self, hid, mid, time):
		newt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
		if newt<datetime.now():
			return 'Old date'
		self.cursor.execute("SELECT time FROM shows WHERE hid=%d"%hid)
		for t in self.cursor.fetchall():
			oldt = t[0]
			dif = ''
			if(oldt>newt):
				dif = oldt-newt
			else:
				dif = newt-oldt
			if timedelta.total_seconds(dif)<7200:
				return 'Intersects slot'
		self.cursor.execute("INSERT INTO shows(hid, mid, time) VALUES(%d, %d, '%s')"%(hid,mid,time))
		self.conn.commit()
		return 'Success'




