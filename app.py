import binascii
import requests
import rlp
import json
from ethereum import transactions, utils

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
        req = request.get_json()
        source = req['source']
        dest = req.get('dest', '')
        value = req.get('value', 0)
        data = binascii.unhexlify(req.get('data', ''))
        gasprice = 20 * 10 ** 9
        startgas = 2 * 10 ** 6
        account = db.session.query(Account).filter(Account.addr==source).limit(1).with_for_update().one()
        priv = binascii.unhexlify(account.priv)
        nonce = req['nonce']
        tx = transactions.Transaction(nonce, gasprice, startgas, dest, value, data).sign(priv)
        raw_tx = binascii.hexlify(rlp.encode(tx))
#        r = requests.post('http://127.0.0.1:8545', json={'method': 'eth_sendRawTransaction', 'params': ['0x' + ra_tx.decode()], 'id': 1, 'jsonrpc': '2.0'}) 
        return {'result': raw_tx.decode()}


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

