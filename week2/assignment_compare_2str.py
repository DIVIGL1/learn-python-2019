# -*- coding: utf-8 -*-
"""
Created on Sun May 26 18:19:12 2019

@author: Dim-Dim
"""

def compare_2str(str1, str2):
    if not (isinstance(str1,str) and isinstance(str2,str)): return (0)
    elif str1==str2: return(1)
    elif len(str1)>len(str2): return(2)
    elif str2=="learn": return(3)
        

print(compare_2str(1, ""))
print(compare_2str("", ""))
print(compare_2str("Test", "Test"))
print(compare_2str("Длинный", "Short"))
print(compare_2str("Short", "Длинный"))
print(compare_2str("", "learn"))