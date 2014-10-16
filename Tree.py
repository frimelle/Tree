# This Python file uses the following encoding: utf-8

import gzip 
import json

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

counter_no_some = 0
counter_nodes = 0
counter_roots = 0
counter_in_tree = 0
counter_level = 1

def isInstanceOfTaxon(json_l):
	#check if the things we will look for are actually there (otherwise there are errors, e.g. when there is no datavalue attribute)
		if 'claims' in json_l and 'P31' in json_l['claims'] and 'datavalue' in json_l['claims']['P31'][0]['mainsnak']:
			#check if instance of (P31) taxon (Q16521):
			instanceOf_id = json_l['claims']['P31'][0]['mainsnak']['datavalue']['value']['numeric-id']
			if instanceOf_id == 16521: 
				return True
		else:
			return False

def hasParentTaxon(json_l):
	#check if there is a parent taxon (P171) for this item
	if 'P171' in json_l['claims']:
		if 'datavalue' in json_l['claims']['P171'][0]['mainsnak']:
			return True
	else:
		return False

def hasSubclassOf(json_l):
	if 'P279' in json_l['claims'] and 'datavalue' in json_l['claims']['P279'][0]['mainsnak']:
		return True

def hasNoSomeValueParent(json_l):
	if 'P171' in json_l['claims'] and not 'datavalue' in json_l['claims']['P171'][0]['mainsnak']:
		return True

#for debugging
def printChildren(parent):
	x = 0
	print "parent taxon: "
	print parent.data
	print ' --------------------------------'
	print "children: "
	for c in parent.children:
		print c.data
		x = x + 1	
	print ' --------------------------------'
	print x 
	print ' --------------------------------'


def traversing( node, f, counter_level ):
	#f.write('<ul class="level' + str(counter_level) + '">' + '\n')
	f.write('node.data' + '\n' + str(counter_level))
	counter_level += 1
	for c in node.children:
		traversing(c, f, counter_level)
		global counter_in_tree
		counter_in_tree = counter_in_tree + 1


#here starts the actual important stuff
f = gzip.open('20140922.json.gz')
node_dict = {} #list of the nodes already added to the tree
root_array = []
no_some_value_node = Node('NoSomeValue')
node_dict['no_some'] = no_some_value_node

for line in f:
	line = line.rstrip().rstrip(',')
	try:
		json_l = json.loads(line)
	except ValueError, e:
		continue

	if isInstanceOfTaxon(json_l):
		
		child_id = json_l['id']
		
		if node_dict.has_key(child_id):
			child = node_dict[child_id]
		else:
			child = Node(child_id)
			node_dict[child_id] = child
			counter_nodes = counter_nodes + 1
	
		#check if there is a parent taxon (P171) for this item or if it is a subclass of antother taxon
		if hasParentTaxon(json_l): 
			if hasParentTaxon(json_l):
				parent_id = 'Q' + str(json_l['claims']['P171'][0]['mainsnak']['datavalue']['value']['numeric-id'])
			
			if node_dict.has_key(parent_id):
				parent = node_dict[parent_id]
			else:
				parent = Node(parent_id)
				node_dict[parent_id] = parent
				counter_nodes = counter_nodes + 1
					
			parent.add_child(child)
		
		elif hasNoSomeValueParent(json_l):
			no_some_value_node.add_child(child)
			counter_no_some = counter_no_some + 1

		else: #not hasParentTaxon(json_l) and not hasNoSomeValueParent(json_l):
			root_array.append(child)
			counter_roots = counter_roots + 1

count_r_ch = 0
roots_file = open('roots.txt', 'w')
tree_file = open('tree.txt', 'w')
for r in root_array:
	#write a tree from Biota
	if r.data == 'Q2382443': 
		traversing(r, tree_file, counter_level)
	
	#write all root nodes in a file to hopefully have an overview, which subtrees need to be integrated
	if r.children: #check if the "root" actually has children
#		print 'Writing root to file'
		roots_file.write(str(r.data) + ' ')
		count_r_ch = count_r_ch + 1

roots_file.close()

print "Nodes: " + str(counter_nodes)
print "Roots: " + str(counter_roots)
print "Roots, excluding roots without children: " + str(count_r_ch)
print "Nodes with parent taxon no or some value: " + str(counter_no_some)
print "Nodes in Biota Tree: " + str(counter_in_tree)


