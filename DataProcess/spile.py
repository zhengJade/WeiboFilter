import pandas as pd
import numpy as np
import argparse

def spile_data(data, portion: int):
    data.drop_duplicates(keep='first', inplace=True)
    data = data.sample(frac=1.0)
    dim = data.shape[0]
    test_dim = dim * 0.05
    train_dim = dim - test_dim
    step = round(train_dim/portion)
    for i in range(portion):
        cov_data = data[i*step:(i+1)*step+1]
        cov_data.to_csv('CoVTrain{}.csv'.format(i))
    
    data_test = data[portion*step:]
    data_test.to_csv('CoVTest.csv')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--portion', default=4, type=int, help='spile dataset')
    parser.add_argument('--data', default='../DataProvider/CoVData.csv', type=str)
    opt = parser.parse_args()

    data = pd.read_csv(opt.data, engine = 'python', encoding = 'utf-8')
    spile_data(data, opt.portion)

if __name__ == '__main__':
    main()