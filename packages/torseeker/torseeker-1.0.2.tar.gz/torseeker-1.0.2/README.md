TorSeeker
==========

**TorSeeker** is a command line tool and a Python module that can be used to query information about Tor relays.

From the command line, queries can be performed relatively easy by using a two letter country code or via one or multiple Tor IP addresses.

As a Python module, **TorSeeker** offers a reasonable and easy approach for querying information about Tor relays from within your own Python script or module.

Internet connection is required in order to perform Tor network queries.

For full documentation, please visit [torseeker.readthedocs.io](https://torseeker.readthedocs.io)


Installation
============

This section provides several methods for installing **TorSeeker**.


From the Source
---------------

**TorSeeker** can be build and deployed directly from the source. It can be obtained as follows:

    $ git clone https://github.com/rwprimitives/tor-seeker.git


Installing from PyPi
--------------------

It is highly recommended that **TorSeeker** be installed using `pip` to ensure that the latest version is being used.

To install simply run:

    $ pip install torseeker


Getting Started
===============

This section walks you through the different ways **TorSeeker** can be used as a command line tool.


Basic Usage
-----------

**TorSeeker** provides two simple methods for querying information about Tor relays. A query can be performed by specifying a two letter country code or by using one or multiple Tor IP addresses. The end result will be the same.


Synopsis
--------

To view the different options supported, execute `torseeker` with `-h` or `--help` option:

    usage: torseeker [-h] [-d] [-v] (-c  | --ip  [...])

    A tool used to query information about Tor relays by using a two 
    letter country code or via Tor IP addresses.

    optional arguments:
      -h, --help       show this help message and exit
      -d, --details    show additional information
      -v               show program's version number and exit
      -c , --country   two letter country code of interest
      --ip  [ ...]     one or more tor IP addresses spaced separated


Query Tor relays by Country
---------------------------

The following example shows how to use `-c` option with the two letter country code for Costa Rica: 

    $ torseeker -c cr

    TorSeeker v1.0.2 by eldiablo
    
    Country: Costa Rica
    Total relays: 12
    Guard relays: 2
    Middle relays: 5
    Exit relays: 5


Using the same command and specify the `-d` option to get additional information about the relays:

    $ torseeker -c cr -d

    TorSeeker v1.0.2 by eldiablo
    
    Country: Costa Rica
    Total relays: 12
    Guard relays: 2
    Middle relays: 5
    Exit relays: 5
    
    
    GUARD RELAYS [2]
    ----------------
    138.59.18.106   | Port: 443, Nickname: Albis, Country: Costa Rica, First seen: 2019-02-20 21:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-02-24 02:11:04
    138.59.18.105   | Port: 88, Nickname: TheMind, Country: Costa Rica, First seen: 2019-02-20 14:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-02-17 06:16:04
    
    
    MIDDLE RELAYS [5]
    -----------------
    200.122.181.101 | Port: 443, Nickname: Karai, Country: Costa Rica, First seen: 2018-01-11 14:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-03-16 19:21:09
    201.192.156.175 | Port: 8118, Nickname: khazad8337, Country: Costa Rica, First seen: 2022-03-19 16:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-03-19 15:20:08
    190.10.8.50     | Port: 443, Nickname: cragg, Country: Costa Rica, First seen: 2019-10-31 15:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-02-19 23:07:03
    190.10.8.68     | Port: 443, Nickname: cressington, Country: Costa Rica, First seen: 2016-04-08 16:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-01-08 22:56:28
    200.122.181.78  | Port: 443, Nickname: Splinter, Country: Costa Rica, First seen: 2018-01-17 20:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2021-06-30 21:23:25
    
    
    EXIT RELAYS [5]
    ---------------
    138.59.17.40    | Port: 443, Nickname: barwin, Country: Costa Rica, First seen: 2020-02-06 18:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2021-11-24 10:22:18, IPv6: 2803:6900:533:1:216:3eff:fe70:a38, IPv6 Port: 443
    179.48.251.188  | Port: 443, Nickname: toritico01, Country: Costa Rica, First seen: 2019-02-13 15:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-02-21 10:10:31
    200.122.181.2   | Port: 443, Nickname: Michelangelo, Country: Costa Rica, First seen: 2020-10-02 16:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-03-16 19:11:08
    138.59.18.110   | Port: 443, Nickname: demonteal, Country: Costa Rica, First seen: 2019-05-14 18:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-03-23 12:51:11
    190.10.8.166    | Port: 443, Nickname: Donatello, Country: Costa Rica, First seen: 2021-03-12 20:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-01-04 22:48:54


Query Tor relays via IP address
-------------------------------

The following example shows how to use `--ip` option with the two Tor relay IP addresses: 

    $ torseeker --ip 138.59.18.106 190.10.8.166

    TorSeeker v1.0.2 by eldiablo
    
    Total relays: 2
    Guard relays: 1
    Middle relays: 0
    Exit relays: 1


Using the same command and specify the `-d` option to get additional information about the relays:

    $ torseeker --ip 138.59.18.106 190.10.8.166 -d

    TorSeeker v1.0.2 by eldiablo
    
    Total relays: 2
    Guard relays: 1
    Middle relays: 0
    Exit relays: 1
    
    
    GUARD RELAYS [1]
    ----------------
    138.59.18.106   | Port: 443, Nickname: Albis, Country: Costa Rica, First seen: 2019-02-20 21:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-02-24 02:11:04
    
    
    MIDDLE RELAYS [0]
    -----------------
    None
    
    
    EXIT RELAYS [1]
    ---------------
    190.10.8.166    | Port: 443, Nickname: Donatello, Country: Costa Rica, First seen: 2021-03-12 20:00:00, Last seen: 2022-03-24 02:00:00, Last restarted: 2022-01-04 22:48:54
