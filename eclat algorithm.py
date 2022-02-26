# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 18:14:02 2021

@author: AADITYA RAJ BARNWAL
"""
from sortedcontainers import SortedDict
import time
import memory_profiler
from memory_profiler import profile

def compute_freq_itemset(itemsets, trans_info,num_trans,min_sup,freq_itemset):

        new_itemsets = []
        new_trans_info={}
        for item in itemsets:
            cardinality = len(trans_info[item])
            freq = cardinality/num_trans
            if freq > min_sup:
                freq_itemset[item] = freq
                new_trans_info[item]=trans_info[item]
             # improved check point*********************
               
            
        return new_itemsets,new_trans_info,freq_itemset


def print_freq_itemsets(freq_itemset):

        for itemset, sup in freq_itemset.items():
            print(itemset, ":", sup)
  

def sort_item_sets(set1,set2):
    return sorted(set1), sorted(set2)


def generate_next_itemsets(itemsets, trans_info, set_size,num_trans,min_sup):
        print("item set size : ",set_size)
        #print(itemsets[1])
        new_trans_info = {}
        new_itemsets = []
        intersection = []
        new_item = []
        i_set1 = []
        i_set2 = []
        for i,item1 in enumerate(itemsets):
            for k,j in enumerate(range(i+1,len(itemsets))):
                if set_size > 1:
                    i_set1,i_set2 = sort_item_sets(list(itemsets[i]),list(itemsets[j]))
                    i_set1,i_set2 = i_set1[:set_size-1],i_set2[:set_size-1]
                if i_set1 != i_set2 :
                    continue
                else:
                    intersection = list(set(trans_info[itemsets[i]]) & set(trans_info[itemsets[j]]))
                    freq = len(intersection)/num_trans
                    if freq <= min_sup :
                        continue
                    else:
                        if set_size != 1:
                            new_item = frozenset(sorted(list(itemsets[i]|itemsets[j])))
                        else:
                            new_item = frozenset([itemsets[i],itemsets[j]])
                            
                        new_itemsets.append(new_item)
                        new_trans_info[new_item] = intersection

        return new_trans_info,new_itemsets
            
          
 
@profile            
def Main():
    begin=time.time()
    total_count_of_items_in_all_transaction=0
    file_name=input("Input the file name with extension ")     # file name
    minimum_support= float(input("Enter Minimum support number: "))  # minimum support count
    itemToTrans = {}
    total_trans = 0
    f=open(file_name,"r")
    t_id = 0
    frequent_itemset={}
    for i,items in enumerate(f):
        t_id+=1
        for j,item in enumerate(items.split()):
            item = int(item)
            total_count_of_items_in_all_transaction+=1
            if item in itemToTrans:
                itemToTrans[item].append(t_id)
            else:
                itemToTrans[item] = [t_id]
        total_trans+=1
    itemToTrans = SortedDict(itemToTrans)
    #print_the_order(itemToTrans)
    verticalData = {}
    freq_itemset = {}
    min_sup = 0
    num_trans = 0
    min_sup=minimum_support
    num_trans=total_trans
    verticalData=itemToTrans   # 
    
    ######################################
    
    set_size = 1
    new_itemsets, new_trans_info, freq_itemset = compute_freq_itemset(verticalData.keys(), verticalData,num_trans,min_sup,freq_itemset) #this function compute the frequent item set 
    print(len(new_itemsets))
    maximal_freq_itemsets_size=0
    #print(new_itemsets[1])
    while True:
            if len(new_itemsets)== 0:
                print("finished")
                print_freq_itemsets(freq_itemset)
                break
            maximal_freq_itemsets_size=max(len(new_itemsets),maximal_freq_itemsets_size)
            new_trans_info, new_itemsets  = generate_next_itemsets(new_itemsets, new_trans_info, set_size,num_trans,min_sup)
            new_itemsets, new_trans_info, freq_itemset= compute_freq_itemset(new_itemsets, new_trans_info,num_trans,min_sup,freq_itemset)
            set_size += 1
    end=time.time()
    
    
    print('The Total Time Taken ',end-begin)
    print('Total No. of Transaction ',total_trans)
    print('Total no. of items ',len(itemToTrans.keys()))
    print('The average length of transactions ',total_count_of_items_in_all_transaction/total_trans)
    
    print("Total no. of frequent itemsets : ",len(freq_itemset))
    
    
    print("Size of maximal frequent itemset : ", set_size)


if __name__ == "__main__":
    
  Main() 
    
    
    
    
    
    
    
