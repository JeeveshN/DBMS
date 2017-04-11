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
		self.cursor.execute("SELECT type, uid FROM user WHERE email='%s' AND pass='%s'" % (id, pwd))
		res = self.cursor.fetchall()
		print (res)
		try:
			type = res[0][0]
		except:
			return None
		return type,res[0][1]

	# Done
	def get_halls(self):
		self.cursor.execute("select * from hall")
		res = self.cursor.fetchall()
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
		platinum = int(platinum)
		gold = int(gold)
		silver = int(silver)
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
		return json

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
		descr = str(descr)
		img = str(img)
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

	# Done
	def delete_show(self, hid, mid, time):
		try:
			time = time.strftime("%Y-%m-%d %H:%M:%S")
		except:
			pass
		print(time)
		print("DELETE FROM shows WHERE hid=%d AND mid=%d AND time='%s'"%(hid, mid, time))
		self.cursor.execute("DELETE FROM shows WHERE hid=%d AND mid=%d AND time='%s'"%(hid, mid, time))
		self.conn.commit()
		return 'Success'

	def register_user(self, fname, lname, email, phno, pwd):
		type = "User"
		self.cursor.execute("INSERT INTO user(fname, lname, email, phno, pass, type) VALUES('%s', '%s', '%s', '%s', '%s', '%s')"%(fname, lname, email, phno, pwd, type))
		uid = self.cursor.lastrowid
		return uid

	def get_shows_of_movie(self, mid):
		mid = int(mid)
		d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.cursor.execute("SELECT * FROM hall NATURAL JOIN shows NATURAL JOIN movie WHERE mid=%d AND time>'%s'"%(mid, d))
		res = self.cursor.fetchall()
		json = []
		for (mid,hid,h_name,n_seats,time,avail,title,rating,descr,img,lang) in res:
			x = {
				"mid": mid,
				"hid": hid,
				"h_name": h_name,
				"time": time,
				"avail": avail
			}
			json.append(x)
		return json

	def get_shows_of_hall(self,hid):
		self.cursor.execute("SELECT * FROM hall NATURAL JOIN shows NATURAL JOIN movie WHERE hid=%d" %hid)
		res = self.cursor.fetchall()
		json = []
		for (mid,hid,h_name,n_seats,time,avail,title,rating,descr,img,lang) in res:
			x = {
				'hid':hid,
				'mid':mid,
				'h_name':h_name,
				"title": title,
				"img":img,
				"descr":descr,
				"lang":lang,
				"time": time,
				"avail": avail
			}
			json.append(x)
		return json

	def get_seats(self, mid, hid, time):
		mid = int(mid)
		hid = int(hid)
		if not isinstance(time, str):
			time = time.strftime("%Y-%m-%d %H:%M:%S")
		self.cursor.execute("SELECT bid FROM booking WHERE hid=%d AND mid=%d AND time='%s'"%(hid, mid, time))
		bids = []
		for b in self.cursor.fetchall():
			x = b[0]
			bids.append(x)
		booked_sids = []
		if len(bids)>0:
			f_str = ','.join(['%s']*len(bids))
			self.cursor.execute("SELECT sid FROM seats_booked WHERE hid=%d AND bid in (%s)" % (hid, (f_str % tuple(bids))))
			for b in self.cursor.fetchall():
				x = b[0]
				booked_sids.append(x)
		self.cursor.execute("SELECT sid, type FROM has_seats WHERE hid=%d"%hid)
		sid_status = {}
		sid_type = {}
		for (b,t) in self.cursor.fetchall():
			if b in booked_sids:
				sid_status[b] = 'booked'
			else:
				sid_status[b] = 'avail'
			sid_type[b] = t

		self.cursor.execute("SELECT title FROM movie WHERE mid=%d" % mid)
		title = self.cursor.fetchall()[0][0]
		json = {
			'title': title,
			'mid': mid,
			'hid': hid,
			'time': time,
			'seats': sid_status,
			'seat_type': sid_type
		}
		return json

	def book(self, mid, hid, time, uid, seat_list):
		mid = int(mid)
		hid = int(hid)
		uid = int(uid)
		if not isinstance(time, str):
			time = time.strftime("%Y-%m-%d %H:%M:%S")
		n_seats = 0
		for _ in seat_list:
			n_seats += 1
		self.cursor.execute("INSERT INTO booking(mid, hid, time, uid, n_seats) VALUES(%d, %d, '%s', %d, %d)" % ( mid, hid, time, uid, n_seats))
		bid = self.cursor.lastrowid
		for sid in seat_list:
			self.cursor.execute("INSERT INTO seats_booked(bid, sid, hid) VALUES(%d,%d,%d)"%(bid, sid, hid))
		self.conn.commit()
		return 'Success'

	def get_movie(self, mid):
		mid= int(mid)
		self.cursor.execute("select * from movie where mid = %d" % mid)
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


"""
Receive movie from user
Return hall and time of shows (Page 1)
Receive a hall and time
Return list of available seats (Page 2)
Get set of seats, hid, mid, time, eid
Make booking EZPZ
"""
