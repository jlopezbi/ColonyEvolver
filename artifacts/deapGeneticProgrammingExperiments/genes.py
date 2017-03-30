
'''
Experimental code, trying to imagine how to create 
directed graph representation of classes of nodes
'''
class Node(object):

    def __init__(self,processor,refrence_type):
        self.processor = processor
        #the refrence_type is the 'pointer' to another class, possibly self
        self.refrence_type = refrence_type

    def process_inputs(*args):
        outputs = self.processor(args)
        return [self.refrence_type(outputs)]
        

class NetworkMaker(object):
    ''' returns node classes that have refrences to
    other node classes'''

    def __init__(self):
        pass
    
    def run


nodes = collector.get_node_types()
configured_nodes = []
for node in nodes:
    configured_node = nodeConnector.randomly_connect(node,nodes)
    configured_nodes.append(configured_node)


