import math

def inverseMod(base,exponent,prime): #finds the inverse of a mod
    for i in range(0,prime):
        if (i*(base**exponent))%prime == 1:
            return i

def func1():
    a = float(input("Enter x coord: "))
    b = float(input("Enter y coord: "))
    pointOld = [1980.0,431.0] #point P must be floating point to work
    point = [pointOld[0],pointOld[1]]
    A = int(input("Enter number A: ")) #from y^2 = x^3 + A*x + B
    p = int(input("Enter prime p: ")) #prime
    n = int(input("Enter number of multiplications: "))
    for i in range(1,n):#number of multiplications equals the second number in range
        if (pointOld[0] == "0"): #"0" is used to define the point O
            pointOld[0] = point[0]
            pointOld[1] = point[1]
        elif (pointOld[0] == point[0]) and (pointOld[1]%p == (-1*point[1])%p):
            pointOld[0] = "0"
        else:
            if (pointOld[0] != point[0]) and (pointOld[1] != point[1]):
                b = (point[0]-pointOld[0])
                a = inverseMod(b,1,p)
                m = (((point[1] - pointOld[1])%p)*a)%p
            elif(pointOld[0] == point[0]) and (pointOld[1] == point[1]):
                b = (2*pointOld[1])
                a = inverseMod(b,1,p)
                m = ((((3*pointOld[0]*pointOld[0]+A))%p)*a)%p
            x = (m*m - pointOld[0] - point[0])%p
            y = (m*(pointOld[0] - x) - pointOld[1])%p
            pointOld[0] = x
            pointOld[1] = y
    print pointOld
    
func1()

# example output using example elliptic curve Y^2 = X^3 + 171*X + 853
# input:
# x = 1980 and y = 431
# A = 171 and p = 2671.
# n = 1943
# output:
# [1432.0,667.0]
