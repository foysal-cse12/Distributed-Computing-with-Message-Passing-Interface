# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 23:43:53 2019

@author: foysal
"""

from mpi4py import MPI
import numpy as np
import time
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
number_of_processes = comm.Get_size()
print("number of process is :", number_of_processes)
comm.barrier()

def split_vector(v,n_splits):
    vec= v
    print("vector is:",vec)
    split_vec=np.array_split(vec,n_splits)
    return split_vec

print("rank :", rank, " size:",size)
vector_size=5
if rank==0:

    v1=np.random.randint(9,size=(vector_size,vector_size))
    v2=np.random.randint(9,size=(vector_size,vector_size))
    time_start=MPI.Wtime()
    print("v1 (matrix A): ",v1)
    print("v2 (matrix B): ",v2)
    v3=np.random.randint(9,size=(vector_size,vector_size))

split_row=None
split_col=None
for row in range(vector_size):

    for col in range(vector_size):

        if rank==0:
            split_row=split_vector(v1[row,:],size)      #splitting all the rows
            split_col=split_vector(v2[:,[col]],size)    ##splitting all the columns
            print ("split row..: ",split_row)
            print ("split column..: ",split_col)

        row_scatter=comm.scatter(split_row,0)           #scattering rows and columns
        col_scatter=comm.scatter(split_col,0)
        print ("row_scatter..: ",row_scatter)
        print ("col_scatter..: ",col_scatter)

        dotproduct = np.dot(row_scatter, col_scatter)
        print ("dotproduct..: ",dotproduct)
        gathered_result = comm.gather(dotproduct, 0)    #gathering rows and columns
        print ("gathered_result..: ",gathered_result)

        if rank == 0:
            v3[row][col] = np.sum(gathered_result)
            #print ("v3[row][col]..: ",v3[row][col])
            print ("v3[row: ", row, "][col: ", col, "]..: ",v3[row][col])


if rank == 0:
    print("1st matrix:",v1)
    print("2nd matrix :",v2)
    print("3rd matrix :",v3)
    time_end = MPI.Wtime()
    t_diff = time_end - time_start
    print("Time taken = \n" ,t_diff)
