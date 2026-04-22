import ambiente
from ambiente import No


class FronteiraBFS:
    def __init__(self):
        self.fronteira = []

    def adicionar(self, no):
        self.fronteira.append(no)

    def remover(self):
        if not self.fronteira:
            raise ValueError("Fronteira vazia.")
        return self.fronteira.pop(0)

    def esta_vazia(self):
        return len(self.fronteira) == 0
    
class FronteiraDFS:
    def __init__(self):
        self.fronteira = []

    def adicionar(self, no):
        self.fronteira.append(no)

    def remover(self):
        if not self.fronteira:
            raise ValueError("Fronteira vazia.")
        return self.fronteira.pop()

    def esta_vazia(self):
        return len(self.fronteira) == 0
    




class Bfs:
    def bfs(matriz, estado_inicial):
        nos_alcancados = set()
        nos_expandidos = 0
        estado_inicial = No(estado_inicial[0], estado_inicial[1], matriz[estado_inicial[0]][estado_inicial[1]])
        if ambiente.estado_final(estado_inicial):
            return estado_inicial, 1, 0
        fronteira = FronteiraBFS()
        fronteira.adicionar(estado_inicial)
        nos_alcancados.add((estado_inicial.i, estado_inicial.j))
        nos_alcancados_qtd = 1
        while not fronteira.esta_vazia():
            no = fronteira.remover()
            nos_expandidos += 1
            for no_filho in ambiente.funcao_transicao(no):
                if ambiente.e_estado_final(no_filho):
                    return no_filho, nos_alcancados_qtd, nos_expandidos
                coord = (no_filho.i, no_filho.j)
                if coord not in nos_alcancados:
                    nos_alcancados.add(coord)
                    nos_alcancados_qtd += 1
                    fronteira.adicionar(no_filho)
        return None, nos_alcancados_qtd, nos_expandidos
    
class Dfs:
    def dfs(matriz, estado_inicial):
        nos_alcancados = set()
        nos_expandidos = 0
        estado_inicial = No(estado_inicial[0], estado_inicial[1], matriz[estado_inicial[0]][estado_inicial[1]])
        if ambiente.estado_final(estado_inicial):
            return estado_inicial, 1, 0
        fronteira = FronteiraDFS()
        fronteira.adicionar(estado_inicial)
        nos_alcancados.add((estado_inicial.i, estado_inicial.j))
        nos_alcancados_qtd = 1
        while not fronteira.esta_vazia():
            no = fronteira.remover()
            nos_expandidos += 1
            for no_filho in ambiente.funcao_transicao(no):
                if ambiente.e_estado_final(no_filho):
                    return no_filho, nos_alcancados_qtd, nos_expandidos
                coord = (no_filho.i, no_filho.j)
                if coord not in nos_alcancados:
                    nos_alcancados.add(coord)
                    nos_alcancados_qtd += 1
                    fronteira.adicionar(no_filho)
        return None, nos_alcancados_qtd, nos_expandidos

        