import numpy as np
import itertools
import collections
import time

class Nodo:
    """
    Classe para representação de um nodo (nó) 
    da árvore do espaço de estados. Contém:

    - 'estado': Disposição atual dos números na tabela 3x3
    - 'pai': Estado pai do estado corrente
    - 'acao': Ação realizada para produzir o estado atual
    """
    def __init__(self, estado, pai=None, acao=None):
        self.estado = estado
        self.pai = pai
        self.acao = acao

        if acao is None:
          self.acao = "Z"
       
 
    @property 
    def caminho_(self):
        """
        Recupera o caminho do estado atual até o inicial
        """
        nodo, caminho = self, []
        while nodo:
            caminho.append(nodo)
            nodo = nodo.pai
        yield from reversed(caminho)

    @property
    def objetivo(self):
        """ Verifica se é um estado objetivo """
        return self.estado.objetivo

    @property
    def acoes(self):
        """ Acessa as ações disponíveis para o estado corrente """
        return self.estado.acoes

    def __str__(self):
        return str(self.estado)


class Busca():
    
    def __init__(self, inicio):
      self.inicio = inicio
    
    def buscar(self, tipo_busca, mostrar=None):
        """
        Realiza busca em largura ou em profundidade
        """
        
        
        borda = collections.deque([Nodo(self.inicio)])
        explorado = set()
        explorado.add(str(borda[0].estado))
        
        if mostrar:
          print("Ordem de visita dos estados:\n")      
        
        #Busca em largura
        if tipo_busca == 'largura':

          while borda:
              borda = collections.deque(list(borda))
              nodo_atual = borda.popleft()
              
              if mostrar:
                print(*(nodo_atual.estado.tabela), sep="\n")
                print("\n")
                                                      
              if nodo_atual.objetivo:
                  return nodo_atual.caminho_

              for movimento, acao in sorted(nodo_atual.acoes, key=lambda x: x[1]):
                  adjacente = Nodo(movimento(), nodo_atual, acao)

                  if str(adjacente.estado) not in explorado:
                      borda.append(adjacente)
                      explorado.add(str(adjacente.estado))

        
        #Busca em profundidade
        elif tipo_busca == 'profundidade':
          
          while borda:
            borda = collections.deque(list(borda))
            nodo_atual = borda.pop()
            
            if mostrar:
              print(*(nodo_atual.estado.tabela), sep="\n")
              print("\n")
                       
            if nodo_atual.objetivo:
                return nodo_atual.caminho_          

            for movimento, acao in sorted(nodo_atual.acoes, key=lambda x: x[1], reverse=True):
                adjacente = Nodo(movimento(), nodo_atual, acao)

                if str(adjacente.estado) not in explorado:
                    borda.append(adjacente)
                    explorado.add(str(adjacente.estado))

        
class QuebraCabeca():
    """
    Classe que representa a tabela 3x3 do 
    quebra-cabeça, composta por 9 números de 1 a 9.
    """
    def __init__(self, tabela):
        self.tamanho = 3
        self.tabela = tabela

    @property
    def objetivo(self):
        """
        
        O quebra-cabeça é resolvido se, para toda linha, coluna e diagonal
        da tabela, os números que as compõem somam 15. Assim, um estado
        objetivo é identificado caso a concatenação de uma lista contendo
        estas somas tenha apenas um único elemento e ele seja igual a 15.
        """
        
        estado = np.array(self.tabela)

        diagonais = np.array(np.concatenate([[estado.trace()] * self.tamanho,
                                            [estado[::-1].trace()] * self.tamanho]))

        somas = np.concatenate([estado.sum(axis=0), estado.sum(axis=1), diagonais])
        
        x = np.unique(somas)
        
        return (len(x) == 1) and (x[0] == 15)

        
    @property 
    def acoes(self):
        """
        Retorna lista de tuplas da forma (coordenadas, ação).
        """
        def definir_movimento(origem, destino):
            return lambda: self.mover(origem, destino)

        #Movimentos possíveis a partir do estado corrente
        conj_movimentos = []
        for i, j in itertools.product(range(self.tamanho),
                                      range(self.tamanho)):
            

            #O número presente no nome de cada direção 
            #indica a prioridade na ordem de consulta. 
            #Troque-os para customizar a ordem.
            direcoes = {'1 Cima':    (i+1, j),
                        '2 Baixo':   (i-1, j),
                        '3 Esquerda':(i, j+1),
                        '4 Direita': (i, j-1)}

            for acao, (l, c) in direcoes.items():
                if l >= 0 and c >= 0 and l < self.tamanho and c < self.tamanho and \
                   self.tabela[l][c] == 9:
                    
                    movimento = definir_movimento((i,j), (l,c)), acao
                    conj_movimentos.append(movimento)

        return conj_movimentos


    def copiar(self):
        """
        Retorna cópia do estado corrente quebra-cabeça
        """
        tabela = []
        for lin in self.tabela:
            tabela.append([x for x in lin])
        return QuebraCabeca(tabela)

    def mover(self, origem, destino):
        """
        Retorna a new estado derivado do movimento do número 9.
        """
        copia = self.copiar()
        i, j = origem
        r, c = destino
        copia.tabela[i][j], copia.tabela[r][c] = copia.tabela[r][c], copia.tabela[i][j]
        return copia

    def print_estado(self):
        """
        Imprime a configuração dos números da tabela 
        """
        for lin in self.tabela:
            print(lin)
        print()

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for lin in self.tabela:
            yield from lin


     
def main(tipo_busca: str, mostrar: bool = None):
  """
  Executa a busca solicitada sobre o espaço de estados e 
  calcula o tempo de execução.
  """
  estado_inicial = [[6,9,8],
                    [7,1,3],
                    [2,5,4]]

  
  b = Busca(QuebraCabeca(estado_inicial))
  t_inicial = time.perf_counter()
  p = b.buscar(tipo_busca, mostrar)
  t_final = time.perf_counter()

  tempo_execucao = t_final - t_inicial
  passos = 0

  if mostrar:
    print("Caminho do estado inicial até o estado objetivo: \n")
    for nodo in p:
        if nodo.acao == 'Z':
          print("Estado Inicial")
        else:
          print(nodo.acao[2:])

        nodo.estado.print_estado()
        passos += 1

    print(f"Comprimento do caminho até o objetivo: {passos}")
    print(f"Tempo de execução total: {tempo_execucao} segundos")

  return passos, tempo_execucao

if __name__ == '__main__':
  
  while True:
    tipo_busca = input("Escolha o tipo de busca a ser executado (largura/profundidade): ")
    
    if tipo_busca not in {'largura', 'profundidade'}:
      print("Opção inválida.\n")
    else: 
      break
  
  print()
  main(tipo_busca, True)    
