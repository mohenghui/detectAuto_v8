import os
import xml.etree.ElementTree as ET

def collect_unique_classes_from_xml(annotations_folder):
    classes = set()
    for file in os.listdir(annotations_folder):
        if file.endswith('.xml'):
            xml_file_path = os.path.join(annotations_folder, file)
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            for object in root.findall('object'):
                class_name = object.find('name').text
                classes.add(class_name)
    return sorted(classes)

def write_classes_to_yaml(classes, yaml_file):
    with open(yaml_file, 'w') as file:
        file.write("names:\n")
        for index, class_name in enumerate(classes):
            file.write(f"  {index}: {class_name}\n")

# 使用示例
annotations_folder = r"D:\vscode_work\bisai\ultralytics-main\data\plane\Annotations"  # Annotations文件夹路径
yaml_file = r"D:\vscode_work\bisai\ultralytics-main\data\plane\classes.yaml"  # 输出的YAML文件路径

unique_classes = collect_unique_classes_from_xml(annotations_folder)
write_classes_to_yaml(unique_classes, yaml_file)
