
import threading
import queue
import glob
from urllib import request

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'}
timeout = 20


class FaceScrub(threading.Thread):
    def __init__(self, thread_id, que_num, que_idx, que_und, que_liner):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.que_idx = que_idx
        self.que_und = que_und
        self.que_liner = que_liner
        self.que_num = que_num
        self.root = 'images'

    def run(self):
        while not self.que_liner.empty():
            liner = self.que_liner.get_nowait()
            self.download(liner)

    def download(self, liner):
        content = liner.split('\t')
        name = content[0].replace(' ', '_')
        img_id = content[1]
        face_id = content[2]
        url = content[3]
        bbox = content[4]
        format = url[-3:]

        counter = len(glob.glob('{}/{}/*'.format(self.root, name)))

        try:
            req = request.Request(url, headers=headers)
            response = request.urlopen(req, timeout=timeout)
            data = response.read()
            save_path = '{}/{}/{}.{}'.format(self.root, name, counter+1, format)
            file = open(save_path, 'bw')
            file.write(data)
            collect_info = '{}\t{}\t{}\t{}\t{}\n'\
                .format(name, save_path, bbox, img_id, face_id)
            self.que_idx.put(collect_info)
            print('thread-{}: No{:6d}, save to {} success'
                  .format(self.thread_id, self.que_num.get(), save_path))
        except:
            self.que_und.put(liner)
            print('thread-{}: {} fail'.format(self.thread_id, url))


def get_information_queue(type, num_thread):
    src_file = open('facescrub_{}.txt'.format(type), 'r')
    liner_que = queue.Queue()
    number_que = queue.Queue()

    # construct liner queue
    for liner in src_file:
        liner_que.put(liner)

    # distribute urls
    average_per_thread = int(liner_que.qsize() / num_thread)
    queue_list = []
    number = 0
    for n in range(num_thread):
        queue_list.append(queue.Queue())
        counter = 0
        while counter < average_per_thread and not liner_que.empty():
            queue_list[n].put_nowait(liner_que.get_nowait()) # no wait
            number += 1
            counter += 1
            number_que.put_nowait(number)

    # return queue list
    return queue_list, number_que


def grab_faces(path, type, num_thread):
    file_idx = open('record/facescrub_idx_{}.txt'.format(type), 'w')
    file_und = open('record/facescrub_und_{}.txt'.format(type), 'w')

    queue_list, number_que = get_information_queue('actors', num_thread)
    assert len(queue_list) == num_thread

    queue_list_idx = queue.Queue()
    queue_list_und = queue.Queue()

    # create faces reptiles
    thread_list = []
    for n in range(num_thread):
        reptile = FaceScrub(n, number_que, queue_list_idx,
                               queue_list_und, queue_list[n])
        reptile.start()
        thread_list.append(reptile)

    for thread in thread_list:
        thread.join()

    while not queue_list_idx.empty():
        liner = queue_list_idx.get_nowait()
        file_idx.write(liner)
    while not queue_list_und.empty():
        liner = queue_list_und.get_nowait()
        file_und.write(liner)

    file_idx.close()
    file_und.close()

    print('finish {}...'.format(type))



if __name__ == '__main__':
    grab_faces('images', 'actors', 6)
    grab_faces('images', 'actresses', 6)

