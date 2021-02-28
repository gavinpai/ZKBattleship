import pedersen
from matplotlib import pyplot as plt
def pedersen_histogram():
    x= 1000000
    gen = pedersen.Pedersen(256)
    c0 = []
    c1 = []
    for i in range(x):
        c0.append(gen.commit(0).c / 1.0)
        c1.append(gen.commit(1).c / 1.0)
        if (i % 10000 == 0):
            print(i // 10000)

    plt.title("Histogram of Commitments when Message Equals Zero")
    plt.hist(c0, bins = "auto", range = (0, gen.state.p / 1.0))  
    plt.ylabel("Occurences")
    plt.xlabel("Commitment value")
    plt.show()
    plt.title("Histogram of Commitments when Message Equals One")
    plt.hist(c1, bins = "auto", range = (0, gen.state.p / 1.0))  
    plt.ylabel("Occurences")
    plt.xlabel("Commitment value")
    plt.show()
pedersen_histogram()
