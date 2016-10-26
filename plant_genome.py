
#Pseudo CODe below:
# trying to figure out how to make genome system
# Below is a class based appraoch; genome would be a series of classes


class b_node(object):
    def spawn(self):
        pass

class c_node(object):
    self.behavior = {}
    self.behavior[condition0:response0]
    self.behavior[condition1:response1]
    
    def respond(self,inputs):
        for condition in self.coniditions:
            if self.satisfies(inputs,condition):
                function = self.behavior[condition]
                return function(inputs)
             
    def response0(inputs):
        new_pos = process_inputs(inputs)
        return b_node(new_pos) #reference to another type of node

'''
Or perhaps code for a plant would be generated using the genome!
'''

class a_node(object):
    def responds(inputs):
        if satisfies(inputs,condition0):
            self.response
    def spawn(self,inputs):
        return (b_node(modified_inputs),b_node(modified_inputs))
    def die(self):
        #delete from plant somehow
        pass


class base_node(object):
    def respond(collision):
        # spawn, die, etc.
        pass
    
    def store_info():
        pass

    def spawn():
        pass

    def die():
        pass










