from tqdm import tqdm
import pandas as pd
import argparse
from data_process import forward_filter, other_filter, title_filter
import csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='nCoV_100k_train.labled.csv', type=str)
    parser.add_argument('--save_name', default='CoVData.csv', type=str)
    opt = parser.parse_args()
    data = pd.DataFrame(columns = ['text', 'time'])
    line = 0
    with open(opt.data_path) as csv_python:
        reader = csv.reader(csv_python, delimiter=',')
        next(reader)
        for lines in tqdm(reader, desc='处理进度', ncols = 120):
            text = lines[1]
            time = lines[7]
            forward_text = forward_filter(text)
            title_text = title_filter(forward_text)
            other_text = other_filter(title_text)
            data.loc[line] = {'text': other_text, 'time': time,}
            line += 1
        save_name = './datasets/{}'.format(opt.save_name)
        data.to_csv(save_name)
            
if __name__ == '__main__':
    main()