# MMPreTrain 与 DINOv2 少样本路线

当自采照片数量较少时，可先用 YOLO 裁剪电池或铭牌，再用 MMPreTrain 微调分类头，或用 DINOv2 提取图像特征并做相似图片检索。推荐只把外观类别作为辅助信息：圆柱、软包、方形、品牌或铭牌可见度。

化学体系仍要依赖铭牌明文、二维码或可靠型号库。DINOv2/MMPreTrain 不能从普通 RGB 外观凭空推断 LFP、NMC 等内部化学体系；证据不足时继续输出 `UNKNOWN`。

安装训练依赖：

```bash
pip install -r requirements-transfer.txt
```

训练和评估时按品牌、光照、拍摄设备和背景分组切分数据，避免同一块电池的近似照片同时出现在训练集和验证集。模型权重和数据集许可证需单独记录。
