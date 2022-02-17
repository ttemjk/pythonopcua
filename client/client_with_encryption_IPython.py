
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

    # If connected to server_with_method.py, you can try these from the Ipython
    # command line:     
    # objects = client.nodes.objects
    # obj = await client.nodes.root.get_child(["0:Objects", "0:MyObject"])
    # await obj.call_method("0:mymethod", 2)

    # If the argument is "2" as above, the method in server returns "True",
    # and "False" otherwise.
    # A bit longer method call:
    # await obj.call_method("0:mymethod", ua.Variant(2, ua.VariantType.Int64))

    # You can also read a varialbe (with value 2001.0):
    # child = await objects.get_child(['0:MyObject', '0:MyVariable'])
    # print(await child.get_value())
    

    # With server server_with_encryption.py yYou can try these from the
    # IPython command line:
    # (Note that the server increments the variable with 0.1
    # in 1 sec periods!)
        #objects = client.nodes.objects
        #child = await objects.get_child(['0:MyObject', '0:MyVariable'])
        #print(await child.get_value())
        #await child.set_value(4.2) # Must be decimal! 
        #print(await child.get_value())


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(task(loop))
    loop.close()


if __name__ == "__main__":
    main()
