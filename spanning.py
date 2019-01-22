# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)



from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        self.rootID = self.switchID  # initially the root is the same as the origin switch
        self.distanceToRoot = 0  # initially the root and the origin are same, so distance = 0
        self.partSpanningTree = {}
        for link in self.links:
            self.partSpanningTree[link] = False  # links are not connected in the begining

        self.switchThrough = self.switchID

    def send_initial_messages(self):

        for link in self.links:
            message = Message(self.switchID, 0, self.switchID, link, False)
            self.send_message(message)
        return

    def process_message(self, message):
        # case 1 - root of message < root of the origin/self
        if message.root < self.rootID:
            self.rootID = message.root
            self.distanceToRoot = message.distance + 1
            self.switchThrough = message.origin

            for link in self.links:
                if link == message.origin:  # check if the message and the self switch
                    self.partSpanningTree[link] = True
                    self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, link, True))
                else:
                    self.partSpanningTree[link] = False
                    self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, link, False))

        # case 2 - root of message == root of the self switch
        elif message.root == self.rootID:
            if message.distance + 1 < self.distanceToRoot:  # case 2a - where message distance to root is less than the root distance
                self.distanceToRoot = message.distance + 1
                self.switchThrough = message.origin
                for link in self.links:
                    if link == message.origin:
                        self.partSpanningTree[link] = True
                        self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, link, True))
                    else:
                        self.partSpanningTree[link] = False
                        self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, link, False))
            elif message.distance + 1 > self.distanceToRoot:
                self.partSpanningTree[message.origin] = message.pathThrough
                # for link in self.links:   # this causes multiple extra pairs of connection
                #     if link == message.origin:
                #         self.partSpanningTree[link] = True
            elif message.distance + 1 == self.distanceToRoot:
                # use the tie breaker rule
                if message.origin < self.switchThrough:  # update two items here: self.activelinks and switchThrough
                    self.partSpanningTree[self.switchThrough] = False
                    self.send_message(
                        Message(self.rootID, self.distanceToRoot, self.switchID, self.switchThrough, False))

                    self.switchThrough = message.origin
                    self.partSpanningTree[message.origin] = True
                    self.send_message(
                        Message(self.rootID, self.distanceToRoot, self.switchID, self.switchThrough, True))

        return

    def generate_logstring(self):

        logs_to_print = []
        # print "spanning tree"
        # print sorted(self.partSpanningTree)
        # sort the self.partSpanningTree
        for link in sorted(self.partSpanningTree):
                # print "link: " + str(link) + " switch: " + str(self.switchID)
                if self.partSpanningTree[link]:
                    seq = str(self.switchID) + " - " + str(link)
                    # only add once by using the following trick
                    if seq not in logs_to_print:
                        logs_to_print.append(seq)

        return ', '.join(logs_to_print)