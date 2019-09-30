import numpy as np

# optimization:
# we can use entropy as the heuristic metrics


class Board(object):
    # m x n board, k regions,
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k
        assert m * n % k == 0
        # note: index start from 0
        self.board_ = np.zeros(shape=(m, n))

    # random fill the board, with, k, reginos,
    # regions should be connected, marked with {1, 2, ..., k}
    def random_init(self):
        pass

    def __str__(self):
        res = ''.join(['x' * self.n + '\n' for _ in range(self.m)])
        # return res
        return str(self.board_)


class AI(object):
    # m x n board, k regions,
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k
        self.replies = {}
        pass

    # give a query it think can reduce our possible board space most
    # return a tuple of (int, int),  which is the left top corner of the query
    def next_query(self):
        return (0, 0)
        pass

    # pos: the left top corner of the query
    # reply: a tuple of length self.k, representing, how many 1, 2,..k block in
    # that 2x2 grid.  (2, 1, 1, 0), that there is two 'I's, one 'II' and one 'III'
    # add the reply to the current knowledge
    def add_constraint(self, pos, reply):
        self.replies[pos] = reply
        pass

    # return True if there is only one possible solution
    def is_guess_complete(self):
        return True

    # the final guess, return a complete board
    def guess(self):
        return Board(self.m, self.n, self.k)


# given, a complete board as the hidden answer,
# the 'AI' choose a plase to query, get the reply(a constraint)
# then guess the complete board based on the a replies.
# repeat untill 'AI' guess correct
def test():
    m, n, k = 6, 6, 4

    # init the correct answer
    complete_board = Board(m, n, k)
    complete_board.random_init()
    print("the correct answer is :")
    print(complete_board)

    a = AI(m, n, k)
    while not a.is_guess_complete():
        # pos is a tuple, e.g. (2,3)
        pos = a.next_query()
        reply = complete_board.query(pos)
        a.add_constraint(pos, reply)

    print("My guess is :")
    print(a.guess())


if __name__ == '__main__':

    test()
