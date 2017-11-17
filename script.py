
import os



def make_directory(path, type):
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


if __name__ == '__main__':
    # make directory
    make_directory('H:\DATA\FaceScrub', 'actors')
    make_directory('H:\DATA\FaceScrub', 'actresses')
