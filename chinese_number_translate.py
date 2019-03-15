from utils import Number

# 初始化一些基本参数，包括中文基本数字1-9与单位
chinese_num = {'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

units = {'亿': 100000000, '万': 10000, '千': 1000, '百': 100, '十': 10}
rules = {'个': 1}
keys = list(units.keys())
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        rules[keys[j] + keys[i]] = units[keys[i]] * units[keys[j]]
    rules[keys[i]] = units[keys[i]]


def preprocess_data(num):
    """
    预处理数据，包括清除数据中的','和'个'
    :param num: 中文数字（包括混合形式）
    :return: 返回处理后的数字
    """
    new_num = num
    for idx in reversed(range(len(num))):
        if num[idx] == '个' or num[idx] == ',':
            new_num = new_num[:idx] + new_num[idx + 1:]

    return new_num


def find_size(num):
    """
    依据单位从大到小原则，找出这个中文数字（包括混合形式）的最大单位
    :param num: 中文数字（包括混合形式）
    :return: 返回一个tuple，其中第一个元素是最大单位，第二个元素是这个单位所代表的大小
    """
    num_type = '个'
    for key in rules:
        if key in num:
            return key, rules[key]

    return num_type, rules[num_type]


def get_value(num):
    """
    获取经过处理的中文数字（包括混合形式）代表的阿拉伯形式值
    :param num: 中文数字（包括混合形式）
    :return: 返回num的阿拉伯数字形式
    """
    # 如果长度为0则返回0值
    if len(num) == 0:
        return 0

    # 如果这个数字是一个阿拉伯数字则转化成int返回
    if num.isdigit():
        return int(num)

    # 对个位数以及单个’十‘和首个字是’十‘的形式进行单独处理
    size = find_size(num)
    if size[0] == '个':
        if num[0] in chinese_num:
            return chinese_num[num[0]]
        else:
            return int(num[0])
    elif num == '十':
        return 10
    else:
        if num[0] == '十':
            num = '一' + num
        nums = num.split(size[0])

        if len(nums[1]) == 1:
            return get_value(nums[0]) * size[1] + get_value(nums[1]) * int(size[1] / 10)
        else:
            return get_value(nums[0]) * size[1] + get_value(nums[1])


def cn_num_translate(num):
    """
    计算中文数字（包括混合形式）的值
    :param num:
    :return:
    """
    value = 0
    nums = num.split('零')
    for sub_num in nums:
        value = value + get_value(preprocess_data(sub_num))
    return value


def process_sentence(line):
    """
    处理句子，把其中的中文数字，包括各种形式，提取出来
    :param line: 一句话
    :return: 返回这句话中中文数字的数组
    """
    nums_inf = []
    num = ''
    i = 0
    while i < len(line):
        while i < len(line) and \
                ((line[i].isdigit() or line[i] in chinese_num or line[i] in rules) or line[i] == ','):
            num = num + line[i]
            i = i + 1

        if len(num) != 0:

            nums_inf.append((num, i-len(num)+1))
            num = ''

        i = i + 1

    return nums_inf


def sentence_num_translate(sentence):
    """
    计算一个句子中数字信息的数组
    :param sentence: 一个句子
    :return: 返回这个句子中数字信息的数组
    """
    nums_inf = process_sentence(sentence)
    nums_set = []
    for num_inf in nums_inf:
        value = cn_num_translate(num_inf[0])
        nums_set.append(Number(num_inf[1], len(num_inf[0]), value))

    return nums_set
