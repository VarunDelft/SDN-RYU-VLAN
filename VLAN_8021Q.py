#IMPLEMENTATION OF IEEE 802.1Q VLAN TAGGING AND UNTAGGING 
#DESIRED VLAN CONFIGURATION IS KNOWN PRIORI AND MUST BE ADDED TO THE GLOBAL VARIABLES

#Name: VARUN NAIR
#STUDENT ID: 4504550
#DELFT UNIVERSITY OF TECHNOLOGY , Dept. of Electrical Engineering



from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import vlan
from ryu.lib.packet import ether_types

#GLOBAL VARIABLES  
port_vlan = {2:{3:[" "],1:[30],2:[20],4:[20,30]},3:{4:[20,30],1:[30],2:[20],3:[" "]}}  #port_vlan[a][b]=c => 'a'= dpid, 'b'= port number,'c'= VLAN ID
									
access= {2:[1,2],3:[1,2]}			#access[a]=[B] => 'a' = dpid ,'[B]'=List of ports configured as Access Ports

trunk = {2:[4],3:[4]}				#trunk[a]=[B] => 'a' = dpid ,'[B]'=List of ports configured as Trunk Ports


class VlanSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(VlanSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
	

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    def vlan_members(self,dpid,in_port,src_vlan):
	
	B=[]
	self.access_ports = []
	self.trunk_ports = []
	
	if src_vlan == "NULL":
	    return
	
	for item in port_vlan[dpid]:
    	    vlans=port_vlan[dpid][item]
            if src_vlan in vlans and item!=in_port:
                B.append(item)


	for port in B:
	    if port in access[dpid]:
	        self.access_ports.append(port)
	    else:
		self.trunk_ports.append(port)

#---------------------------------------------------------------#
 
    def getActionsArrayTrunk(self,out_port_access,out_port_trunk,parser):
	actions= [ ]
	
	for port in out_port_trunk:
	    actions.append(parser.OFPActionOutput(port))

	actions.append(parser.OFPActionPopVlan())

	for port in out_port_access:
	    actions.append(parser.OFPActionOutput(port))

        return actions


    def getActionsArrayAccess(self,out_port_access,out_port_trunk,src_vlan, parser):
	actions= [ ]
	

	for port in out_port_access:
	    actions.append(parser.OFPActionOutput(port))
	
	actions.append(parser.OFPActionPushVlan(33024))
	actions.append(parser.OFPActionSetField(vlan_vid=src_vlan))

	for port in out_port_trunk:
	    actions.append(parser.OFPActionOutput(port))

        return actions

    def getActionsNormalUntagged(self,dpid,in_port,parser):
	actions= [ ]

	for port in port_vlan[dpid]:
	    if port_vlan[dpid][port][0]==" " and port!=in_port:
	        actions.append(parser.OFPActionOutput(port))
        

	if dpid in trunk:
	
	    for port in trunk[dpid]:
	        if port!=in_port:
	            actions.append(parser.OFPActionOutput(port))

	return actions

#---------------------------------------------------------------#


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
	
	
	#SWITCH ID
        dpid = datapath.id


        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
	vlan_header = pkt.get_protocols(vlan.vlan)    #If packet is tagged,then this will have non-null value

	

	
	if eth.ethertype == ether_types.ETH_TYPE_8021Q :       #Checking for VLAN Tagged Packet
	    vlan_header_present = 1
	    src_vlan=vlan_header[0].vid
	elif dpid not in port_vlan:
	    vlan_header_present = 0
	    in_port_type = "NORMAL SWITCH "                    #NORMAL NON-VLAN L2 SWITCH
	    src_vlan = "NULL"
	elif port_vlan[dpid][in_port][0]== " " or in_port in trunk[dpid]:
	    vlan_header_present = 0
	    in_port_type = "NORMAL UNTAGGED"                  #NATIVE VLAN PACKET
	    src_vlan = "NULL"
	else:
	    vlan_header_present = 0
            src_vlan=port_vlan[dpid][in_port][0]               # STORE VLAN ASSOCIATION FOR THE IN PORT

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
	
        dst = eth.dst
        src = eth.src
	

	#CREATE NEW DICTIONARY ENTRY IF IT DOES NOT EXIST
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
	
	#Determine which ports are members of in_port's VLAN
	self.vlan_members(dpid,in_port,src_vlan)  	
	out_port_type = " "        

        if dst in self.mac_to_port[dpid]:                       #MAC ADDRESS TABLE CREATION
	    out_port_unknown = 0
            out_port = self.mac_to_port[dpid][dst]
	    if src_vlan!= "NULL":
	        if out_port in access[dpid]:
	            out_port_type = "ACCESS"
	        else:
	            out_port_type = "TRUNK"
	    else :
	        out_port_type = "NORMAL"
        else:
	    out_port_unknown = 1
            out_port_access = self.access_ports        #List of All Access Ports Which are Members of Same VLAN (to Flood the Traffic)
	    out_port_trunk = self.trunk_ports	       #List of All Trunk  Ports Which are Members of Same VLAN (to Flood the Traffic)

	

#########################################  -----FLOW ENTRY ADDITION SEGMENT    ----###############################################
#


        if out_port_unknown!=1:                                                           # IF OUT PORT IS KNOWN 
	    if vlan_header_present and out_port_type == "ACCESS" :                      #If VLAN Tagged and needs to be sent out through ACCESS port 
                match = parser.OFPMatch(in_port=in_port, eth_dst=dst, vlan_vid=(0x1000 | src_vlan))  
                actions = [parser.OFPActionPopVlan(), parser.OFPActionOutput(out_port)]   # STRIP VLAN TAG and SEND TO OUTPUT PORT
            elif vlan_header_present and out_port_type == "TRUNK" :
                match = parser.OFPMatch(in_port=in_port, eth_dst=dst, vlan_vid=(0x1000 | src_vlan))
                actions = [parser.OFPActionOutput(out_port)]                              #SEND THROUGH TRUNK PORT AS IS   
	    elif vlan_header_present!=1 and out_port_type == "TRUNK" :
	        match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
                actions = [parser.OFPActionPushVlan(33024), parser.OFPActionSetField(vlan_vid=src_vlan), parser.OFPActionOutput(out_port)]
	    else:
		match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
	        actions = [parser.OFPActionOutput(out_port)]
		

	    # verify if we have a valid buffer_id, if avoid yes to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)

	else :                                                                                          #FOR FLOODING ACTIONS
	    if vlan_header_present:                                                                     #IF TAGGED
                actions = self.getActionsArrayTrunk(out_port_access,out_port_trunk,parser)
	    elif vlan_header_present==0 and src_vlan!= "NULL":                                          #IF UNTAGGED  BUT GENERATED FROM VLAN ASSOCIATED PORT
		actions = self.getActionsArrayAccess(out_port_access,out_port_trunk,src_vlan, parser)
	    elif in_port_type == "NORMAL UNTAGGED":                                                     #IF UNTAGGED AND BELONGING TO NATIVE VLAN (CAPTURED ON A VLAN AWARE SWITCH)
	        actions = self.getActionsNormalUntagged(dpid,in_port,parser)
	    else :
	        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]                                  # FOR NORMAL NON-VLAN L2 SWITCH


        


        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
