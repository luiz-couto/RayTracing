
#TEST PPM FILE

import glm
import math
from dataclasses import dataclass
import numpy as np
import random
MAXFLOAT = 3.4028234664e+38

class Ray:
    def __init__(self,a,b):
        self.a = glm.vec3(a)
        self.b = glm.vec3(b)
        self.origin = self.a
        self.direction = self.b
       
    def point_at_parameter(self,t):
        return self.a + t*self.b  

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
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything


class camera:
    def __init__(self):
        self.lower_left_corner = glm.vec3(-2.0,-1.0,-1.0)
        self.horizontal = glm.vec3(4.0,0.0,0.0)
        self.vertical = glm.vec3(0.0,2.0,0.0)
        self.origin = glm.vec3(0.0,0.0,0.0)
    def get_ray(self,u,v):
        return (Ray(self.origin,self.lower_left_corner + u*self.horizontal + v*self.vertical - self.origin))


def random_in_unit_sphere():
    p = 2.0*glm.vec3(random.uniform(0,0.999999999999999),random.uniform(0,0.999999999999999),random.uniform(0,0.999999999999999)) - glm.vec3(1.0,1.0,1.0)
    while(p[0]*p[0] + p[1]*p[1] + p[2]*p[2] >= 1.0):
        p = 2.0*glm.vec3(random.uniform(0,0.999999999999999),random.uniform(0,0.999999999999999),random.uniform(0,0.999999999999999)) - glm.vec3(1.0,1.0,1.0)
    return p


def color(r,world):
   
    rec = hit_record
    if(world.hit(r,0.001,MAXFLOAT,rec)):
        target = glm.vec3(rec.p + rec.normal + random_in_unit_sphere())
        return 0.5*color(Ray(rec.p,target - rec.p),world)
    else:
        unit_direction = glm.vec3(r.direction/glm.length(r.direction))
        t = 0.5*(unit_direction[1]+1)
        return (1.0 - t)*glm.vec3(1.0,1.0,1.0) + t*glm.vec3(0.5,0.7,1.0)



def main():

    nx = 200
    ny = 100
    ns = 100

    f = open("test.ppm","w+")
    f.write("P3\n"+ str(nx) +" "+ str(ny) + "\n255\n")
    
    

    _list = {}
    _list[0] = sphere(glm.vec3(0.0,0.0,-1),0.5)
    _list[1] = sphere(glm.vec3(0.0,-100.5,-1),100)
    world = hitable_list(_list,2)
    cam = camera()

    for j in range(ny-1,-1,-1):
        for i in range(0,nx,1):
            col = glm.vec3(0.0,0.0,0.0)
            for s in range(0,ns,1):
                u = float(i + random.uniform(0,0.999999999999999))/float(nx)
                v = float(j + random.uniform(0,0.999999999999999))/float(ny)
                r = cam.get_ray(u,v)
                p = glm.vec3(r.point_at_parameter(2.0))
                col = color(r,world) + col
            col = col/float(ns)
            col = glm.vec3(math.sqrt(col[0]),math.sqrt(col[1]),math.sqrt(col[2]))
            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])
            f.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")
   
main()