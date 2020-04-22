import re

def forward_filter(text: str):
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

def title_filter(text: str):
    str_text = ''
    text_list = list(text)
    stack = []
    dict_text = {'#':'#', '【':'】'}
    for s in text_list:
        if len(stack) == 0:
            str_text += s
            
        elif s == '#' and dict_text['#'] == stack[len(stack)-1]:
            stack.pop()
            str_text = ''
            continue

        elif s == '】' and '】' == stack[len(stack)-1]:
            stack.pop()
            str_text = ''
            continue

        if s == '#' or s == '【':
            stack.append(dict_text[s])
            str_text = ''
        
            
    return str_text
        

def other_filter(text: str):
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