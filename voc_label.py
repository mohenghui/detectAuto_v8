import xml.etree.ElementTree as ET
import os
import os.path
from os import getcwd
from os.path import join

# 可配置的变量
dataset_path = '/root/autodl-tmp/ultralytics-main/datasets/plane'
annotations_folder = join(dataset_path, 'Annotations')
labels_folder = join(dataset_path, 'labels')
images_folder = join(dataset_path, 'images')
sets = ['train', 'test', 'val']
classes = ['E2',"J20","B2","F14","Tornado","F4","B52","JAS39","Mirage2000"]
# "  0: B2
#   1: B52
#   2: E2
#   3: F14
#   4: F4
#   5: J20
#   6: JAS39
#   7: Mirage2000
#   8: Tornado
# "
#   0: E2
#   1: J20
#   2: B2
#   3: F14
#   4: Tornado
#   5: F4
#   6: B52
#   7: JAS39
#   8: Mirage2000
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(image_id):
    xml_file = join(annotations_folder, '%s.xml' % image_id)
    if os.path.isfile(xml_file):
        in_file = open(xml_file)
        out_file = open(join(labels_folder, '%s.txt' % image_id), 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

for image_set in sets:
    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)
    image_ids = open(join(dataset_path, '%s.txt' % image_set)).read().strip().split()
    list_file = open(join(dataset_path, '%s.txt' % image_set), 'w')
    for image_id in image_ids:
        list_file.write(join(images_folder, '%s.jpg\n' % image_id))
        convert_annotation(image_id)
    list_file.close()
