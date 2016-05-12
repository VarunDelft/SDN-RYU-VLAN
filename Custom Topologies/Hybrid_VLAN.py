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
     
	midHost_1 = self.addHost( 'h2' )
        midHost_2 = self.addHost( 'h3' )
	
        rightHost_1 = self.addHost( 'h4' )
	rightHost_2 = self.addHost( 'h5' )
	rightHost_3 = self.addHost( 'h6' )

        leftSwitch = self.addSwitch( 's1' )
        midSwitch = self.addSwitch( 's2' )
        rightSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( leftHost_1, leftSwitch )
	
	self.addLink( midHost_1, midSwitch )
	self.addLink( midHost_2, midSwitch )
        
        self.addLink( rightHost_1, rightSwitch )
	self.addLink( rightHost_2, rightSwitch )
	self.addLink( rightHost_3, rightSwitch )
	self.addLink( leftSwitch, midSwitch )
	self.addLink( midSwitch, rightSwitch )

topos = { 'mytopo': ( lambda: MyTopo() ) }
