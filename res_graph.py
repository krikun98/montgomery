import argparse
import matplotlib.pyplot as plt


def attributes(mode='num', type='absolute', lang='en'):
    algo_types = ["Standard exponentiation", "Montgomery exponentiation", "Parallel Montgomery exponentiation"]
    filename = "results"
    title = "Comparison of finite field modular exponentiation algorithms for small polynomials"
    xlabel = "GF(2^k) order k"
    ylabel = "Time in seconds per 10000 exponentiations"
    if mode == 'bignum':
        filename += '_bignum'
    elif mode == 'dhke':
        filename += '_dhke'
    if lang == 'en':
        if mode == 'bignum':
            title = "Comparison of finite field modular exponentiation algorithms for RFC polynomials"
            ylabel = "Time in seconds per exponentiation"
        elif mode == 'dhke':
            title = "Comparison of finite field modular exponentiation algorithms for DHKE implementations"
            ylabel = "Time in seconds per key exchange"
        if type == 'relative':
            ylabel = ylabel.replace("Time in seconds", "Percentage of time")
    elif lang == 'ru':
        algo_types = ["Алгоритм 'слева направо'", "Алгоритм Монтгомери", "Параллельный алгоритм Монтгомери"]
        title = "Сравнение алгоритмов возведения в степень по модулю для небольших многочленов"
        xlabel = "Степень конечного поля GF(2^k)"
        ylabel = "Время на 10000 операций возведения в степень"
        if mode == 'bignum':
            title = "Сравнение алгоритмов возведения в степень по модулю для многочленов IETF"
            ylabel = "Время на операцию возведения в степень"
        elif mode == 'dhke':
            title = "Сравнение алгоритмов возведения в степень по модулю для алгоритма Диффи-Хеллмана"
            ylabel = "Время на операцию обмена ключами"
        if type == 'relative':
            ylabel = ylabel.replace("Время", "Процент времени")
    return filename, type, lang, title, xlabel, ylabel, algo_types


def draw_graph(params):
    filename, type, lang, title, xlabel, ylabel, algo_types = params
    input_file = filename + '.txt'
    plt.clf()
    bit_length = []
    data = [[], [], []]
    with open(input_file) as f:
        for line in f:
            x = line.split()
            algo_bit_length = int(x[0])
            algo_type = int(x[1])
            algo_time = float(x[2])
            data[algo_type].append([algo_bit_length, algo_time])
            if algo_bit_length not in bit_length:
                bit_length.append(algo_bit_length)
    bit_length.sort()
    print(bit_length)
    if type != 'relative':
        for algo_index in range(3):
            data[algo_index].sort(key=lambda algo_data: algo_data[0])
            algo_time = []
            for algo_bit_length in bit_length:
                times_bit_length = [time[1] for time in data[algo_index] if time[0] == algo_bit_length]
                algo_time_sum = sum(times_bit_length)
                print(algo_index, algo_bit_length, algo_time_sum, len(times_bit_length))
                algo_time.append(float(algo_time_sum / len(times_bit_length)))
            clr = "bgrcmykw"
            plt.plot(bit_length, algo_time, color=clr[algo_index], label=algo_types[algo_index])
    elif type == 'relative':
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
                algo_time.append(float((algo_time_sum / len(times_bit_length)) / reference_algo_time[i] * 100))
            clr = "bgrcmykw"
            plt.plot(bit_length, algo_time, color=clr[algo_index], label=algo_types[algo_index])

    if type == 'relative':
        filename += "_percent"
        plt.ylim(0, 100)
    if lang == 'ru':
        filename += '_ru'

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(0, -0.15), loc=2)
    plt.grid(True)
    plt.savefig('graphs/' + lang + '/' + filename + ".png", bbox_inches='tight')


for mode in ('num', 'bignum', 'dhke'):
    for type in ('absolute', 'relative'):
        for lang in ('en', 'ru'):
            draw_graph(attributes(mode, type, lang))
