
from IPython import embed
import asyncio

# IPython embed() requires nested asyncio evnet loops:
import nest_asyncio   # Allows nested asyncio event loops.
nest_asyncio.apply()  # Applies the patch to asyncio 
# see: https://pypi.org/project/nest-asyncio/
# and: https://github.com/erdewit/nest_asyncio


import logging
import sys
sys.path.insert(0, "..")
from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

from asyncua.common.utils import create_nonce

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("asyncua")

#cert_idx = 1
#cert = f"certificates/peer-certificate-example-{cert_idx}.der"
#private_key = f"certificates/peer-private-key-example-{cert_idx}.pem"

cert = "certificates/opcuaClient_cert.der"
private_key = "certificates/opcuaClient_private_key.pem"

async def task(loop):
    url = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
    client = Client(url=url)
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=cert,
        private_key=private_key,
#        server_certificate="certificate-example.der"
        server_certificate="certificates/opcuaServer_cert.der"
    )
    async with client:
        await  embed(using='asyncio')

    # If connected to server, you can try these from the Ipython
    # command line (<namespace> can be "0"):     
    # objects = client.nodes.objects
    # obj = await client.nodes.root.get_child(["<namespace>:Objects", \
    # "<namespace>:<ObjectName>"])
    # await obj.call_method("<namespace>:<method_name>", <argument_values>)

    # A bit longer method call:
    # await obj.call_method("0:<method_name>", ua.Variant(<value>, \
    # ua.VariantType.<type, see uatypes.py, e.g. Int64>))
    # uatypes.py can be found in:
    # "https://github.com/FreeOpcUa/opcua-asyncio/blob/master/asyncua/ua/uatypes.py"

    # You can also read a variable:
    # child = await objects.get_child(['<namespace>:<object_name>', \
    # '<namespace>:<variable_name>'])
    # print(await child.get_value())
    

def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(task(loop))
    loop.close()


if __name__ == "__main__":
    main()
