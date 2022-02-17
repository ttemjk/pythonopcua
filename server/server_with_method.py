import asyncio
import sys

import logging
sys.path.insert(0, "..")
from asyncua import Server
from asyncua import ua
from asyncua import uamethod
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.users import UserRole
from asyncua.server .user_managers import CertificateUserManager

logging.basicConfig(level=logging.DEBUG)

# method to be exposed through server
def func(parent, variant):
    print("func method call with parameters: ", variant.Value)
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]
    #return [ua.Variant(variant.Value, ua.VariantType.Int64)]


async def main():

    cert_user_manager = CertificateUserManager()
    await cert_user_manager.add_admin("certificates/opcuaClient_cert.der", name='test_user')

    server = Server(user_manager=cert_user_manager)

    await server.init()

    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt], permission_ruleset=SimpleRoleRuleset())
    
    #server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt],)
    


    # load server certificate and private key. This enables endpoints
    # with signing and encryption.

#    await server.load_certificate("certificate-example.der")
#    await server.load_private_key("private-key-example.pem")

    await server.load_certificate("opcuaServer_cert.der")
    await server.load_private_key("opcuaServer_private_key.pem")

    idx = 0

    # get Objects node, this is where we should put our custom stuff
    objects = server.nodes.objects 

    # populating our address space
    await objects.add_folder(idx, "myEmptyFolder")
    myobj = await objects.add_object(idx, "MyObject")

    # populating our address space
    #myobj = await server.nodes.objects.add_object(idx, "MyObject")
    myvar = await myobj.add_variable(idx, "MyVariable", 2001.0)
    await myvar.set_writable()  # Set MyVariable to be writable by clients

    await myobj.add_method(idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    
    # starting!

    async with server:
        while True:
            await asyncio.sleep(1)
    
if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())
