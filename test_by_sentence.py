from utils import load_file
from chinese_number_translate import sentence_num_translate

sentences = load_file('sentence_data.txt')
for sentence in sentences:
    print('Original sentence:', sentence.strip('\n'))
    print('Information:')
    inf_set = sentence_num_translate(sentence.strip('\n'))
    for inf in inf_set:
        print(inf.__dict__)
    print()
