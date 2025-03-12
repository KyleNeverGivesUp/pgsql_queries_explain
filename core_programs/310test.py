def Mystery(n):
    sum=0
    for i in range(1,n+1):
        for j in range(1,i+1):
            # print(f"i'm i: {i}")
            # print(f"i'm j: {j}")
            print(f"==============")
            print(f"==============")
            print(f"==============")
            sum=sum+1
    return sum
if "__main__" == __name__:
    print(Mystery(3))