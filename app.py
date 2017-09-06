from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lastwill_sign:lastwill_sign@localhost/lastwill_sign'
app.config['USERNAME'] = 'lastwill_sign'
app.config['PASSWORD'] = 'lastwill_sign'
db = SQLAlchemy(app)

from models import Account

class Signer(Resource):
    def post(self):
        return {'status': 0}


class KeyManager(Resource):
    def post(self):
        try:
            account = db.session.query(Account).filter(Account.used==False).limit(1).with_for_update().one()
        except NoResultFound:
            return {'status': 1, 'message': 'NoResultFound'}
        account.used = True
        db.session.add(account)
        db.session.commit()
        return {'status': 0, 'addr': account.addr}


api = Api(app)
api.add_resource(Signer, '/sign/')
api.add_resource(KeyManager, '/get_key/')

