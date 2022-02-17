
# A script to be run in the IPython launched by 
# "client_with_encryption_IPython.py"
# type in the IPython terminal "%load attest"
objects= client.nodes.objects
obj = await client.nodes.root.get_child(["0:Objects", "0:MyObject"])
TPMnonce=create_nonce(SecurityPolicyBasic256Sha256.symmetric_key_size)
TPMnonceStr=TPMnonce.hex()
print ('Attestation request sent with a hex-nonce, waiting for a response \
(a hex-string)')
await obj.call_method("0:attest", ua.Variant(TPMnonceStr, ua.VariantType.String))
