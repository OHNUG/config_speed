import re

from netmiko import ConnectHandler
from device import lab_device
from rich import print


def connect():

    """Connect to the device and display uptime"""

    ch = ConnectHandler(**lab_device)
    version = ch.send_command("show version")
    for line in version.split("\n"):
        if "uptime" in line:
            print("Connected to: " + line)

    return ch


def configure_loopbacks():

    """Configures a specified number of loopback interfaces"""

    desired_num_loopbacks = 20
    interface_config = []
    full_config = []

    while desired_num_loopbacks > 0:

        inter_config = [
            "interface loopback " + str(desired_num_loopbacks),
            "deacription Demo loopback interface #: " + str(desired_num_loopbacks),
            "ip address 1.1.1." + str(desired_num_loopbacks) + "255.255.255.255",
        ]

        interface_config.append(inter_config)
        desired_num_loopbacks -= 1

    for interface in interface_config:
        for e in interface:
            full_config.append(e)

    return full_config


if __name__ == "__main__":

    config_to_send = configure_loopbacks()
    print("\nSending the following configurations to your device:\n")
    print(config_to_send)

    connect().send_config_set(config_to_send)

    print("\nConfiguration complete\n")