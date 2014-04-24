from flask import Flask
from flask import render_template
from flask import request
from classifier import Classifier
app = Flask(__name__)
 
s = Classifier('localhost',27017,'news_db','news_collection')
s.fillDicts()
print "Document classification finished"
 
@app.route('/')
def main():
	return render_template('index.html')

@app.route('/classify',methods = ['POST'])
def classify():
	dict = s.classify(request.form["text"])
	dict = sorted(dict.items(), key=lambda x: -x[1])
	resultString = ""
	for index in dict:
		resultString += index[0] + " : " + str(index[1]) + "<br>"		
	return resultString
	
if __name__ == "__main__":
	app.debug = True
	app.run()

