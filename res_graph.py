import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Comparison of finite field modular exponentiation algorithms')
parser.add_argument("-s", "--source", default="results.txt")
args = parser.parse_args()
algo_types = ["Standard exponentiation", "Montgomery exponentiation", "Parallel Montgomery exponentiation"]
data = [[], [], []]
with open(args.source) as f:
    k = [2, 2, 2]
    c = [0, 0, 0]
    temp = [0, 0, 0]
    for line in f:
        x = line.split()
        bit_length = int(x[0])
        algo_type = int(x[1])
        algo_time = float(x[2])
        if bit_length == k[algo_type]:
            c[algo_type] += 1
            temp[algo_type] += algo_time
        else:
            data[algo_type].append([k[algo_type], float(temp[algo_type] / c[algo_type])])
            c[algo_type] = 1
            temp[algo_type] = algo_time
            k[algo_type] = bit_length

for algo_index in range(3):
    bit_length, algo_time = zip(*data[algo_index])
    clr = "bgrcmykw"
    plt.plot(bit_length, algo_time, color=clr[algo_index], label=algo_types[algo_index])

plt.title("Comparison of finite field modular exponentiation algorithms")
plt.xlabel("GF(2^k) power k")
plt.ylabel("Time in seconds per 10000 exponentiations")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig("results.svg",bbox_inches='tight')
