import argparse
import matplotlib.pyplot as plt

mode = "bignum"
type = "absolute"
title = ""
ylabel = ""
filename = ""
k_mod = 0
if mode == "DHKE":
    filename = "results_dhke"
    title = "Comparison of finite field modular exponentiation algorithms for DHKE implementations"
    ylabel = "Time in seconds per key exchange"
    k_mod = 1
elif mode == "bignum":
    filename = "results_bignum"
    title = "Comparison of finite field modular exponentiation algorithms for RFC polynomials"
    ylabel = "Time in seconds per exponentiation"
elif mode == "num":
    filename = "results"
    title = "Comparison of finite field modular exponentiation algorithms for small polynomials"
    ylabel = "Time in seconds per 10000 exponentiations"
    k_mod=-1

parser = argparse.ArgumentParser(description='Comparison of finite field modular exponentiation algorithms')
parser.add_argument("-s", "--source", default=filename+".txt")
args = parser.parse_args()
algo_types = ["Standard exponentiation", "Montgomery exponentiation", "Parallel Montgomery exponentiation"]
bit_length = []
data = [[], [], []]
with open(args.source) as f:
    for line in f:
        x = line.split()
        algo_bit_length = int(x[0]) + k_mod
        algo_type = int(x[1])
        algo_time = float(x[2])
        data[algo_type].append([algo_bit_length, algo_time])
        if algo_bit_length not in bit_length:
            bit_length.append(algo_bit_length)
bit_length.sort()
print(bit_length)
if type == "absolute":
    for algo_index in range(3):
        data[algo_index].sort(key=lambda algo_data: algo_data[0])
        algo_time = []
        for algo_bit_length in bit_length:
            times_bit_length = [time[1] for time in data[algo_index] if time[0] == algo_bit_length]
            algo_time_sum = sum(times_bit_length)
            print(algo_index, algo_bit_length, algo_time_sum, len(times_bit_length))
            algo_time.append(float(algo_time_sum/len(times_bit_length)))
        clr = "bgrcmykw"
        plt.plot(bit_length, algo_time, color=clr[algo_index], label=algo_types[algo_index])
elif type == "relative":
    data[0].sort(key=lambda algo_data: algo_data[0])
    reference_algo_time = []
    for algo_bit_length in bit_length:
        times_bit_length = [time[1] for time in data[0] if time[0] == algo_bit_length]
        algo_time_sum = sum(times_bit_length)
        print(0, algo_bit_length, algo_time_sum, len(times_bit_length))
        reference_algo_time.append(float(algo_time_sum / len(times_bit_length)))
    for algo_index in range(1, 3):
        data[algo_index].sort(key=lambda algo_data: algo_data[0])
        algo_time = []
        for i in range(len(bit_length)):
            times_bit_length = [time[1] for time in data[algo_index] if time[0] == bit_length[i]]
            algo_time_sum = sum(times_bit_length)
            print(algo_index, bit_length[i], algo_time_sum, len(times_bit_length))
            algo_time.append(float((algo_time_sum/len(times_bit_length))/reference_algo_time[i]*100))
        clr = "bgrcmykw"
        plt.plot(bit_length, algo_time, color=clr[algo_index], label=algo_types[algo_index])


if type == 'relative':
    filename += "_percent"
    plt.ylim(0, 100)
    ylabel = ylabel.replace("Time in seconds", "Percentage of time")

plt.xlabel("GF(2^k) order k")
plt.ylabel(ylabel)
plt.legend(bbox_to_anchor=(0, -0.15), loc=2)
plt.grid(True)
plt.savefig(filename+".png",bbox_inches='tight')
