from flaskext.mysql import MySQL

class Database():

	def __init__(self, app):
		sql = MySQL()
		sql.init_app(app)
		self.conn = sql.connect()
		self.cursor = self.conn.cursor()


	def auth_user(self, id, pwd):
		self.cursor.execute("SELECT type FROM user WHERE email='%s' AND pass='%s'" % (id, pwd))
		res = self.cursor.fetchall()
		try:
			type = res[0][0]
		except:
			return None
		return type

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
		return str(json)

	def add_hall(self, h_name, platinum, gold, silver):
		i = 1
		self.cursor.execute("INSERT INTO hall(h_name) VALUES('%s')" % h_name)
		(hid, h_name, n_seats) = self.cursor.fetchone()
		for _ in range(platinum):
			self.cursor.execute("INSERT INTO has_seats(hid,sid,type) VALUES(%d, %d, 'Platinum')" % (hid, i))
			i += 1
		for _ in range(gold):
			self.cursor.execute("INSERT INTO has_seats(hid,sid,type) VALUES(%d, %d, 'Gold')" % (hid, i))
			i += 1
		for _ in range(silver):
			self.cursor.execute("INSERT INTO has_seats(hid,sid,type) VALUES(%d, %d, 'Silver')" % (hid, i))
			i += 1
		self.conn.commit()

	def delete_hall(self, hid):
		hid = str(hid)
		self.cursor.execute("DELETE FROM hall WHERE hid=%s" % (hid))
		self.conn.commit()

	def get_movies(self):
		self.cursor.execute("select * from movie")
		res = self.cursor.fetchall()
		print(type(res))
		json = []
		for (mid, title, rating, descr, img, lang) in res:
			x = {
				"mid": mid,
				"title": title,
				"rating": rating,
				"descr": descr,
				"img": img,
				"lang": lang
			}
			json.append(x)
		return str(json)

	def add_movies(self, title, descr, rating, lang, img):
		query = "INSERT INTO movie(title, rating, descr, img, lang) VALUES('%s','%s','%s','%s','%s')" % (title, rating, descr, img, lang)
		self.cursor.execute(query)
		self.conn.commit()

	def delete_movie(self, mid):
		mid = str(mid)
		self.cursor.execute("DELETE FROM movie WHERE mid=%s" % (mid))

