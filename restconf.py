from rich import print
from device import home_lab_device
import httpx
import json


base_url = "https://192.168.128.120/restconf"
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json",
}
username = home_lab_device["username"]
password = home_lab_device["password"]


def get_interfaces():

    """Return all interfaces via restconf"""

    with httpx.Client(
        headers=headers, verify=False, auth=(username, password)
    ) as client:
        r = client.get(
            url=base_url
            + "/data/ietf-interfaces:interfaces/interface=GigabitEthernet1%2F0%2F10"
        )

    return r.json()


def get_capabilities():

    with httpx.Client(
        headers=headers, verify=False, auth=(username, password)
    ) as client:
        r = client.get(url=base_url + "/data/ietf-yang-library:modules-state")

    return r.json()


def payload_builder(my_ints):
    """Builds JSON Payloads for Interface config. Example paylod below"""

    """
    {
        'interface': [
            {
                'name': 'Loopback100',
                'description': 'Description for interface 1',
                'type': 'iana-if-type:softwareLoopback',
                'enabled': 'true',
                'ietf-ip:ipv4': {'address': [{'ip': '1.1.1.1', 'netmask': '255.255.255.255'}]}
            },
            {
                'name': 'Loopback101',
                'description': 'Description for interface 1',
                'type': 'iana-if-type:softwareLoopback',
                'enabled': 'true',
                'ietf-ip:ipv4': {'address': [{'ip': '1.1.1.2', 'netmask': '255.255.255.255'}]}
            }
        ]
    }
    """

    interfaces = []

    for my_int in my_ints:

        interface = {
            "name": my_int["name"],
            "description": my_int["description"],
            "type": "iana-if-type:softwareLoopback",
            "enabled": "true",
            "ietf-ip:ipv4": {
                "address": [{"ip": my_int["ip"], "netmask": my_int["netmask"]}]
            },
        }

        interfaces.append(interface)

    return interfaces


def add_interfaces(self):

    # add_loopback = payload_builder(my_ints)
    add_loopback = {"interface": payload_builder(my_ints)}

    with httpx.Client(
        headers=headers, verify=False, auth=(username, password), timeout=None
    ) as client:
        r = client.post(
            url=base_url + "/data/ietf-interfaces:interfaces?content=config",
            json=add_loopback,
        )


if __name__ == "__main__":

    desired_num_loopbacks = 100
    my_ints = []

    while desired_num_loopbacks > 0:

        interface = {
            "name": "Loopback" + str(desired_num_loopbacks),
            "description": "Demo loopback interface #: " + str(desired_num_loopbacks),
            "type": "ianaift:softwareLoopback",
            "enabled": "true",
            "ip": "1.1.1." + str(desired_num_loopbacks),
            "netmask": "255.255.255.255",
        }

        my_ints.append(interface)
        desired_num_loopbacks -= 1

    print("\nAdding new interfaces:\n")
    print(my_ints)
    add_interfaces(my_ints)
