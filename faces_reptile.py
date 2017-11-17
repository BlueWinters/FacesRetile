
import threading
import time
import queue

class FacesReptile(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


def get_information_queue(path, type, num_thread):
    src_file = open('{}/facescrub_{}.txt'.format(path, type), 'r')
    liner_que = queue.Queue()

    # construct liner queue
    for liner in src_file:
        content = liner.split('\t')
        liner_que.put(content)

    # distribute urls
    counter = int(liner_que.qsize() / num_thread)
    queue_list = []
    for n in range(num_thread):
        queue_list.append(queue.Queue())
        i = 0
        while i < counter and not liner_que.empty():
            queue_list[n].put(liner_que.get())
            i += 0




def grab_faces(path, type, num_thread):
    src_file = open('{}/facescrub_{}.txt'.format(path, type), 'r')
    idx_file = open('{}/record/facescrub_idx_{}.txt'.format(path, type), 'w')
    liner_que = queue.deque()

    # construct liner queue
    for liner in src_file:
        content = liner.split('\t')
        liner_que.append(content)
        # print(content)

    # create faces reptile
    for n in range(num_thread):
        reptile = FacesReptile()





if __name__ == '__main__':
    get_information_queue('H:\DATA\FaceScrub', 'actors', 4)



    # src_file_actors = open('facescrub_actors.txt', 'r')
    # src_file_actresses = open('facescrub_actresses.txt', 'r')
    #
    #
    #
    # threadLock = threading.Lock()
    # threads = []
    #
    # # 创建新线程
    # thread1 = myThread(1, "Thread-1", 1)
    # thread2 = myThread(2, "Thread-2", 2)
    #
    # # 开启新线程
    # thread1.start()
    # thread2.start()
    #
    # # 添加线程到线程列表
    # threads.append(thread1)
    # threads.append(thread2)
    #
    # # 等待所有线程完成
    # for t in threads:
    #     t.join()

