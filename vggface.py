import threading
import queue
import os
import glob
from urllib import request

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'}
timeout = 20


class VggFace(threading.Thread):
    def __init__(self, root, thread_id, que_num, que_und, que_txt):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.que_und = que_und
        self.que_txt = que_txt
        self.que_num = que_num
        self.root = root

    def run(self):
        while not self.que_txt.empty():
            txt_file = self.que_txt.get_nowait()
            name = txt_file[:-4]
            file = open('{}/files/{}'.format(self.root, txt_file), 'r')
            info = open('{}/raw/{}/info.txt'.format(self.root, name), 'w')
            for liner in file:
                self.download(liner, name, info)
            info.close()
            file.close()

    def download(self, liner, name, info):
        content = liner.split(' ')
        url = content[1]
        point = str(content[2:]).replace(' ', ',')
        format = url[-3:]

        counter = len(glob.glob('{}/{}/*'.format(self.root, name)))

        try:
            req = request.Request(url, headers=headers)
            response = request.urlopen(req, timeout=timeout)
            data = response.read()
            save_path = '{}/raw/{}/{}.{}'.format(self.root, name, counter+1, format)
            file = open(save_path, 'bw')
            file.write(data)
            collect_info = '{}\t{}\t{}\n'.format(name, save_path, point)
            info.writelines(collect_info)
            print('thread-{}: No{:6d}, save to {} success'
                  .format(self.thread_id, self.que_num.get(), save_path))
        except:
            self.que_und.put(liner)
            print('thread-{}: {} fail'.format(self.thread_id, url))


def get_name_queue_list(file_list, num_thread):
    que_name = queue.Queue()
    que_num = queue.Queue()
    que_list = []

    ave_que_len = int(len(file_list) / num_thread)

    for file in file_list:
        que_name.put_nowait(file)

    number = 0
    for n in range(num_thread):
        que_list.append(queue.Queue())
        counter = 0
        while counter < ave_que_len and not que_name.empty():
            que_list[n].put_nowait(que_name.get_nowait())
            counter += 1
            number += 1
            que_num.put_nowait(number)

    # the last
    while not que_name.empty():
        que_list[-1].put_nowait(que_name.get_nowait())
        number += 1
        que_num.put_nowait(number)

    return que_list, que_num


def grab_faces(root, num_thread):
    file_list = os.listdir('{}/files'.format(root))

    queue_list, number_que = get_name_queue_list(file_list, num_thread)
    assert len(queue_list) == num_thread

    queue_list_und = queue.Queue()

    # create faces reptiles
    thread_list = []
    for n in range(num_thread):
        reptile = VggFace(root, n, number_que, queue_list_und, queue_list[n])
        reptile.start()
        thread_list.append(reptile)

    for thread in thread_list:
        thread.join()

    file_und = open('{}/vggface_und.txt'.format(root), 'w')
    while not queue_list_und.empty():
        liner = queue_list_und.get_nowait()
        file_und.write(liner)

    file_und.close()

    print('finish {}...'.format(type))



if __name__ == '__main__':
    grab_faces('vggface', 6)