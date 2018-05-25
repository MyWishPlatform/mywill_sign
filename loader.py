#!/usr/bin/env python3

import psycopg2
import sha3
from ecdsa import SigningKey, SECP256k1
import binascii

conn = psycopg2.connect("dbname='lastwill_sign' user='lastwill_sign' host='localhost' password='lastwill_sign'")
cur = conn.cursor()

while 1:
    try:
        priv = input()
    except EOFError:
        break
    sk = SigningKey.from_string(binascii.unhexlify(priv), curve=SECP256k1)
    pub_hex = sk.get_verifying_key().to_string()
    pub = binascii.hexlify(pub_hex).decode()
    keccak = sha3.keccak_256()
    keccak.update(pub_hex)
    addr = "0x{}".format(keccak.hexdigest()[24:])
    cur.execute("INSERT INTO accounts (priv, pub, addr, used) VALUES ('{priv}', '{pub}', '{addr}', false);".format(priv=priv, pub=pub, addr=addr))

conn.commit()
cur.close()
conn.close()
