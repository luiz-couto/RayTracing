
#TEST PPM FILE

import glm
import math


class Ray:
    def __init__(self,a,b):
        self.a = glm.vec3(a)
        self.b = glm.vec3(b)
        self.origin = self.a
        self.direction = self.b
       
    def point_at_parameter(self,t):
        return self.a + t*self.b  

def hit_sphere(center,radius,r):
    oc = glm.vec3(r.origin - center)
    a = glm.dot(r.direction,r.direction)
    b = 2.0*glm.dot(oc,r.direction)
    c = glm.dot(oc,oc) - radius*radius
    discriminant = b*b - 4*a*c
    if(discriminant < 0):
        return -1.0
    if(discriminant >= 0):
        return ((-b - math.sqrt(discriminant))/(2.0*a))

def color(r):
    
    t = hit_sphere(glm.vec3(0,0,-1),0.5,r)
    
    if(t > 0.0):
        n = glm.vec3(r.point_at_parameter(t) - glm.vec3(0,0,-1)/glm.length(r.point_at_parameter(t) - glm.vec3(0,0,-1)))
        return 0.5*glm.vec3(n[0]+1.0,n[1]+1.0,n[2]+1.0)
    unit_direction = glm.vec3(r.direction/glm.length(r.direction))
    t = 0.5*(unit_direction[1] + 1.0)
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

    for j in range(99,-1,-1):
        for i in range(0,200,1):
            u = i/nx
            v = j/ny
            r = Ray(origin,lower_left_corner + u*horizontal + v*vertical)
            col = glm.vec3(color(r))

            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])
            f.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")
   
main()