from __future__ import print_function
from apriorieficiente import inicio as api
import sys
import zerorpc

# importar las funciones que deseo utilizar
class Apriori(object):
    def apri(self, ds, sup, conf, longRule, rulesOfElements, repetidos):
        try:
            return api(ds, sup, conf, longRule, rulesOfElements, repetidos)
        except Exception as e:
            return e
    def prueba(self, text):
        return text

# crear el servidor
def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)

def main():
    addr = 'tcp://0.0.0.0:' + parse_port()
    s = zerorpc.Server(Apriori(), 1000000000)
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
