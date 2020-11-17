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

#### IETF Interface Types

loopback: `ianaift:softwareLoopback`
ethernet: `ianaift:ethernetCsmacd`