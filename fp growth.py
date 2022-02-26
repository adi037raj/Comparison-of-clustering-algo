# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 15:57:44 2021

@author: AADITYA RAJ BARNWAL
"""

from memory_profiler import profile
import copy
import time
total_trans = 0
llist = {}
begin=time.time()
def create_sort_function(tup): #this is just to sort the itemset
    tup.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return tup

def sort_tran_and_write(input_file_name, output_file_name): #reading from file and sorting and storing in another file, so that we can use the sorted file again and again
    global total_trans
    support_count_of_each_item = {}
    global total_counts_item
    total_counts_item=0
    f = open(input_file_name, "r")
    lines = f.readlines()

    for line_index,line in enumerate(lines):
        total_trans+=1
        for item_index,items in enumerate(line.split()):
            item = int(items)
            total_counts_item+=1
            if item not in support_count_of_each_item:
                support_count_of_each_item[item] = 1
            else:
                support_count_of_each_item[item] += 1
    
    f.close()
    
    overall = []
    f = open(output_file_name, "w")
    for line_index,line in enumerate(lines):
        freq_table = []
        for index,item in enumerate(line.split()):
            freq_table.append((int(item), support_count_of_each_item[int(item)]))
        
        table = []
        freq_table = create_sort_function(freq_table)
        for i,_ in freq_table:
            table.append(i)
        overall.append(table)

    for l_index,l in enumerate(overall):
        st = ""
        for _,i in enumerate(range(len(l))):
            if i == len(l) - 1:
                st += str(l[i])
            else:
                st += str(l[i]) + " "

        f.write(st + "\n")
    f.close()

    return support_count_of_each_item

file_name=input("Input the file name with extension ")
support_info = sort_tran_and_write(file_name, "newtdata.txt") #first parameter is the input test file name and then I am sorting it based on the frequency count of each item in every transaction and saving to a new file

class TreeFP:

    freq_itemset = {}
    total_trans = 0
    min_sup = 0
    maximal_freq_itemset_size=0
    maximal_freq_itemsets_size=0
    
    def create_tree(self, root, fileptr): #for creating the FP tree for each item in the tree
        lines  = fileptr.readlines()
        for index,line in enumerate(lines):
            items = line.split()
            transaction = []
            for item_index,item in enumerate(items):
                transaction.append(int(item))

            root.insert_node(transaction)

    def __init__(self, min_sup, total_runs):
        self.total_trans = total_runs
        self.min_sup = min_sup

    def create_treefp_condidtional(self, root, trans):
        for trans_index,trans_value in enumerate(trans):
            root.insert(trans_value)

    def evaluateSupport(self, llist, item_list, prev_set): # for calculationg the support of each itemset
     item = prev_set[0]
     node = llist[item]
     head = llist[item]
     paths = {}
     freq_item_list = []
     paths_list = []
     freq_items={}
     while True:
            
            if node != None:
                break

            freq = node.count
            node = node.parent
            path = []
            while node.parent == None:
                  path.append(node.item)
                  node.nodeCount+=freq
                  node = node.parent
		   
            while freq != 0 and len(path) > 0:
                    paths_list.append(path)
                    freq-=1
			
            path.reverse()
            head = head.next
            node = head
     for index,y in enumerate(item_list):
			  
              x=[y]
			  
              x+=prev_set
			  
              if y not in llist.keys():
			    
                freq_items[frozenset(x)] = 0  
				
                continue
			  
              else:
			    
                 node = llist[item]
			  
              freq = 0
			  
              while True:
				
                 if node==None:
				  
                     break
                 freq+=node.count
                 node.count = 0
                 node = node.next
              freq_items[frozenset(x)]=freq
     for index,y in enumerate(item_list):
                  x=[y]
                  x+=prev_set
                  if freq_items[frozenset(x)]/self.total_trans>=self.min_sup:
                   self.freq_itemset[frozenset(x)] = freq_items[frozenset(x)] / self.total_trans
                   freq_item_list.append(item)
     print("freq :", freq_item_list)
     return freq_item_list,paths_list

    def evaluate_treefp_support(self, itemlist, pathslist,prevset, level):     #for calculating te treefp support overall type
        prev_set = copy.deepcopy(prevset)
        if len(itemlist) <= 1:
            return
        else:
            paths_list = pathslist
            prev_set.insert(0, 0)
            new_itemlist = copy.deepcopy(itemlist)
            while len(new_itemlist) <= 1:
                prev_set[0] = new_itemlist[0]
                new_itemlist = new_itemlist[1:]

                root = TreeNode(0)
                self.createCondidtionalFPtree(root,  paths_list)
                if prev_set[0] in root.llist:
                    new_itemlist, paths_list = self.evaluateSupport(root.llist, new_itemlist, prev_set)
                    self.evaluate_treefp_support(new_itemlist, paths_list, prev_set, level +1)

    def print_itemsets(self):           #for printing the itemsets at each iterationn

        print("------------- frequent itemsets -------------")
        freqitemset = sorted(self.freq_itemset.items(), key=lambda x: len(x[0]), reverse=False)
        for itemset, sup in freqitemset:
            print(itemset, ":", sup)
        
        self.freq_itemset = freqitemset
        count=0
        max_len = 0
        for item,sup in self.freq_itemset:
            count+=1
            curr_len = len(item)
            if curr_len>max_len:
                max_len=curr_len
                count=0
        self.maximal_freq_itemset_size=max_len
        self.maximal_freq_itemsets_size=count
        
    @profile
    def run_algo(self, sortedFreqItems, root):                         # this the running alogirhtm
        sortedFreqItems.reverse()
        ptr_list = sortedFreqItems
        llist = root.llist
        print(ptr_list)
        print("started")
        for index,item in enumerate(sortedFreqItems):
            prev_set = [ptr_list[0]]
            ptr_list = ptr_list[1:]

            new_itemlist, paths_list = self.evaluateSupport(llist,ptr_list, prev_set)
            self.evaluate_treefp_support( new_itemlist, paths_list, prev_set,1)
        self.print_itemsets()

class TreeNode:          # A data structure for creaating the tree Node
    nextNode = None
    parentNode = None
    childNodes = {}
    nodeCount = 1
    llist = {}
    item = []

    def __init__(self, item):
        self.next = None
        self.parent = None
        self.childs = {}
        self.count = 0
        self.llist = {}
        self.item = item



    def insert_node(self, trans_details):         #for insertion a new node in the tree
        node = self

        for index,item in enumerate(trans_details):
            prev_node = node
            if item not in node.childs:
                new_node = TreeNode(item)
                node.childs[item] = new_node
                node = new_node

                if item not in self.llist.keys():
                    self.llist[item] = node
                else:
                    node.next = self.llist[item]
                    self.llist[item] = node

            else:
                node = node.childs[item]
                node.count+=1
                
            node.parent = prev_node


filename = "newtdata.txt"
filePtr = open(filename, "r")

sorted_items = []
freq_itemlist = []
min_sup =  float(input("Enter Minimum support number: "))      #minimum support

for item, freq in support_info.items():
    sorted_items.append((item,freq))

sorted_items = create_sort_function(sorted_items)

fpObj = TreeFP(min_sup, total_trans)
root = TreeNode(0)

for (item, trans) in sorted_items:
    if (trans/total_trans) >= min_sup: 
        freq_itemlist.append(item)
        fpObj.freq_itemset[frozenset([item])]= (trans/total_trans)

print(total_trans)
print("1 freq itemsets : ", len(freq_itemlist))
fpObj.create_tree(root, filePtr)
print("created FP tree")
fpObj.run_algo(freq_itemlist, root)
end=time.time()
print('The time taken ',end-begin)
print('The transaction are ',total_trans)
print('Total no. of items ',len(support_info.keys()))
print('Average length of transaction is ',total_counts_item/total_trans)
print('The no. of frequent itemset ',len(fpObj.freq_itemset))

print("Size of maximal frequent itemset : ", fpObj.maximal_freq_itemset_size)













