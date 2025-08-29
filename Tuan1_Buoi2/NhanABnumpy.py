import numpy as np
import time
Max = 1000

a = np.ones((Max, Max), dtype=int)
b = np.ones((Max, Max), dtype=int)

#micro seconds
start_time = time.perf_counter()

c = np.zeros((Max, Max), dtype=int)
c = np.dot(a, b)

end_time = time.perf_counter()

print("Thoi gian chay la", (end_time - start_time) * 1e6, "micro giay")
