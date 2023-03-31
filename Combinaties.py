# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:27:47 2023

@author: Thoma
"""
import pandas as pd
locations=['Rotterdam','New York','Sao Paolo','Mexico stad','Kaapstad']
vessels=['Vessel1']#,'vessel2']
Current_location_vessel=['Rotterdam']#,'New York']
Snelheid= 25 #13.5=25 km/h
pick_up_time=[3,200,600,30,100]

days_to_travel = [[0,20,40,25,45],
                  [20,0,15,10,30],
                  [40,15,0,15,20],
                  [25,10,15,0,25],
                  [45,30,20,25,0]]

# df_vessel,df_cargo
df_travel = pd.DataFrame(days_to_travel)
df_travel.columns = locations
df_travel['Location'] = locations
df_travel.set_index('Location',inplace=True)



# A Python program to print all
# permutations using library function
from itertools import permutations


def combinations(locations,Current_location_vessel):
    Combinations_vessel_list=list()
    for location in range(2,len(locations)+1):
        Combination=list(permutations(locations,location))
        Combinations_vessel=[ i for i in Combination if i[0]==Current_location_vessel]
        [Combinations_vessel_list.append(list(i)) for i in Combinations_vessel]
    return Combinations_vessel_list
    
def feasible(combination,df_travel,pick_up_time):
    Arrival_day=[0]
    # print(combination)
    for position in range(len(combination)):
        if position+1<len(combination):
            distance=df_travel[combination[position]][combination[position+1]]
            time_arrival=Arrival_day[-1]+distance
            Arrival_day.append(time_arrival)
    
    Unfeasible=False
    for i,j in zip(Arrival_day,combination):
        if Unfeasible==False:
            loc=locations.index(j)
            if i>pick_up_time[loc]:
                Unfeasible=True
  
    if Unfeasible==False: 
        return combination,Arrival_day

    
for vessel in range(len(vessels)):
    combo=combinations(locations,Current_location_vessel[vessel])
    Feasible_combinations=[feasible(i,df_travel,pick_up_time) for i in combo]
    for i in Feasible_combinations:
        if i !=None:
            print(i[0])
    
        
    