
#TEST PPM FILE

import glm
import math
from dataclasses import dataclass
import numpy as np
MAXFLOAT = 3.4028234664e+38

class Ray:
    def __init__(self,a,b):
        self.a = glm.vec3(a)
        self.b = glm.vec3(b)
        self.origin = self.a
        self.direction = self.b
       
    def point_at_parameter(self,t):
        return self.a + t*self.b  

#hit_record = namedtuple("hit_record","t p normal")
@dataclass
class hit_record:
    t: float
    p: glm.vec3
    normal: glm.vec3

class sphere:
    def __init__(self,cen,r):
        self.center = glm.vec3(cen)
        self.radius = r
    def hit(self,r,t_min,t_max,rec):
        oc = glm.vec3(r.origin - self.center)
        a = glm.dot(r.direction,r.direction)
        b = glm.dot(oc,r.direction)
        c = glm.dot(oc,oc) - self.radius*self.radius
        discriminant = b*b - a*c
        if(discriminant > 0):
            temp = (-b - math.sqrt(b*b-a*c))/a
            if(temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center)/self.radius
                return True
            temp = (-b + math.sqrt(b*b - a*c))/a
            if(temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center)/self.radius
                return True
        return False

class hitable_list:
    def __init__(self,l,n):
        self._list = l
        self.list_size = n
    def hit(self,r,t_min,t_max,rec):
        temp_rec = hit_record
        hit_anything = False
        closest_so_far = t_max
        for i in range(0,self.list_size,1):
            if(self._list[i].hit(r,t_min,closest_so_far,temp_rec)):
                print(self._list[i].hit(r,t_min,closest_so_far,temp_rec))
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything



# def hit_sphere(center,radius,r):
#     oc = glm.vec3(r.origin - center)
#     a = glm.dot(r.direction,r.direction)
#     b = 2.0*glm.dot(oc,r.direction)
#     c = glm.dot(oc,oc) - radius*radius
#     discriminant = b*b - 4*a*c
#     if(discriminant < 0):
#         return -1.0
#     if(discriminant >= 0):
#         return ((-b - math.sqrt(discriminant))/(2.0*a))

# def color(r):
    
#     t = hit_sphere(glm.vec3(0,0,-1),0.5,r)
    
#     if(t > 0.0):
#         n = glm.vec3(r.point_at_parameter(t) - glm.vec3(0,0,-1)/glm.length(r.point_at_parameter(t) - glm.vec3(0,0,-1)))
#         return 0.5*glm.vec3(n[0]+1.0,n[1]+1.0,n[2]+1.0)
#     unit_direction = glm.vec3(r.direction/glm.length(r.direction))
#     t = 0.5*(unit_direction[1] + 1.0)
#     return (1.0 - t)*glm.vec3(1.0,1.0,1.0) + t*glm.vec3(0.5,0.7,1.0)

def color(r,world):
   
    rec = hit_record
    if(world.hit(r,0.0,MAXFLOAT,rec)):
        return 0.5*glm.vec3(rec.normal[0]+1,rec.normal[1]+1,rec.normal[2]+1)
    else:
        unit_direction = glm.vec3(r.direction/glm.length(r.direction))
        t = 0.5*(unit_direction[1]+1)
        return (1.0 - t)*glm.vec3(1.0,1.0,1.0) + t*glm.vec3(0.5,0.7,1.0)


def main():

    nx = 200
    ny = 100

    f = open("test.ppm","w+")
    f.write("P3\n"+ str(nx) +" "+ str(ny) + "\n255\n")
    
    lower_left_corner = glm.vec3(-2.0,-1.0,-1.0)
    horizontal = glm.vec3(4.0,0.0,0.0)
    vertical = glm.vec3(0.0,2.0,0.0)
    origin = glm.vec3(0.0,0.0,0.0)

    _list = {}
    _list[0] = sphere(glm.vec3(0.0,0.0,-1),0.5)
    _list[1] = sphere(glm.vec3(0.0,-100.5,-1),100)
    world = hitable_list(_list,2)

    for j in range(99,-1,-1):
        for i in range(0,200,1):
            u = i/nx
            v = j/ny
            r = Ray(origin,lower_left_corner + u*horizontal + v*vertical)
            #col = glm.vec3(color(r))
            p = glm.vec3(r.point_at_parameter(2.0))
            col = color(r,world)
            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])
            f.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")
   
main()