from rich import print
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.dom import minidom

# A scratchpad for learning how to build XML payloads


def payload_builder(my_ints):

    root = Element("config")
    parent = SubElement(
        root, "interfaces", {"xmlns": "urn:ietf:params:xml:ns:yang:ietf-interfaces"}
    )

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

    xml = payload_builder(my_ints)

    print(xml)