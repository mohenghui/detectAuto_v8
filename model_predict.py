from ultralytics import YOLO
import cv2
import os

class predict():
    def __init__(self, weight_path='plane.pt'):
        # 获取当前脚本的完整路径
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        # 构建权重文件的完整路径
        full_weight_path = os.path.join(current_script_path, weight_path)
        self.model = YOLO(full_weight_path)
    def detect_image(self, image_path):
        results = []
        results_yolo = self.model(image_path)
        for r in results_yolo:
            tmp_r = r.boxes
            for xyxy, conf, cls in zip(tmp_r.xyxy, tmp_r.conf, tmp_r.cls):
                # 将Tensor转换为标准Python类型
                xmin, ymin, xmax, ymax = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                conf = float(conf)
                class_pred = int(cls)

                results.append([ymin, xmin, ymax, xmax, conf, class_pred])

        # self.draw_boxes(image_path, results)
        return results

    def draw_boxes(self, image_path, results):
        # 读取图像
        img = cv2.imread(image_path)
        for res in results:
            ymin, xmin, ymax, xmax, conf, class_pred = res
            # 绘制矩形框
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            # 添加文本
            text = f'Class: {class_pred}, Conf: {conf:.2f}'
            cv2.putText(img, text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 创建保存路径
        save_folder = './result'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        save_path = os.path.join(save_folder, os.path.basename(image_path))

        # 保存图像
        cv2.imwrite(save_path, img)

if __name__ == "__main__":
    p = predict(weight_path='./plane.pt')
    image_path = r"./data/J20zhandouji_Bing_0216.jpeg"
    results = p.detect_image(image_path)
    print(results)
    p.draw_boxes(image_path,results)
