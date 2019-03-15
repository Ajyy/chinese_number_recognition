from chinese_number_translate import cn_num_translate
from utils import load_file

data = load_file('data/number_data.txt')

for num in data:
    print('Original one:', num.strip('\n'))
    print('Translate:', cn_num_translate(num.strip('\n')))
    print()