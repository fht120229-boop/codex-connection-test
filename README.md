# 电池铭牌 OCR 工具链

这个仓库把铭牌识别和少样本外观识别拆成可运行的 Python 管线，并提供移动端接入说明：

1. **ProductLabel-OCR 流程**：OpenCV 放大、灰度化、双边滤波、Otsu 二值化，再把结果交给 OCR，并抽取品牌、型号、容量、电压和生产日期等结构化字段。
2. **PaddleOCR**：识别中文、英文、数字和电池型号文字。
3. **Ultralytics YOLO**：先定位电池或铭牌，再裁剪给 OCR；也可接入分类或分割模型。
4. **YOLO Flutter**：移动端使用摄像头和 TFLite/Core ML 模型做实时定位，详见 [`docs/mobile-integration.md`](docs/mobile-integration.md)。
5. **MMPreTrain 与 DINOv2**：少量自采照片时用于迁移学习、特征提取和相似图片检索，详见 [`docs/transfer-learning.md`](docs/transfer-learning.md)。
6. **二维码/条码识别**：使用 OpenCV `QRCodeDetector`，可选 zxing-cpp 扩展一维条码格式。

## 使用

基础依赖：

```bash
pip install -r requirements.txt
```

启用 YOLO、EasyOCR、PaddleOCR 和更广的条码格式：

```bash
pip install -r requirements-optional.txt
```

只运行二维码和图像预处理时，可以跳过可选依赖。运行完整流程：

```bash
python run_pipeline.py ./battery-nameplate.jpg --yolo-model ./weights/text-detector.pt
```

没有 YOLO 权重时仍可运行 PaddleOCR：

```bash
python run_pipeline.py ./battery-nameplate.jpg
```

少样本迁移学习依赖单独列在 `requirements-transfer.txt`，避免普通 OCR 部署安装大型训练栈。

## 输出和证据规则

`BatteryOCRPipeline.run()` 返回结构化字段、`ocr_text`、文字区域、二维码结果、使用的 OCR 引擎、化学体系证据和冲突标记。只有识别到明确的 `LFP/LiFePO4/磷酸铁锂`、`NMC/NCM/三元锂`、`NCA`、`LMO`、`LCO` 或 `铅酸` 文字时才输出对应化学体系；品牌、外观、颜色、电压、容量和无法解释的二维码编号不会被当成化学体系证据。多种显式标记冲突时输出 `UNKNOWN` 并设置 `chemistry_conflict=true`，交给人工复核。

## 上游参考

- [ProductLabel-OCR](https://github.com/RamesanPP/ProductLabel-OCR)
- [vertex_yolo_easyocr](https://github.com/francisco-shotquality/vertex_yolo_easyocr)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [OpenCV QRCodeDetector](https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html)
- [zxing-cpp](https://github.com/zxing-cpp/zxing-cpp)
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [YOLO Flutter](https://github.com/ultralytics/yolo-flutter-app)
- [MMPreTrain](https://github.com/open-mmlab/mmpretrain)
- [DINOv2](https://github.com/facebookresearch/dinov2)

Ultralytics YOLO 使用 AGPL-3.0；如果把 YOLO 服务或修改后的组件用于闭源商业产品，请先完成许可证评估。EasyOCR、PaddleOCR、zxing-cpp 和模型权重的条款也以各自上游仓库为准。本仓库只提供适配层，不复制上游模型或代码。
