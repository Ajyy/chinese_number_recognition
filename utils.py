class Number:
    def __init__(self, offset, length, value):
        self.offset = offset
        self.length = length
        self.value = value


# 以utf-8的格式导入相关文件
def load_file(path):
    lines = []
    with open(path, 'r', encoding='utf_8') as file:
        for line in file:
            lines.append(line)

    return lines
