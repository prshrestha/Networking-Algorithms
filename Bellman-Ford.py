# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm.


from Node import *
from helpers import *


class DistanceVector(Node):

    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)

        self.node_distance = {self.name: 0}  # distance to itself is 0 initially

    def send_initial_messages(self):
	
        msg = (self.name, self.node_distance.items())
        # print "this is the message"

        for destination_incoming_links in self.neighbor_names:
            # print "destination_incoming_links in send initial message"
            # print destination_incoming_links
            # print "message in send initial message"
            # print msg
            self.send_msg(msg, destination_incoming_links)

    def process_BF(self):

        for msg in self.messages:
            node_name = msg[0]
            vec_node_distance = msg[1]

            node_cost = self.get_outgoing_neighbor_weight(node_name)
            node_cost = int(node_cost)

            for (node_name, total_cost) in vec_node_distance:

                if node_name == self.name:
                    continue
                if total_cost <= -50:
                    total_cost = -99
                else:
                    total_cost = total_cost + node_cost
                if node_name not in self.node_distance or total_cost < self.node_distance[node_name]:
                    self.node_distance[node_name] = total_cost

                    msg = (self.name, self.node_distance.items())

                    for destination_incoming_links in self.neighbor_names:
                        self.send_msg(msg, destination_incoming_links)

        # Empty queue
        self.messages = []

    def log_distances(self):
        seq_to_print = ""
        for k, v in self.node_distance.items():
            seq_to_print += k + str(v) + ","
        seq_to_print = seq_to_print[:-1]

        add_entry(self.name, seq_to_print)