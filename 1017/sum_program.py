import os
os.system('clear')
print("\n")
while True:
    N = int(input("請輸入數字N: "))
    
    if N <= 1024:
        # 如果N小於等於1024
        sum = 0
        for i in range(1, N+1):
            sum = sum + i
        print(sum)
    else:
        # 如果N大於1024
        n = N % 1024
        sum = 0
        for i in range(1, n+1):
            sum = sum + i
        print(sum)
    print("\n")
