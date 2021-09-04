from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(resources={
    r'/*': {
        'origins': [
            'http://localhost:3000'
        ]
    }
})

cors.init_app(app)

# 123host
# database = {
#     'host':'103.97.125.252',
#     'user':'loozzike_gdtg',
#     'password':'e6&GXqJ_p=ma',
#     'dtb':'loozzike_gdtg'
# }

# az
# database = {
#     'host':'45.252.248.10',
#     'user':'byvxrfzw_gdtg',
#     'password':'cC$+2=Zc-=oo',
#     'dtb':'byvxrfzw_gdtg'
# }


# dncloud
database = {
    'host':'194.233.75.100',
    'user':'hieufish_ahihi',
    'password':'7Q(kH}vKL};j',
    'dtb':'hieufish_gdtg'
}

# pythonanywhere
# database = {
#     'host':'loozzi.mysql.pythonanywhere-services.com',
#     'user':'loozzi',
#     'password':'7Q(kH}vKL};j',
#     'dtb':'loozzi$gdtg'
# }

app.secret_key = "adsflkjqoijqawsef0asiodjf9028344jfoasijfpoajsdlkfjaso9fj390asdofjasdoijflsdfdsfasdkjfo"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://:/?charset=utf8mb4"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8mb4".format(database['user'], database['password'], database['host'], database['dtb'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['JSON_AS_ASCII'] = False


db = SQLAlchemy(app=app)