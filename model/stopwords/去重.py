# 打开原始文本文件和新文件
with open('hit_stopwords.txt', 'r', encoding='utf-8') as original_file, \
        open('new_file.txt', 'w', encoding='utf-8') as new_file:
    # 创建一个空集合用于存储已遇到的行
    seen_lines = set()

    # 逐行读取和处理
    for line in original_file:
        # 去除行尾的换行符，这样我们可以比较纯文本内容
        line_content = line.rstrip('\n')

        # 如果行没有在集合中，则写入新文件并添加到集合中
        if line_content not in seen_lines:
            seen_lines.add(line_content)
            new_file.write(line)  # 保留原始行的换行符

print("重复行已去除，并已按原始顺序保存到new_file.txt。")