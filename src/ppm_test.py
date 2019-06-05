
#TEST PPM FILE

import glm
import math
from dataclasses import dataclass
import numpy as np
import random

MAXFLOAT = 3.4028234664e+38
M_PI = 3.14159265358979323846264338327950288

class Ray:
    def __init__(self,a,b):
        self.a = glm.vec3(a)
        self.b = glm.vec3(b)
        self.origin = self.a
        self.direction = self.b
       
    def point_at_parameter(self,t):
        return self.a + t*self.b  



class sphere:
    def __init__(self,cen,r,material):
        self.center = glm.vec3(cen)
        self.radius = r
        self.material = material
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
                rec.mat_ptr = self.material
                return True
            temp = (-b + math.sqrt(b*b - a*c))/a
            if(temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center)/self.radius
                rec.mat_ptr = self.material
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
    def __init__(self, lookfrom, lookat, vup, vfov, aspect):
        self.theta = vfov*M_PI/180
        self.half_height = math.tan(self.theta/2)
        self.half_width = aspect * self.half_height
        self.origin = lookfrom
        self.w = glm.vec3((lookfrom - lookat)/(glm.length(lookfrom - lookat)))
        self.u = glm.vec3(glm.cross(vup,self.w)/glm.length(glm.cross(vup,self.w)))
        self.v = glm.cross(self.w,self.u)
        self.lower_left_corner = glm.vec3(-self.half_width,-self.half_height, -1.0)
        self.lower_left_corner = self.origin - self.half_width*self.u - self.half_height*self.v - self.w
        self.horizontal = 2*self.half_width*self.u
        self.vertical = 2*self.half_height*self.v
    def get_ray(self,s,t):
        return(Ray(self.origin,self.lower_left_corner + s*self.horizontal + t*self.vertical - self.origin))

class camera_blur:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
        self.lens_radius = aperture/2
        self.theta = vfov*M_PI/180
        self.half_height = math.tan(self.theta/2)
        self.half_width = aspect * self.half_height
        self.origin = lookfrom
        self.w = glm.vec3((lookfrom - lookat)/(glm.length(lookfrom - lookat)))
        self.u = glm.vec3(glm.cross(vup,self.w)/glm.length(glm.cross(vup,self.w)))
        self.v = glm.cross(self.w,self.u)
        
        self.lower_left_corner = self.origin - self.half_width*focus_dist*self.u - self.half_height*focus_dist*self.v - focus_dist*self.w
        self.horizontal = 2*self.half_width*focus_dist*self.u
        self.vertical = 2*self.half_height*focus_dist*self.v
    def get_ray(self,s,t):
        rd = glm.vec3(self.lens_radius*random_in_unit_disk())
        offset = self.u*rd[0] + self.v*rd[1]
        return(Ray(self.origin + offset,self.lower_left_corner + s*self.horizontal + t*self.vertical - self.origin - offset))


class lambertian:
    def __init__(self,a):
        self.albedo = glm.vec3(a)
    def scatter(self,r_in,rec,attenuation,scattered):
        target = glm.vec3(rec.p + rec.normal + random_in_unit_sphere())
        scattered = Ray(rec.p, target - rec.p)
        attenuation = self.albedo
        return (True,scattered,attenuation)

class metal:
    def __init__(self,a,f):
        self.albedo = a
        if(f < 1):
            self.fuzz = f
        else:
            self.fuzz = 1    
    def scatter(self,r_in,rec,attenuation,scattered):
        reflected = glm.vec3(reflect(r_in.direction/glm.length(r_in.direction),rec.normal))
        scattered = Ray(rec.p, reflected + self.fuzz*random_in_unit_sphere())
        attenuation = self.albedo
        return(glm.dot(scattered.direction, rec.normal) > 0,scattered,attenuation)

class dielectric:
    def __init__(self,ri):
        self.ref_idx = ri
    def scatter(self,r_in,rec,attenuation,scattered):
        outward_normal = glm.vec3
        reflected = glm.vec3(reflect(r_in.direction, rec.normal))
        attenuation = glm.vec3(1.0,1.0,1.0)
        refracted = glm.vec3
        if(glm.dot(r_in.direction, rec.normal) > 0):
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0/self.ref_idx
        x,refracted = refract(r_in.direction,outward_normal,ni_over_nt,refracted)
        if(x == True):
            scattered = Ray(rec.p, refracted)
        else:
            scattered = Ray(rec.p, reflected)
            return (False,scattered,attenuation)
        return (True,scattered,attenuation)

class dielectric:
    def __init__(self,ri):
        self.ref_idx = ri
    def scatter(self,r_in,rec,attenuation,scattered):
        outward_normal = glm.vec3
        reflected = glm.vec3(reflect(r_in.direction, rec.normal))
        attenuation = glm.vec3(1.0,1.0,1.0)
        refracted = glm.vec3
        if(glm.dot(r_in.direction, rec.normal) > 0):
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * glm.dot(r_in.direction,rec.normal) / glm.length(r_in.direction)
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0/self.ref_idx
            cosine = -glm.dot(r_in.direction,rec.normal) / glm.length(r_in.direction)
       
        x,refracted = refract(r_in.direction,outward_normal,ni_over_nt,refracted)
        if(x == True):
            reflect_prob = schlick(cosine, self.ref_idx)
        else:
            scattered = Ray(rec.p, reflected)
            reflect_prob = 1.0
        if(ran() < reflect_prob):
            scattered = Ray(rec.p, reflected)
        else:
            scattered = Ray(rec.p, refracted)
        return (True,scattered,attenuation)



@dataclass
class hit_record:
    t: float
    p: glm.vec3
    normal: glm.vec3
    mat_ptr: lambertian    #can be any material

def random_in_unit_disk():
    p = 2.0*glm.vec3(ran(),ran(),0.0) - glm.vec3(1.0,1.0,0.0)
    while(glm.dot(p,p) >= 1.0):
        p = 2.0*glm.vec3(ran(),ran(),0.0) - glm.vec3(1.0,1.0,0.0)
    return p



def reflect(v,n):
    return (v - 2*glm.dot(v,n)*n)

def refract(v,n,ni_over_nt,refracted):
    uv = glm.vec3(v/glm.length(v))
    dt = glm.dot(uv, n)
    discriminant = 1.0 - ni_over_nt*ni_over_nt*(1-dt*dt)
    if(discriminant > 0):
        refracted = ni_over_nt*(uv - n*dt) - n*math.sqrt(discriminant)
        return (True,refracted)
    else:
        refracted = glm.vec3
        return (False,refracted)

def schlick(cosine,ref_idx):
    r0 = (1-ref_idx) / (1+ref_idx)
    r0 = r0*r0
    return r0 + (1-r0)*math.pow((1-cosine),5)

def random_in_unit_sphere():
    p = 2.0*glm.vec3(ran(),ran(),ran()) - glm.vec3(1.0,1.0,1.0)
    while(p[0]*p[0] + p[1]*p[1] + p[2]*p[2] >= 1.0):
        p = 2.0*glm.vec3(ran(),ran(),ran()) - glm.vec3(1.0,1.0,1.0)
    return p


def color(r,world,depth):
    rec = hit_record
    if(world.hit(r,0.001,MAXFLOAT,rec)):

        attenuation = glm.vec3 
        scattered = Ray 
        x,scattered,attenuation = (rec.mat_ptr.scatter(r,rec,attenuation,scattered))
        
        if(depth < 50 and x == True):
            return attenuation*color(scattered,world,depth+1)
        else:
            return glm.vec3(0.0,0.0,0.0)
    else:
        unit_direction = glm.vec3(r.direction/glm.length(r.direction))
        t = 0.5*(unit_direction[1]+1)
        return (1.0 - t)*glm.vec3(1.0,1.0,1.0) + t*glm.vec3(0.5,0.7,1.0)

def ran():
    return random.uniform(0,0.999999999999999)


def random_scene():
    
    _list = {}
    _list[0] = sphere(glm.vec3(0.0,-1000.0,0.0),1000,lambertian(glm.vec3(0.5,0.5,0.5)))
    i = 1
    for a in range(-11,11,1):
        for b in range(-11,11,1):
            choose_mat = ran()
            center = glm.vec3(a+0.9*ran(),0.2,b+0.9*ran())
            if(glm.length(center - glm.vec3(4.0,0.2,0.0)) > 0.9):
                if(choose_mat < 0.5):
                    _list[i] = sphere(center,0.2,lambertian(glm.vec3(ran()*ran(),ran()*ran(),ran()*ran())))
                    i = i+1
                if(choose_mat >= 0.5 and choose_mat < 0.8):
                    _list[i] = sphere(center,0.2,metal(glm.vec3(0.5*(1 + ran()),0.5*(1 + ran()),0.5*(1 + ran())), 0.5*(1 + ran())))
                    i = i+1
                if(choose_mat >= 0.8):
                    _list[i] = sphere(center,0.2,dielectric(1.5))
                    i + i+1
   
    _list[i] = sphere(glm.vec3(0.0,1.0,0.0),1.0,dielectric(1.5))
    i = i + 1
    _list[i] = sphere(glm.vec3(-4.0,1.0,0.0),1.0,lambertian(glm.vec3(0.4,0.2,0.1)))
    i = i + 1
    _list[i] = sphere(glm.vec3(4.0,1.0,0.0),1.0,metal(glm.vec3(0.7,0.6,0.5),0.0))
    i = i + 1

    return (_list,i)

def main():

    nx = 200
    ny = 100
    ns = 100

    f = open("test.ppm","w+")
    f.write("P3\n"+ str(nx) +" "+ str(ny) + "\n255\n")
    
    _list,i = random_scene()

    # _list = {}
    # # _list[0] = sphere(glm.vec3(0.0,0.0,-1),0.5,lambertian(glm.vec3(0.1,0.2,0.5)))
    # #_list[0] = sphere(glm.vec3(0.0,-1000.0,0.0),1000,lambertian(glm.vec3(0.5,0.5,0.5)))
    # _list[0] = sphere(glm.vec3(0.0,-100.5,-1),100,lambertian(glm.vec3(0.117,0.223,0.141)))
    # # _list[2] = sphere(glm.vec3(1.0,0.0,-1.0),0.5,metal(glm.vec3(0.8,0.6,0.2),0.3))
    # _list[1] = sphere(glm.vec3(0.5,0.865,-1.0),0.5,dielectric(1.5))
    # _list[2] = sphere(glm.vec3(0.5,0.865,-1.0),-0.45,dielectric(1.5))
    # _list[3] = sphere(glm.vec3(1.0,0.0,-1.0),0.5,dielectric(1.5))
    # _list[4] = sphere(glm.vec3(1.0,0.0,-1.0),-0.45,dielectric(1.5))
    # _list[5] = sphere(glm.vec3(0.0,0.0,-1.0),0.5,dielectric(1.5))
    # _list[6] = sphere(glm.vec3(0.0,0.0,-1.0),-0.45,dielectric(1.5))
    world = hitable_list(_list,i)
    
    
    

    lookfrom = glm.vec3(13.0,2.0,3.0)
    #lookfrom = glm.vec3(3.4,1.0,1.5) 
    lookat = glm.vec3(0.0,0.0,0.0)
    #lookat = glm.vec3(0.0,0.0,-1.0)
    dist_to_focus = 10.0
    aperture = 0.1

    #cam = camera(glm.vec3(3.4,1.0,1.5), glm.vec3(0.0,0.0,-1.0), glm.vec3(0.0,1.0,0.0), 40, float(nx)/float(ny))
    cam = camera_blur(lookfrom,lookat,glm.vec3(0.0,1.0,0.0),20,float(nx)/float(ny),aperture,dist_to_focus)


    for j in range(ny-1,-1,-1):
        for i in range(0,nx,1):
            col = glm.vec3(0.0,0.0,0.0)
            for s in range(0,ns,1):
                u = float(i + ran())/float(nx)
                v = float(j + ran())/float(ny)
                r = cam.get_ray(u,v)
                p = glm.vec3(r.point_at_parameter(2.0))
                col = color(r,world,0) + col
            col = col/float(ns)
            col = glm.vec3(math.sqrt(col[0]),math.sqrt(col[1]),math.sqrt(col[2]))
            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])
            f.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")
   
main()