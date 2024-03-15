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
    def __init__(self,lado):
        self.lado = lado
        self.inicializa_tabuleiro()
        self.movimentos = {'cima': self.mover_cima, 'baixo': self.mover_baixo, 'direita': self.mover_direita, 'esquerda': self.mover_esquerda}

    def inicializa_tabuleiro(self):
        self.tabuleiro = np.arange(1,self.lado*self.lado+1)
        self.tabuleiro = np.reshape(self.tabuleiro,(self.lado,self.lado))
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
            self.y = self.y - 1;
            return True
        return False

    def mover_baixo(self):
        if self.pode_descer():
            self.troca(self.x, self.y + 1)
            self.y = self.y + 1;
            return True
        return False

    def mover_direita(self):
        if self.pode_direita():
            self.troca(self.x + 1, self.y)
            self.x = self.x + 1;
            return True
        return False

    def mover_esquerda(self):
        if self.pode_esquerda():
            self.troca(self.x - 1, self.y)
            self.x = self.x - 1;
            return True
        return False

    def movimentos_possiveis(self):
        lista_movimentos = []
        lista_acoes = []
        # pra cima
        if self.pode_subir():
            novo_y = self.y - 1
            lista_movimentos.append((self.x, novo_y))
            lista_acoes.append('cima')

        # pra baixo
        if self.pode_descer():
            novo_y = self.y + 1
            lista_movimentos.append((self.x, novo_y))
            lista_acoes.append('baixo')

        # pra direita
        if self.pode_direita():
            novo_x = self.x + 1
            lista_movimentos.append((novo_x, self.y,))
            lista_acoes.append('direita')

        # pra esquerda
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


class QuebraCabeça:
    tamanho = 5
    def __init__(self, tam):
        self.tamanho = tam
        self.tabuleiro = Tabuleiro(self.tamanho)
    def aleatoriza(self, num_moves):
        self.tabuleiro.print_tabuleiro()
        self.tabuleiro.print_pos()

        self.num_moves = num_moves
        movements = tabuleiro.movimentos
        for move in range(num_moves):
            possible = tabuleiro.movimentos_possiveis()[1]
            move = random.choice(possible)
            print(f'selected move {move}')
            movementsrandom.choice(possible)
        self.tabuleiro.print_tabuleiro()

def bfs(initial, goal_test):
    frontier = [Node(initial, None, None)]
    explored = {initial}

    while frontier:
        current_node = frontier.pop(0)
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for action in current_state.movimentos_possiveis()[1]:
            child = current_state.movimentosaction
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

        if goal_test(current_state):
            return current_node

        for action in current_state.movimentos_possiveis()[1]:
            child = current_state.movimentosaction
            if child not in explored:
                explored.add(child)
                frontier.append(Node(child, current_node, action))

    return None

def dls(initial, goal_test, limit=50):
    def recursive_dls(node, goal_test, limit):
        if goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for action in node.state.movimentos_possiveis()[1]:
                child = node.state.movimentosaction
                result = recursive_dls(Node(child, node, action), goal_test, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    return recursive_dls(Node(initial, None, None), goal_test, limit)

def gbsf(initial, goal_test, heuristic):
    frontier = [(heuristic(initial), Node(initial, None, None))]
    explored = {initial}

    while frontier:
        _, current_node = min(frontier, key=lambda x: x[0])
        frontier.remove((_, current_node))
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for action in current_state.movimentos_possiveis()[1]:
            child = current_state.movimentosaction
            if child not in explored:
                explored.add(child)
                frontier.append((heuristic(child), Node(child, current_node, action)))

    return None
