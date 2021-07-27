import pymysql
import numpy as np
import pickle
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import warnings
warnings.filterwarnings("ignore")

db = pymysql.connect(host="localhost",user="root",passwd="mysql",database="adityaraj")

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@cross_origin()
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@cross_origin()
@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        experience = request.form['experience']
        test_score = request.form['test_score']
        interview_score = request.form['interview_score']
        cur = db.cursor()
        cur.execute(f"Insert into salary1 (Experience,TestScore,InterviewScore) values ({experience},{test_score},{interview_score})")
        db.commit()
        feat = [[experience,test_score,interview_score]]
        pred = model.predict(feat)
        output = round(pred[0], 2)
        return render_template('index.html', prediction_text="Employee salary should be $ {}".format(output))


if __name__ == "__main__":
    app.run()