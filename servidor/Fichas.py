import sys
import hashlib
import random

class Fichas():

    fichas = list()

    def __init__(self, ronda, nombres):
        cad = "".join(nombres)+str(ronda)
        for i in range(0, 7):
            for j in range(i, 7):
                tok = cad+str(i)+str(j)+str(random.randrange(0, 2500))
                self.fichas.append(
                    {
                        'token': hashlib.md5(tok.encode('utf-8')).hexdigest(),
                        'entero_uno': i,
                        'entero_dos': j
                    }
                )
    
    def randPop(self):
        return self.fichas.pop(random.randrange(len(self.fichas)))

    def imprimir(self):
        print(len(self.fichas))
        for ficha in self.fichas:
            print(ficha)

    def tomarMano(self):
        mano = []
        for i in range(7):
            mano.append(self.randPop())
        return mano
