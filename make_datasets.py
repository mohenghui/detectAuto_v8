import csv
import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def find_image_file(dataset_folder, base_filename):
    for file in os.listdir(dataset_folder):
        if os.path.splitext(file)[0] == base_filename and file.endswith(('.png', '.jpg', '.jpeg')):
            return file
    return None

def convert_csv_to_xml_and_copy_images(dataset_folder, annotations_folder, images_folder):
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for file in os.listdir(dataset_folder):
        if file.endswith('.csv'):
            csv_file_path = os.path.join(dataset_folder, file)
            base_filename = os.path.splitext(file)[0]
            image_filename = find_image_file(dataset_folder, base_filename)

            if not image_filename:
                continue  # 如果找不到相应的图片文件，则跳过

            # 复制图片文件到images文件夹
            shutil.copy(os.path.join(dataset_folder, image_filename), os.path.join(images_folder, image_filename))

            root = ET.Element("annotation")
            ET.SubElement(root, "folder").text = images_folder
            ET.SubElement(root, "filename").text = image_filename
            ET.SubElement(root, "path").text = os.path.join(images_folder, image_filename)
            source = ET.SubElement(root, "source")
            ET.SubElement(source, "database").text = "Unknown"

            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                first_row = next(reader, None)
                if first_row:
                    size = ET.SubElement(root, "size")
                    ET.SubElement(size, "width").text = first_row['width']
                    ET.SubElement(size, "height").text = first_row['height']
                    ET.SubElement(size, "depth").text = "3"
                    ET.SubElement(root, "segmented").text = "0"

                    create_object_element(root, first_row)

                    for row in reader:
                        create_object_element(root, row)

            formatted_xml = prettify(root)
            xml_filename = base_filename + '.xml'
            with open(os.path.join(annotations_folder, xml_filename), 'w') as xmlfile:
                xmlfile.write(formatted_xml)

def create_object_element(root, row):
    object_elem = ET.SubElement(root, "object")
    ET.SubElement(object_elem, "name").text = row['class']
    ET.SubElement(object_elem, "pose").text = "Unspecified"
    ET.SubElement(object_elem, "truncated").text = "0"
    ET.SubElement(object_elem, "difficult").text = "0"
    bndbox = ET.SubElement(object_elem, "bndbox")
    ET.SubElement(bndbox, "xmin").text = row['xmin']
    ET.SubElement(bndbox, "ymin").text = row['ymin']
    ET.SubElement(bndbox, "xmax").text = row['xmax']
    ET.SubElement(bndbox, "ymax").text = row['ymax']

# 使用示例
dataset_folder = r"D:\vscode_work\bisai\dataset\train"  # 数据集文件夹路径
annotations_folder = r"D:\vscode_work\bisai\ultralytics-main\data\plane\Annotations"  # Annotations文件夹路径
images_folder = r"D:\vscode_work\bisai\ultralytics-main\data\plane\images"  # 图片文件夹路径

convert_csv_to_xml_and_copy_images(dataset_folder, annotations_folder, images_folder)
