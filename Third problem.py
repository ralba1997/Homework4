print('\n Two players play the following game with a nucleotide sequence of length n = nA + nT + nC + nG,'
      '\n where nA, nT , nC , and nG are the number of A,T,C, and G in the sequence. '
      '\n At every turn a player may delete either one or two nucleotides from the sequence. '
      '\n The player who is left with a uni-nucleotide sequence of an arbitrary length '
      '\n (i.e., the sequence containing only one of 4 possible nucleotides) loses. '
      '\n WHO WILL WIN?')


def NucleotideGame(Nucleotide_Sequence):  # take as input a random nucleotide sequence
    Nucleo_Seq_upper = Nucleotide_Sequence.upper()
    nA = 0
    nT = 0
    nC = 0
    nG = 0

    for i in Nucleo_Seq_upper:
        if i == 'A':
            nA += 1
        elif i == 'T':
            nT += 1
        elif i == 'C':
            nC += 1
        elif i == 'G':
            nG += 1

    total = nA + nT + nC + nG
    values = [nA, nT, nC, nG]
    values.sort()

    # Case0: All the heaps are empty
    if values == [0, 0, 0, 0]:
        return "IMPOSSIBLE GAME"

    # Case1: Only one non-empty heap
    if values[:3] == [0, 0, 0] and values[3] != 0:
        return "FIRST PLAYER LOSES"

    # Case2: If "total" is a multiple of 3, the second player wins the game,
    # but there are 18 exceptions where the first player wins and where the three smallest heaps are:
    # (0,0,1); (0,0,2); (0,1,1); (0,1,2); (0,1,3); (0,2,2); (0,2,3); (1,1,1); (1,1,2);
    # (1,1,3); (1,2,2); (1,2,3); (1,2,4); (1,3,3); (2,2,2); (2,2,3); (2,2,4); (2,3,3).

    if total % 3 == 0:
        is_exception = 0
        exceptions = [[0, 0, 1], [0, 0, 2], [0, 1, 1], [0, 1, 2], [0, 1, 3], [0, 2, 2], [0, 2, 3], [1, 1, 1], [1, 1, 2],
                      [1, 1, 3], [1, 2, 2], [1, 2, 3], [1, 2, 4], [1, 3, 3], [2, 2, 2], [2, 2, 3], [2, 2, 4], [2, 3, 3]]
        for exception in exceptions:
            if values[:3] == exception:
                is_exception = 1
        if is_exception == 1:
            return "FIRST PLAYER WINS"
        else:
            return "SECOND PLAYER WINS"

    # Case3: If "total" is a multiple of 3 + 1, the first player wins because he is
    # able to put the other player in a 'total = multiple of 3' situation.
    # In this case there is an exception where the second player is able to win
    # and when the three smallest heaps are (1,1,1)
    if total % 3 == 1:
        exception = [1, 1, 1]
        if values[:3] == exception:
            return "SECOND PLAYER WINS"
        else:
            return "FIRST PLAYER WINS"

    # Case4: If "total" is a multiple of 3 + 2, the first player wins because he is
    # able to put the other player in a 'total = multiple of 3' situation.
    # In this case there are 6 exceptions where the second player is able to win
    # and when the three smallest heaps are:
    # (0,1,2); (0,2,2); (1,2,2); (1,2,3); (2,2,2); (2,2,3).
    if total % 3 == 2:
        is_exception = 0
        exceptions = [[0, 1, 2], [0, 2, 2], [1, 2, 2], [1, 2, 3], [2, 2, 2], [2, 2, 3]]
        for exception in exceptions:
            if values[:3] == exception:
                is_exception = 1
        if is_exception == 1:
            return "SECOND PLAYER WINS"
        else:
            return "FIRST PLAYER WINS"


print(NucleotideGame(input("Please insert a nucleotide sequence:")))