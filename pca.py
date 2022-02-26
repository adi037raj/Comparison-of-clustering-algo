import numpy as np
import matplotlib.pyplot as plt
def read_file():               # Reading the data from the file
    
    fileptr = open("movement_libras.txt",'r')        # file is movement libreas
    Complete = fileptr.readlines()
    total_row=0
    total_data=[]
    total_colums = len(Complete[0].split(','))-1 # as last i is class 
    for elements in Complete:
        total_row+=1
        elements = elements.split(',')
        if elements:
            elements = [float(i) for i in elements]
            total_data.append(elements[:-1])
    
    return total_colums,total_row,total_data                  # returning the total attributes,instances and data 

def calculate_the_mean_matrix(total_colums,total_data,total_row):         # for calculating the mean matrix
    mean_attributes = []
    for i in range(total_colums):
        attributes = []
        for row in total_data:
            attributes.append(row[i])
       
        mean_attributes.append(np.mean(attributes))
    
    mean_attributes=np.array([np.array(mean_attributes),]*total_row).transpose()           #transposing the mean matrix to get the mean value of each columns
    return mean_attributes


def sort_everythin(eigen_values,eigen_vectors):
    i = np.argsort(eigen_values)[::-1]                               # getting sorted  the eigen values index in reverse direction
                                   
    eigen_vectorsorted = eigen_vectors[:, i]
    return eigen_vectorsorted    
if __name__ == "__main__":

    total_colums,total_row,total_data=read_file()
    
    data_transpose = np.transpose(np.array(total_data))
    
    Mean_Matrix=calculate_the_mean_matrix(total_colums,total_data,total_row)  
    
    Meaned_data = (data_transpose - Mean_Matrix)               
    # the Z(centred value) Matrix
    cov_matrix = np.cov(Meaned_data)
    print("covariance matrix",cov_matrix)    
    eigen_values, eigen_vectors = np.linalg.eig(cov_matrix)
   
    print("Eigenvalues are ",eigen_values)
    
    print("Eigenvectors",eigen_vectors)
    reduced_dim=5                                                                    # dimension reduction component
                        # same with eigen vectors
    
    eigenvector_subset = sort_everythin(eigen_values, eigen_vectors)[:, 0:reduced_dim]                      # calculating the subset from d to r dimension
    dim_reduced = np.dot(eigenvector_subset.transpose(), Meaned_data).transpose()           # calculating the reduced dimension

    print("Data reduction ",dim_reduced)
    
    plt.plot(dim_reduced[:,0:3])
    plt.legend(['dim 1', 'dim2','dim3'])
    plt.show()
   