
# A script to be run in the IPython launched by 
# "client_with_encryption_IPython.py"
# type in the IPython terminal "%load attest"
import base64
objects= client.nodes.objects
obj = await client.nodes.root.get_child(["0:Objects", "0:MyObject"])
TPMnonce=create_nonce(SecurityPolicyBasic256Sha256.symmetric_key_size)
TPMnonceBase64Bytes=base64.standard_b64encode(TPMnonce)
TPMnonceStr=TPMnonceBase64Bytes.decode()
print ('Attestation request sent with a base64-nonce, waiting for a response \
(a base64-string)')
await obj.call_method("0:attest", ua.Variant(TPMnonceStr, ua.VariantType.String))
