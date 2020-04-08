import pandas as pd
import encode
from tqdm import tqdm
import re
import argparse

'''
trainPath = "~/train_dataset/nCoV_100k_train.labled.csv"        
#encode.re_encode(trainPath)

data = pd.read_csv(trainPath, engine ='python', encoding = 'utf-8')

train_data = data[2000:]
test_data = data[:2000]
train_data.to_csv('nCoV_100k_train.labled.csv')
test_data.to_csv('nCoV_100k_test.labled.csv')
print(test_data)
'''
class DataFilter(object):
    def __init__(self, data_path: str, train_name: str, test_name: str, csv_name: str):
        self.csv_train = train_name
        self.csv_test = test_name
        self.csv_name = csv_name
        cov_data = pd.read_csv(data_path, engine = 'python', encoding = 'utf-8')
        cov_data.dropna(axis=0,how='any', inplace = True)
        cov_data = cov_data[:10000]
        dim = cov_data.shape[0]

        self.data = pd.DataFrame(columns = ['text', 'label'])
        line = 0
        for cov_line, cov in tqdm(cov_data.iterrows(), desc='处理进度', total=dim, ncols = 120):
            text = cov['微博中文内容']
            label = cov['情感倾向']
            if label not in ['-1', '0', '1']:
                continue
            forward_text = self.forward_filter(text)
            title_text = self.title_filter(forward_text)
            other_text = self.other_filter(title_text)
            if other_text == '#':
                continue
            self.data.loc[line] = {'text': other_text, 'label': label}
            line += 1

    def forward_filter(self, text: str):
        str_text = ''
        count = 0
        text_list = list(text)
        for s in text_list:
            if s == '/' and count == 3:
                count = 2
                str_text = ''
                continue
            elif s == '/':
                count += 1
                continue
            if s == ':':
                str_text = ''
                continue
            str_text += s
        
        return str_text

    def title_filter(self, text: str):
        str_text = ''
        text_list = list(text)
        stack = []
        dict_text = {'#':'#', '】':'【'}
        for s in text_list:
            if len(stack) == 0:
                str_text += s
            
            elif s == '#' and dict_text['#'] == stack[len(stack)-1]:
                stack.pop()
                str_text = ''
                continue

            elif s == '】' and dict_text['】'] == stack[len(stack)-1]:
                stack.pop()
                str_text = ''
                continue

            if s == '#' or s == '【':
                stack.append(s)
                str_text = ''
        
        return str_text

    def other_filter(self, text: str):
        text = text.replace('网页链接', '')
        text = text.replace('评论配图', '')
        text = text.replace('原图来源', '')
        text = text.replace('展开全文', '')
        text = text.replace('转发微博', '')
        regex = re.compile(r'[^\u4e00-\u9fa5A-Za-z0-9]')
        text = regex.sub(' ', text)
        if len(text) <= 2:
            return '#'
        else:
            return text

    def text_spile(self, train: float, test: float):
        if train + test != 10 or train < 0 or test < 0:
            print('######### train 和 test 为切分比例，应该大于0且和小于10 ##########')
            return
        
        length = self.data.shape[0]
        train_len = length * (train/(train + test))
        train_len = int(train_len)

        train = self.data[:train_len]
        test = self.data[train_len:]

        train.to_csv(self.csv_train)
        test.to_csv(self.csv_test)

    def save_csv(self):
        print('>'*50, self.save_csv, '已保存')
        self.data.to_csv(self.csv_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spile', default='spile', type=str, help='是否直接切割数据集')
    parser.add_argument('--dataset_name', default='CoVData.csv', type=str)
    opt = parser.parse_args()
    print(opt.spile)
    data = DataFilter('~/train_dataset/nCoV_100k_train.labled.csv', 'CoV_train.csv', 'CoV_test.csv', 'CoVData.csv')
    if opt.spile == 'spile':
        data.save_csv()
    else:
        data.text_spile(9, 1)


if __name__ == '__main__':
    main()