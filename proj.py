from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from collections import namedtuple
import os
from csv import DictReader


log = core.getLogger()
policyFile = "%s/practice codes/proj/layer2.csv" % os.environ[ 'HOME' ]
Policy = namedtuple('Policy', ('dl_src', 'dl_dst'))

policyFile2 = "%s/practice codes/proj/layer3.csv" % os.environ[ 'HOME' ]
Policy2 = namedtuple('Policy2', ('nw_src', 'nw_dst'))

policyFile3 = "%s/practice codes/proj/singlehost.csv" % os.environ[ 'HOME' ]
Policy3 = namedtuple('Policy3', ('hst'))

class Firewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
    
    def read_policies (self, file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter = ",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy(EthAddr(row['mac_0']), EthAddr(row['mac_1']))
        return policies

    def read_policies2 (self, file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter = ",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy2(IPAddr(row['ip_0']), IPAddr(row['ip_1']))
        return policies

    def read_policies3 (self, file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter = ",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy3(IPAddr(row['ip']))
        return policies

    def _handle_ConnectionUp (self, event):
        # for layer 2
        policies = self.read_policies(policyFile)
        for policy in policies.itervalues():
            
            msg = of.ofp_flow_mod()
            msg.priority = 20
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))

            match = of.ofp_match()

            # policy in one direction(layer 2)
            match.dl_src = policy.dl_src
            match.dl_dst = policy.dl_dst
            msg.match = match
            event.connection.send(msg)

            # policy for opposite direction(layer 2)
            match.dl_src = policy.dl_dst
            match.dl_dst = policy.dl_src
            msg.match = match
            event.connection.send(msg)

            
        #for layer 3
        policies2 = self.read_policies2(policyFile2)
        for policy2 in policies2.itervalues():
            msg = of.ofp_flow_mod()
            msg.priority = 20
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))

            
            match = of.ofp_match()

            # policy in one direction(layer 3)
            match.dl_type = 0x800
            match.nw_src = policy2.nw_src
            match.nw_dst =  policy2.nw_dst
            msg.match = match
            event.connection.send(msg)

            # policy for opposite direction(layer 3)
            match.nw_src = policy2.nw_dst
            match.nw_dst = policy2.nw_src
            msg.match = match
            event.connection.send(msg)

        # blocking single host
        policies3 = self.read_policies3(policyFile3)
        for policy3 in policies3.itervalues():
            msg = of.ofp_flow_mod()
            msg.priority = 20
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))

            match = of.ofp_match()

            # policy fro blocking single host
            match.dl_type = 0x800
            match.nw_dst =  policy3.hst
            msg.match = match
            event.connection.send(msg)        

def launch ():

    #Starting the Firewall
    
    core.registerNew(Firewall)