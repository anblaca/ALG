import re
import dist_thresh 
from trie import Trie
from time import process_time
import numpy as np
import collections


class SpellSuggester:

    """
    Clase que implementa el método suggest para la busqueda de terminos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """
        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))
        #self.vocabulary = vocab_file_path
    
    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

    def suggest(self, term, distance, threshold):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]

        results = {} # diccionario termino:distancia

        for word in self.vocabulary:
                if distance == "levenshtein":
                    d = dist_thresh.levenshtein(term,word,threshold)
                elif distance == "restricted":
                    d = dist_thresh.damerauLevenshtein(term,word,threshold)
                else:
                    d = dist_thresh.damerauLevenshteinIntermedia(term,word,threshold)

               #si la distancia mayor que t, pasamos de palabra 
                if d is not None:
                    if d <= threshold:
                        results[word] = d

        return results

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """
    def distanciaTrievsCadena(self,trie,x,t):
        res = {}  
        """Creo dos arrays numpy de longitud numstates del trie que contienen 0s """
        aAnt,aAct = np.zeros(trie.get_num_states()),np.zeros(trie.get_num_states())

        """Relleno array etapa anterior con la longitud de las inserciones"""
        for i in range (1,len(aAnt)):
            aAnt[i] = aAnt[trie.get_parent(i)]+1
        
        
        """Programacion dinamica, bucle j procesa cada letra de String x, bucle i actualiza
        distancias teniendo en cuenta el array de la etapa anterior aAnt y indices anteriores de
        su mismo array aAct"""    
        for j in range (len(x)):
            for i in range (len(aAnt)):
                ins,sus,a = 2**31,2**31,2**31
                
                """Coste borrado"""
                bor = aAnt[i]+1
                
                """Condición para borrado, acierto y substitución"""
                if i > 0:
                    """Coste inserción"""
                    ins = aAct[trie.get_parent(i)]+1
                    """Condición para acierto"""
                    if trie.get_label(i) == x[j]:
                        """Coste acierto"""
                        a = aAnt[trie.get_parent(i)]
                        """Condición para sustitución"""    
                    else:
                        """Coste sustitución"""           
                        sus = aAnt[trie.get_parent(i)]+1     
                
                """Asigno la minima distancia"""
                aAct[i] = min(ins,bor,a,sus)
                
           # """Veo si la etapa ha superado el treshold"""    
           # if min (aAct[i] for i in range (len(aAct))) > t:
           #     return t+1
        
            """ Me preparo para la nueva etapa"""        
            aAnt = aAct
            aAct = np.zeros(trie.get_num_states())
        
        """Busco estados finales en la última etapa, si los encuentro, los imprimo"""
        for i in range (len(aAnt)):
            if trie.is_final(i) and aAnt[i] <= t:
                a = trie.get_output(i)
                res[i] = a 
        return res            
    
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)

if __name__ == "__main__":
    spellsuggester = TrieSpellSuggester("quijote.txt")
    a = spellsuggester.suggest("cocina","intermediate",3)
    print(a.keys())
    # cuidado, la salida es enorme print(suggester.trie)
    #n = 3
    #vocab_file_path = "quijote.txt"
    #tokenizer = re.compile("\W+")
    #tallasDiccionario = [100, 1000, 10000, 50000, 90000]  
    #with open(vocab_file_path, "r", encoding='utf-8') as fr:
    #    c = collections.Counter(tokenizer.split(fr.read().lower()))
    #    if '' in c:
    #        del c['']
    #    reversed_c = [(freq, word) for (word,freq) in c.items()]
    #    sorted_reversed = sorted(reversed_c, reverse=True)
    #    sorted_vocab = [word for (freq,word) in sorted_reversed]

    #palabras =["casa","amiga","amos","andar","canales","cuarjada","costado","celoso"] 
    #thresholds = [0,1,3]  
    
    #distancias = ["levenshtein", "restricted", "intermediate"]
    
   # tiempoTotal = 0
   # for tallaDiccionario in tallasDiccionario:
   #     diccionario = sorted(sorted_vocab[:tallaDiccionario])
   #     spellsuggester = TrieSpellSuggester(diccionario)
   #     for palabra in palabras:
   #         for threshold in thresholds:
   #             for distancia in distancias:
   #                 tiempoTotal = 0
   #                 for i in range(n):
   #                     time1 = process_time()
   #                     spellsuggester.suggest(palabra,distancia,threshold)
   #                     time2 = process_time()
   #                     tiempoTotal += time2-time1
   #                 tiempoTotal /= n
   #                 print(f"TallaDiccionario: {tallaDiccionario}, palabra: {palabra},distancia: {distancia},threshold: {threshold}, tiempo: { tiempoTotal}\n")
#Para el tie
    #tiempoTotal = 0
    #for tallaDiccionario in tallasDiccionario:
    #    diccionario = sorted(sorted_vocab[:tallaDiccionario])
    #    spellsuggester = TrieSpellSuggester(diccionario)
    #    for palabra in palabras:
    #        for threshold in thresholds:
    #                tiempoTotal = 0
    #                for i in range(n):
    #                    time1 = process_time()
    #                    spellsuggester.distanciaTrievsCadena(spellsuggester.trie,palabra,threshold)
    #                    time2 = process_time()
    #                    tiempoTotal += time2-time1
    #                tiempoTotal /= n
    #                print(f"Talla: {tallaDiccionario}, palabra: {palabra},threshold: {threshold}, tiempo: { tiempoTotal}\n")




