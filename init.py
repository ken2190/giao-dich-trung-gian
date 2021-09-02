from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database = {
    'host':'194.233.75.100',
    'user':'hieufish_gdtg',
    'password':'A8v.}#zdQgxt',
    'dtb':'hieufish_gdtg'
}

app.secret_key = "adsflkjqoijqawsef0asiodjf9028344jfoasijfpoajsdlkfjaso9fj390asdofjasdoijflsdfdsfasdkjfo"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://loozzike_gdtg:e6&GXqJ_p=ma@103.97.125.252/loozzike_gdtg?charset=utf8mb4"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8mb4".format(database['user'], database['password'], database['host'], database['dtb'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['JSON_AS_ASCII'] = False


db = SQLAlchemy(app=app)