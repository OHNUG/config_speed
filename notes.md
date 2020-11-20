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

#### Other notes
Copy ios image downloaded to macbook.

Enable remote login:
System Preferences > Sharing > Check Remote Login

From the switch:
`copy scp://<username>:<password>@<ipaddress>/Downloads/<imagename> flash:`

I ran into timeout issues with both netconf & restconf.

For Netconf I added `timeout=300` to the manager
For Restconf I added `timeout=None` to the Client instance