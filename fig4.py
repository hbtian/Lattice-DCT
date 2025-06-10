import matplotlib.pyplot as plt
import numpy as np

N = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43]
PEval_time = [4.785602, 3.964122, 11.932379, 13.242561, 24.063174, 19.623973, 25.331332, 24.833217, 36.880340, 57.704448, 75.882825, 64.353907, 136.108250, 144.621253]
timezk = [4.463856, 3.603740, 10.785470, 11.826540, 22.240898, 17.469315, 22.633961, 21.008194, 32.939044, 52.983040, 70.262056, 57.507858, 127.993240, 134.897897]
FinalEval_time = [2.122214, 4.014088, 13.801080, 22.729231, 36.267536, 53.440319, 78.487256, 115.153901, 156.844362, 215.909090, 287.703508, 395.543494, 521.539852, 654.721679]
timevzk = [1.747129, 3.197963, 12.516019, 20.728825, 33.306649, 49.353288, 72.943373, 108.086029, 148.227042, 205.250774, 271.720735, 374.906125, 498.553854, 628.058462]

def plot_time_comparison():
    plt.figure()
    plt.plot(N, PEval_time,label='PartialEval Time',marker='o', linewidth=2)
    plt.plot(N, timezk,label='PartialEval Proof Time',marker='s', linewidth=2)
    plt.plot(N, FinalEval_time,label='FinalEval Time',marker='p', linewidth=2)
    plt.plot(N, timevzk,label='FinalEval Verify Time',marker='^', linewidth=2)
    plt.xlim(0, 45)
    plt.ylim(-30, 700)
    plt.xlabel('N')
    plt.ylabel('Time')

    plt.legend(loc="upper left")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_time_comparison()