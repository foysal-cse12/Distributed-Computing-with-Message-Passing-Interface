# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 18:42:52 2019

@author: foysal
"""

from mpi4py import MPI
import numpy as np
import time
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
comm.barrier()

def split_vector(v,n_splits):       #splitting the vector function
    vec= v
    ##print("vector is:",vec)
    split_vec=np.array_split(vec,n_splits)
    return split_vec


size_vector=5
print("rank :", rank, " size:",size)
if rank==0:
    time_start=MPI.Wtime()          #start time

    v1=np.random.randint(9,size=(size_vector,size_vector))
    v2=np.random.randint(9,size=(size_vector,1))
    print("v1 (matrix) : ",v1)
    print("v2: ",v2)
    vec2=split_vector(v2[:,[0]],size)
    print("vec2 after spliting (1st coloumn)",vec2)              #splitting the second vector(10,1)

    v3=np.random.randint(9,size=(size_vector,1))    #result vector
    #print("original vector",np.dot(v1,v2))
    for row in range(size_vector):
        vec1=split_vector(v1[row],size)
        #print("vec1 row", row , " ",vec1)
        
        print("vec1 row ", row ," is ",vec1)

        vec3=0
        vec3=vec3+np.dot(vec1[0],vec2[0]) # #dot product of one splitting part of vectors
        print("1st sum",vec3)
        for i in range(1,size):
            # sending splitting part of matrix and vector
            print ("sending v1: ",vec1[i])
            print ("sending v2: ",vec2[i])
            comm.send(vec1[i],dest=i)
            comm.send(vec2[i],dest=i)

            receivedData = comm.recv(source=i)
            vec3=vec3 + receivedData
            print("i is:",i)
            print("sum add 0",vec3,"from",i)

        print("vec 3 sum is:",vec3)
        v3[row]=vec3


    print("final vector v3",v3)
    print("original vector",np.dot(v1,v2))
    time_end=MPI.Wtime()
    print("Time taken",(time_end-time_start))



else:
    for row in range(size_vector):
        data1=comm.recv(source=0)
        data2=comm.recv(source=0)
        comm.send(np.dot(data1,data2),dest=0)
        print("data sent to 0 from rank ",rank ,"is", np.dot(data1,data2) ,"where data1: ",data1,"data2: ",data2)

print(MPI.Wtime())
comm.barrier()


