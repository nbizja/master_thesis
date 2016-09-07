import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv


#AP5_all_delays = [[0.357, 0.216, 0.215, 0.218, 0.216, 0.214, 0.222, 0.235, 0.217, 0.233, 0.219, 0.224, 0.233, 0.22, 0.226, 0.23, 0.224, 0.219, 0.215, 0.222, 0.219, 0.217, 0.217, 0.222, 0.217, 0.225, 0.002, 0.217, 0.219, 0.221, 0.22, 0.222, 0.002, 0.215, 0.22, 0.232, 0.228, 0.218, 0.001, 0.223, 0.001, 0.226, 0.222, 0.001, 0.217, 0.224, 0.218, 0.216, 0.214, 0.225, 0.214, 0.218, 0.219, 0.214, 0.216, 0.226, 0.221, 0.217, 0.226, 0.223, 0.22, 0.221, 0.215, 0.226, 0.22, 0.216, 0.229, 0.001, 0.222, 0.215, 0.225, 0.219, 0.218, 0.218, 0.213, 0.218, 0.217, 0.212, 0.215, 0.215], [0.362, 0.228, 0.214, 0.215, 0.223, 0.218, 0.215, 0.217, 0.214, 0.221, 0.217, 0.215, 0.215, 0.221, 0.221, 0.224, 0.226, 0.001, 0.214, 0.219, 0.238, 0.002, 0.001, 0.217, 0.216, 0.002, 0.22, 0.001, 0.214, 0.227, 0.22, 0.22, 0.217, 0.003, 0.002, 0.218, 0.217, 0.218, 0.219, 0.218, 0.226, 0.001, 0.222, 0.219, 0.229, 0.216, 0.218, 0.222, 0.214, 0.216, 0.001, 0.22, 0.219, 0.22, 0.235, 0.218, 0.002, 0.224, 0.001, 0.224, 0.214, 0.213, 0.213, 0.217, 0.001, 0.218, 0.221, 0.002, 0.219, 0.216, 0.234, 0.215, 0.001, 0.001, 0.216, 0.219, 0.225, 0.001, 0.214, 0.219], [0.378, 0.214, 0.214, 0.217, 0.212, 0.213, 0.213, 0.214, 0.217, 0.226, 0.003, 0.221, 0.215, 0.23, 0.22, 0.225, 0.003, 0.217, 0.219, 0.218, 0.225, 0.224, 0.229, 0.217, 0.22, 0.233, 0.224, 0.228, 0.23, 0.224, 0.226, 0.222, 0.002, 0.224, 0.001, 0.219, 0.224, 0.222, 0.216, 0.226, 0.002, 0.221, 0.233, 0.219, 0.219, 0.219, 0.225, 0.225, 0.23, 0.229, 0.225, 0.001, 0.227, 0.221, 0.237, 0.214, 0.001, 0.216, 0.217, 0.223, 0.224, 0.217, 0.22, 0.218, 0.216, 0.218, 0.229, 0.22, 0.001, 0.23, 0.002, 0.219, 0.223, 0.227, 0.001, 0.22, 0.001, 0.216, 0.221, 0.214], [0.42, 0.221, 0.214, 0.224, 0.224, 0.217, 0.225, 0.222, 0.22, 0.217, 0.215, 0.226, 0.232, 0.224, 0.22, 0.213, 0.002, 0.223, 0.215, 0.216, 0.216, 0.217, 0.212, 0.213, 0.22, 0.211, 0.002, 0.216, 0.217, 0.213, 0.217, 0.213, 0.222, 0.216, 0.216, 0.215, 0.214, 0.258, 0.006, 0.217, 0.004, 0.216, 0.222, 0.24, 0.219, 0.009, 0.221, 0.221, 0.222, 0.002, 0.222, 0.228, 0.222, 0.221, 0.227, 0.001, 0.222, 0.213, 0.218, 0.221, 0.215, 0.217, 0.214, 0.212, 0.216, 0.228, 0.003, 0.002, 0.219, 0.001, 0.222, 0.221, 0.223, 0.218, 0.23, 0.223, 0.228, 0.002, 0.002, 0.002], [0.365, 0.216, 0.219, 0.215, 0.215, 0.216, 0.218, 0.223, 0.219, 0.221, 0.217, 0.224, 0.222, 0.219, 0.221, 0.217, 0.226, 0.22, 0.218, 0.001, 0.22, 0.227, 0.22, 0.218, 0.217, 0.223, 0.227, 0.226, 0.222, 0.221, 0.225, 0.217, 0.001, 0.001, 0.214, 0.222, 0.218, 0.221, 0.218, 0.217, 0.22, 0.219, 0.216, 0.216, 0.22, 0.215, 0.226, 0.23, 0.229, 0.001, 0.219, 0.218, 0.22, 0.221, 0.215, 0.217, 0.214, 0.219, 0.223, 0.23, 0.001, 0.215, 0.229, 0.22, 0.223, 0.221, 0.223, 0.224, 0.001, 0.001, 0.226, 0.002, 0.223, 0.22, 0.217, 0.217, 0.001, 0.224, 0.227, 0.228], [0.369, 0.219, 0.227, 0.218, 0.218, 0.226, 0.226, 0.221, 0.218, 0.215, 0.226, 0.214, 0.224, 0.215, 0.217, 0.213, 0.224, 0.222, 0.217, 0.222, 0.218, 0.223, 0.223, 0.222, 0.219, 0.217, 0.227, 0.229, 0.228, 0.221, 0.218, 0.001, 0.215, 0.001, 0.219, 0.215, 0.216, 0.222, 0.226, 0.217, 0.224, 0.002, 0.218, 0.231, 0.216, 0.218, 0.001, 0.214, 0.217, 0.22, 0.221, 0.214, 0.217, 0.214, 0.218, 0.22, 0.22, 0.22, 0.002, 0.218, 0.002, 0.212, 0.001, 0.213, 0.215, 0.001, 0.001, 0.211, 0.213, 0.216, 0.22, 0.214, 0.002, 0.213, 0.213, 0.213, 0.001, 0.003, 0.215, 0.001], [0.369, 0.217, 0.214, 0.215, 0.219, 0.213, 0.223, 0.213, 0.212, 0.001, 0.212, 0.217, 0.217, 0.237, 0.213, 0.212, 0.213, 0.215, 0.228, 0.216, 0.215, 0.216, 0.218, 0.213, 0.214, 0.218, 0.222, 0.213, 0.229, 0.227, 0.222, 0.236, 0.228, 0.215, 0.001, 0.235, 0.232, 0.215, 0.001, 0.004, 0.228, 0.222, 0.235, 0.218, 0.216, 0.224, 0.216, 0.218, 0.001, 0.218, 0.235, 0.22, 0.226, 0.222, 0.232, 0.229, 0.223, 0.23, 0.002, 0.22, 0.001, 0.22, 0.214, 0.228, 0.002, 0.216, 0.222, 0.221, 0.221, 0.001, 0.24, 0.001, 0.227, 0.215, 0.229, 0.225, 0.214, 0.221, 0.219, 0.218], [0.358, 0.226, 0.222, 0.216, 0.217, 0.214, 0.232, 0.223, 0.217, 0.221, 0.22, 0.219, 0.228, 0.227, 0.218, 0.222, 0.221, 0.225, 0.22, 0.223, 0.219, 0.231, 0.226, 0.001, 0.223, 0.215, 0.212, 0.219, 0.219, 0.219, 0.002, 0.222, 0.224, 0.229, 0.222, 0.221, 0.219, 0.213, 0.217, 0.222, 0.23, 0.214, 0.217, 0.002, 0.224, 0.215, 0.214, 0.216, 0.221, 0.22, 0.219, 0.221, 0.223, 0.226, 0.223, 0.002, 0.233, 0.218, 0.001, 0.217, 0.002, 0.226, 0.227, 0.229, 0.221, 0.219, 0.219, 0.002, 0.001, 0.221, 0.22, 0.212, 0.214, 0.215, 0.217, 0.001, 0.215, 0.002, 0.215, 0.214], [0.359, 0.219, 0.226, 0.22, 0.233, 0.216, 0.226, 0.226, 0.226, 0.218, 0.218, 0.224, 0.227, 0.224, 0.222, 0.219, 0.221, 0.237, 0.224, 0.222, 0.002, 0.217, 0.228, 0.226, 0.217, 0.001, 0.218, 0.23, 0.229, 0.22, 0.222, 0.223, 0.218, 0.223, 0.217, 0.218, 0.219, 0.217, 0.226, 0.218, 0.221, 0.22, 0.226, 0.001, 0.224, 0.218, 0.002, 0.224, 0.213, 0.213, 0.215, 0.225, 0.228, 0.229, 0.223, 0.002, 0.217, 0.231, 0.225, 0.221, 0.222, 0.001, 0.221, 0.217, 0.001, 0.001, 0.216, 0.214, 0.216, 0.219, 0.219, 0.001, 0.218, 0.214, 0.219, 0.22, 0.222, 0.002, 0.226, 0.219], [0.364, 0.229, 0.216, 0.214, 0.213, 0.212, 0.001, 0.214, 0.215, 0.215, 0.217, 0.002, 0.217, 0.214, 0.215, 0.002, 0.218, 0.221, 0.214, 0.213, 0.217, 0.216, 0.214, 0.217, 0.218, 0.221, 0.214, 0.001, 0.215, 0.216, 0.213, 0.216, 0.216, 0.213, 0.001, 0.213, 0.001, 0.216, 0.214, 0.215, 0.001, 0.226, 0.225, 0.002, 0.223, 0.216, 0.217, 0.224, 0.219, 0.229, 0.228, 0.229, 0.22, 0.218, 0.227, 0.216, 0.218, 0.214, 0.213, 0.219, 0.223, 0.218, 0.219, 0.23, 0.216, 0.228, 0.001, 0.225, 0.219, 0.225, 0.001, 0.221, 0.214, 0.221, 0.216, 0.212, 0.216, 0.223, 0.001, 0.219]]
#AP5_avg_delay = [0.0462625, 0.0275625, 0.027262500000000002, 0.02715, 0.027375000000000003, 0.026987500000000005, 0.0250125, 0.027600000000000003, 0.027187499999999996, 0.024850000000000004, 0.02455, 0.024825000000000003, 0.027875, 0.027887500000000003, 0.0274125, 0.024712500000000002, 0.022225, 0.025000000000000005, 0.0273, 0.024650000000000002, 0.024862500000000003, 0.024875, 0.02485, 0.024575, 0.027262500000000005, 0.022075, 0.0221, 0.02225, 0.027775, 0.027612500000000005, 0.0248125, 0.0249, 0.0193125, 0.019250000000000003, 0.0164125, 0.027600000000000003, 0.02485, 0.027750000000000004, 0.0193, 0.024712500000000002, 0.0169625, 0.0220875, 0.027950000000000003, 0.0168625, 0.027587499999999997, 0.024675, 0.021975, 0.027625, 0.02475, 0.0221625, 0.024987500000000003, 0.024925000000000003, 0.027762500000000006, 0.027575, 0.028162499999999997, 0.019312500000000003, 0.0221375, 0.027525, 0.0166, 0.027700000000000002, 0.016550000000000002, 0.024499999999999997, 0.0246625, 0.027625000000000004, 0.019137499999999998, 0.022074999999999997, 0.01955, 0.016525, 0.01915, 0.019312500000000003, 0.0226125, 0.0190625, 0.022037499999999998, 0.024525, 0.024637500000000003, 0.0246, 0.01925, 0.013825, 0.021937500000000002, 0.0218625]
#AP5_total_delay = [89.02600000000001, 79.74199999999995, 88.36399999999992, 86.39299999999987, 82.99899999999991, 81.16899999999993, 86.06599999999987, 85.14499999999991, 84.64999999999985, 87.73999999999994]
AP5_all_delays = [[0.379, 0.221, 0.225, 0.223, 0.214, 0.221, 0.213, 0.215, 0.213, 0.234, 0.212, 0.246, 0.225, 0.248, 0.236, 0.229, 0.002, 0.229, 0.22, 0.216, 0.222, 0.225, 0.219, 0.215, 0.226, 0.22, 0.222, 0.219, 0.223, 0.221, 0.221, 0.221, 0.222, 0.228, 0.224, 0.233, 0.001, 0.218, 0.215, 0.213, 0.215, 0.213, 0.213, 0.213, 0.002, 0.001, 0.221, 0.215, 0.212, 0.216, 0.213, 0.213, 0.222, 0.219, 0.219, 0.22, 0.221, 0.217, 0.218, 0.215, 0.229, 0.221, 0.217, 0.214, 0.219, 0.219, 0.226, 0.221, 0.22, 0.22, 0.225, 0.232, 0.22, 0.219, 0.223, 0.22, 0.22, 0.225, 0.221, 0.219], [0.353, 0.226, 0.214, 0.216, 0.227, 0.215, 0.224, 0.224, 0.22, 0.22, 0.218, 0.222, 0.226, 0.216, 0.217, 0.215, 0.217, 0.217, 0.215, 0.217, 0.218, 0.215, 0.225, 0.218, 0.216, 0.222, 0.003, 0.224, 0.223, 0.222, 0.225, 0.215, 0.218, 0.002, 0.222, 0.222, 0.22, 0.226, 0.218, 0.001, 0.216, 0.214, 0.219, 0.002, 0.213, 0.221, 0.002, 0.215, 0.215, 0.22, 0.221, 0.22, 0.216, 0.221, 0.22, 0.226, 0.226, 0.001, 0.221, 0.226, 0.004, 0.22, 0.228, 0.221, 0.002, 0.22, 0.001, 0.217, 0.22, 0.222, 0.229, 0.221, 0.228, 0.244, 0.218, 0.224, 0.233, 0.002, 0.227, 0.227], [0.395, 0.22, 0.212, 0.215, 0.218, 0.214, 0.217, 0.221, 0.213, 0.216, 0.214, 0.234, 0.217, 0.217, 0.212, 0.231, 0.214, 0.212, 0.001, 0.215, 0.212, 0.215, 0.213, 0.214, 0.214, 0.215, 0.212, 0.212, 0.211, 0.214, 0.212, 0.213, 0.214, 0.219, 0.001, 0.215, 0.216, 0.216, 0.218, 0.217, 0.212, 0.216, 0.221, 0.002, 0.224, 0.227, 0.226, 0.225, 0.219, 0.22, 0.216, 0.22, 0.222, 0.223, 0.244, 0.22, 0.001, 0.002, 0.002, 0.24, 0.218, 0.217, 0.219, 0.212, 0.002, 0.213, 0.214, 0.212, 0.215, 0.215, 0.002, 0.215, 0.223, 0.22, 0.221, 0.214, 0.218, 0.213, 0.214, 0.215], [0.403, 0.214, 0.218, 0.221, 0.212, 0.221, 0.002, 0.216, 0.218, 0.215, 0.213, 0.002, 0.221, 0.218, 0.22, 0.223, 0.232, 0.221, 0.234, 0.221, 0.229, 0.222, 0.003, 0.229, 0.215, 0.235, 0.22, 0.213, 0.213, 0.002, 0.218, 0.214, 0.214, 0.001, 0.215, 0.212, 0.215, 0.214, 0.215, 0.001, 0.001, 0.214, 0.002, 0.215, 0.213, 0.215, 0.223, 0.218, 0.214, 0.002, 0.213, 0.002, 0.216, 0.002, 0.216, 0.213, 0.219, 0.001, 0.215, 0.002, 0.215, 0.001, 0.219, 0.213, 0.001, 0.219, 0.215, 0.215, 0.219, 0.213, 0.002, 0.002, 0.226, 0.216, 0.223, 0.215, 0.225, 0.001, 0.221, 0.001], [0.38, 0.217, 0.226, 0.213, 0.215, 0.219, 0.216, 0.216, 0.229, 0.214, 0.003, 0.213, 0.001, 0.215, 0.213, 0.001, 0.212, 0.216, 0.217, 0.226, 0.213, 0.003, 0.002, 0.213, 0.213, 0.001, 0.215, 0.213, 0.225, 0.223, 0.215, 0.215, 0.213, 0.214, 0.225, 0.215, 0.001, 0.215, 0.224, 0.212, 0.214, 0.217, 0.214, 0.213, 0.218, 0.212, 0.216, 0.002, 0.213, 0.213, 0.218, 0.002, 0.216, 0.224, 0.001, 0.215, 0.002, 0.223, 0.002, 0.221, 0.213, 0.212, 0.213, 0.233, 0.213, 0.212, 0.216, 0.227, 0.218, 0.225, 0.002, 0.215, 0.001, 0.219, 0.218, 0.222, 0.213, 0.219, 0.214, 0.002], [0.428, 0.214, 0.227, 0.23, 0.222, 0.223, 0.221, 0.218, 0.221, 0.22, 0.218, 0.222, 0.219, 0.215, 0.222, 0.228, 0.222, 0.228, 0.226, 0.22, 0.002, 0.22, 0.225, 0.231, 0.225, 0.226, 0.226, 0.225, 0.23, 0.235, 0.222, 0.214, 0.223, 0.214, 0.002, 0.001, 0.218, 0.223, 0.213, 0.22, 0.216, 0.213, 0.215, 0.237, 0.001, 0.218, 0.233, 0.213, 0.214, 0.216, 0.003, 0.214, 0.216, 0.219, 0.214, 0.216, 0.214, 0.214, 0.005, 0.001, 0.213, 0.214, 0.213, 0.225, 0.001, 0.214, 0.002, 0.242, 0.217, 0.214, 0.22, 0.002, 0.215, 0.214, 0.214, 0.225, 0.225, 0.232, 0.003, 0.223], [0.374, 0.213, 0.214, 0.213, 0.213, 0.215, 0.215, 0.214, 0.214, 0.216, 0.216, 0.002, 0.216, 0.001, 0.217, 0.214, 0.215, 0.227, 0.216, 0.216, 0.214, 0.217, 0.216, 0.214, 0.213, 0.215, 0.219, 0.216, 0.001, 0.214, 0.213, 0.217, 0.214, 0.217, 0.215, 0.214, 0.226, 0.001, 0.219, 0.216, 0.22, 0.22, 0.212, 0.214, 0.217, 0.219, 0.221, 0.004, 0.222, 0.225, 0.23, 0.216, 0.001, 0.221, 0.002, 0.221, 0.229, 0.223, 0.22, 0.219, 0.001, 0.004, 0.223, 0.229, 0.219, 0.232, 0.223, 0.22, 0.228, 0.221, 0.215, 0.219, 0.001, 0.223, 0.223, 0.218, 0.001, 0.226, 0.001, 0.225], [0.395, 0.221, 0.216, 0.003, 0.216, 0.218, 0.235, 0.217, 0.22, 0.215, 0.218, 0.222, 0.219, 0.223, 0.216, 0.227, 0.215, 0.214, 0.217, 0.231, 0.217, 0.217, 0.219, 0.003, 0.222, 0.231, 0.223, 0.001, 0.223, 0.001, 0.221, 0.215, 0.002, 0.212, 0.22, 0.225, 0.222, 0.002, 0.219, 0.215, 0.222, 0.22, 0.221, 0.214, 0.219, 0.213, 0.214, 0.214, 0.217, 0.213, 0.001, 0.214, 0.001, 0.228, 0.214, 0.212, 0.216, 0.23, 0.219, 0.213, 0.222, 0.214, 0.218, 0.216, 0.217, 0.002, 0.002, 0.001, 0.001, 0.213, 0.217, 0.002, 0.217, 0.213, 0.214, 0.213, 0.217, 0.214, 0.219, 0.229], [0.373, 0.224, 0.217, 0.227, 0.221, 0.22, 0.223, 0.22, 0.219, 0.232, 0.216, 0.003, 0.219, 0.221, 0.219, 0.217, 0.225, 0.24, 0.227, 0.217, 0.224, 0.232, 0.215, 0.229, 0.218, 0.236, 0.22, 0.219, 0.224, 0.215, 0.225, 0.225, 0.228, 0.229, 0.223, 0.221, 0.215, 0.216, 0.002, 0.239, 0.228, 0.219, 0.222, 0.215, 0.214, 0.213, 0.215, 0.214, 0.218, 0.229, 0.213, 0.214, 0.215, 0.001, 0.001, 0.224, 0.002, 0.214, 0.221, 0.003, 0.215, 0.213, 0.213, 0.214, 0.002, 0.217, 0.215, 0.223, 0.002, 0.001, 0.214, 0.214, 0.214, 0.222, 0.215, 0.217, 0.233, 0.001, 0.225, 0.002], [0.41, 0.221, 0.222, 0.215, 0.214, 0.215, 0.216, 0.213, 0.222, 0.223, 0.23, 0.221, 0.22, 0.214, 0.002, 0.223, 0.223, 0.225, 0.218, 0.224, 0.222, 0.237, 0.231, 0.223, 0.222, 0.002, 0.22, 0.002, 0.218, 0.22, 0.002, 0.219, 0.216, 0.222, 0.219, 0.225, 0.222, 0.22, 0.223, 0.221, 0.217, 0.213, 0.214, 0.213, 0.225, 0.215, 0.212, 0.215, 0.214, 0.217, 0.236, 0.214, 0.224, 0.001, 0.216, 0.213, 0.002, 0.216, 0.217, 0.003, 0.223, 0.229, 0.22, 0.215, 0.226, 0.22, 0.002, 0.218, 0.002, 0.229, 0.227, 0.218, 0.217, 0.233, 0.221, 0.001, 0.228, 0.002, 0.224, 0.226]]
AP5_avg_delay = [0.04862500000000001, 0.027387500000000002, 0.027387500000000002, 0.024700000000000003, 0.02715, 0.027262500000000002, 0.024775000000000002, 0.027174999999999998, 0.0273625, 0.0275625, 0.024475, 0.0198375, 0.0247875, 0.02485, 0.024675, 0.0251, 0.024712500000000005, 0.027862500000000002, 0.0248875, 0.027537500000000003, 0.0246625, 0.0250375, 0.0221, 0.024862500000000003, 0.0273, 0.022537500000000002, 0.02475, 0.0218, 0.0248875, 0.0220875, 0.024675000000000002, 0.027100000000000003, 0.02455, 0.021975, 0.022075000000000004, 0.0247875, 0.02195, 0.021887499999999997, 0.024575000000000007, 0.021937500000000006, 0.0245125, 0.026987500000000005, 0.0244125, 0.021725, 0.021825000000000004, 0.024425000000000006, 0.0247875, 0.021687500000000002, 0.026975, 0.024637500000000003, 0.022049999999999997, 0.0216125, 0.0218625, 0.019487499999999998, 0.0193375, 0.027250000000000003, 0.01665, 0.0192625, 0.019250000000000003, 0.0167875, 0.0219125, 0.021812500000000002, 0.027287500000000003, 0.0274, 0.013775, 0.0246, 0.01645, 0.02495, 0.019275, 0.0246625, 0.019412500000000003, 0.01925, 0.022025, 0.0277875, 0.027375, 0.024612500000000002, 0.025162500000000004, 0.0166875, 0.0221125, 0.0196125]
AP5_total_delay = [84.58799999999988, 90.1059999999999, 85.44600000000001, 84.10099999999994, 84.03299999999987, 87.32199999999989, 81.36199999999987, 86.66199999999986, 81.36899999999991, 85.40799999999989]



#AP3_all_delays = [[0.017, 0.213, 0.001, 0.212, 0.216, 0.222, 0.213, 0.217, 0.001, 0.212, 0.228, 0.22, 0.002, 0.215, 0.223, 0.216, 0.001, 0.228, 0.215, 0.002, 0.221, 0.215, 0.222, 0.001, 0.215, 0.002, 0.003, 0.217, 0.217, 0.213, 0.216, 0.215, 0.212, 0.216, 0.213, 0.215, 0.221, 0.214, 0.222, 0.215, 0.001, 0.22, 0.001, 0.001, 0.001, 0.001, 0.214, 0.218, 0.214, 0.216, 0.217, 0.218, 0.219, 0.214, 0.001, 0.001, 0.225, 0.213, 0.212, 0.214, 0.218, 0.213, 0.222, 0.212, 0.212, 0.225, 0.002, 0.214, 0.219, 0.233, 0.002, 0.222, 0.003, 0.218, 0.002, 0.009, 0.219, 0.215, 0.217, 0.224], [0.015, 0.223, 0.223, 0.228, 0.002, 0.223, 0.222, 0.213, 0.001, 0.227, 0.212, 0.23, 0.219, 0.23, 0.217, 0.214, 0.221, 0.001, 0.221, 0.002, 0.219, 0.001, 0.001, 0.232, 0.001, 0.001, 0.002, 0.001, 0.214, 0.223, 0.001, 0.001, 0.23, 0.225, 0.223, 0.213, 0.223, 0.001, 0.231, 0.221, 0.001, 0.003, 0.218, 0.219, 0.001, 0.222, 0.227, 0.219, 0.221, 0.224, 0.228, 0.221, 0.222, 0.221, 0.014, 0.002, 0.22, 0.001, 0.221, 0.232, 0.22, 0.233, 0.235, 0.219, 0.001, 0.001, 0.216, 0.218, 0.23, 0.217, 0.234, 0.216, 0.002, 0.001, 0.213, 0.222, 0.225, 0.225, 0.223, 0.23], [0.234, 0.236, 0.002, 0.001, 0.224, 0.001, 0.23, 0.001, 0.217, 0.002, 0.222, 0.224, 0.215, 0.001, 0.226, 0.229, 0.001, 0.225, 0.001, 0.217, 0.214, 0.218, 0.232, 0.227, 0.218, 0.214, 0.217, 0.001, 0.001, 0.214, 0.218, 0.229, 0.216, 0.219, 0.226, 0.22, 0.22, 0.222, 0.245, 0.22, 0.217, 0.003, 0.225, 0.221, 0.221, 0.225, 0.001, 0.224, 0.226, 0.001, 0.223, 0.218, 0.215, 0.222, 0.222, 0.224, 0.005, 0.214, 0.219, 0.229, 0.001, 0.001, 0.228, 0.216, 0.002, 0.227, 0.224, 0.002, 0.227, 0.22, 0.001, 0.227, 0.225, 0.233, 0.213, 0.223, 0.214, 0.23, 0.223, 0.002], [0.016, 0.216, 0.228, 0.216, 0.217, 0.221, 0.223, 0.215, 0.225, 0.226, 0.216, 0.22, 0.222, 0.215, 0.222, 0.221, 0.22, 0.225, 0.223, 0.001, 0.217, 0.222, 0.001, 0.226, 0.229, 0.22, 0.222, 0.002, 0.225, 0.224, 0.22, 0.221, 0.222, 0.001, 0.001, 0.221, 0.221, 0.002, 0.215, 0.221, 0.222, 0.214, 0.001, 0.215, 0.214, 0.214, 0.001, 0.212, 0.219, 0.212, 0.212, 0.001, 0.217, 0.22, 0.002, 0.217, 0.215, 0.001, 0.001, 0.214, 0.223, 0.001, 0.219, 0.213, 0.001, 0.002, 0.002, 0.001, 0.002, 0.212, 0.212, 0.214, 0.212, 0.212, 0.214, 0.213, 0.002, 0.003, 0.214, 0.213], [0.239, 0.221, 0.218, 0.002, 0.001, 0.214, 0.002, 0.215, 0.255, 0.002, 0.243, 0.218, 0.002, 0.001, 0.213, 0.001, 0.002, 0.22, 0.003, 0.219, 0.221, 0.234, 0.24, 0.235, 0.232, 0.002, 0.233, 0.001, 0.221, 0.004, 0.233, 0.218, 0.222, 0.004, 0.221, 0.22, 0.218, 0.214, 0.235, 0.218, 0.002, 0.001, 0.212, 0.213, 0.215, 0.005, 0.214, 0.214, 0.248, 0.239, 0.235, 0.226, 0.215, 0.002, 0.217, 0.002, 0.214, 0.217, 0.211, 0.003, 0.221, 0.001, 0.23, 0.22, 0.22, 0.244, 0.239, 0.014, 0.236, 0.013, 0.241, 0.225, 0.221, 0.001, 0.218, 0.001, 0.237, 0.218, 0.234, 0.223], [0.241, 0.218, 0.216, 0.001, 0.22, 0.214, 0.001, 0.223, 0.221, 0.236, 0.217, 0.001, 0.215, 0.225, 0.002, 0.002, 0.224, 0.217, 0.219, 0.219, 0.218, 0.225, 0.225, 0.229, 0.227, 0.226, 0.225, 0.218, 0.232, 0.216, 0.218, 0.218, 0.238, 0.218, 0.221, 0.001, 0.001, 0.002, 0.217, 0.001, 0.218, 0.218, 0.227, 0.218, 0.217, 0.219, 0.223, 0.002, 0.002, 0.219, 0.001, 0.218, 0.215, 0.221, 0.228, 0.225, 0.233, 0.221, 0.218, 0.001, 0.22, 0.218, 0.221, 0.225, 0.218, 0.001, 0.22, 0.001, 0.216, 0.226, 0.219, 0.213, 0.226, 0.237, 0.228, 0.234, 0.001, 0.221, 0.221, 0.219], [0.015, 0.219, 0.217, 0.222, 0.001, 0.238, 0.219, 0.235, 0.001, 0.218, 0.001, 0.216, 0.223, 0.231, 0.244, 0.001, 0.219, 0.231, 0.225, 0.227, 0.001, 0.217, 0.227, 0.215, 0.213, 0.002, 0.233, 0.001, 0.227, 0.217, 0.001, 0.222, 0.216, 0.219, 0.223, 0.226, 0.001, 0.222, 0.215, 0.001, 0.226, 0.001, 0.226, 0.219, 0.228, 0.002, 0.219, 0.222, 0.219, 0.233, 0.223, 0.001, 0.001, 0.224, 0.223, 0.001, 0.219, 0.222, 0.223, 0.234, 0.002, 0.227, 0.222, 0.001, 0.228, 0.002, 0.22, 0.212, 0.001, 0.213, 0.003, 0.215, 0.001, 0.215, 0.001, 0.001, 0.212, 0.219, 0.218, 0.001], [0.231, 0.219, 0.219, 0.004, 0.001, 0.235, 0.014, 0.221, 0.222, 0.213, 0.001, 0.236, 0.271, 0.222, 0.217, 0.227, 0.001, 0.012, 0.001, 0.001, 0.222, 0.22, 0.218, 0.219, 0.001, 0.218, 0.224, 0.225, 0.215, 0.001, 0.001, 0.218, 0.221, 0.22, 0.229, 0.222, 0.002, 0.012, 0.225, 0.241, 0.222, 0.219, 0.224, 0.22, 0.233, 0.001, 0.228, 0.218, 0.002, 0.223, 0.217, 0.219, 0.22, 0.212, 0.001, 0.212, 0.221, 0.001, 0.226, 0.212, 0.002, 0.225, 0.223, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.234, 0.216, 0.215, 0.219, 0.001, 0.22, 0.002, 0.002, 0.215, 0.22, 0.002], [0.015, 0.23, 0.217, 0.215, 0.217, 0.235, 0.213, 0.212, 0.215, 0.214, 0.001, 0.214, 0.212, 0.213, 0.001, 0.215, 0.001, 0.001, 0.001, 0.001, 0.214, 0.003, 0.22, 0.212, 0.211, 0.213, 0.215, 0.212, 0.001, 0.231, 0.225, 0.223, 0.001, 0.213, 0.217, 0.217, 0.216, 0.213, 0.215, 0.214, 0.213, 0.001, 0.235, 0.216, 0.213, 0.22, 0.214, 0.216, 0.214, 0.001, 0.224, 0.213, 0.221, 0.217, 0.001, 0.221, 0.001, 0.218, 0.215, 0.233, 0.215, 0.001, 0.001, 0.214, 0.214, 0.221, 0.214, 0.213, 0.212, 0.215, 0.214, 0.001, 0.216, 0.219, 0.001, 0.003, 0.001, 0.215, 0.214, 0.215], [0.014, 0.214, 0.002, 0.226, 0.215, 0.001, 0.215, 0.004, 0.231, 0.001, 0.214, 0.216, 0.001, 0.218, 0.001, 0.214, 0.001, 0.216, 0.221, 0.219, 0.212, 0.001, 0.222, 0.215, 0.002, 0.001, 0.217, 0.001, 0.213, 0.214, 0.001, 0.001, 0.002, 0.234, 0.213, 0.001, 0.215, 0.217, 0.214, 0.001, 0.001, 0.001, 0.227, 0.001, 0.001, 0.217, 0.221, 0.003, 0.001, 0.001, 0.216, 0.223, 0.232, 0.229, 0.225, 0.226, 0.236, 0.22, 0.224, 0.22, 0.226, 0.222, 0.223, 0.231, 0.222, 0.222, 0.002, 0.217, 0.216, 0.214, 0.002, 0.213, 0.212, 0.212, 0.223, 0.212, 0.212, 0.214, 0.233, 0.22]]
#AP3_avg_delays = [0.012962499999999998, 0.0276125, 0.019287500000000003, 0.016587499999999998, 0.016425000000000002, 0.022549999999999997, 0.019400000000000004, 0.02195, 0.0198625, 0.0193875, 0.019437499999999996, 0.024937499999999998, 0.019775, 0.0221375, 0.019575, 0.01925, 0.0111375, 0.019700000000000002, 0.016624999999999997, 0.013850000000000001, 0.0244875, 0.01945, 0.0226, 0.0251375, 0.0193625, 0.0137375, 0.0223875, 0.0109875, 0.022075000000000004, 0.021962500000000003, 0.016675, 0.022075, 0.02225, 0.0221125, 0.024837500000000005, 0.021949999999999997, 0.019225, 0.016487500000000002, 0.027925, 0.019412499999999992, 0.0165375, 0.0110125, 0.02245, 0.021787499999999998, 0.0193, 0.016575, 0.022025, 0.021849999999999998, 0.019575000000000002, 0.019612499999999998, 0.02495, 0.021975, 0.024712500000000002, 0.024775000000000002, 0.014174999999999998, 0.0166375, 0.0223625, 0.0191, 0.024625, 0.0224, 0.01935, 0.016774999999999998, 0.0253, 0.0219, 0.0164875, 0.014325000000000001, 0.016749999999999998, 0.0136625, 0.019499999999999997, 0.024962500000000002, 0.0168, 0.024512500000000003, 0.0192125, 0.019362499999999998, 0.0191625, 0.014000000000000002, 0.0165625, 0.024687500000000005, 0.0277125, 0.019362499999999998]
#AP3_total_delay = [80.45199999999996, 79.65700000000001, 85.35499999999998, 79.80299999999994, 81.41100000000002, 85.74299999999994, 84.08899999999994, 80.19999999999995, 84.10900000000002, 83.55999999999993]
AP3_all_delays = [[0.227, 0.225, 0.221, 0.226, 0.223, 0.236, 0.221, 0.225, 0.216, 0.001, 0.218, 0.214, 0.002, 0.216, 0.218, 0.229, 0.001, 0.218, 0.002, 0.22, 0.001, 0.227, 0.222, 0.218, 0.218, 0.215, 0.236, 0.219, 0.222, 0.214, 0.22, 0.219, 0.227, 0.221, 0.001, 0.223, 0.002, 0.224, 0.219, 0.219, 0.218, 0.22, 0.22, 0.22, 0.001, 0.001, 0.001, 0.227, 0.218, 0.216, 0.214, 0.217, 0.225, 0.221, 0.235, 0.233, 0.228, 0.216, 0.216, 0.217, 0.214, 0.213, 0.215, 0.219, 0.214, 0.213, 0.214, 0.216, 0.215, 0.213, 0.214, 0.213, 0.213, 0.215, 0.213, 0.214, 0.214, 0.218, 0.219, 0.219], [0.23, 0.223, 0.216, 0.217, 0.002, 0.001, 0.217, 0.217, 0.214, 0.221, 0.219, 0.001, 0.217, 0.216, 0.221, 0.216, 0.226, 0.222, 0.22, 0.226, 0.233, 0.226, 0.224, 0.223, 0.228, 0.001, 0.001, 0.222, 0.239, 0.001, 0.232, 0.223, 0.221, 0.002, 0.001, 0.223, 0.217, 0.225, 0.002, 0.001, 0.227, 0.217, 0.003, 0.001, 0.218, 0.01, 0.003, 0.216, 0.213, 0.214, 0.215, 0.222, 0.235, 0.221, 0.218, 0.227, 0.221, 0.001, 0.223, 0.249, 0.001, 0.227, 0.218, 0.226, 0.001, 0.228, 0.001, 0.221, 0.245, 0.221, 0.227, 0.22, 0.222, 0.228, 0.222, 0.226, 0.217, 0.001, 0.221, 0.22], [0.234, 0.002, 0.216, 0.214, 0.001, 0.219, 0.221, 0.002, 0.001, 0.001, 0.219, 0.001, 0.226, 0.001, 0.222, 0.219, 0.224, 0.002, 0.001, 0.001, 0.219, 0.225, 0.223, 0.001, 0.223, 0.001, 0.219, 0.222, 0.223, 0.216, 0.219, 0.004, 0.218, 0.227, 0.001, 0.22, 0.214, 0.221, 0.001, 0.225, 0.227, 0.221, 0.001, 0.002, 0.221, 0.221, 0.22, 0.215, 0.219, 0.226, 0.221, 0.23, 0.226, 0.219, 0.235, 0.219, 0.001, 0.002, 0.002, 0.229, 0.217, 0.222, 0.221, 0.227, 0.001, 0.219, 0.222, 0.223, 0.222, 0.22, 0.001, 0.217, 0.222, 0.215, 0.216, 0.218, 0.223, 0.22, 0.219, 0.219], [0.239, 0.218, 0.222, 0.229, 0.217, 0.219, 0.002, 0.226, 0.223, 0.216, 0.223, 0.001, 0.221, 0.217, 0.002, 0.228, 0.002, 0.219, 0.217, 0.225, 0.223, 0.002, 0.002, 0.223, 0.226, 0.001, 0.229, 0.223, 0.222, 0.001, 0.216, 0.222, 0.225, 0.001, 0.227, 0.213, 0.216, 0.215, 0.229, 0.001, 0.001, 0.228, 0.001, 0.224, 0.218, 0.226, 0.223, 0.226, 0.225, 0.005, 0.219, 0.001, 0.217, 0.002, 0.226, 0.226, 0.234, 0.002, 0.221, 0.001, 0.218, 0.001, 0.218, 0.233, 0.001, 0.224, 0.224, 0.225, 0.218, 0.217, 0.001, 0.001, 0.228, 0.222, 0.218, 0.227, 0.22, 0.001, 0.229, 0.001], [0.013, 0.218, 0.218, 0.001, 0.229, 0.218, 0.218, 0.23, 0.22, 0.23, 0.001, 0.217, 0.001, 0.217, 0.001, 0.001, 0.22, 0.217, 0.216, 0.214, 0.214, 0.001, 0.001, 0.218, 0.233, 0.001, 0.22, 0.231, 0.213, 0.222, 0.226, 0.219, 0.22, 0.222, 0.219, 0.222, 0.001, 0.226, 0.222, 0.231, 0.222, 0.228, 0.22, 0.225, 0.226, 0.224, 0.224, 0.001, 0.22, 0.218, 0.218, 0.002, 0.223, 0.223, 0.001, 0.221, 0.001, 0.218, 0.001, 0.22, 0.216, 0.219, 0.219, 0.215, 0.222, 0.214, 0.213, 0.215, 0.002, 0.001, 0.001, 0.215, 0.001, 0.217, 0.001, 0.217, 0.217, 0.22, 0.216, 0.002], [0.019, 0.215, 0.218, 0.238, 0.22, 0.001, 0.219, 0.226, 0.002, 0.001, 0.217, 0.231, 0.234, 0.001, 0.222, 0.23, 0.222, 0.222, 0.002, 0.216, 0.002, 0.224, 0.221, 0.001, 0.23, 0.221, 0.218, 0.23, 0.002, 0.231, 0.215, 0.221, 0.221, 0.002, 0.002, 0.001, 0.217, 0.216, 0.224, 0.219, 0.221, 0.223, 0.22, 0.222, 0.001, 0.22, 0.221, 0.222, 0.228, 0.214, 0.001, 0.218, 0.001, 0.214, 0.001, 0.228, 0.003, 0.221, 0.004, 0.001, 0.215, 0.001, 0.236, 0.222, 0.001, 0.222, 0.002, 0.001, 0.002, 0.219, 0.239, 0.005, 0.213, 0.212, 0.212, 0.22, 0.222, 0.221, 0.004, 0.222], [0.018, 0.226, 0.002, 0.212, 0.217, 0.002, 0.001, 0.001, 0.225, 0.002, 0.217, 0.001, 0.213, 0.002, 0.214, 0.225, 0.254, 0.214, 0.216, 0.213, 0.214, 0.214, 0.001, 0.215, 0.001, 0.002, 0.001, 0.217, 0.001, 0.218, 0.213, 0.215, 0.222, 0.213, 0.218, 0.002, 0.216, 0.001, 0.001, 0.214, 0.216, 0.222, 0.219, 0.214, 0.224, 0.218, 0.214, 0.001, 0.218, 0.216, 0.212, 0.215, 0.001, 0.214, 0.001, 0.001, 0.226, 0.22, 0.215, 0.226, 0.001, 0.001, 0.216, 0.217, 0.221, 0.231, 0.217, 0.223, 0.215, 0.219, 0.233, 0.001, 0.002, 0.215, 0.216, 0.222, 0.002, 0.218, 0.001, 0.225], [0.019, 0.002, 0.215, 0.002, 0.22, 0.215, 0.216, 0.215, 0.213, 0.214, 0.213, 0.212, 0.217, 0.213, 0.213, 0.214, 0.215, 0.215, 0.001, 0.001, 0.002, 0.212, 0.215, 0.002, 0.216, 0.216, 0.215, 0.011, 0.217, 0.001, 0.221, 0.005, 0.001, 0.001, 0.216, 0.001, 0.222, 0.002, 0.224, 0.001, 0.001, 0.219, 0.228, 0.212, 0.233, 0.002, 0.212, 0.226, 0.216, 0.001, 0.001, 0.233, 0.002, 0.232, 0.221, 0.216, 0.218, 0.215, 0.216, 0.223, 0.217, 0.29, 0.218, 0.229, 0.217, 0.002, 0.002, 0.001, 0.001, 0.223, 0.217, 0.001, 0.231, 0.219, 0.219, 0.234, 0.252, 0.002, 0.216, 0.223], [0.18, 0.218, 0.003, 0.004, 0.215, 0.255, 0.219, 0.002, 0.216, 0.274, 0.247, 0.003, 0.254, 0.214, 0.214, 0.216, 0.215, 0.002, 0.004, 0.002, 0.257, 0.007, 0.223, 0.219, 0.218, 0.218, 0.003, 0.226, 0.221, 0.222, 0.223, 0.23, 0.221, 0.223, 0.232, 0.223, 0.235, 0.219, 0.001, 0.223, 0.222, 0.214, 0.216, 0.221, 0.221, 0.221, 0.226, 0.222, 0.214, 0.212, 0.213, 0.213, 0.213, 0.002, 0.002, 0.214, 0.004, 0.22, 0.257, 0.005, 0.217, 0.243, 0.22, 0.22, 0.033, 0.256, 0.22, 0.224, 0.002, 0.003, 0.227, 0.218, 0.224, 0.234, 0.242, 0.221, 0.217, 0.002, 0.25, 0.001], [0.036, 0.238, 0.22, 0.23, 0.225, 0.217, 0.214, 0.23, 0.003, 0.228, 0.22, 0.002, 0.232, 0.002, 0.003, 0.228, 0.217, 0.223, 0.002, 0.003, 0.003, 0.232, 0.219, 0.002, 0.219, 0.002, 0.229, 0.002, 0.229, 0.229, 0.002, 0.22, 0.227, 0.22, 0.004, 0.222, 0.222, 0.222, 0.003, 0.004, 0.221, 0.225, 0.226, 0.243, 0.002, 0.222, 0.219, 0.223, 0.225, 0.224, 0.226, 0.223, 0.225, 0.002, 0.23, 0.22, 0.002, 0.218, 0.224, 0.001, 0.001, 0.222, 0.213, 0.213, 0.214, 0.002, 0.002, 0.213, 0.002, 0.213, 0.213, 0.212, 0.213, 0.213, 0.218, 0.001, 0.214, 0.001, 0.214, 0.216]]
AP3_avg_delays = [0.015187500000000001, 0.0223125, 0.021887499999999997, 0.0196625, 0.0221125, 0.019787500000000003, 0.02185, 0.019675, 0.0191625, 0.01735, 0.024925, 0.0110375, 0.022712500000000004, 0.0162375, 0.019125, 0.025075000000000004, 0.022450000000000005, 0.021925000000000004, 0.0110125, 0.0165125, 0.0171, 0.019624999999999997, 0.019387500000000002, 0.016525, 0.02515, 0.010975, 0.0196375, 0.0225375, 0.0223625, 0.0194375, 0.024837500000000005, 0.022225, 0.0250375, 0.01665, 0.0140125, 0.019374999999999996, 0.022025, 0.022137499999999997, 0.014074999999999999, 0.016725, 0.0222, 0.0277125, 0.019425, 0.022300000000000004, 0.019562500000000003, 0.019562500000000003, 0.0220375, 0.0222375, 0.027449999999999995, 0.021824999999999997, 0.02175, 0.022175000000000004, 0.0196, 0.019375, 0.017124999999999998, 0.025062499999999998, 0.014225000000000002, 0.0191625, 0.019737499999999998, 0.01715, 0.0189625, 0.0204875, 0.027424999999999998, 0.027762500000000006, 0.0140625, 0.0226375, 0.016462499999999998, 0.022025, 0.014049999999999998, 0.0218625, 0.019662500000000003, 0.0162875, 0.0221125, 0.027375, 0.024712500000000002, 0.025, 0.024975, 0.013799999999999998, 0.0223625, 0.01935]
AP3_total_delay = [81.5109999999999, 90.662, 80.54999999999991, 82.56499999999996, 82.38200000000002, 83.61299999999999, 78.8309999999999, 83.04299999999996, 83.15900000000003, 82.11599999999987]

ROOT_all_delays = [[0.04, 0.013, 0.222, 0.011, 0.213, 0.214, 0.227, 0.226, 0.22, 0.217, 0.221, 0.215, 0.22, 0.226, 0.234, 0.22, 0.235, 0.223, 0.01, 0.011, 0.016, 0.23, 0.219, 0.017, 0.011, 0.216, 0.223, 0.021, 0.222, 0.018, 0.226, 0.01, 0.009, 0.012, 0.238, 0.015, 0.228, 0.01, 0.227, 0.011, 0.012, 0.232, 0.226, 0.224, 0.231, 0.017, 0.211, 0.216, 0.223, 0.018, 0.009, 0.217, 0.012, 0.216, 0.232, 0.219, 0.227, 0.213, 0.233, 0.215, 0.217, 0.225, 0.224, 0.229, 0.228, 0.01, 0.011, 0.012, 0.015, 0.224, 0.23, 0.009, 0.23, 0.213, 0.212, 0.226, 0.214, 0.012, 0.214, 0.213], [0.031, 0.214, 0.011, 0.02, 0.233, 0.228, 0.215, 0.022, 0.011, 0.221, 0.22, 0.009, 0.217, 0.214, 0.214, 0.214, 0.228, 0.012, 0.01, 0.212, 0.217, 0.013, 0.218, 0.217, 0.218, 0.223, 0.014, 0.213, 0.214, 0.218, 0.224, 0.216, 0.214, 0.22, 0.218, 0.224, 0.214, 0.219, 0.01, 0.217, 0.218, 0.22, 0.224, 0.22, 0.227, 0.213, 0.22, 0.222, 0.223, 0.225, 0.231, 0.223, 0.217, 0.012, 0.016, 0.221, 0.02, 0.22, 0.214, 0.024, 0.213, 0.226, 0.214, 0.213, 0.013, 0.216, 0.212, 0.225, 0.01, 0.017, 0.213, 0.218, 0.217, 0.219, 0.216, 0.217, 0.221, 0.013, 0.215, 0.011], [0.032, 0.214, 0.223, 0.217, 0.216, 0.212, 0.212, 0.225, 0.212, 0.225, 0.215, 0.012, 0.219, 0.01, 0.019, 0.223, 0.221, 0.215, 0.009, 0.012, 0.012, 0.221, 0.222, 0.032, 0.225, 0.014, 0.219, 0.01, 0.226, 0.223, 0.01, 0.217, 0.227, 0.22, 0.017, 0.224, 0.229, 0.213, 0.016, 0.223, 0.217, 0.213, 0.218, 0.216, 0.021, 0.221, 0.213, 0.212, 0.222, 0.214, 0.216, 0.214, 0.213, 0.014, 0.223, 0.22, 0.015, 0.212, 0.229, 0.019, 0.013, 0.222, 0.231, 0.215, 0.223, 0.02, 0.01, 0.216, 0.01, 0.23, 0.213, 0.214, 0.224, 0.211, 0.213, 0.01, 0.213, 0.014, 0.22, 0.218]]
ROOT_avg_delays = [0.0012875, 0.0055125, 0.0057, 0.0031, 0.008275000000000001, 0.008175, 0.008175, 0.005912499999999999, 0.0055375, 0.0082875, 0.0082, 0.0029500000000000004, 0.0082, 0.005625, 0.005837500000000001, 0.008212500000000001, 0.008549999999999999, 0.005625, 0.0003625, 0.0029375, 0.0030625, 0.0058000000000000005, 0.0082375, 0.0033250000000000003, 0.005675, 0.0056625, 0.0057, 0.0030499999999999998, 0.008275000000000001, 0.0057374999999999995, 0.00575, 0.0055375, 0.005625, 0.0056500000000000005, 0.005912499999999999, 0.005787499999999999, 0.0083875, 0.005525, 0.0031625, 0.0056375, 0.0055875000000000005, 0.0083125, 0.00835, 0.00825, 0.005987500000000001, 0.005637499999999999, 0.00805, 0.008125, 0.00835, 0.0057125, 0.0057, 0.008175, 0.005525, 0.0030250000000000003, 0.0058874999999999995, 0.00825, 0.003275, 0.0080625, 0.008450000000000001, 0.003225, 0.0055375, 0.0084125, 0.0083625, 0.008212500000000001, 0.0058000000000000005, 0.003075, 0.0029125, 0.0056625, 0.00043750000000000006, 0.0058874999999999995, 0.0082, 0.0055125, 0.0083875, 0.0080375, 0.0080125, 0.0056625, 0.0081, 0.0004875, 0.0081125, 0.005525]
ROOT_total_delay = [75.35200000000002, 76.08299999999998, 74.38399999999997]


#AP3_DELAY = [0.240, 0.221, 0.001, 0.213, 0.221, 0.217, 0.213, 0.213, 0.214, 0.219, 0.001, 0.212, 0.213, 0.212, 0.218, 0.002, 0.220, 0.213, 0.218, 0.001, 0.214, 0.002, 0.213, 0.220, 0.218, 0.230, 0.222, 0.218, 0.226, 0.228, 0.221, 0.001, 0.216, 0.219, 0.222, 0.218, 0.222, 0.216, 0.217, 0.224, 0.221, 0.222, 0.001, 0.220, 0.223, 0.212, 0.232, 0.001, 0.214, 0.221, 0.222, 0.001, 0.213, 0.216, 0.213, 0.214, 0.216, 0.212, 0.212, 0.212, 0.214, 0.215, 0.223, 0.001, 0.224, 0.001, 0.231, 0.223, 0.222, 0.220, 0.224, 0.214, 0.222, 0.215, 0.219, 0.213, 0.001, 0.212, 0.215, 0.001, 0.216, 0.001, 0.219, 0.221, 0.222, 0.218, 0.221, 0.228, 0.222, 0.218, 0.002, 0.218, 0.218, 0.217, 0.226, 0.220, 0.225, 0.218, 0.218, 0.219]
#AP5_DELAY = [0.220, 0.219, 0.215, 0.212, 0.214, 0.215, 0.214, 0.216, 0.221, 0.227, 0.214, 0.219, 0.218, 0.217, 0.222, 0.222, 0.22, 0.217, 0.213, 0.215, 0.214, 0.22, 0.212, 0.216, 0.213, 0.213, 0.22, 0.218, 0.22, 0.218, 0.229, 0.215, 0.221, 0.222, 0.212, 0.214, 0.215, 0.219, 0.212, 0.215, 0.213, 0.219, 0.225, 0.235, 0.213, 0.214, 0.218, 0.001, 0.212, 0.216, 0.212, 0.001, 0.217, 0.25, 0.214, 0.219, 0.212, 0.212, 0.215, 0.214, 0.214, 0.221, 0.234, 0.002, 0.23, 0.001, 0.227, 0.214, 0.226, 0.228, 0.224, 0.233, 0.223, 0.222, 0.221, 0.224, 0.226, 0.231, 0.216, 0.22, 0.218, 0.216, 0.22, 0.219, 0.221, 0.214, 0.216, 0.221, 0.219, 0.212, 0.001, 0.215, 0.214, 0.217, 0.212, 0.213, 0.212, 0.212, 0.213, 0.213]

AP3_hits = 0
AP5_hits = 0
AP3_miss_delays = []
AP5_miss_delays = []
AP3_hit_delays = []
AP5_hit_delays = []
AP3_hit_list = []
AP5_hit_list = []

for delays in AP3_all_delays:
    for d in delays:
        if d < 0.1:
            AP3_hits += 1
            AP3_hit_list.append(1)
            AP3_hit_delays.append(d)
        else:
            AP3_hit_list.append(0)
            AP3_miss_delays.append(d)

for delays in AP5_all_delays:
    for d in delays:
	    if d < 0.1:
	        AP5_hits += 1
	        AP5_hit_list.append(1)
	        AP5_hit_delays.append(d)
	    else:
	        AP5_hit_list.append(0)
	        AP5_miss_delays.append(d)

#bwm-ng --output csv --unit bytes -d M -t 40000 -T sum --count 0 
#-F /home/ubuntu/mag/experiments/AP3_100_c.csv --sumhidden 0 --daemon 1 
#--interfaces s1-eth3,s2-eth1,s3-eth1,s4-eth1,s5-eth1,s6-eth1,s7-eth1,s8-eth1,s9-eth1,s10-eth1,s11-eth1,s12-eth1,s13-eth1,s14-eth1,s15-eth1,s16-eth1,s17-eth1,s18-eth1,s19-eth1,s20-eth1,s21-eth1,s22-eth1,s23-eth1,s24-eth1,s25-eth1,s26-eth1,s27-eth1,s28-eth1,s29-eth1,s30-eth1,s31-eth1,s32-eth1,s33-eth1,s34-eth1,s35-eth1,s36-eth1,s37-eth1,s38-eth1,s39-eth1,s40-eth1,s41-eth1,s42-eth1,s43-eth1,s44-eth1,s45-eth1,s46-eth1,s47-eth1,s48-eth1,s49-eth1,s50-eth1,s51-eth1,s52-eth1,s53-eth1,s54-eth1,s55-eth1,s56-eth1,s57-eth1,s58-eth1,s59-eth1,s60-eth1,s61-eth1,s62-eth1,s63-eth1,s64-eth1,s65-eth1,s66-eth1,s67-eth1,s68-eth1,s69-eth1,s70-eth1,s71-eth1,s72-eth1,s73-eth1,s74-eth1,s75-eth1,s76-eth1,s77-eth1,s78-eth1,s79-eth1,s80-eth1,s81-eth1,s82-eth1,s83-eth1,s84-eth1,s85-eth1,s86-eth1,s87-eth1,s88-eth1,s89-eth1,s90-eth1,s91-eth1,s92-eth1,s93-eth1,s94-eth1,s95-eth1,s96-eth1,s97-eth1,s98-eth1,s99-eth1,s100-eth1,s101-eth1,s102-eth1,s103-eth1,s104-eth1,s105-eth1,s106-eth1,s107-eth1,s108-eth1,s109-eth1,s110-eth1,s111-eth1,s112-eth1,s113-eth1,s114-eth1,s115-eth1

depths = {'s1-eth3': 0, 's2-eth1': 1, 's3-eth1': 2, 's4-eth1': 2, 's5-eth1': 1, 's6-eth1': 2, 's7-eth1': 2}
traffic = {3: [0, 0, 0], 5: [0, 0, 0]}
packets = {3: [0, 0, 0], 5: [0, 0, 0]}
std = {3: [], 5: []}

fieldnames = ['timestamp', 'interface', 'tx', 'rx',
 'total', 'packets_out', 'packets_in', 'packets_total', 'errors_out', 'errors_in']
for exp in [3,5]:
    with open('experiments/2AP%d_u1_c400_r440_all.csv' % exp, 'rb') as csvfile:
        rows = csv.DictReader(csvfile, fieldnames, delimiter=';')
        for row in rows:
            if row['interface'] != 'total':
                std[exp].append(float(row['total']) / float(1024 * 1024))
                traffic[exp][depths[row['interface']]] += float(row['total']) / float(1024 * 1024)
                packets[exp][depths[row['interface']]] += int(row['packets_total'])

    for j in range(0, len(traffic)):
        traffic[exp][j] = traffic[exp][j] / float(10)
        packets[exp][j] = packets[exp][j] / float(10)


N = 3

menStd = (2, 3, 4, 1, 2)
std3 = np.std(std[3])
std5 = np.std(std[5])
ind = [0, 0.8, 1.6]#np.arange(N)  # the x locations for the groups
ind2 = [0.2, 1, 1.8]

width = 0.2       # the width of the bars

print traffic[5]
fig, ax = plt.subplots()
rects1 = ax.barh(ind, tuple(reversed(traffic[3])), width, color='r', xerr=std3, ecolor='k')

rects2 = ax.barh(ind2, tuple(reversed(traffic[5])), width, color='b', xerr=std5, ecolor='k')

# add some text for labels, title and axes ticks
ax.set_ylabel('Topology depth')
ax.set_xlabel('Data transfered [MB]')


ax.set_title('Traffic by depth and cache location for 1 user')
ax.set_yticks(ind2)
ax.set_yticklabels(('2', '1', 'G'))
ax.legend((rects1[0], rects2[0]), ('1-median', '2-median'), bbox_to_anchor=(0., 0.50, 1., .102))

#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)

plt.show()



print "AP3 hits: %d  Hit rate: %.2f%%" % (AP3_hits, AP3_hits / float(len(AP3_DELAY)))
print "AP5 hits: %d  Hit rate: %.2f%%" % (AP5_hits, AP5_hits / float(len(AP5_DELAY)))

print "\nAP3 average miss del#ay: " + str(np.mean(np.array(AP3_miss_delays)))
print "AP5 average miss delay: " + str(np.mean(np.array(AP5_miss_delays)))

print "\nAP3 average hit delay: " + str(np.mean(np.array(AP3_hit_delays)))
print "AP5 average hit delay: " + str(np.mean(np.array(AP5_hit_delays)))

print "\nAP3 average total delay: " + str(np.mean(np.array(AP3_DELAY)))
print "AP5 average total delay: " + str(np.mean(np.array(AP5_DELAY)))

df1 = pd.DataFrame({'delay' : AP3_DELAY})
rm1 = pd.expanding_mean(df1, 10)

df2 = pd.DataFrame({'delay' : AP5_DELAY})
rm2 = pd.expanding_mean(df2, 10)


#plt.plot(range(1,len(rm1) + 1), rm1, 'r')
#plt.plot(range(1,len(rm2) + 1), rm2, 'b')


#plt.plot(range(1,len(AP3_DELAY) + 1), AP3_DELAY, 'r', label='Single Median - AP1')
#plt.plot(range(1,len(AP5_DELAY) + 1), AP5_DELAY, 'b', label='2-median - S3')
#plt.xlabel('Number of requests', fontsize=18)
#plt.ylabel('Delay [ms]', fontsize=16)

#plt.plot(range(1,len(AP3_td) + 1), AP3_td, 'r--', range(1,len(AP5_td) + 1), AP5_td, 'g--') 
#plt.show()