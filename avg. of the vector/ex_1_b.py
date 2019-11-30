# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 22:59:27 2019

@author: foysal
"""

from mpi4py import MPI
import numpy as np
import time
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
comm.barrier()

def split_vector(size_vector,n_splits):       #function to split vector
    vec= np.random.randint(9,size=size_vector)
    print("vector is:",vec)
    split_vec=np.array_split(vec,n_splits)
    return split_vec

print("rank",rank,"size",size)
size_vector=10
if rank==0:
    time_start=MPI.Wtime()          #start time
    vec1=split_vector(size_vector,size)
    #print("vector :",vec1)
    for i in range(size):
        print("vector :",vec1[i]) # print each split part of vec1

    vec3=np.random.rand(size)
    #print('new vector: ',vec3)
    #print(vec3)
    vec3[0]=np.mean(vec1[0])        #Mean of one part of vector
    print("mean vec1 (one splitting part):",vec3[0])
    #print("vec 0 is:",vec3[0])
    for i in range(1,size):

        comm.send(vec1[i],dest=i)   #send it to other processes
        receivedData = comm.recv(source=i)

        vec3[i]=receivedData

        print("Data received to 0",vec3[i],"from",i)


    final_sum=0
    #print ('length of vector 3: ', len(vec3))
    for i in range(len(vec3)):      #averaging of all the vector chunks
        final_sum=final_sum + vec3[i]

    final_average=final_sum/size
    print("final average:",final_average)
    time_end=MPI.Wtime()
    print("Time taken",(time_end-time_start))



else:
    data1=comm.recv(source=0)

    print("data: ",data1)
    print("data recieved is ",data1,"from ",rank)

    comm.send(np.mean(data1),dest=0)
    print("data sent to",rank ,"is", np.mean(data1))

print(MPI.Wtime())
comm.barrier()

