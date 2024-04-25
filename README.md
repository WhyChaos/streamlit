## 启动服务
```
streamlit run main.py --server.port 8000
```
## 安装依赖
```
pip install -r requirements.txt
```

## 创建镜像，创建容器并启动服务
```
docker build -t my-python-app .
docker run -d -p 42010:8000 --name test my-python-app

```

<h1 style="color:red;">注意</h1>
在effects/photo_effct.py中get_lang_sam_api()实现的是识别背景图中‘纸’的区域，返回的是bool数组。

目前是伪实现，返回的是固定bool数组


具体实现，调用 [LangSAM](https://github.com/luca-medeiros/lang-segment-anything) ，如下是大致代码。也可根据地址用docker部署

```
model = LangSAM()
image_pil = Image.open(image).convert("RGB")
text_prompt = 'paper'
masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)
masks_np = [mask.squeeze().cpu().numpy() for mask in masks]
return masks_np

```

