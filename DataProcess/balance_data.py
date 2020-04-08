import pandas as pd
from tqdm import tqdm
import argparse

def balance_label(data_path: str):
    data = pd.read_csv(data_path, engine = 'python', encoding = 'utf-8')
    dim = data.shape[0]
    balance_data = pd.DataFrame(columns = ['text', 'label'])
    line = 0
    label0 = 0
    for _, cov in tqdm(data.iterrows(), desc = '均衡进度', total = dim, ncols = 120):
        label = cov['label']
        text = cov['text']
        if label == 1 or label == -1:
            balance_data.loc[line] = {'text': text, 'label': label}
            line += 1

        elif label == 0 and label0 % 2 == 0:
            balance_data.loc[line] = {'text': text, 'label': label}
            line += 1
        if label == 0:
            label0 += 1
    print(balance_data.shape)
    balance_data.to_csv(data_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trainset', default='CoV_train.csv', type=str, help='要均衡的训练集路径')
    parser.add_argument('--testset', default='CoV_test.csv', type=str, help='要均衡的测试集路径')

    opt = parser.parse_args()
    balance_label(opt.trainset)
    balance_label(opt.testset)

if __name__ == '__main__':
    main()
    