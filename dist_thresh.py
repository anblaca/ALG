# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 00:13:35 2020

@author: BorjaMesa
"""

import numpy as np

def levenshtein(x,y,t):   #x,y Strings. t int.

    f = len(x)+1
    c = len(y)+1
    m = np.zeros((f,c))
    
    # Si strings vacios, devuelvo 0
    if f == 1 and c == 1:
        return 0

        # relleno matrix las filas i y columna 0 de la matriz m de forma ascendente 1,2,3,4...
    for i in range(1, f):
        m[i][0] = i

        # relleno matrix las columnas i y fila 0 de la matriz m de forma ascendente 1,2,3,4...
    for i in range(1, c):
        m[0][i] = i
        
        #relleno el resto de la matriz  
    for i in range(1, c):
        flag = False
        for j in range(1, f):
            
            
            #si los caracteres anteriores de x e y son iguales, no se suma distancia
            if x[j-1] == y[i-1]:
                m[j][i] = m[j-1][i-1]
                
                
            #si son distintos se elije el minimo entre borrado, insertado o substitucion. 
            #Consultando valores anteriores de la matriz  
            else:
                m[j][i] = min(m[j-1][i] + 1,    # borrado
                          m[j][i-1] + 1,        # insertado
                          m[j-1][i-1] + 1)      # substitucion
        
            #Compruebo si la distancia está por debajo del threshold      
            if m[j][i] < t:
                    flag = True
                    
        #Si hay algún valor por debajo del threshold continuo
        if flag == False:
            return None  
                
                
    # impresión matriz        
  #  for r in range(f):
        # print(m[r])
        
        
    return m[j][i]

    

def damerauLevenshtein(x,y,t):   #x,y Strings, versión restringida.

    f = len(x)+1
    c = len(y)+1
    m = np.zeros((f,c))
    
    # Si strings vacios, devuelvo 0
    if f == 1 and c == 1:
        return 0

        # relleno matrix las filas i y columna 0 de la matriz m de forma ascendente 1,2,3,4...
    for i in range(1, f):
        m[i][0] = i

        # relleno matrix las columnas i y fila 0 de la matriz m de forma ascendente 1,2,3,4...
    for i in range(1, c):
        m[0][i] = i
        
        #relleno el resto de la matriz  
    for i in range(1, c):
        flag = False
        for j in range(1, f):
            
            #si los caracteres anteriores de x e y son iguales, no se suma distancia
            if x[j-1] == y[i-1]:
                m[j][i] = m[j-1][i-1]
                
                
            #Si son distintos se elije el minimo entre borrado, insertado o substitución. 
            #Consultando valores anteriores de la matriz.
            
            
            # En el caso que podamos aplicar nueva regla
            elif i > 1 and j > 1 and x[j-2] == y[i-1] and x[j-1] == y[i-2]:
                m[j][i] = min(m[j-1][i] + 1,    # borrado
                          m[j][i-1] + 1,        # insertado
                          m[j-1][i-1] + 1,      # substitución
                          m[j-2][i-2] + 1)      # Nuevo caso
                
                
            # En el caso de que no podamos aplicar la nueva regla    
            else:
                m[j][i] = min(m[j-1][i] + 1,    # borrado
                          m[j][i-1] + 1,        # insertado
                          m[j-1][i-1] + 1,)      # substitucion
            
            #Compruebo si la distancia está por debajo del threshold      
            if m[j][i] < t:
                    flag = True
                    
        #Si hay algún valor por debajo del threshold continuo
        if flag == False:
            return None             
                
    # impresión matriz        
   # for r in range(f):
    # print(m[r])
        
        
    return m[j][i] 




def damerauLevenshteinIntermedia(x,y,t):   #x,y Strings, versión intermedia.

    f = len(x)+1
    c = len(y)+1
    m = np.zeros((f,c))
    
    # Si strings vacios, devuelvo 0
    if f == 1 and c == 1:
        return 0

        # relleno matrix las filas i y columna 0 de la matriz m de forma ascendente 1,2,3,4...
    for i in range(1, f):
        m[i][0] = i

        # relleno matrix las columnas i y fila 0 de la matriz m de forma ascendente 1,2,3,4...
    for i in range(1, c):
        m[0][i] = i
        
        #relleno el resto de la matriz  
    for i in range(1, c):
            flag = False
            for j in range(1, f):
                
                #si los caracteres anteriores de x e y son iguales, no se suma distancia
                if x[j-1] == y[i-1]:
                    m[j][i] = m[j-1][i-1]
                    
                    
                #Si son distintos se elije el minimo entre borrado, insertado o substitución. 
                #Consultando valores anteriores de la matriz.
                
                
                # En el caso que podamos aplicar regla 1
                elif i > 1 and j > 1 and x[j-2] == y[i-1] and x[j-1] == y[i-2]:
                    m[j][i] = min(m[j-1][i] + 1,    # borrado
                              m[j][i-1] + 1,        # insertado
                              m[j-1][i-1] + 1,      # substitución
                              m[j-2][i-2] + 1)      # Caso regla 1
                    
                # En el caso que podamos aplicar regla 2    
                elif i > 1 and j > 2 and x[j-3] == y[i-1] and x[j-1] == y[i-2]:
                    m[j][i] = min(m[j-1][i] + 1,    # borrado
                              m[j][i-1] + 1,        # insertado
                              m[j-1][i-1] + 1,      # substitución
                              m[j-3][i-2] + 2)      # Caso regla 2
                    
                # En el caso que podamos aplicar regla 3   
                elif i > 2 and j > 1 and x[j-2] == y[i-1] and x[j-1] == y[i-3]:
                    m[j][i] = min(m[j-1][i] + 1,    # borrado
                              m[j][i-1] + 1,        # insertado
                              m[j-1][i-1] + 1,      # substitución
                              m[j-2][i-3] + 2)      # Caso regla 3
                        
                    
                # En el caso general   
                else:
                    m[j][i] = min(m[j-1][i] + 1,    # borrado
                              m[j][i-1] + 1,        # insertado
                              m[j-1][i-1] + 1,)      # substitucion
                    
                #Compruebo si la distancia está por debajo del threshold      
                if m[j][i] < t:
                    flag = True
                    
            #Si hay algún valor por debajo del threshold continuo
            if flag == False:
                    return None
                
    
        
    # impresión matriz        
  #  for r in range(f):
   #    print(m[r])
        
        
    return m[j][i]     



# print ("")
# levenshtein("acb", "acba",0)
# print ("")
# levenshtein("acb", "ba",3)
