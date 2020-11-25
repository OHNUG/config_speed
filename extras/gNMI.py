import sys

sys.path.insert(0, "reference/rpc/gnmi/")
import grpc

# import gnmi_pb2
# import gnmi_pb2_grpc

from cisco_gnmi import ClientBuilder

gnmi_dir = "/Users/tlofreso/Projects/config_speed/certs/"

with open(gnmi_dir + "rootCA.pem", "rb") as f:
    ca_cert = f.read()
with open(gnmi_dir + "client.crt", "rb") as f:
    client_cert = f.read()
with open(gnmi_dir + "client.key", "rb") as f:
    client_key = f.read()

# client = (
#     ClientBuilder("192.168.128.120:50505")
#     .set_os("IOS XE")
#     .set_secure_from_file(
#         root_certificates=gnmi_dir + "rootCA.pem",
#         private_key=gnmi_dir + "client.key",
#         certificate_chain=gnmi_dir + "client.crt",
#     )
#     .set_call_authentication("admin", "@#$Secure1")
#     .construct()
# )

client = (
    ClientBuilder("192.168.128.120:50505")
    .set_os("IOS XE")
    .set_secure_from_target()
    .set_call_authentication("admin", "@#$Secure1")
    .construct()
)

print(client.capabilities())