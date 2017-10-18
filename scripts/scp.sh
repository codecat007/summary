#!/usr/bin/expect
set name [lindex $argv 0] 
set addr [lindex $argv 1] 
set passwd [lindex $argv 2] 

for {set i 0} {$i < 1000} {incr i} {
    puts "<-------- $i: scp start"
    set timeout 30
    spawn  scp $name root@$addr:/run/
    expect "password:"
    send "$passwd\r"
    interact
    puts "$i: scp over -------->"
}

