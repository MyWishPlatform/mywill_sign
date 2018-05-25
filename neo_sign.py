from neo.Wallets.Wallet import Wallet
from neo.SmartContract.ContractParameterContext import ContractParametersContext
import binascii
import json
from neo.SmartContract.Contract import Contract as WalletContract


from neo.Core.TX.Transaction import ContractTransaction
from neo.IO.MemoryStream import MemoryStream
from neocore.IO.BinaryReader import BinaryReader
from private import PRIVATE


def sign_context(binary_tx, private):

    wallet = Wallet(b'', b'0'*32, True)
    wallet.CreateKey(binascii.unhexlify(private))
    script_hash = WalletContract.CreateSignatureContract(list(wallet._keys.values())[0].PublicKey)
    wallet._contracts[script_hash.ScriptHash.ToBytes()] = script_hash
    tx = ContractTransaction.DeserializeFromBufer(binascii.unhexlify(binary_tx))
    context = ContractParametersContext(tx, isMultiSig=False)
    context.ScriptHashes = [script_hash.ScriptHash]
    wallet.Sign(context)
    return [x.ToJson() for x in context.GetScripts()]


