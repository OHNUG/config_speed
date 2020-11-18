from rich import print
from ncclient import manager
from device import home_lab_device
from xml.dom.minidom import parseString

import xmltodict

from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.dom import minidom


def connect():

    mgr = manager.connect(
        host=home_lab_device["host"],
        port=830,
        username=home_lab_device["username"],
        password=home_lab_device["password"],
        hostkey_verify=False,
        device_params={"name": "default"},
        look_for_keys=False,
        allow_agent=False,
    )

    return mgr


def get_capabilities():

    """Gather netconf capabilities from device"""

    with connect() as connection:
        print(
            "\n***Remote Devices Capabilities for device {}***\n".format(
                home_lab_device["host"]
            )
        )

        capabilities = connection.server_capabilities

    return capabilities


def get_interfaces():

    """Return all interfaces via netconf"""

    payload = """
    <filter>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
      </interfaces>
    </filter>
    """

    with connect() as connection:
        # ints = connection.get_config("running", payload)
        ints = connection.get(filter=payload)
        interface_data = xmltodict.parse(ints.xml)["rpc-reply"]["data"]["interfaces"][
            "interface"
        ]

    return interface_data


def payload_builder(my_ints):

    """Builds XML Payloads for Interface config. Example payload below"""

    """Example:
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback100</name>
          <description>My awesome new loopback interface</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>1.1.1.1</ip>
              <netmask>255.255.255.255</netmask>
            </address>
          </ipv4>
          <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
        </interface>
      </interfaces>
    </config>
    """

    # Parent structure
    root = Element("config")
    parent = SubElement(
        root, "interfaces", {"xmlns": "urn:ietf:params:xml:ns:yang:ietf-interfaces"}
    )

    # Loop for interfaces
    for my_int in my_ints:

        child = SubElement(parent, "interface")
        int_name = SubElement(child, "name")
        int_name.text = my_int["name"]
        int_description = SubElement(child, "description")
        int_description.text = my_int["description"]
        int_type = SubElement(
            child, "type", {"xmlns:ianaift": "urn:ietf:params:xml:ns:yang:iana-if-type"}
        )
        int_type.text = my_int["type"]
        int_enabled = SubElement(child, "enabled")
        int_enabled.text = my_int["enabled"]
        int_ipv4 = SubElement(
            child, "ipv4", {"xmlns": "urn:ietf:params:xml:ns:yang:ietf-ip"}
        )
        int_address = SubElement(int_ipv4, "address")
        int_ip = SubElement(int_address, "ip")
        int_ip.text = my_int["ip"]
        int_netmask = SubElement(int_address, "netmask")
        int_netmask.text = my_int["netmask"]

    payload = tostring(root, method="html").decode("utf-8")

    return payload


def add_interfaces(self):

    add_loopback = payload_builder(my_ints)

    with connect() as connection:

        response = connection.edit_config(add_loopback, target="candidate")
        print(response)

        connection.commit()


if __name__ == "__main__":

    my_ints = [
        {
            "name": "Loopback100",
            "description": "Description for interface 1",
            "type": "ianaift:softwareLoopback",
            "enabled": "true",
            "ip": "1.1.1.1",
            "netmask": "255.255.255.255",
        },
        {
            "name": "Loopback200",
            "description": "Description for interface 2",
            "type": "ianaift:softwareLoopback",
            "enabled": "true",
            "ip": "2.2.2.2",
            "netmask": "255.255.255.255",
        },
    ]

    print("\nInterfaces on switch prior to change:\n")
    for e in get_interfaces():
        print(e["name"])

    print("\nAdding new interfaces\n")
    add_interfaces(my_ints)

    print("\nInterfaces on switch post change:\n")
    for e in get_interfaces():
        print(e["name"])
