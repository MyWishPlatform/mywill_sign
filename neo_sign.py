from neo.Wallets.Wallet import Wallet
from neo.SmartContract.ContractParameterContext import ContractParametersContext
import binascii
import json
from neo.SmartContract.Contract import Contract as WalletContract


from neo.Core.TX.Transaction import ContractTransaction
from neo.IO.MemoryStream import MemoryStream
from neocore.IO.BinaryReader import BinaryReader
from private import PRIVATE


def sign_context(context_json, private):

    wallet = Wallet(b'', b'0'*32, True)
    wallet.CreateKey(binascii.unhexlify(private))
    context = json.dumps(context_json)
    hashes = WalletContract.CreateSignatureContract(list(wallet._keys.values())[0].PublicKey)
    wallet._contracts[hashes.ScriptHash.ToBytes()] = hashes
    context = ContractParametersContext.FromJson(context, isMultiSig=False)

    wallet.Sign(context)

    return [x.ToJson() for x in context.GetScripts()]


if __name__ == "__main__":
    context = {'type': 'Neo.Core.ContractTransaction', 'hex': '80000120838ce8215ad56c44564c8f35bf097ab0419e8abd015c98f2f2502b67abda97efa5a6614f0f1c8883f3a9f90ac64fcf09cfa3c915630100029b7cffdaa674beae0f930ebe6085af9093e5fe56b34a5c220ccdcf6efc336fc500c2eb0b000000001b279694b5a608e0f7f90541a5acc1b3d1cf520f9b7cffdaa674beae0f930ebe6085af9093e5fe56b34a5c220ccdcf6efc336fc50027b92900000000838ce8215ad56c44564c8f35bf097ab0419e8abd', 'items': {}}
    print(sign_context(context, PRIVATE))

