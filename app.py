import logging

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:krenil123@localhost/Assignment-3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

api = Api(app)


def configure_logger():
    logging.basicConfig(filename='logs.txt', level=logging.DEBUG,
                        format=f'%(asctime)s ::%(levelname)s :%(name)s %(threadName)s : %(message)s')
    return logging.getLogger(__name__)


logger = configure_logger()
logger.debug("App is running.")
