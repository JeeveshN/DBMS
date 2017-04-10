from flaskext.mysql import MySQL

class Database():

	def __init__(self, app):
		sql = MySQL()
		sql.init_app(app)
		self.cursor = sql.connect().cursor()

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

	def auth_user(self, id, pwd):
		self.cursor.execute("SELECT type FROM user WHERE email='%s' AND pass='%s'" % (id, pwd))
		res = self.cursor.fetchall()
		try:
			type = res[0][0]
		except:
			return None
		return type
