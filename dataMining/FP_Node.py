#Structure taken from https://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Frequent_Pattern_Mining/The_FP-Growth_Algorithm
class FP_Node:
    def __init__(self,label,count,children, parent):
        self.label = label
        self.count = count
        self.parent = parent
        self.children = children

    def get_label(self):
        return self.label

    def set_label(self,label):
        self.label(label)

    def get_count(self):
        return self.count

    def set_count(self,count):
        self.count = count

    def increment_count(self):
        self.count+=1

    def get_children(self):
        return self.children

    def set_children(self,children):
        self.children = children

    def add_child(self,child):
        self.children.append(child)

    def get_parent(self):
        return self.parent

    def get_node_link(self):
        return self.node_link

    def set_node_link(self,node_link):
        self.node_link = node_link

    def add_node_to_link(self,node):
        self.node_link.append(node)

    # parent should never change

    def get_child(self,label):
        for child in self.children :
            if child.label == label:
                return child
        return None

    def insert(self,clusters):
        first = clusters[0]
        clusters.remove(first)
        #Check if child exists
        child =self.get_child(first)
        if(child != None):
            # If self has a child such that child.label == first then increment child.count
            child.increment_count()
        else:
            # else create a new node N , with its count initialized to 1, its parent link linked to this
            child = FP_Node(first,1,[],self)

        if(len(clusters)>0):
            self.insert(clusters)



