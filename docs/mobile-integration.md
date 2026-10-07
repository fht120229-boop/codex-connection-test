# YOLO Flutter 移动端接入

[YOLO Flutter](https://github.com/ultralytics/yolo-flutter-app) 适合把“摄像头 → 电池/铭牌框选 → 裁剪”放到 Android 或 iOS 端。建议的移动端链路是：

```text
Camera
  -> YOLO TFLite/Core ML detector
  -> crop the nameplate region
  -> PaddleOCR service or mobile OCR runtime
  -> QR decoder
  -> evidence-only fields
```

移动端只上传裁剪后的铭牌图和 OCR/二维码证据，Python 服务负责 PaddleOCR、字段结构化和冲突检查。YOLO 模型需要按电池和铭牌类别重新训练；示例权重不能直接代表 LFP/NMC。相机端没有识别到铭牌时应返回“未检测到铭牌”，不要按电池外观猜化学体系。

Ultralytics 组件使用 AGPL-3.0。用于闭源商业应用前要完成许可证评估，并固定模型版本和权重来源。
