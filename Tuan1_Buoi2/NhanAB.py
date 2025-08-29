import time
Max = 1000

a = [[1 for _ in range(Max)] for _ in range(Max)]
b = [[1 for _ in range(Max)] for _ in range(Max)]

#micro seconds
start_time = time.perf_counter()
c = [[0 for _ in range(Max)] for _ in range(Max)]
for i in range(Max):
    for j in range(Max):
        for k in range(Max):
            c[i][j] += a[i][k] * b[k][j]

end_time = time.perf_counter() 

print("Thoi gian chay la", (end_time - start_time) * 1e6, "micro giay")
