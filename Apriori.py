# -*- coding: utf-8 -*-
import time

from memory_profiler import profile
"""
Created on Sun Sep 26 15:31:11 2021

@author: ADITYA
"""
from collections import defaultdict



def Calculate(Element_sets,Pointers):          # calculating the frequent itemset at kth level by scanning the file again
        frequency_count_of_each_element = {}

        for Element in Element_sets:
            Pointers.seek(0)
            lines = Pointers.readlines()
            frequency_count_of_each_element[frozenset(Element)] = 0
            for i,line in enumerate(lines):
                trans_items = line.split()
                new_list = []
                for j,elm in enumerate(trans_items):
                    new_list.append(int(elm))
                if set(Element).issubset(set(new_list)):
                    frequency_count_of_each_element[frozenset(Element)] += 1


        return frequency_count_of_each_element



def calculate_the_support_and_transactions(lines):        # simple function return the frequency count of each element
    frequency_count_of_each_element={}
    total_counts_of_items_all_transaction=0
    No_of_total_transactions_given=0
    Element_sets = []
    for i,line in enumerate(lines):
        contents = line.split()
        No_of_total_transactions_given += 1
        for j,Element in enumerate(contents):
            Element = int(Element)
            total_counts_of_items_all_transaction+=1
            if Element not in frequency_count_of_each_element.keys():
                Element_sets.append(Element)
                frequency_count_of_each_element[Element] = 1
            else:
                frequency_count_of_each_element[Element] += 1
                
    Element_sets = sorted(Element_sets)

    return frequency_count_of_each_element,Element_sets,No_of_total_transactions_given,total_counts_of_items_all_transaction

def Initialize_everything():            # This function Initializes all variables and file name and eread the file and return all the necessary parameters
     MINIMUM_SUPPORT = float(input("Enter Minimum support number: "))
     
     FILE_NAME=input("Input the file name with extension ")
     No_of_total_transactions_given = 0
     
     Element_sets = []
     frequency_count_of_each_element = {}
     
     f=open(FILE_NAME,"r")
     lines = f.readlines()
     frequency_count_of_each_element,Element_sets,No_of_total_transactions_given,total_counts_of_items_all_transaction=calculate_the_support_and_transactions(lines)
     return MINIMUM_SUPPORT,f,frequency_count_of_each_element,Element_sets,No_of_total_transactions_given,total_counts_of_items_all_transaction



@profile        # for calculating the memory used(space complexity)
def Apriori_Algo(Element_sets,frequency_count_of_each_element,Minimum_support,file_pointer,total_transaction,container_of_all_itemset): #this is the heart of the program
    iteration=1
    Itemsets_frequents = []
    Itemsets_Infrequents = []
    for Element in Element_sets:
            Temp_items = Element
            if frequency_count_of_each_element[Temp_items]/total_transaction > Minimum_support:
                Itemsets_frequents.append(Element)
                container_of_all_itemset[Temp_items] = frequency_count_of_each_element[Temp_items]/total_transaction
            else:
                Itemsets_Infrequents.append(Element)
    print(Itemsets_frequents)
    global max_size_itemset_frequent
    max_size_itemset_frequent=0
    Current_Candidates_Itemsets = []
    for _ in iter(int, 1):             # infinte loop
        print("Iteration Level",iteration)
        
        if iteration!=1:               # if it is not the frequent 1 itemset
            temp=[]
            print(Itemsets_frequents)
            for val1,i in enumerate(range(len(Element_sets))):
             for val2,j in enumerate(range(i+1, len(Element_sets))):
                item1 = Element_sets[i]
                item2 = Element_sets[j]
                if frequency_count_of_each_element[frozenset(item1)]/total_transaction<Minimum_support:
                    break
                if frequency_count_of_each_element[frozenset(item2)]/total_transaction<Minimum_support:
                    continue

                if item1[:iteration-1] != item2[:iteration-1]:
                    break
                else:
                    element = item1[:iteration-1]
                    element.append(item1[iteration-1])
                    temp.append(element)
                    element.append(item2[iteration-1])
                    
            Current_Candidates_Itemsets=temp
        else:              # if it is frequent 1 itemset
            for val1,i in enumerate(range(len(Element_sets))):
                for val2,j in enumerate(range(i+1, len(Element_sets))):
                    if frequency_count_of_each_element[Element_sets[i]]/total_transaction<Minimum_support:
                        break
                    if frequency_count_of_each_element[Element_sets[j]]/total_transaction<Minimum_support:
                        continue
                    Current_Candidates_Itemsets.append([Element_sets[i], Element_sets[j]])
            

        for i,element in enumerate(Current_Candidates_Itemsets):
            for j,itemset in enumerate(Itemsets_Infrequents):
                if iteration == 1:
                    itemset = [itemset]
                if set(itemset).issubset(set(element)):
                    Current_Candidates_Itemsets.remove(element)
    
        frequency_count_of_each_element=Calculate(Current_Candidates_Itemsets,file_pointer)
        iteration+=1
        max_size_itemset_frequent=len(Itemsets_frequents)
        print(Current_Candidates_Itemsets)
        temp_freq_itemsets=Itemsets_frequents
        Itemsets_frequents = []
        Itemsets_Infrequents = []
        Element_sets=Current_Candidates_Itemsets
        for i,Element in enumerate(Element_sets):
            Temp_items = frozenset(Element)
            if frequency_count_of_each_element[Temp_items]/total_transaction <=Minimum_support:
                Itemsets_Infrequents.append(Element)
            else:
                Itemsets_frequents.append(Element)
                container_of_all_itemset[Temp_items] = frequency_count_of_each_element[Temp_items]/total_transaction
                

        if len(Itemsets_frequents) == 0:
                
                for itemset, sup in container_of_all_itemset.items():
                   print(itemset, ":", sup)
                print("Completed")
                break

    return temp_freq_itemsets,iteration-1








if __name__ == "__main__":
    
    begin=time.time()
    container_of_all_itemset={}
    MINIMUM_SUPPORT,f_pointer,Support_info,Element_sets,total_transaction,total_counts_of_items_all_transaction= Initialize_everything()
    Itemsets_frequents,iteration= Apriori_Algo(Element_sets,Support_info,MINIMUM_SUPPORT,f_pointer,total_transaction,container_of_all_itemset)
    f_pointer.close()
    end=time.time()
    print('Total Time Taken ',end-begin)
    print('Total no. of transaction ',total_transaction)
   
    print('Total No. of itemsets',len(Element_sets))
    print('Average length of transaction ',total_counts_of_items_all_transaction/total_transaction)
    print('total no. Last Level Frequent Itemset ',len(Itemsets_frequents))
    print('The size of maximal freq itemset ',iteration)
    print('The No. of maximum frequent itemsets ',max_size_itemset_frequent)
    