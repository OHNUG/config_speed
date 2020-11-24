## Notes

#### IOS-XE | Enable NETCONF

```
!
! Configure a user with priv 15 access
!
enable
configure terminal
username admin privilege 15 password my_pass
aaa authentication login default local
aaa authorization exec default local
end
!
! Configure NETCONF-YANG
!
enable
configure terminal
netconf-yang
netconf-yang feature candidate-datastore
end
!
```

#### IOS-XE | Enable RESTCONF

```
!
! Configure a user with priv 15 access
!
enable
configure terminal
username admin privilege 15 password my_pass
aaa authentication login default local
aaa authorization exec default local
end
!
! Configure NETCONF-YANG
!
enable
configure terminal
restconf
ip http secure-server
end
!
```

#### IOS-XE | Enable gNMI

Create certs on gNMI server:
```
# Setting up a CA
mkdir certs && cd certs
openssl genrsa -out rootCA.key 2048
openssl req -subj /C=/ST=/L=/O=/CN=rootCA -x509 -new -nodes -key rootCA.key -sha256 -out rootCA.pem
 
# Setting up device cert and key
openssl genrsa -out device.key 2048
openssl req -subj /C=/ST=/L=/O=/CN=192.168.128.120 -new -key device.key -out device.csr
openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -sha256
# Encrpyt device key - needed for input to IOS
openssl rsa -des3 -in device.key -out device.des3.key -passout pass:oAn3U3uGUuWKQxvRdgE5Xfq67qB
 
# Setting up client cert and key
openssl genrsa -out client.key 2048
openssl req -subj /C=/ST=/L=/O=/CN=gnmi_client -new -key client.key -out client.csr
openssl x509 -req -in client.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out client.crt -sha256
```

Install certs on device:
```
!
! File contents pasted below are:
! rootCA.pem > device.des3.key > device.crt respectively
!
! Create and Install certs
!
enable
configure terminal
crypto pki import trustpoint1 pem terminal password oAn3U3uGUuWKQxvRdgE5Xfq67qB 
% Enter PEM-formatted CA certificate.
% End with a blank line or "quit" on a line by itself.
-----BEGIN CERTIFICATE-----
MIICnjCCAYYCCQCRsW5K9gyR5DANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZy
b290Q0EwHhcNMjAxMTIwMTEzMDI0WhcNMjAxMjIwMTEzMDI0WjARMQ8wDQYDVQQD
DAZyb290Q0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDABbyPwD+m
W4o0GrLAPu0RRMl/eY8cJWQfX7KsPhaT93M2vQ89v5ghBIU8+m1ekDiwdWrAdSkX
bBJTWGlBZ8ntlVv/x9fe7L6XbYCW4Oe4eQgrEUvKhmdUsOfjJM7R0Qy/TWNn0ivF
jwKI/mO2TaEclq4CTMybp1r16HWhHVvNAV9RspXQvXtyKsOQckb0MAW8N1WIGxbv
e9lISSX9OtlYNiXekSO7wn/ZzIoLZrHC9+lPzt0wuKDnA/orM7DWPXpKh+5x8Cyd
Sa4rvYAue20dyrJozAXfrTlNbLj5XxlwuGyJyBHwbZrnXA5BCdI0cWCeJfeqelwo
wu/FHUXA5oLLAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAJ/3Dmax5Sl7kB8+1u4F
dzG6XoHA+s7h4VIpNtStI4Zwtp0uVgl6huIniWayLOTamVIUDTHAIOWFNhHKEnVy
gUDJ8JMafvvrvTBjwB1WuNn4JHxg6y++/+2QLgmagt3e85P5YTM97X9PReZzT4sq
U9/2ul2cUpwbdZVPcWLzxI0gfl5aLrulKaiGEvNGsTvgbXd9OLLQ5ZiQ2IZTAXPg
JedxdNSnoTVNYtlR7Lwl2L5Jd6cB6jt++N7Du6YnH8HjlEOwEeMklwFtf1ppvSnu
JuetDkAECb2YciAZEnp11T4S4qrZ2gMr2z0ucMN3/RqpLSs+D59TkIeixFwpU6hm
eKY=
-----END CERTIFICATE-----
quit
% Enter PEM-formatted encrypted private General Purpose key.
% End with "quit" on a line by itself.
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,1A962EA75B241E89

78PeMwSs1ffCvmT2XkdPAqROMXa4HBcAcP9Ma2+Pxws3ZHnYsU7gpniiJ1AQfJFc
5TbW/fXD/JFqyG0oFyed2HrwgtlgM/eMTX7Rrt9Vr6zUGlnInWKAQ5i/PK1KOsKI
TAcHQ9vFoCezv4kXgC0aFEZ5n45zdn8txaeaCFdTerQ9TofnhJrGR3p3lDfO0BNw
NyMGMtOy5TkR4nwFfqRqKolstIICXvZfVELNL5WiCR4cnGI9wFh0IyrXMwoxiT1a
U1q/2L3M4xgXcCOm0i84MgGMcLdy8NKlbbNnqt0cqwARTrE+Fj7fBQN0ycZ7PRUc
kSI+Dty9Vs6i82Fe1rRFegQENn18hMcRbqt51YHuxiAH7K2dx8GixXTnA0sjXXGt
14cEY3Y3YMwX3IHNJ5fPwYQ7yBlVaBd+3ksV2DXEqOdkEsbM3hHmC3VtUGBNtqzk
sayOmEyx+o0jAhK2pYQuJcwxEy2WdW5bv74P/zIoRRIs86hMlQ7OfJ8ijueS0QPf
7pJGoXFbI3Sq/6QMk4Gr3T1LtDtb/S3PK/o0C2g1Va0+3XdE2H7KDOBs9ISDDh5v
csQPOBu8C9alpRtsAyZfztzo9Dv9R8pRDSNW3e20jkTgf48xA4BlejjDfn1cI55E
GX2nqBo6blxQbLVpJe0DZbj1d52+TiEly0PjalyKUmyejH6Ls9cVrf7U7zog7gmW
sdCFRA8NbqtnRUwoGHZq8ZmkuYbgyvD67Xn1ZY5qu4FPudkGfp/lpuT34W7Sr4i8
OEyHvhQODucNfXsqAK2kGmAPZeUl3dtN0fkGBn9T8Hx+SIPRgHlrbwZBhM+51eWv
pgpoBlNop6QFMvpy4+j8jb+T15w+4UOTlsPGMp1NNplOi1xDflmgDga/9NM5UNMF
9tEqJY+hdTet9Njwg3D56mr6G22VIBJLUO0vTqv5Q5fv3W/7KjgsiPq16pgQRFG1
PX2EifUp+si+PPJjn4k72lnkmdYnYJUG9Wmbs8GpjqpEJDDf9UuZN6fu4T9fT+MI
30llIk9dcXOzjm5F03AmvDLMgMkfwJSYjj3/SFp2MoXzyN8PshlMyf8y7x+s3r1V
TL/ExWi9nJe97Sg1i0dYRviCZhSlH3nFaSvJb5ts9ZA9+m9G8Bm9SKtFEeKez3r6
Wr1Z/ck/bGoA0nOAVGuntgLrWbXrpNx/nJjc0D7VFqJCgtUp6XkFG/vxxF+HvWnb
xfr0tSsZ0rE2ohHd/X4E/xMvmDuT82sUV3uJJiPVinB+MkEMz6ObDbn4gtVzZTDv
sTaYRIneAeUWfe0iZIhFxMjZSOInQKfnzCyloBaRDpn6Nqw6adTEOGXrFVcrdK61
wGGQfLHfw2gN+npIAehaV5k2H4d6WnIn8vJUjjGEvBJ4gEuUvKo/3BX0plz4xGSB
lIg42CtwQdpMGuZHNMrMSnqE20nsOPxk/Rr0pAWX/HJUvuDe6JLL05aYOx5Vb4bp
2oA7HuJUabY1sUYeu+Hcfbh6PtS/njDsdn8ltM+ZpPQwETVNI95GAHBj13q64y7g
rPk1ZAsQTAI8xg8qmGL5zX9tW8x3URoiB4BedcRwX/HPt2oqN9+6Zw==
-----END RSA PRIVATE KEY-----
quit
% Enter PEM-formatted General Purpose certificate.
% End with a blank line or "quit" on a line by itself.
-----BEGIN CERTIFICATE-----
MIICpzCCAY8CCQCPnwNMXhcx6TANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZy
b290Q0EwHhcNMjAxMTIwMTEzMDU2WhcNMjAxMjIwMTEzMDU2WjAaMRgwFgYDVQQD
DA8xOTIuMTY4LjEyOC4xMjAwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
AQCixOF7iBXvk4+szubHE37yE06WXvuktrU6dkdvSnvxHsKHe+OXIr4CY+EDCyHv
7KNmg6/N0HgoIfPEiCtrSDBKh8EOHrQ0UWYVdMwrs/2Pyye8L37bK0OfAYj1yxa5
37dutzlHzMpV5Fx+L+wMaL2zpqojH8G7mGkHACs1ptvnA3PWgCE1khfFuzbAkGKV
PUC3JqdefMeokWJrPr+dQfSvxIC8XMxJ3U2013UQ3n39DT5iLN/+xZ8LnMVKa1dA
FZG4xk2KLjvKZh1C3HqcxmbL5rlRjYVwEykZWZNMQL3V8BaaSQL/KYEzffxZ1ywI
RibKlrWx67jj8+X5uvdcN1n5AgMBAAEwDQYJKoZIhvcNAQELBQADggEBABWTKZ63
yOVRlIQW8ug1y+S8c8zEl9rSkhDQeUcNN2XjU35WLVS3A4eqPaxV0Q3pNqtW0nEH
tt7ZVjAXGrCPpLCSE3yM+2+f08L+nkhvHDZM9BgpS5yI0Mwgje8RChfzQgSmnjWl
kO/+Qj2LXVNKFvJYrjusRhWF1WdOZYl00ZqpNsHtjW3P+QbcJv+U9SLjxy3RmK7f
k5Bu46XgI8+8/flMyrxGPcXBk3XggqfZAsbZplE3uke1WBXLUgbtD0zdAiN8Pw9g
BFBai8LbmibCu/wBou+ZB5+2unZ91OILkE09Bg82s/oBQf286oMnPlJ6LrnQSoZq
iQpUIoQMapqUlbg=
-----END CERTIFICATE-----
quit
% PEM files import succeeded.
!
crypto pki trustpoint trustpoint1
revocation-check none
end
!
! Enable gNMI
!
enable
configure terminal
gnmi-yang
gnmi-yang secure-trustpoint trustpoint1
gnmi-yang secure-server
gnmi-yang secure-client-auth
gnmi-yang secure-port 50505
end
!
show gnmi-yang state
!
```


Also, Big Sur sucks. Here's how to install grpc in macos big sur: `GRPC_PYTHON_BUILD_SYSTEM_ZLIB=true pip install grpcio` without that command, I kept hitting errors for clang. Found [here](https://github.com/grpc/grpc/issues/24677)

#### IETF Interface Types

loopback: `ianaift:softwareLoopback`
ethernet: `ianaift:ethernetCsmacd`

#### Other notes
Copy ios image downloaded to macbook.

Enable remote login:
System Preferences > Sharing > Check Remote Login

From the switch:
`copy scp://<username>:<password>@<ipaddress>/Downloads/<imagename> flash:`

I ran into timeout issues with both netconf & restconf.

For Netconf I added `timeout=300` to the manager
For Restconf I added `timeout=None` to the Client instance