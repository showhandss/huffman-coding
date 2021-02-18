n = 0
for i in range(1,21):
    T = 0
    TH = 0
    F = 0
    for j in range(1,i):
        T = T + 1
        for k in range(1,j):
            TH = TH + 1
            for m in range(1,k):
                n = n + 1
                F = F +1
                print("i=",i," j=",j," k=",k," m=",m," n=",n)
    print("F = ",F)
    print("TH = ",TH)
    print("T = ",T)
print(n)