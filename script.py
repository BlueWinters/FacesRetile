
import os
import glob


def make_directory_facescrub(path, type):
    src_file = open('{}/facescrub_{}.txt'.format(path, type), 'r')
    num_file = open('{}/facescrub_num_{}.txt'.format(path, type), 'w')
    name_dict = {}

    for liner in src_file:
        content = liner.split('\t')
        name = content[0].replace(' ', '_')
        img_id = content[1]
        face_id = content[2]
        url = content[3]
        bbox = content[4]

        # fast search
        if name not in name_dict:
            name_dict[name] = 1
        else:
            name_dict[name] += 1

        name_path = '{}/images/{}'.format(path, name)
        if not os.path.exists(name_path):
            os.makedirs(name_path)

    # write dict to files
    for name in name_dict:
        num_file.writelines('{}\t{}\n'.format(name, name_dict[name]))


def make_directory_vggface(src_path, out_path):
    file_list = glob.glob('{}/*.txt'.format(src_path))
    num_file = open('vggface_num_file.txt', 'w')
    name_dict = {}

    def get_images_number(file_path):
        file = open(file_path, 'r')
        counter = 0
        for liner in file:
            if liner is not '\n':
                counter += 1
        return counter

    for file in file_list:
        name = file[:-4]
        assert name is not None
        # make directory
        path = '{}/{}'.format(out_path, name)
        if not os.path.exists(path):
            os.mkdir(path)
        name_dict[name] = get_images_number('{}/{}'.format(src_path, file))

    # write dict to files
    for name in name_dict:
        num_file.writelines('{}\t{}\t'.format(name, name_dict[name]))



if __name__ == '__main__':
    # make directory
    make_directory_facescrub('H:\DATA\FaceScrub', 'actors')
    make_directory_facescrub('H:\DATA\FaceScrub', 'actresses')
