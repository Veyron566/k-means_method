from math import sqrt
import copy

def read(namef,list_of_objects):      #reading the data file
    _file = open(namef, 'r')
    for line in _file:
        words=line.split(',')
        if (words[0]== ''):
            continue                 #first line contains names of variables
        words[-1]=words[-1][0:-1]      #cutting the '\n' symbols
        
        for i in range(1,len(words)):#converting to numbers
            words[i]=float(words[i])
        list_of_objects.append(words)
    _file.close()
    
def distance(first_obj,list_of_objects):#list_of_objects [['name',number,...,number],...]
    list_distanses=list()
    for i in range(len(list_of_objects)):   
        prom=0
        for k in range(1,len(list_of_objects[i])): #pass the name of element
            prom=prom+(first_obj[k]-list_of_objects[i][k])*(first_obj[k]-list_of_objects[i][k])
        list_distanses.append(sqrt(prom))
    return list_distanses
         
def min_index(list_):
    min_ind=0
    min_value=list_[0]
    for i in range(1,len(list_)):
        if min_value>list_[i]:
            min_value=list_[i]
            min_ind=i
    return min_ind

def create_list_of_classes(count_of_classes):
    list_of_classes=list()
    for i in range(count_of_classes):
        class_list=list()
        list_of_classes.append(class_list)
        list_of_classes[i].append("class_"+str(i))
    return list_of_classes
       
def calculating(count_of_classes=2):
    list_of_objects=list()#structure: [[name,item...item],[name,item...item]]
    read("data_test_2.csv",list_of_objects)
    list_of_classes=create_list_of_classes(count_of_classes)
    #list_of_classes[[class_1, object_index,...,object_index], ...,[[class_n, object_index,...,object_index]]]
    #object_index - index in list_of_objects
    
    count_of_variables=len(list_of_objects[1])
    #list_etalons=list_of_objects[0:count_of_classes]
    '''
    copying to avoid dublicating links 
    '''
    list_etalons=copy.deepcopy(list_of_objects)
    list_etalons=list_etalons[0:count_of_classes]
    '''
    list_etalons=list()
    for i in range(count_of_classes):
        list_etalons.append(list_of_objects[i])
    '''    
    etalon_weight=dict()
    for i in range(count_of_classes):
        etalon_weight[list_etalons[i][0]]=1#key: name of etalon, value: weight
        list_of_classes[i].append(i)
        
    #first iteration
    for j in range(len(list_of_objects)-len(list_etalons)):
        #j-step of first iteration
        list_distanses=distance(list_of_objects[count_of_classes+j],list_etalons) 
        min_distance_index=min_index(list_distanses)
    
        list_of_classes[min_distance_index].append(count_of_classes+j)
        '''
        object list_of_objects[count_of_classes+0] 
        need to be join to 
        list_etalons[min_distance_index] etalon.
        '''
        mdi=min_distance_index
        etalon_inter=list_etalons[mdi]
        weight=etalon_weight[list_etalons[mdi][0]]
        for i in range(1,count_of_variables):#counting vector E
            list_etalons[mdi][i]=(weight*
                                  etalon_inter[i]+
                                  list_of_objects[count_of_classes+j][i])/(weight+1)
    
        etalon_weight[list_etalons[mdi][0]]=etalon_weight[list_etalons[mdi][0]]+1 #increment weight
    
    #continuing iterations 
    list_of_classes_new=create_list_of_classes(count_of_classes)
    i=0
    while list_of_classes!=list_of_classes_new:
        if i>0:
            list_of_classes=copy.deepcopy(list_of_classes_new)    
            list_of_classes_new=create_list_of_classes(count_of_classes)
        i=i+1
        for j in range(len(list_of_objects)):
            list_distanses=distance(list_of_objects[j],list_etalons) 
            min_distance_index=min_index(list_distanses)
        
            list_of_classes_new[min_distance_index].append(j)
            mdi=min_distance_index
            weight=etalon_weight[list_etalons[mdi][0]]
            for i in range(1,count_of_variables):#counting vector E
                list_etalons[mdi][i]=(weight*
                                      list_etalons[mdi][i]+
                                      list_of_objects[j][i])/(weight+1.0)
        
            etalon_weight[list_etalons[mdi][0]]=etalon_weight[list_etalons[mdi][0]]+1 #increment weight
    
    #counting centers of mass:
    center_mass=list()
    for i in range(count_of_classes):
        list_=list()
        center_mass.append(list_)
        center_mass[i].append('#'+str(i))
        
    for i in range(len(list_of_classes)):#i-class
        for j in range(1,count_of_variables):#j-variable
            inter=0
            for k in range(1,len(list_of_classes[i])):#k-object in class
                inter=inter+list_of_objects[list_of_classes[i][k]][j]
            center_mass[i].append(inter/(len(list_of_classes[i])-1)) 
    
    #final clastering
    list_of_classes=create_list_of_classes(count_of_classes)
    for i in range(len(list_of_objects)):
        list_distanses = distance(list_of_objects[i], center_mass)
        mdi=min_index(list_distanses)
        list_of_classes[mdi].append(list_of_objects[i])
    
    return list_of_classes
