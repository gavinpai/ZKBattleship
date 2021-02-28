import pedersen
from matplotlib import pyplot as plt
import time
import statistics
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

def time_generate():
    c = []
    x = 1000
    a = ("16", "32", "64", "128", "256")
    times = [[],[],[],[],[]]
    t = []
    e = []
    for i in range(len(a)):
        for j in range(x):
            start = time.time()
            gen = pedersen.Pedersen(2 ** (4 + i))
            end = time.time()
            times[i].append(end - start)
        t.append(statistics.fmean(times[i]))
        e.append(statistics.stdev(times[i]))
    
    plt.ylabel("Bits")
    plt.xlabel("Time (s)")
    plt.title("Commitment Bit Length vs Time of Generation")
    plt.barh(a, t, xerr = e)
    plt.show()
        

time_generate()
