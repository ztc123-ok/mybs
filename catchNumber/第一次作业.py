import  pymysql

connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou", charset="utf8")
cursor = connect.cursor()

sql = "insert into textCNN(embedding,epoch,learning_rate,max_len,batch_size,hidden_num,accuracy,precisions,recall,specificity,best_use) " \
      "values (20,15,0.001,20,10,2,87.37,82.35,93.33,82.00,1)"
cursor.execute(sql)
connect.commit()
cursor.close()
connect.close()

