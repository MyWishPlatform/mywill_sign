import binascii
import requests
import rlp
import json
from ethereum import transactions, utils

from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from neo_sign import sign_context, PRIVATE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lastwill_sign:lastwill_sign@localhost/lastwill_sign'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
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
        network = req.get('network', '')
        print('signer network', network, flush=True)
        if network in ['ETHEREUM_MAINNET', 'ETHEREUM_ROPSTEN']:
            print('eth', flush=True)
            gasprice = 20 * 10 ** 9
        if network in ['RSK_MAINNET', 'RSK_TESTNET']:
            print('rsk', flush=True)
            gasprice = 1 * 10 ** 9
        if network == '':
            gasprice = 1 * 10 ** 9
        gaslimit = req.get('gaslimit', 10 ** 6) # 10 ** 6 is suitable for deploy
        account = db.session.query(Account).filter(Account.addr==source).limit(1).with_for_update().one()
        priv = binascii.unhexlify(account.priv)
        nonce = req['nonce']
        tx = transactions.Transaction(nonce, gasprice, gaslimit, dest, value, data).sign(priv)
        raw_tx = binascii.hexlify(rlp.encode(tx))
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

class NeoSign(Resource):
    def post(self):
        return sign_context(request.get_json()['binary_tx'], PRIVATE)

api = Api(app)
api.add_resource(Signer, '/sign/')
api.add_resource(KeyManager, '/get_key/')
api.add_resource(NeoSign, '/neo_sign/')
