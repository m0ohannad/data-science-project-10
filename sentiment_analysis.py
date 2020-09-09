import requests
from flask import jsonify

#payload = {'count': 1000 , 'sort_order': 'ASC'}
count = 1000
sort_order = 'ASC'
result = requests.get("http://127.0.0.1:3000/get_data/{}/{}".format(count,sort_order) , headers= {"Content-Type": "application/json"})


data = result.json()
review = []
label = []

for d in data:
	review.append(d[0])
	label.append(d[1])

print(review)


import pickle
with open('model.pickle', 'rb') as file:
	model = pickle.load(file)

with open('vectorizer.pickle', 'rb') as file:
	vectorizer = pickle.load(file)


import re
def clean_text(text):
	text = text.lower()
	text = re.sub("@[a-z0-9_]+", ' ', text)
	text = re.sub("[^ ]+\.[^ ]+", ' ', text)
	text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
	text = re.sub("[^a-z\' ]", ' ', text)
	text = re.sub(' +', ' ', text)

	return text


clean_review = []
for r in review:
	clean_review.append(clean_text(r))

review_vector = vectorizer.transform(clean_review)

label_pred = model.predict(review_vector)


count = 1000
label_positive = 'positive'
label_negative = 'negative'
positive_result = requests.get("http://127.0.0.1:3000/get_data_count/{}/{}".format(label_positive, count) , headers= {"Content-Type": "application/json"})
negative_result = requests.get("http://127.0.0.1:3000/get_data_count/{}/{}".format(label_negative , count) , headers= {"Content-Type": "application/json"})

positive_count = positive_result.json()
negative_count = negative_result.json()

print("عدد النصوص الإيجابية:")
print(positive_count)
print("عدد النصوص السلبية:")
print(negative_count)


from sklearn.metrics import accuracy_score
print('دقة عمل النموذج:')
print(accuracy_score(label, label_pred)*100)
