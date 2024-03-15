import pandas as pd
from sklearn import datasets
import numpy as np
import random

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Tabuleiro:
    def __init__(self, lado):
        self.lado = lado
        self.inicializa_tabuleiro()
        self.movimentos = {'cima': self.mover_cima, 'baixo': self.mover_baixo, 'direita': self.mover_direita, 'esquerda': self.mover_esquerda}

    def inicializa_tabuleiro(self):
        self.tabuleiro = np.arange(1, self.lado*self.lado+1)
        self.tabuleiro = np.reshape(self.tabuleiro, (self.lado, self.lado))
        self.tabuleiro[-1][-1] = 0
        self.x = self.lado - 1
        self.y = self.lado - 1

    def troca(self, novo_x, novo_y):
        aux = self.tabuleiro[novo_x][novo_y]
        self.tabuleiro[novo_x][novo_y] = self.tabuleiro[self.x][self.y]
        self.tabuleiro[self.x][self.y] = aux

    def mover_cima(self):
        if self.pode_subir():
            print(f'para cima: {self.x}{self.y-1}')
            self.troca(self.x, self.y-1)
            self.y = self.y - 1
            return True
        return False

    def mover_baixo(self):
        if self.pode_descer():
            self.troca(self.x, self.y + 1)
            self.y = self.y + 1
            return True
        return False

    def mover_direita(self):
        if self.pode_direita():
            self.troca(self.x + 1, self.y)
            self.x = self.x + 1
            return True
        return False

    def mover_esquerda(self):
        if self.pode_esquerda():
            self.troca(self.x - 1, self.y)
            self.x = self.x - 1
            return True
        return False

    def movimentos_possiveis(self):
        lista_movimentos = []
        lista_acoes = []
        # para cima
        if self.pode_subir():
            novo_y = self.y - 1
            lista_movimentos.append((self.x, novo_y))
            lista_acoes.append('cima')

        # para baixo
        if self.pode_descer():
            novo_y = self.y + 1
            lista_movimentos.append((self.x, novo_y))
            lista_acoes.append('baixo')

        # para direita
        if self.pode_direita():
            novo_x = self.x + 1
            lista_movimentos.append((novo_x, self.y))
            lista_acoes.append('direita')

        # para esquerda
        if self.pode_esquerda():
            novo_x = self.x - 1
            lista_movimentos.append((novo_x, self.y))
            lista_acoes.append('esquerda')

        return lista_movimentos, lista_acoes

    def pode_descer(self):
        if self.y < (self.lado - 1):
            return True
        else:
            return False

    def pode_subir(self):
        if self.y > 0:
            return True
        else:
            return False

    def pode_direita(self):
        if self.x < (self.lado - 1):
            return True
        else:
            return False

    def pode_esquerda(self):
        if self.x > 0:
            return True
        else:
            return False

    def print_pos(self):
        print(f'x = {self.x}, y = {self.y}')

    def print_tabuleiro(self):
        print(self.tabuleiro)


class QuebraCabeca:
    tamanho = 5
    def __init__(self, tam):
        self.tamanho = tam
        self.tabuleiro = Tabuleiro(self.tamanho)
    def aleatoriza(self, num_moves):
        self.tabuleiro.print_tabuleiro()
        self.tabuleiro.print_pos()

        self.num_moves = num_moves
        movements = self.tabuleiro.movimentos
        for _ in range(num_moves):
            possible = self.tabuleiro.movimentos_possiveis()[1]
            move = random.choice(possible)
            print(f'selected move {move}')
            movements[move]()
        self.tabuleiro.print_tabuleiro()

def bfs(initial, goal_test):
    frontier = [Node(initial, None, None)]
    explored = {initial}

    while frontier:
        current_node = frontier.pop(0)
        current_state = current_node.state

        if goal_test(current_state.state):  # Correção aqui
            return current_node

        for action in current_state.movimentos_possiveis()[1]:
            child = current_state.movimentos[action]()
            if child not in explored:
                explored.add(child)
                frontier.append(Node(child, current_node, action))

    return None

def dfs(initial, goal_test):
    frontier = [Node(initial, None, None)]
    explored = {initial}

    while frontier:
        current_node = frontier.pop()
        current_state = current_node.state

        if goal_test(current_state.tabuleiro):  # Ajuste aqui
            return current_node

        for action in current_state.movimentos_possiveis()[1]:
            child = current_state.movimentos[action]()
            if child not in explored:
                explored.add(child)
                frontier.append(Node(child, current_node, action))

    return None

def dls(initial, goal_test, limit=50):
    def recursive_dls(node, goal_test, limit):
        if goal_test(node.state.tabuleiro):  # Ajuste aqui
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for action in node.state.movimentos_possiveis()[1]:
                child = node.state.movimentos[action]()
                result = recursive_dls(Node(child, node, action), goal_test, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    return recursive_dls(Node(initial, None, None), goal_test, limit)

def ids(initial, goal_test):
    def dls(node, goal_test, limit):
        if goal_test(node.state.tabuleiro):  # Ajuste aqui
            return node
        elif limit == 0:
            return None
        else:
            for action in node.state.movimentos_possiveis()[1]:
                child = node.state.movimentos[action]()
                result = dls(Node(child, node, action), goal_test, limit - 1)
                if result is not None:
                    return result
        return None

    for depth in range(5):  # Valor máximo de profundidade conforme necessário
        result = dls(Node(initial, None, None), goal_test, depth)
        if result is not None:
            return result

    return None

def gbsf(initial, goal_test, heuristic):
    frontier = [(heuristic(initial), Node(initial, None, None))]
    explored = {initial}

    while frontier:
        _, current_node = min(frontier, key=lambda x: x[0])
        frontier.remove((_, current_node))
        current_state = current_node.state

        if goal_test(current_state.tabuleiro):  # Ajuste aqui
            return current_node

        for action in current_state.movimentos_possiveis()[1]:
            child = current_state.movimentos[action]()
            if child not in explored:
                explored.add(child)
                frontier.append((heuristic(child), Node(child, current_node, action)))

    return None


def print_menu():
    print("Escolha o algoritmo que você deseja usar:")
    print("1. Busca em Largura (BFS)")
    print("2. Busca em Profundidade (DFS)")
    print("3. Busca em Profundidade Limitada (DLS)")
    print("4. Busca em Profundidade Iterativa (IDS)")

def print_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(' '.join(str(celula) for celula in linha))

def main():
    quebra_cabeca = QuebraCabeca(5)
    quebra_cabeca.aleatoriza(10)

    print_menu()
    escolha = input("Digite o número do algoritmo que você deseja usar: ")

    # Estado inicial para o algoritmo de busca
    estado_inicial = Tabuleiro(quebra_cabeca.tamanho)
    estado_inicial.tabuleiro = np.copy(quebra_cabeca.tabuleiro.tabuleiro)
    estado_inicial.x = quebra_cabeca.tabuleiro.x
    estado_inicial.y = quebra_cabeca.tabuleiro.y

    # Definição da função goal_test
    def goal_test(state):
        tamanho = state.shape[0]  # Calcula o tamanho do tabuleiro a partir do array numpy
        objetivo = np.arange(1, tamanho * tamanho + 1).reshape((tamanho, tamanho))
        return np.array_equal(state, objetivo)

    match escolha:
        case '1':
            print("Você escolheu BFS.")
            resultado = bfs(estado_inicial, goal_test)
        case '2':
            print("Você escolheu DFS.")
            resultado = dfs(estado_inicial, goal_test)
        case '3':
            print("Você escolheu DLS.")
            resultado = dls(estado_inicial, goal_test)
        case '4':
            print("Você escolheu IDS.")
            resultado = ids(estado_inicial, goal_test)
        case _:
            print("Escolha inválida.")
            return

    if resultado is not None:
        print("Solução encontrada!")
        node = resultado
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        for state in path:
            print_tabuleiro(state.tabuleiro)
            print("\n")
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
