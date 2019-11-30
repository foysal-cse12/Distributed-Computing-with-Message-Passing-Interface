# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 18:20:27 2019

@author: foysal
"""

from mpi4py import MPI
import numpy as np
import time
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
comm.barrier()

def split_vector(vector,n_splits):
    split_vec=np.array_split(vector,n_splits)
    return split_vec


size_vector=10                #size of vector
print("rank",rank,"size",size)
if rank==0:
    time_start=MPI.Wtime()          #start time
    #print ('start time : ',time_start)

    vector_1=np.random.randint(9,size=size_vector)  #initialize vector
    vector_2=np.random.randint(9,size=size_vector)
    vector_3=np.random.randint(9,size=size_vector)

    print("vector 1",vector_1)
    print("vector_2",vector_2)
    #print("vector_3",vector_3)
    #print ('split size: ',size)
    vec1=split_vector(vector_1,size)            #splitting the vector
    print ("after split vec1: ",vec1)

    vec2=split_vector(vector_2,size)
    print ("after split vec2: ",vec2)


    vec3=split_vector(vector_3,size)
    print ("after split vec3: ",vec3)
    #vec3=vec1+vec2
    vec3[0]=vec1[0]+vec2[0]
    print ("after addition v1 and v2: ",vec3)

    for i in range(1,size):

        comm.send(vec1[i],dest=i)
        comm.send(vec2[i],dest=i)

        receivedData = comm.recv(source=i)      #receiving data back from child nodes

        vec3[i]=receivedData

        print("Data received to 0",vec3[i],"from",i)


    print("final vector",vec3)
    time_end=MPI.Wtime()
    print ("start time : ",time_start)
    print ("end time : ",time_end)
    print("Time taken: ",(time_end-time_start))



else:
    data1=comm.recv(source=0)
    data2=comm.recv(source=0)

    print("data received are:",data1,data2,"from",rank)
    t3=[]
    for i in range(len(data1)):
        t3.append(data1[i]+data2[i])

    comm.send(t3,dest=0)
    print("data sent to",rank ,"is", t3)

print(MPI.Wtime())
comm.barrier()