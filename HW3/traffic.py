#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Chunhao Shen, Han Wang

from graphviz import Digraph


from collections import defaultdict
import json
import random
import copy
import numpy as np


# data structure,
# use adjacent matrix to represent the directed graph
#
# e.g. : a street map of 2x2 blocks
#  'o' represent a segment of street, it's a node in the direted graph
#  '[ ]' is a block
#  '+' is an intersection
#
#                     end node
#                     |
#   +  o  +  o  +  o  +       (0,0)(0,1)(0,2)
#   o [ ] o [ ] o [ ] o     (1,0)(1,1)(1,2)(1,3)
#   +  o  +  o  +  o  +       (2,0)(2,1)(2,2)
#   o [ ] o [ ] o [ ] o     (1,0)(1,1)(1,2)(1,3)
#   |
#   start node
#
# how to name the node? use tuple
# (ith-row, jth on each row), count from 0
#  even row has h + 2 nodes
#  odd row has h + 1 nodes


def even(n):
    return n % 2 == 0


def odd(n):
    return not even(n)

# ←
# even
# odd, even is judged by the index of the row (0,1,2,..)


def L(node):
    i, j = node
    return (i, j - 1)


# →
# even
def R(node):
    i, j = node
    return (i, j + 1)


# ↑
# odd
def U(node):
    i, j = node
    return (i - 2, j)


# ↓
# odd
def D(node):
    i, j = node
    return (i + 2, j)


# ←╮
# only appear in odd row
def UL(node):
    i, j = node
    assert(odd(i))
    return (i - 1, j - 1)


# ╭→
# only appear in odd row
def UR(node):
    i, j = node
    assert(odd(i))
    return (i - 1, j)


# ←╯
# odd
def DL(node):
    i, j = node
    assert(odd(i))
    return (i + 1, j - 1)


# ╰→
# odd
def DR(node):
    i, j = node
    assert(odd(i))
    return (i + 1, j)


#  ↑
# -╯
# only appear in even row
def RU(node):
    i, j = node
    assert(even(i))
    return (i - 1, j + 1)


# ↑
# ╰—-
# only appear in even row
def LU(node):
    i, j = node
    assert(even(i))
    return (i - 1, j)


# -╮
#  ↓
# even row
def RD(node):
    i, j = node
    assert(even(i))
    return (i + 1, j + 1)


# ╭—-
# ↓
# even row
def LD(node):
    i, j = node
    assert(even(i))
    return (i + 1, j)


class Edge(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __hash__(self):
        return hash((self.a[0], self.a[1], self.b[0], self.b[1]))

    def __eq__(self, value):
        return (self.a[0], self.a[1], self.b[0], self.b[1]) == (value.a[0], value.a[1], value.b[0], value.b[1])

    def __repr__(self):
        return "({},{})->({},{})".format(self.a[0], self.a[1], self.b[0], self.b[1])


class Map(object):
    def __init__(self, h, w):
        # h : number of blocks on a colomn
        # w :  number of blocks on a row
        # start : the entry point, should be given as a pair e.g. (2,0)
        # end : the finish point, should be given as a pair e.g. (4,3)
        self.h = h
        self.w = w
        # self.start = start
        # self.end = end
        # assert even(start[0]) and start[1] == 0
        # assert even(end[0]) and end[1] == w + 1
        self.n_nodes = (h + 1) * w + (w + 1) * h  # number of nodes
        self.adj = [[0 for _ in range(self.n_nodes)]
                    for _ in range(self.n_nodes)]
        self.dot_ = Digraph(comment='map', engine="neato")
        # keeps all edges, maps Edge to True/False
        self.edges = {}

    # intersections
    # see DOT documents:
    # https://graphviz.readthedocs.io/en/stable/manual.html
    # https://graphviz.readthedocs.io/en/stable/api.html
    def dot(self):

        for i in range(self.w+1):
            for j in range(self.h+1):
                self.dot_.node('{},{}'.format(i, j), pos="{},{}!".format(i, j))

        self.dot_.render('test-output/map.dot', view=True)

    # map node: a pair of int to index in adj matrix
    # return the index in the matrix of the coordinate of that node in original map

    def node2idx(self, node):
        i, j = node
        assert i >= 0 and i <= 2 * self.h
        assert j >= 0 and j <= self.w + 1
        if even(i):
            return self.w * (i // 2) + (self.w + 1) * (i // 2) + j
        else:
            return self.w * (i // 2) + (self.w + 1) * (i // 2 + 1) - 1 + j

    def cut(self, a, b):
        assert(isinstance(a, tuple))
        assert(self.edges[Edge(a, b)])
        i = self.node2idx(a)
        j = self.node2idx(b)
        self.adj[i][j] = 0
        del self.edges[Edge(a, b)]

    def cut2(self, a, b):
        i = self.node2idx(a)
        j = self.node2idx(b)
        assert(self.edges[Edge(a, b)])
        assert(self.edges[Edge(b, a)])
        self.adj[i][j] = 0
        self.adj[j][i] = 0
        del self.edges[Edge(a, b)]
        del self.edges[Edge(b, a)]

    def conn(self, a, b):
        i = self.node2idx(a)
        j = self.node2idx(b)
        self.adj[i][j] = 1
        self.edges[Edge(a, b)] = True

    def conn2(self, a, b):
        i = self.node2idx(a)
        j = self.node2idx(b)
        self.adj[i][j] = 1
        self.adj[j][i] = 1
        self.edges[Edge(a, b)] = True
        self.edges[Edge(b, a)] = True

    # apply f on all nodes
    def forall_nodes(self, f, cond=None):
        for i in range(2 * self.h + 1):
            if even(i):
                for j in range(self.w):
                    f((i, j))
            else:
                for j in range(self.w + 1):
                    f((i, j))

    # node : a pair of int
    # node on top or bottom of the map,
    def is_nodes_on_top_or_bottom(self, node):
        i, j = node
        return i == 0 or i == self.h * 2

    # node : a pair of int
    def is_nodes_on_left_or_right(self, node):
        i, j = node
        return odd(i) and (j == 0 or j == self.w)

    # return all nodes "around" the 'node'
    # by "around", I mean, all legal neighbor nodes
    # this function take care of all the edge cases
    # ends: (0,0),(1,0),(0,w-1),(1,w),(2h-1,0),(2h,0),(2h,w-1),(2h-1,w)
    #  TODO, ends are corners.
    # boundaries:
    # if top edge: L/R/LD/UD; if bottom edge: L/R/LU/RU
    # if left edge: U/D/DR/UR; if right edge: U/D/UL/DL
    def nodes_around(self, node):
        # case 1: ends
        i, j = node
        if i == 0 and j == 0:
            return [R(node), LD(node)]
        if i == 1 and j == 0:
            return [D(node), UR(node)]
        if i == 0 and j == self.w - 1:
            return [L(node), RD(node)]
        if i == 1 and j == self.w:
            return [D(node), UL(node)]
        if i == self.h * 2 - 1 and j == 0:
            return [U(node), DR(node)]
        if i == self.h * 2 and j == 0:
            return [LU(node), R(node)]
        if i == self.h * 2 and j == self.w - 1:
            return [L(node), RU(node)]
        if i == self.h * 2 - 1 and j == self.w:
            return [U(node), DL(node)]
        # case 2: top edge
        if self.is_nodes_on_top_or_bottom(node):
            res = []
            if i == 0:
                res = [LD(node), RD(node)]
            # case 3: bottom edge
            else:
                res = [LU(node), RU(node)]
            if j > 0:
                res.append(L(node))
            if j < self.w:
                res.append(R(node))
            return res

        # case 4: the left edge
        if self.is_nodes_on_left_or_right(node):
            res = []
            if j == 0:
                res = [UR(node), DR(node)]
            # case 5: the right edge
            else:
                res = [UL(node), DL(node)]
            if i > 1:
                res.append(U(node))
            if i < 2 * self.h - 1:
                res.append(D(node))
            return res

        # case 6: normal nodes on even row
        if even(i):
            res = [LU(node), LD(node), RU(node), RD(node)]
            if j > 0:
                res.append(L(node))
            if j < self.w:
                res.append(R(node))
            return res

        # case 7: normal nodes on odd row
        else:
            res = [UL(node), UR(node), DL(node), DR(node)]
            if i > 1:
                res.append(U(node))
            if i < 2 * self.h - 1:
                res.append(D(node))
            return res

    # permissive, all directions are allowed
    def connect_all(self):
        for i in range(2 * self.h + 1):
            if even(i):
                for j in range(self.w):  # +2
                    nodes_list = self.nodes_around((i, j))
                    for each in nodes_list:
                        self.conn2((i, j), each)
            else:
                for j in range(self.w + 1):
                    nodes_list = self.nodes_around((i, j))
                    for each in nodes_list:
                        self.conn2((i, j), each)

    # randomly delete some point
    def delete_randomly(self):
        del_num = 1
        for i in range(del_num):
            rani1 = random.randint(0, self.h * 2)
            rani2 = random.randint(0, self.h * 2)
            # little bug: all the nodes on the right edge are connected
            ranj1 = random.randint(0, self.w - 1)
            ranj2 = random.randint(0, self.w - 1)
            self.cut((rani1, ranj1), (rani2, ranj2))

    def intersection(self):
        intsec = [[" " for _ in range(5)] for _ in range(5)]
        intsec_row = []
        intsec_all = []
        for i in range(self.w + 1):
            intsec_row.append(intsec)
        for j in range(self.h + 1):
            intsec_all.append(intsec_row)

    #  ↑↑↑
    # ←╯|╰→
    # ←-┼-→
    # ←╮|╭→
    #  ↓↓↓

    def find_arrow(self, intsec_all):
        for i in range(self.h + 1):
            for j in range(self.w + 1):
                intsec = intsec_all[i][j]
        # TODO: how can I know the directions of nodes in neighbor?
        pass

    # randomly cut an edge

    def rand_cut_edge(self):
        e = random.choice(list(self.edges))
        self.cut(e.a, e.b)

    # randomly cut 'n' edges
    def rand_cut_edges(self, n):
        for i in range(n):
            self.rand_cut_edge()

    # find path from start nodes to end nodes
    def find_solutions(self):
        # assume always starts here.
        start = (2, -1)
        # assume always nes here.
        starts = [R(start), RU(start), RD(start)]
        end = (self.h * 2 - 2, self.w + 1)
        targets = [L(end), LU(end), LD(end)]

        cur = start
        visited_edges = {}

        # is a -> b -> c a U-turn
        # a, b, c are nodes
        # TODO: not sure if it's correct
        def is_u_turn(a, b, c):
            if a == c:
                return True
            if a == L(c) or a == R(c) or a == U(c) or a == D(c):
                return True

        def find_solution(last, cur, next_steps, targets, visited_edges, path, solutions):
            while len(next_steps) > 0:
                next = next_steps.pop()
                if Edge(cur, next) not in self.edges:
                    continue
                # no U-turn
                if is_u_turn(last, cur, next):
                    continue
                if Edge(cur, next) not in visited_edges:
                    visited_edges[Edge(cur, next)] = True
                    path.append(next)
                    if next in targets:  # reached
                        # print(path)
                        solutions.append(path)
                    find_solution(cur, next, self.nodes_around(next),
                                  targets, visited_edges, path, solutions)
                    del visited_edges[Edge(cur, next)]

        solutions = []
        for s in starts:
            find_solution(start, s, self.nodes_around(s),
                          targets, visited_edges, [], solutions)
        return solutions


if __name__ == "__main__":

    map = Map(3, 3)

    solutions = []
    while (len(solutions) != 1):

        map.connect_all()
        print("len, ", len(map.edges))
        map.rand_cut_edges(int(len(map.edges) * 0.5))
        print("len, ", len(map.edges))

        solutions = map.find_solutions()

    print("num of solutions is ", len(solutions))
    print(solutions[0:3])
