from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from raytracer_utils import *

reference_rays={
 "r":Ray(origin=np.array([0.02236068, 1.95527864, 0]), 
                  direction=np.array([ 0.8, -0.6,  0. ]), 
                  num_bounces=1),
 "t1":Ray(origin=np.array([-0.02236068,  2.04472136,  0.]), 
                  direction=np.array([0.26790212, 0.96344613, 0.]), 
                  num_bounces=1),
 "t2":Ray(origin=np.array([0.20505284, 2.98769612, 0.]), 
              direction=np.array([0., 1., 0.]), 
              num_bounces=2)
}

def load_transmission_test_objects():
    ray=Ray(origin=np.array([0,1,0]),direction=np.array([0,1,0]),num_bounces=0)
    obj1=Plane(origin=np.array([0,2,0]),normal=normalize(np.array([0.5,-1,0])),material=Material(ior=0.667))  
    obj2=Plane(origin=np.array([0.2682928, 2.9634144, 0.]),normal=normalize(np.array([-0.5,1,0])),material=Material(ior=0.667)) 
    return ray,obj1,obj2

def plot_rays(lines,rays,xlim=[-1.5,1.5],ylim=[0.8,3.8],scale=2,name=""):
    for line in lines:
        plt.plot(line[0],line[1])
    c=cm.rainbow(np.arange(len(rays))/float(len(rays)))
    for i,(ray,label) in enumerate(rays):
        plt.arrow(ray.origin[0],ray.origin[1],ray.direction[0],ray.direction[1],
                  width=0.02,length_includes_head=True,color=c[i],edgecolor=None,label=label)
    plt.xlim(xlim[0],xlim[1])
    plt.ylim(ylim[0],ylim[1])
    plt.gcf().set_size_inches(scale*(xlim[1]-xlim[0]),scale*(ylim[1]-ylim[0]))
    plt.legend()
    plt.title(name)
    plt.show()