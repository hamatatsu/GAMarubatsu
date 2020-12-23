import matplotlib.pyplot as plt
import numpy as np
import random

def mating(pool):
    """ランダムに選ばれる両親から交差し、個体数を2倍にする。
       子のみのnewpoolを戻り値とする"""
    newpool = []
    for i in range(len(pool)):
        p1, p2 = random.choice(pool), random.choice(pool)
        # 遺伝子が交差する地点を一か所選ぶ
        crosspoint = int(random.random()*16)
        div = pow(2, crosspoint)
        # 遺伝子を交差させて入れ替える
        f1 = (p1 // div)*div + p2 % div 
        f2 = (p2 // div)*div + p1 % div
        newpool += [f1, f2]
    return newpool

def mutation(pool):
    "突然変異。20％の個体に、1部位の突然変異が起きる"
    for i in range(len(pool)//5):
        p_index = int(random.random()*len(pool))
        p1 = pool[p_index]
        mutate_point = int(random.random()*16)
        bit = pow(2, mutate_point)
        # bitを１つだけ反転させる
        p_bit = p1 & bit
#        p1 = p1 - p_bit + (bit - p_bit)
        p1 = p1 + bit - p_bit * 2
        pool[p_index] = p1
    return
    
def selection(pool) ->list:
    "2倍に増えた個体数をもとに自然淘汰する。上位から40％、下位から10％を残す"
    evaluate = []
    for i in pool:
        e = 16 - bin((i^d)).count("1")
        evaluate.append( (i, e) )
    evaluate.sort(key=lambda x:x[1], reverse=True)
    # 上位と下位に分ける
    l = len(evaluate)
    upper, lower = evaluate[:l//2], evaluate[l//2:]
    # random.shuffleはin placeで戻り値はNone
    random.shuffle(upper)
    random.shuffle(lower)
    survived = upper[:int(l*0.4)] + lower[:data_size - int(l*0.4)]
    return [i for i, e in survived]

def random_selection(pool):
    "自然淘汰をせずにランダムで個体を残す"
    random.shuffle(pool)
    return pool[:data_size] 

def print_evaluate(pool, generation, flag):
    """合致するビット数を評価 
       flat=True  のときは、各個体の評価を表示.
       flag=False のときは、世代数と平均のみ表示"""
    evaluate = []
    for i in pool:
        evaluate.append(16 - bin((i^d)).count("1"))
    if flag:
        for i, e in zip(pool, evaluate):
            print(bin(i)[2:].zfill(16),":", e)
    print("第{}世代".format(generation), end=" ")
    score = sum(evaluate)/len(evaluate)
    print("平均:", score, "\n"*flag)
    return score

def main(pool, select=True, print_flag=True):
    "世代を重ねるメインループ"
    generation = 0
    score = []
    score.append(print_evaluate(pool, generation, print_flag))
    for i in range(40):
        pool = mating(pool)
        mutation(pool)
        if select:
            pool = selection(pool)
        else:
            pool = random_selection(pool)
        generation += 1
        score.append(print_evaluate(pool, generation, print_flag))
    return score

if __name__ == "__main__":        
    d = 0b0101011000001111
    data_size = 20
    # initialize
    #pool = [int(random.random()*256) for i in range(data_size)]
    pool = np.random.randint(65536, size=data_size, dtype=int) 
    pool2 = pool.copy()
    
    scores = main(pool, select=True, print_flag=False)
    scores2 = main(pool2, select=False, print_flag=False)
    
    x = np.arange(len(scores))
    plt.plot(x, np.array(scores)/16, "-", label="selection")
    plt.plot(x, np.array(scores2)/16, ":", label= "without selection")
    plt.legend(fontsize=14)
    plt.ylim(0, 1)