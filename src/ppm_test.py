
#TEST PPM FILE

def main():

    nx = 200
    ny = 100

    f = open("test.ppm","w+")
    f.write("P3\n"+ str(nx) +" "+ str(ny) + "\n255\n")
    for j in range(99,-1,-1):
        for i in range(0,200,1):
            r = i/nx
            g = j/ny
            b = 0.2
            ir = int(255.99*r)
            ig = int(255.99*g)
            ib = int(255.99*b)
            f.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")

main()