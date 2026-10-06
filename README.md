# 电池铭牌 OCR 工具链

用于电池铭牌照片的文字识别、文字区域定位和二维码解码。推荐流程是：

1. 图像预处理：放大、灰度化、去噪、二值化。
2. 复杂背景先定位：用 YOLO 找到文字区域。
3. OCR 识别：使用 PaddleOCR（中文、英文、数字）。
4. 二维码单独解码：使用 OpenCV QRCodeDetector 或 zxing-cpp。

## 1. ProductLabel-OCR

- 项目地址：[RamesanPP/ProductLabel-OCR](https://github.com/RamesanPP/ProductLabel-OCR)
- 适用场景：电池铭牌识别参考实现。
- 处理步骤：放大、灰度化、去噪、二值化，再识别品牌、型号、容量、警告和条码等字段。

## 2. vertex_yolo_easyocr

- 项目地址：[francisco-shotquality/vertex_yolo_easyocr](https://github.com/francisco-shotquality/vertex_yolo_easyocr)
- 适用场景：铭牌倾斜、背景杂乱或文字位置不固定的照片。
- 工作方式：YOLO 先定位文字区域，再交给 EasyOCR 读取。

## 3. PaddleOCR

- 项目地址：[PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- 适用场景：核心 OCR 引擎。
- 特点：支持中文、英文、数字，也适合嵌入前两个项目或部署到移动端。
- 安装示例：

```bash
pip install paddleocr
```

## 4. 二维码识别

OCR 不能替代二维码解码。根据部署平台选择专用解码器：

- [OpenCV QRCodeDetector](https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html)：Python/C++ 快速集成。
- [zxing-cpp](https://github.com/zxing-cpp/zxing-cpp)：支持多种条码和二维码格式的 C++ 库。
- [mobile_scanner](https://pub.dev/packages/mobile_scanner)：Flutter 手机端方案。

## 推荐组合

复杂铭牌照片可以采用：

```text
OpenCV 预处理
    -> YOLO 文字区域定位
    -> PaddleOCR 文字识别
    -> QRCodeDetector / zxing-cpp 二维码解码
    -> 按字段输出品牌、型号、容量、警告和条码
```

## 说明

本仓库保存的是工具链参考和集成入口；各项目的源码、模型和许可证以其上游仓库为准。
