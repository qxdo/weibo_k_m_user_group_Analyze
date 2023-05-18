import numpy as np

import random
import string


# 生成随机二维数组
arr = np.random.randint(0, 10000, size=(1000, 4))

print(arr[0])




# 定义敏感词长度和数量
num_rows = 1000
num_cols = 6
word_len = 8

# 生成随机敏感词列表
sensitive_words = []
for i in range(num_rows):
    row = []
    for j in range(num_cols):
        word = ''.join(random.choices(string.ascii_lowercase + string.digits, k=word_len))
        row.append(word)
    sensitive_words.append(row)

print(sensitive_words)
