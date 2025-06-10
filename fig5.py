# -*- coding: utf-8 -*-
# @Time : 2025-05-30 14:34
# @Author : OrangeMoon
import matplotlib.pyplot as plt
import numpy as np

N = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46]
PartialEval_Time_in_DCT = [0.3217457533,0.3603825569,1.1469094753,1.4160211086,1.8222764730,2.1546583176,2.6973710060,3.8250224590,3.9412956238,4.7214076519,5.6207691431,6.8460490704,8.1150102615,9.7233564854,11.4481085539]
PartialEval_Time_in_DPRF = [0.0022485256,0.0066514015,0.0514006615,0.3769302368,2.8318614960,23.5376307964]
FinalEval_Time_in_DCT = [0.3750846386,0.8161249161,1.2850613594,2.0004067421,2.9608867168,4.0870311260,5.5438826084,7.0678722858,8.6173205376,10.6583154202,15.9827730656,20.6373696327,22.9859974384,26.6632170677,30.9626829624]
FinalEval_Time_in_DPRF = [0.0000572205,0.0000371933,0.0000503063,0.0001699924,0.0003383160,0.0012543201,0.0133564472,0.0955269337]

def plot_time_comparison():
    plt.figure()
    plt.plot(N, PartialEval_Time_in_DCT,label='PartialEval Time in DCT',marker='o', linewidth=2.5)
    plt.plot(N[:6], PartialEval_Time_in_DPRF,label='PartialEval Time in DPRF',marker='s', linewidth=2.5)
    plt.plot(N, FinalEval_Time_in_DCT,label='FinalEval Time in DCT',marker='p', linewidth=2.5)
    plt.plot(N[:8], FinalEval_Time_in_DPRF,label='FinalEval Time in DPRF',marker='^', linewidth=2.5)
    plt.xlim(0, 50)
    plt.ylim(-1, 32)
    plt.xlabel('N')
    plt.ylabel('Time')

    plt.legend(loc="upper left")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_time_comparison()