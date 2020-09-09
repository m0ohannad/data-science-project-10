from flask import Flask, jsonify
from flask import request
import psycopg2

app = Flask(__name__)

connection = psycopg2.connect(user = "postgres", password= "666333", host = "127.0.0.1", port = "5432", database = "project9")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM data_input")
length_table = cursor.fetchall()[0][0]
cursor.close()
connection.close()

@app.route('/get_data_count/<label_name>/', methods=['GET'])
@app.route('/get_data_count/<label_name>/<count>', methods=['GET'])
def get_data_count(label_name, count=length_table):
	connection = psycopg2.connect(user = "postgres", password= "666333", host = "127.0.0.1", port = "5432", database = "project9")
	cursor = connection.cursor()
	try:
		label_id = 0 if label_name == 'negative' else 1 if label_name == 'positive' else 2
		if label_id == 0 or label_id == 1 :
			cursor.execute("SELECT COUNT(*) FROM data_labeling WHERE label_id = {}  AND review_id < {}".format(label_id , count) )
		else:
			cursor.execute("SELECT COUNT(*) FROM data_labeling WHERE review_id < {}".format(count))
		data_count = cursor.fetchall()[0][0]
		return jsonify(data_count)
	except:
		return "ERROR get_data_count"
	cursor.close()
	connection.close()



@app.route('/get_data/<count>/<sort_order>', methods=['GET'])
def get_data(count ,sort_order):
	connection = psycopg2.connect(user = "postgres", password= "666333", host = "127.0.0.1", port = "5432", database = "project9")
	cursor = connection.cursor()
	try:
		cursor.execute("SELECT * FROM data_input ORDER BY date {} LIMIT {} ".format(str(sort_order), count) )
		data = cursor.fetchall()
		data_label = []
		for d in data:
			cursor.execute("SELECT label_id FROM data_labeling WHERE review_id = %s " , (d[0],))
			l = cursor.fetchall()
			data_label.append((d[1],l[0][0]))
		return jsonify(data_label)
	except:
		return "ERROR get_data"
	cursor.close()
	connection.close()



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000)

