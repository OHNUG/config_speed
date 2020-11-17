from rich import print
from ncclient import manager
from device import lab_device
from xml.dom.minidom import parseString

import xmltodict


def connect():

    mgr = manager.connect(
        host=lab_device["host"],
        port=830,
        username=lab_device["username"],
        password=lab_device["password"],
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
                lab_device["host"]
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


def add_interfaces():

    """adds a loopback interface"""

    add_loopback = """
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
    </config>"""

    with connect() as connection:
        response = connection.edit_config(target="running", config=add_loopback)
        print(response)


if __name__ == "__main__":

    add_interfaces()

    # data = get_interfaces()
#
# for e in data:
#    print(e["name"])
#