import pandas as pd
from tqdm import tqdm

data_train_path = 'CoV_train.csv'
data_test_path = 'CoV_test.csv'

cov_data_train = pd.read_csv(data_train_path, engine = 'python', encoding = 'utf-8')
cov_data_test = pd.read_csv(data_test_path, engine = 'python', encoding = 'utf-8')

def label_count(data, data_type: str):
    dim = data.shape[0]
    label1, label0, label_1 = 0, 0, 0
    for cov_line, cov in tqdm(data.iterrows(), desc = data_type, total = dim, ncols = 120):
        label = cov['label']
        if label == 1:
            label1 += 1
        elif label == 0:
            label0 += 1
        else:
            label_1 += 1
    
    print('label1:', label1, 'label0:', label0, 'label-1:', label_1)

label_count(cov_data_train, '训练集')
label_count(cov_data_test, '测试集')
