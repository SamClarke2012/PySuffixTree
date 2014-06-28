"""
   Copyright 2014 Sam Clarke

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
"""

class SharedCounter(object):
    """
    A shared counter object (Integer)
    """

    def __init__(self, start_value):
        self.val = start_value

    def getVal(self):
       return self.val

    def nextVal(self):
        self.val += 1  


class Node(object):
    """
    A generic node object for the suffix tree.

    self.id = the id of the node
    self.parent_edge = The edge leading back to root
    self.child_edges = A dict of edges and their char ids
    self.suffix_link = A suffix link obj (jump to common nodes)
    """
    def __init__(self, Id):
        self.id = Id
        self.parent_edge = None
        self.child_edges = {}
        self.suffix_link = None

    def __str__(self):
        if self.hasSuffixLink():
            return 'Node ' + str(self.id) + ' S-linked to ' + \
                str(self.suffix_link.getDestination())
        else:
            return 'Node ' + str(self.id)
        
    def setParent(self, edge):
        """
        Set the parent edge
        """
        self.parent_edge = edge
        
    def getParent(self):
        """
        Get the parent edge
        """
        return self.parent_edge
        
    def addChild(self, edge):
        """
        Add a child edge
        """
        self.child_edges[edge.getId()] = edge

    def removeChild(self, edge):
        """

        Remove a child edge
        """
        del self.child_edges[edge.getId()]

    def getChildren(self):
        """
        Get child edges (dict)
        """
        return self.child_edges

    def addSuffixLink(self, suffix_link):
        """
        Add a suffix link from this node
        """
        self.suffix_link = suffix_link


    def hasSuffixLink(self):
        """
        Check this node for a suffix link
        """
        return False if self.suffix_link is None else True


    def getSuffixLink(self):
        """
        Get the suffix link for this node
        """
        return self.suffix_link
        

class Edge(object):
    """
    A generic edge object for the suffix tree.

    self.id = the starting char of the suffix. i.e 'a'
    self.start = the index of the suffix start within the target
    self.stop  = the index of the suffix stop
    self.dest_node = the node we connect to (if any)
    """
    def __init__(self, Id, start, stop, destination_node = None):
        self.id = Id
        self.start = start
        self.stop = stop
        self.dest_node = destination_node

    def __str__(self):
        if type(self.stop) is SharedCounter:
            return 'Edge '+str(self.id)+' '+str(self.getLength())+' suffix ['+\
                   str(self.start)+':'+str(self.stop.getVal())+'] connected to '\
                   + str(self.dest_node)
        else:
            return 'Edge '+str(self.id)+' '+str(self.getLength())+' suffix ['+\
                    str(self.start)+':'+str(self.stop)+'] connected to ' + \
                    str(self.dest_node)

    def getId(self):
        """
        Get the edge id (the starting char of the suffix).
        """
        return self.id

    def setDestination(self, node):
        """
        Set the destination node.
        """
        self.dest_node = node

    def getDestination(self):
        """
        Get the destination node.
        """
        return self.dest_node

    def setBound(self, start = None, stop = None):
        """
        Set the suffix indexes.
        """
        if start is not None: self.start = start
        elif stop is not None: self.stop = stop

    def getLength(self):
        """
        Get the length of the suffix
        """
        stop = 0
        if type(self.stop) is SharedCounter:
            stop = self.stop.getVal()
        else:
            stop = self.stop
        return stop - self.start

    def getSuffix(self):
        """
        Get the suffix indexes.
        """
        stop = 0
        if type(self.stop) is SharedCounter:
            stop = self.stop.getVal()
        else:
            stop = self.stop
        return (self.start, stop)

        
class SuffixLink(Edge):
    """
    A sufffix link edge object.
    A logical link between common nodes in the tree.
    """
    def __init__(self, destination_node):

        self.dest_node = destination_node
    
    def __str__(self):

        return str(self.dest_node)

    def getDestination(self):
        """
        Get the destination node
        """
        return self.dest_node

        
class SuffixTree(object):
    """
    A sufffix tree edge object.
    Makes use of the Ukkonen algorithm and it's optimisations.
    """
    def __init__(self):

        self.pos = SharedCounter(-1)
        self.edge_cnt = 0
        self.edges = []
        self.link = None
        self.remainder = 0
        self.active_len = 0
        self.active_length = 0
        self.active_edge = None
        self.root = Node(0)
        self.nodes = [self.root]
        self.active_node = self.root
        self.latest_node = self.root
        self.target = ''

    def __str__(self):
        """
        Prints the nodes in the tree sequentially along with their edges 
        (in node:edge order).
        """
        s = ''
        for node in self.nodes:
            s += '\n\n'+str(node)+'\n\t'
            edges = node.getChildren()
            keys = edges.keys()
            keys.sort()
            for key in keys:
                bounds = edges[key].getSuffix()
                s += str(edges[key])+' '
                for i in xrange(bounds[0], bounds[1]):
                    s += self.target[i]
                s += '\n\t'
        return s


    def buildTree(self, string, debug=False):

        self.target = string
        self.remainder = 1
        for char in string:
            attach_link = False
            self.pos.nextVal()
            # Remainder is one @ each step
            node_edges = self.active_node.getChildren()
            # If the active node does not have an edge for this
            if char in node_edges:
                if debug: print 'Edge exists'
                self.remainder += 1
                self.active_length += 1
                if self.active_edge is None or self.active_length == 1:
                    self.active_edge = char
                if self.active_length >= node_edges[char].getLength():
                        # move to the edge dest
                        self.moveDown(node_edges[self.active_edge])
            else:
                if debug: print 'Edge doesn\'t exist'
                while self.remainder > 1:
                    if char == '$': break
                    if debug: print 'Splitting edge', self.active_edge, self.active_node,'Remainder', self.remainder
                    node_edges = self.active_node.getChildren()
                    self.splitEdge(node_edges[self.active_edge], 
                                            self.active_length, attach_link)
                    attach_link = True
                    self.remainder -= 1
                else:
                    if debug: print 'Adding edge', char
                    new_edge = Edge(char, self.pos.getVal(), self.pos)
                    self.active_node.addChild(new_edge) 
            if debug:
                print 'Char', char
                print 'Active node', self.active_node
                print 'Active edge', self.active_edge
                print 'Active length', self.active_length
                print 'Remainder', self.remainder
                print self


    def moveDown(self, edge):
        """
        Move down to the destination node of the supplied edge.
        e.g

        move from 'A' to 'B'...

                [A]-------------------[B]
        """
        # move to the edge destination node
        dest = edge.getDestination()
        if dest is not None:
            self.active_node = dest
            self.active_edge = None
            self.active_length = 0
        else:
            pass


    def splitEdge(self, edge, index, link):
        """
        Split an existing edge at index
        e.g

        n-----(i)---------- pos++
                \
                 \--------- pos++
        """
        #print 'Splitting edge', edge
        node = Node(len(self.nodes))
        if link and self.latest_node is not None:
            suffix_link = SuffixLink(node)
            self.latest_node.addSuffixLink(suffix_link)
        # copy out existing destination and bounds
        old_dest = edge.getDestination()
        old_bounds = edge.getSuffix()
        old_start = old_bounds[0]
        # Adjust edge finish point to n + index, connect new node
        edge.setBound(stop = old_start + index)
        edge.setDestination(node)   
        # Create new edge representing the remains of the old edge
        offcut = Edge(self.target[old_start + index], old_start + index, 
                    self.pos, old_dest)
        # Add the offcut edge as a child of the new node
        node.addChild(offcut) 
        # Create new edge for the current pos
        n = self.pos.getVal()
        new_edge = Edge(self.target[n], n, self.pos)
        node.addChild(new_edge)
        self.nodes.append(node)
        self.latest_node = node
        # rule 1 - a split from the root node
        if self.active_node == self.root:
            # active length decrements
            self.active_length -= 1
            pos = self.pos.getVal()
            # active edge changes
            self.active_edge = self.target[pos - self.active_length]
            # active node remains root
        else:
            if self.active_node.hasSuffixLink():
                # Set the active node to the link destination
                link = self.active_node.getSuffixLink()
                self.active_node = link.getDestination()
            else:
                self.active_node = self.root # set active node to root
