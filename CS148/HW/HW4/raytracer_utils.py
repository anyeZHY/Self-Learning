import numpy as np
from dataclasses import dataclass
from typing import List, Optional
#helper functions -- No need to change!

_DEFAULT_EPSILON=0.0001
def normalize(vector):
    return vector / np.linalg.norm(vector)

### CORE FUNCTIONALITY ###
@dataclass
class Ray:
    """Use this data structure to define the ray R(t)=A+Dt. 
    Keep track of number of recursive bounces with num_bounces"""
    origin:np.ndarray     =np.zeros(3)
    direction:np.ndarray  =np.zeros(3)
    num_bounces:int       =0

@dataclass
class Intersection:
    """Use this to access information about the ray-geometry intersection point. 
    if the ray intersects from within the object, the returned normal is flipped accordingly"""
    position: np.ndarray = np.zeros(3)
    normal: np.ndarray = np.zeros(3)
    uv: np.ndarray = np.zeros(2)
    from_inside_object: bool = False

@dataclass
class Light:
    """This defines a point light"""
    position: np.ndarray = np.zeros(3)
    color: np.ndarray = np.zeros(3)

@dataclass
class Material:
    """Superclass used to define materials"""
    attenuation_coeffs:np.ndarray=np.zeros(3)
    transmission:float =0.0
    reflectivity:float =0.0
    ior:float          =1.0
    def evaluate_brdf(self, incoming_ray, intersection, visible_lights):
        raise NotImplementedError 

class Geometry:
    """Superclass used to define geometry"""
    def __init__(self, material):
        self.material=material
    def get_material(self) -> Material:
        return self.material
    def get_intersection_t(self, ray) -> float:
        raise NotImplementedError
    def get_intersection_info(self,ray) -> Intersection:
        raise NotImplementedError     

@dataclass
class RayTraceSettings:
    """Settings to keep track of whether we enable recursion"""
    enable_reflection: bool = False
    enable_transmission: bool = False
    enable_shadow_attenuation: bool = False
    max_bounces: int = 8
    epsilon: float = _DEFAULT_EPSILON

### GEOMETRY SUBCLASSES ###
XZ_INDEX=[0,2]
Y_INDEX=1
class Cylinder(Geometry):
    def __init__(self, center:np.ndarray, radius:float, height:float, material:Material):
        super().__init__(material)
        self.xz=center[XZ_INDEX]
        self.y0=center[Y_INDEX]
        self.y1=self.y0+height        
        self.radius=radius

    def get_intersection_t(self, ray) -> Optional[float]:
        e=(ray.origin[XZ_INDEX]-self.xz)
        d=ray.direction[XZ_INDEX]

        a=np.linalg.norm(d)**2
        b=2*e.dot(d)
        c=np.linalg.norm(e)**2-self.radius**2
        k=b**2-4*a*c
        if k<0: return None
        
        y=ray.origin[Y_INDEX]
        dy=ray.direction[Y_INDEX]
        valid_t=[]

        #check caps:
        if abs(dy)>_DEFAULT_EPSILON:
            for height in [self.y0, self.y1]:
                t=(height-y)/dy
                if t>0 and np.linalg.norm(e+d*t)<self.radius:
                    valid_t.append(t)
        #check sides
        for t in [(-b-k**0.5)/(2*a),(-b+k**0.5)/(2*a)]:
            yt=y+dy*t
            if t>0 and yt>self.y0 and yt<self.y1:
                valid_t.append(t)
        if len(valid_t)==0:
            return None
        return min(valid_t)

    def get_intersection_info(self,ray,t) -> Intersection:
        intersect_position=ray.origin+t*ray.direction
        if abs(intersect_position[Y_INDEX]-self.y1)<_DEFAULT_EPSILON:
            intersect_normal=np.array([0,1,0])
        elif abs(intersect_position[Y_INDEX]-self.y0)<_DEFAULT_EPSILON:
            intersect_normal=np.array([0,-1,0])
        else:
            dxz=intersect_position[XZ_INDEX]-self.xz
            intersect_normal=normalize(np.array([dxz[0],0,dxz[1]]))
        from_inside_object=intersect_normal.dot(ray.direction)>0
        return Intersection(
            position=intersect_position,
            normal=intersect_normal,
            from_inside_object=from_inside_object)
    
class Plane(Geometry):
    def __init__(self, origin:np.ndarray, normal:np.ndarray, material:Material):
        super().__init__(material)
        self.origin=origin
        self.normal=normal
        tangent=np.array([normal[1],-normal[0], 0]) if normal[2]==0 else np.array([-normal[2],0, normal[0]])
        self.tangent1=normalize(tangent)
        self.tangent2=normalize(np.cross(normal,self.tangent1))
    def get_intersection_t(self, ray) -> Optional[float]:
        denom=self.normal.dot(ray.direction)
        if abs(denom)<_DEFAULT_EPSILON:
            return None
        t=(self.origin-ray.origin).dot(self.normal)/denom
        if t<0:
            return None
        return t
    def get_intersection_info(self,ray,t) -> Intersection:
        intersect_position=ray.origin+t*ray.direction
        intersect_normal=normalize(self.normal)
        uv=np.array([self.tangent1.dot(intersect_position-self.origin),self.tangent2.dot(intersect_position-self.origin)])
        from_inside_object=intersect_normal.dot(ray.direction)>0
        return Intersection(
            position=intersect_position,
            normal=intersect_normal,
            uv=uv,
            from_inside_object=from_inside_object)

### MATERIAL SUBCLASSES ###
@dataclass 
class DefaultMaterial(Material):
    ambient:np.ndarray =np.zeros(3)
    diffuse:np.ndarray =np.zeros(3)
    specular:np.ndarray=np.zeros(3)
    shininess:float    =100.0
    def evaluate_brdf(self, incoming_ray, intersection, visible_lights):
        color=np.copy(self.ambient)
        N=normalize(intersection.normal)
        V=normalize(incoming_ray.origin-intersection.position)
        for light in visible_lights:
            L=normalize(light.position-intersection.position)
            color += L.dot(N) * np.multiply(self.diffuse, light.color)
            color += (max(0, np.dot(N,normalize(L+V)))**self.shininess) * np.multiply(self.specular, light.color)
        return color

@dataclass 
class CheckeredMaterial(Material):
    ambient:np.ndarray =np.zeros(3)
    diffuse1:np.ndarray =np.zeros(3)
    diffuse2:np.ndarray =np.zeros(3)
    frequency:float=1.0
    def evaluate_brdf(self, incoming_ray, intersection, visible_lights):
        color=np.copy(self.ambient)
        N=normalize(intersection.normal)
        V=normalize(incoming_ray.origin-intersection.position)
        uv=(intersection.uv % self.frequency)/self.frequency > 0.5
        diffuse=self.diffuse1 if uv[0]==uv[1] else self.diffuse2
        for light in visible_lights:
            L=normalize(light.position-intersection.position)
            H=normalize(L+V)
            color += max(0,L.dot(N)) * np.multiply(diffuse, light.color)
        return color

def get_default_scene_objects() -> List[Geometry]:
    # our objects in the scene
    objects = [
       Cylinder(center=np.array([-1, -2, -8]),radius=0.8,height=4.0,
               material=DefaultMaterial(ambient=np.array([0.2, 0.1, 0]),
                        diffuse=np.array([0.8, 0.6, 0]),
                        specular=np.array([1,1,1]),
                        shininess=100)),
        Cylinder(center=np.array([0.15, -2, -6]),radius=1.2, height=3.0,
               material=DefaultMaterial(ambient=np.array([0.0, 0.1, 0.1]),
                        diffuse=np.array([0.4, 0.9, 0.4]),
                        specular=np.array([0.0,0.0,0.0]),
                        shininess=100,
                        transmission=0.7,
                        attenuation_coeffs=np.array([0.7,0.0,0.7]),
                        ior=0.85)),
        Cylinder(center=np.array([0.9, -2, -4]),radius=0.6,height=1.1,
               material=DefaultMaterial(ambient=np.array([0.1, 0.0, 0.2]),
                        diffuse=np.array([0.8, 0.0, 0.5]),
                        specular=np.array([1,1,1]),
                        shininess=100,
                        transmission=0.5,
                        attenuation_coeffs=np.array([0.0,1.0,0.7]),
                        ior=1.1)),
        #ground plane
        Plane(origin=np.array([0, -2.005, 0]),normal=normalize(np.array([0,1.0,0.0])),
            material=CheckeredMaterial(ambient=np.array([0.1, 0.1, 0.1]),
                        diffuse1=np.array([0.9, 0.9, 0.9]),
                        diffuse2=np.array([0.3,0.3,0.3]),
                        reflectivity=0.25,
                        frequency=2)),
        #back plane
        Plane(origin=np.array([0, 0., -30]),normal=normalize(np.array([0,0.0,1.0])),
                material=DefaultMaterial(ambient=np.array([0.0, 0.5, 0.9]),
                        diffuse=np.array([0.0, 0.0, 0.0]),
                        specular=np.array([0.,0.,0.]),
                        shininess=100,
                        transmission=0.0)),
    ]
    return objects

def get_default_scene_lights() -> List[Light]:
    # our lights in the scene
    lights = [
        Light(position=np.array([6, 2, -1]),color=np.array([0.4, 0.6, 0.5])),
        Light(position=np.array([8, 3, 2]),color=np.array([0.6, 0.4, 0.5])),
        Light(position=np.array([0, 1.5, 2]),color=np.array([0.2, 0.2, 0.2])),
    ]
    return lights