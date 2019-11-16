from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

# initialize scheduler with your preferred timezone
scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.start()


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "xyz41607@gmail.com",
    "MAIL_PASSWORD": "abcxyz12345"
}

app.config.update(mail_settings)
mail = Mail(app)


app.config['MONGO_DBNAME'] = 'student'
app.config['MONGO_URI'] = "mongodb://localhost:27017/student"
CORS(app)
mongo = PyMongo(app)

@app.route('/schedulePrint', methods=['POST'])
def schedule_to_print():
    #get time to schedule and text to print from the json
    #time = "2019-11-13 21:50:00"
    #convert to datetime
    student = mongo.db.student
    data = request.get_json(force=True)
    time = data["time"]
    sec = data["section"] 
    docs = list(student.find({"section": sec}))

    output = []
    for i in docs:
        
        output.append(i['email'])
        print(i)
    
    date_time = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
    print(output)
    job = scheduler.add_job(notification, trigger='date', next_run_time=str(date_time),args = [output])
    return "job details: %s" % job


def notification(output):
	print(output)
	with app.app_context():
            msg = Message(subject="Hello",sender=app.config.get("MAIL_USERNAME"),recipients = output,body="Today is the deadline for your assignment !")
            mail.send(msg)

if __name__ == '__main__':
	
	app.run(debug=True,port=2000)
