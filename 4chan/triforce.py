# $$\   $$\           $$\                           
# $$ |  $$ |          $$ |                          
# $$ |  $$ | $$$$$$$\ $$$$$$$\   $$$$$$\  $$$$$$$\  
# $$$$$$$$ |$$  _____|$$  __$$\  \____$$\ $$  __$$\ 
# \_____$$ |$$ /      $$ |  $$ | $$$$$$$ |$$ |  $$ |
#       $$ |$$ |      $$ |  $$ |$$  __$$ |$$ |  $$ |
#       $$ |\$$$$$$$\ $$ |  $$ |\$$$$$$$ |$$ |  $$ |
#       \__| \_______|\__|  \__| \_______|\__|  \__|

import sys

def main(arg, SPACE = '-', TRI = 'Z'):
    if len(arg) == 2:
        try:
            tri = int(arg[1])
        except:
            print 'nice try'
            return 'bad kid'
    else:
        print 'Usage: trifoce -num'
        return 'retawd'
    tri = abs(tri + (tri % 2) - 1)
    part, i = [], 1
    while i <= tri:
        part += [SPACE * ((tri - i)/2) + TRI * i + SPACE * ((tri - i)/2)]
        i += 2
    part += part
    for i in range(len(part)/2):
        part[i] = SPACE * ((len(part[i])+1)/2) + part[i] + SPACE * ((len(part[i])+1)/2)
        print part[i]
    for i in range(len(part)/2, len(part)):
        part[i] += SPACE + part[i]
        print part[i]

if __name__ == '__main__':
    main(sys.argv)