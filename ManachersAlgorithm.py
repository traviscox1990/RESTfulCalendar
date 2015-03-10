#written in python v 2.7.5

def addB(stringArray):

    stringArray2 = ['' for i in range(0,2*len(stringArray)+1)]
    for i in range(0,2*len(stringArray),2):
        stringArray2[i] = '|'
        stringArray2[i+1] = stringArray[i/2]
        
    stringArray2[2*len(stringArray)] = '|'
    
    return stringArray2
        

def removeB(stringArray):

    if (len(stringArray)<3):
        return ""

    string = ""
    for i in range(0,(len(stringArray)-1)/2):
        string += stringArray[i*2+1]
    return string
        

def main():

   
    c = 0
    r = 0
    m = 0
    n = 0
    
    s = raw_input("Enter string you wish to find the"\
                       +" longest palindromic substring in: ")
    s = s.replace(" ", "")
    if ( s == ""):
        print("String is empty. Program terminating")
        return
    S = [i for i in s]
    S2 = addB(S)
    p = [0 for i in range(0,len(S2))]
  
    for i in range(1,len(S2)):
        if ( i > r):
            p[i] = 0
            m = i - 1
            n = i + 1
        else:
            i2 = c*2-i
            if (p[i2]<(r-i)):
                p[i] = p[i2]
                m = -1
            else:
                p[i] = r - i
                n = r + 1
                m = i*2 - n
        while ( (m >= 0) and (n < len(S2)) and (S2[m] == S2[n])):
            p[i] += 1
            m -= 1
            n += 1
        if ((i+p[i])>r):
            c = i
            r = i + p[i]
    length = 0
    c = 0
    for i in range(1,len(S2)):
        if (length < p[i]):
            length = p[i]
            c = i
    S3 = S2[c-length:c+length+1]
    S4 = removeB(S3)
    print("The longest palindromic substring in string "+s+" is:")
    print(S4)
    
    
   



main()
    

    
    
