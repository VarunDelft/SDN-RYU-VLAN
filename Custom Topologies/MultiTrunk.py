"""
Two directly connected switches plus 3 hosts for one switch and two for the other:

              host                        
               |
   host --- switch --- switch --- host
               |          |          
              host       host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost_1 = self.addHost( 'h1' )
        leftHost_2 = self.addHost( 'h2' )
	leftHost_3 = self.addHost( 'h3' )
	midHost_1 = self.addHost( 'h4' )
        midHost_2 = self.addHost( 'h5' )
	midHost_3 = self.addHost( 'h6' )
	midHost_4 = self.addHost( 'h7' )
	midHost_5 = self.addHost( 'h8' )
        rightHost_1 = self.addHost( 'h9' )
	rightHost_2 = self.addHost( 'h10' )
        leftSwitch = self.addSwitch( 's1' )
        midSwitch_1 = self.addSwitch( 's2' )
        midSwitch_2 = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost_1, leftSwitch )
	self.addLink( leftHost_2, leftSwitch )
	self.addLink( leftHost_3, leftSwitch )
	self.addLink( midHost_1, midSwitch_1 )
	self.addLink( midHost_2, midSwitch_1 )
        self.addLink( midHost_3, midSwitch_2 )
        self.addLink( midHost_4, midSwitch_2 )
	self.addLink( midHost_5, midSwitch_2 )
        self.addLink( rightHost_1, rightSwitch )
	self.addLink( rightHost_2, rightSwitch )
	self.addLink( leftSwitch, midSwitch_1 )
        self.addLink( midSwitch_1, midSwitch_2 )
	self.addLink( midSwitch_1, rightSwitch )

topos = { 'mytopo': ( lambda: MyTopo() ) }
