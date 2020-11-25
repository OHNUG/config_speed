# Config Speed
This is a small project I wrote to play with Model Driven Programmability. I intend to measure the performance of various configuration methods.

### The Test
Each script will:
- Add a specified number of loopback interfaces. (100)
- Interfaces will be configured with an IP address, and description.
- Where applicable, configurations will use [IETF Standard models](https://github.com/YangModels/yang/tree/master/standard/ietf/RFC) (no vendor specific models).

Truncated config example:
```
!
!
interface Loopback1
 description Demo loopback interface #: 1
 ip address 1.1.1.1 255.255.255.255
!
interface Loopback2
 description Demo loopback interface #: 2
 ip address 1.1.1.2 255.255.255.255
!
interface Loopback3
 description Demo loopback interface #: 3
 ip address 1.1.1.3 255.255.255.255
!
interface Loopback4
 description Demo loopback interface #: 4
 ip address 1.1.1.4 255.255.255.255
!
!
...
```

### Summary of Details for Various Protocols:
|            | SSH            | REST     | NETCONF  | RESTCONF | gRPC |
|------------|----------------|----------|----------|----------|------|
| Transport  | ssh            | https    | ssh      | https    | HTTP/2     |
| Port       | 22             | 443      | 830      | 443      | Varies     |
| RFC        |                |          | 6241     | 8040     |      |
| Data       | CLI | JSON/XML | XML      | JSON/XML | JSON/XML     |
| Python lib | netmiko        | httpx | ncclient | httpx | grpcio |

### Results:
| | SSH | NETCONF | RESTCONF |
|-|-----|---------|----------|
|Runs in Seconds (1,2,3)|24.10, 24.08, 23.36|16.40,46.19,47.04|45.32,43.97,44.83|
|Average|**23.85**|**36.55**|**44.71**|

### Payload Sizes:
| | SSH | NETCONF | RESTCONF |
|-|-----|---------|----------|
|

## Configurations
### SSH

#### IOS-XE | Enable SSH
```
!
! Configure a user with priv 15 access for all tests
!
enable
configure terminal
username admin privilege 15 password my_pass
aaa authentication login default local
aaa authorization exec default local
!
! Configure SSH
!
hostname LabSwitch
ip domain-name homeLab
crypto key generate rsa
!
! enable ssh
ip ssh version 2
!
!
!
```

### NETCONF

#### IOS-XE | Enable NETCONF
```
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

### RESTCONF

#### IOS-XE | Enable RESTCONF
```
!
! Configure RESTCONF-YANG
!
enable
configure terminal
restconf
ip http secure-server
end
!
```

## Notes
One observation, the consistency for enabling various config operations differes quite a bit. Some vendors are more consistent than others:

Configuring: SSH / NETCONF / RESTCONF / gNMI / REST in Cisco's IOS-XE:
```
!
conf t
!
ip ssh version 2
netconf-yang
restconf
gnmi-yang
ip http secure-server
!
```

Contrast this to Arista's EOS:
```
!
conf t
!
management ssh
!
management api netconf
management api restconf
management api gnmi
management api http-commands
!
```

Or Juniper's JUNOS:
```
set system services ssh
set system services netconf
set system services http

set extension-server request-response grpc ssl
```
In the case of Juniper, I was not able to find a configuration for RESTCONF. In addtion, grpc seems to be available via extension services.



