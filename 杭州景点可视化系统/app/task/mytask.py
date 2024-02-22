import _thread
import time

# 需要线程执行的函数
def print_time(threadName,delay):
    print("开启线程,线程id",_thread.get_ident())
    count = 0
    while count<5:
        time.sleep(delay)
        count += 1
        # ctime 以本地时区时间显示时间
        time_now = time.strftime("%H:%M:%S", time.localtime())
        print(time_now)

    # 这里之后写一个死循环，到时间点执行更新函数 ，这里要设sleep不然太耗cpu，判断给他一个区间
    # while True:
    #     time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    #     if time_now == "15:30:10":  # 此处设置每天定时的时间
    #
    #         # 此处3行替换为需要执行的动作
    #         print("hello")
    #         subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 定时发送测试"
    #         print(subject)
    #
    #         time.sleep(2)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次

def doTask():
    try:
        # 开始创建一个新的线程
        _thread.start_new_thread(print_time,("thread_1",2))
        _thread.start_new_thread(print_time,("thread_2",4))
    except:
        print("无法启动新的线程")
