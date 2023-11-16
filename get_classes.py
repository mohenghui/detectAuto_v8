import csv
import os

def collect_unique_classes(dataset_folder):
    classes = set()
    for file in os.listdir(dataset_folder):
        if file.endswith('.csv'):
            csv_file_path = os.path.join(dataset_folder, file)
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    classes.add(row['class'])
    return sorted(classes)

def write_classes_to_yaml(classes, yaml_file):
    with open(yaml_file, 'w') as file:
        file.write("names:\n")
        for index, class_name in enumerate(classes):
            file.write(f"  {index}: {class_name}\n")

# 使用示例
dataset_folder = r"D:\vscode_work\bisai\dataset\train"  # 数据集文件夹路径
yaml_file = r"D:\vscode_work\bisai\ultralytics-main\data\plane\classes.yaml"  # 输出的YAML文件路径

unique_classes = collect_unique_classes(dataset_folder)
write_classes_to_yaml(unique_classes, yaml_file)