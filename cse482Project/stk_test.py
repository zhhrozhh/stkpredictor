from stk_alu import *
import sys
if __name__ == '__main__':
    stk_code = sys.argv[1]
    salu = StkALU(code = stk_code,n=2)
    salu.set_training_data()
    salu.n_day_naive_bayes_train()
    x = salu.n_day_naive_bayes_dist()
    #salu.n_gram_train()
    #x = salu.n_gram_dist()
    #print(salu.n_day_naive_bayes_feature_counter)
    #print(x.dist)
    #print(log(2))
    #print(salu.n_day_naive_bayes_label_counter)
    x.plot()