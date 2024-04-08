import _thread
import time
from spider import passenger,update_sight
from mechineLearning import use_textCNN
import subprocess

def run_restart():
    # 构建迁移命令
    command1 = ['python', 'manage.py', 'runserver']

    # 执行命令
    try:
        # subprocess.check_call 会等待命令完成，并在命令返回非零退出码时抛出异常
        subprocess.check_call(command1)
        print("Restart have been applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error applying Restart: {e}")

    # 需要线程执行的函数
def print_time(threadName,delay):
    print("开启线程,线程id",_thread.get_ident())
    # count = 0
    # while count<5:
    #     time.sleep(delay)
    #     count += 1
    #     # ctime 以本地时区时间显示时间
    #     time_now = time.strftime("%H:%M:%S", time.localtime())
    #     print(time_now)

    # 这里之后写一个死循环，到时间点执行更新函数 ，这里要设sleep不然太耗cpu，判断给他一个区间；定时任务更新数据库记得使用django的save
    while True:
        time_now = time.strftime("%H:%M", time.localtime())  # 刷新
        time.sleep(delay)
        if time_now == "14:00":  # 此处设置每天定时的时间

            # 此处3行替换为需要执行的动作
            print('触发自动更新。。。')
            # passenger.passenger() # 特定景点+客流量更新（推荐）
            # update_sight.updateTask() # 更新全部景点（注意：景点有2000+，更新一次需要10h+，不推荐）
            time.sleep(66)  # 因为以秒定时，所以暂停66秒，使之不会在60秒内执行多次
            use_textCNN.textCNNTask()
            run_restart()

def doTask():
    try:
        # 开始创建一个新的线程
        _thread.start_new_thread(print_time,("thread_1",4))
    except:
        print("无法启动新的线程,这会导致无法更新数据")
