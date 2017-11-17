
import threading
import time
import queue
import urllib.request

class FacesReptile(threading.Thread):
    def __init__(self, thread_id, que_idx, que_und, que_liner):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.que_idx = que_idx
        self.que_und = que_und
        self.que_liner = que_liner

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

        try:
            urllib.request.urlopen('http://upload.wikimedia.org/wikipedia/commons/5/5d/AaronEckhart10TIFF.jpg')
            urllib.urlretrieve()
        except:
            pass


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
            queue_list[n].put_nowait(liner_que.get_nowait()) # no wait
            i += 1
    # return queue list
    return queue_list


def grab_faces(path, type, num_thread):
    src_file = open('{}/facescrub_{}.txt'.format(path, type), 'r')
    idx_file = open('{}/record/facescrub_idx_{}.txt'.format(path, type), 'w')
    und_file = open('')

    queue_list = get_information_queue('H:\DATA\FaceScrub', 'actors', 4)
    assert len(queue_list) == num_thread

    queue_list_idx = queue.Queue()
    queue_list_und = queue.Queue()

    # create faces reptiles
    for n in range(num_thread):
        reptile = FacesReptile(n, queue_list_idx, queue_list_und, queue_list[n])
        reptile.start()

    # for





if __name__ == '__main__':
    # get_information_queue('H:\DATA\FaceScrub', 'actors', 4)
    # data = urllib.request.urlopen('http://upload.wikimedia.org/wikipedia/commons/5/5d/AaronEckhart10TIFF2.jpg')
    # data = urllib.request.urlopen('http://www.google.com.hk')
    # print(data.read())

    url = 'http://upload.wikimedia.org/wikipedia/commons/5/5d/AaronEckhart10TIFF.jpg'
    urllib.urlretrieve(url, 'tmp.jpg')
    try:
        data = urllib.request.urlopen(url)
        urllib.urlretrieve(url, 'tmp.jpg')
        print(data)
        print('success')
    except:
        print(data)
        print('fail')


