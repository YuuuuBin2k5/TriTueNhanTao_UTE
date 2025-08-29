
#include <bits/stdc++.h>
using namespace std;

const int MAX = 1000;

int a[MAX][MAX], b[MAX][MAX], c[MAX][MAX];

// Hàm tính thời gian chạy phép nhân ma trận
void thoiGianChay() {
    auto start = chrono::high_resolution_clock::now();
    for (int i = 0; i < MAX; i++) {
        for (int j = 0; j < MAX; j++) {
            for (int k = 0; k < MAX; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    auto end = chrono::high_resolution_clock::now();
    cout << chrono::duration_cast<chrono::microseconds>(end - start).count() << " microseconds" << endl;
}

int main() {
    thoiGianChay();

    return 0;
}

