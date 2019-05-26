import numpy as np 
import matplotlib.pyplot as plt 
import math

#To find Internal stress around dislocation due to surrounding disloactions 
def get_internal_stress(x_coords,shear_modulus,poissons_ratio,burgers_vector):
    d=shear_modulus*burgers_vector/(2*np.pi*(1-poissons_ratio))
    stress=np.array([])
    swap=0
    for j in range(len(x_coords)):
        stress_final=0
        # Use swapping teqnique to find distance between dislocations
        swap=x_coords[j]
        x_coords[j]=x_coords[0]
        x_coords[0]=swap
        for i in range(len(x_coords)-1): #Its is length minus one due to distance calculation is between two points
            stress_iteration=d/(x_coords[0]-x_coords[i+1])
            stress_final=stress_final+stress_iteration
        stress=np.append(stress,stress_final)
    return stress

##Delete below lines

print(get_internal_stress(np.array([0,2,3.5,4]),20.,0.3,0.1))