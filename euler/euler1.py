import sys
import os
ans = 0
for x in range(1,1000):
    if (x % 3 == 0):
        ans = x+ans
    elif(x % 5 == 0):
        ans = x+ans
    
print ans





