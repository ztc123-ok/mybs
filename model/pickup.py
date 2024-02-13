import csv

# 打开原始CSV文件
with open('t_comment_detail.csv', 'r',encoding='utf-8') as file:
    reader = csv.reader(file)

    # 打开新CSV文件并写入标题行
    with open('good.csv', 'w', newline='', encoding='utf-8') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(['content', 'rating'])

        # 遍历原始CSV文件的每一行
        for row in reader:
            # 提取需要的两列数据
            column1 = row[6]
            column2 = row[9]

            if(len(column1)>30 and column2 == '好评'):
                # 将数据写入新CSV文件
                writer.writerow([column1, column2])