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

#To find velocity as position changes
def velocity(burgers_vector,drag_coefficient,shear_stress,t_ext):
    velocitys=np.array([])
    for i in range(len(shear_stress)):
        velocity =(burgers_vector/drag_coefficient)*(shear_stress[i]+t_ext)
        velocitys=np.append(velocitys,velocity)
    return velocitys

#Function to plot positions of two dislocations with 
def plot_trajectories(times,positions):
    positions_plot=np.around(positions,11)
    plt.xlabel(r'Position of Dislocation [$\mu$m]')
    plt.ylabel('time[ns]')
    plt.title('trajectory of dislocations $(t_{0}:circles,t_{end}:diamonds)$')
    positions_scaled=positions/1e-6         #positions scaled by e-6
    times_scaled=times/1e-9                 #times scaled by e-9
    plt.plot(positions_scaled[0:],times_scaled[0:],'b--',positions_scaled[0:1],times_scaled[0:1],'bo',positions_scaled[-1:],times_scaled[-1:],'yD')
    plt.savefig('Task_5a_img.png')

# System_Definition
system_length_x= 2e-6                                   #m
shear_modulus= 26e9                                     #Pa
poissons_ratio=0.33
burgers_vector=0.256e-9                                 #m
drag_coefficient=1e-4                                   #Pa-s
total_time=30e-9                                        #s
delta_t=10e-11                                          #s
number_steps=total_time/delta_t

#Initial_Values
length= 2e-6                                             #m
n_dislocations=4
initial_position=length*np.array([0.1,0.13,0.16,0.3])    #x-co-ordinates
tau_external=-25000000                                    # External force

#variables initialization for plotting purpose
final_position=np.array([])
vel=np.array([])
final_position=initial_position                          #for loop initiating purpose
positions=np.array([initial_position])
times=np.array([0])
vels=np.zeros([1,len(initial_position)])


#Loop to calculate final positions with time

for i in range(math.ceil(number_steps)):
    shear_stress=get_internal_stress(np.copy(final_position),shear_modulus,poissons_ratio,burgers_vector)
        #Here np.copy is used for call by value purpose in order to prevent function modifying outside variable
        #In internl stress calculation function my initial positions get swapped according to requirement.
    vel=velocity(burgers_vector,drag_coefficient,shear_stress,tau_external)
    #vels=np.append(vels,[vel],axis=0)
    final_position=final_position+delta_t*vel
    for j in range(len(initial_position)):
        if final_position[j]<=0:
            final_position[j]=0
            vel[j]=0
    vels=np.append(vels,[vel],axis=0)
    positions=np.append(positions,[final_position],axis=0)
    times=np.append(times,[(i+1)*delta_t],axis=0)


#Below velocity function is carried out in order to capture velocity at end of simulation
vel=velocity(burgers_vector,drag_coefficient,shear_stress,tau_external)
for j in range(len(initial_position)):
        if final_position[j]<=0:
            final_position[j]=0
            vel[j]=0
vels=np.append(vels,[vel],axis=0)

vels_actual=vels[1:]  #Because my first list is zeros which is just taken to initiate my velocity array


# Calling plot function for plotting purpose
plotting=plot_trajectories(times,positions)



