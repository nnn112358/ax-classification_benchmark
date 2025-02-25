# ax-classification_benchmark


Environment
- MCU or Board name: "M5Stack Module-LLM(ax630c)"
- Operating System:
   "Linux m5stack-LLM 4.19.125 #1 SMP PREEMPT Thu Nov 14 17:40:17 CST 2024 aarch64 aarch64 aarch64 GNU/Linux"
- PyAXEngine version :"PyAXEngine 0.0.1 RC3"

## Model conversion
This runs on Ubuntu PC.
Download the model from Pytorch and perform static int8 quantization.
After this,Convert with Pulsar2. See sample mobilenetv2.

```
$ pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
$ cd model_conv
$ mkdir -p models
$ mkdir -p quantized_models
$ mkdir -p calibration_images
$ cd models
$ python classification_torch_model_export.py
$ cd ..
$ python onnx_quantize_static_image_batch.py
```


## execution
This runs on M5Stack Module-LLM.

```
root@m5stack-LLM:# wget https://github.com/AXERA-TECH/pyaxengine/releases/download/0.0.1rc3/axengine-0.0.1-py3-none-any.whl
root@m5stack-LLM:# pip install axengine-0.0.1-py3-none-any.whl
root@m5stack-LLM:# ./batch_run_onnx.sh
root@m5stack-LLM:# ./batch_run_axmodel.sh
```


## Result 
This is Process Time[msec]

| Model Name | CPU Process(onnxruntime) | CPU Process(onnxruntime) | NPU Process(pyaxengine) | NPU Process(pyaxengine) |
|------------|-------------------------|-------------------------|----------------------|----------------------|
|            | default (float32) | onnx-quantized (int8) | ax-model(quant) NPU1(half core) (int8) | ax-model(quant) NPU2(full core) (int8) |
| shufflenet_v2_x0_5 | 38.2 | 34.0 | 1.1 | 1.0 |
| shufflenet_v2_x1_0 | 91.3 | 62.4 | 1.4 | 1.5 |
| shufflenet_v2_x1_5 | 154.9 | 75.3 | 1.7 | 1.6 |
| shufflenet_v2_x2_0 | 276.8 | 150.8 | 5.5 | 2.4 |
| mobilenet_v2 | 221.4 | 88.5 | 1.7 | 1.4 |
| mobilenet_v3_large | 206.2 | 87.4 | 2.4 | 2.0 |
| squeezenet1_0 | 303.1 | 241.2 | 2.5 | 1.5 |
| squeezenet1_1 | 173.0 | 78.0 | 2.8 | 1.1 |
| resnet18 | 653.1 | 321.1 | 3.4 | 3.1 |
| resnet34 | 1317.5 | 645.8 | 5.7 | 5.1 |
| resnet50 | 1461.2 | 687.1 | 8.3 | 6.1 |
| resnet152 | 4104.1 | 1878.0 | 17.1 | 12.4 |
| vgg11 | 2529.1 | 1427.9 | 28.8 | 26.2 |
| vgg13 | 3785.1 | 1878.0 | 31.9 | 28.8 |
| vgg16 | 5141.4 | 2620.2 | 35.9 | 32.0 |
| vgg19 | 6408.4 | 3268.9 | 39.9 | 35.2 |


# AI モデル性能比較表

| モデル | NPU1(half core) (int8) | MACs | TOPS |
|-------------------|----------------------|-----------------|------|
| shufflenet_v2_x0_5 | 1.1 | 43,050,627 | 0.08 |
| shufflenet_v2_x1_0 | 1.4 | 149,074,867 | 0.21 |
| shufflenet_v2_x1_5 | 1.7 | 301,331,587 | 0.35 |
| shufflenet_v2_x2_0 | 5.5 | 590,568,883 | 0.21 |
| mobilenet_v2 | 1.7 | 319,949,192 | 0.38 |
| mobilenet_v3_large | 2.4 | 232,570,144 | 0.19 |
| squeezenet1_0 | 2.5 | 832,767,864 | 0.67 |
| squeezenet1_1 | 2.8 | 357,475,224 | 0.26 |
| resnet18 | 3.4 | 1,821,452,264 | 1.07 |
| resnet34 | 5.7 | 3,674,276,328 | 1.29 |
| resnet50 | 8.3 | 4,117,342,184 | 0.99 |
| resnet152 | 17.1 | 11,572,291,560 | 1.35 |
| vgg11 | 28.8 | 7,630,106,088 | 0.53 |
| vgg13 | 31.9 | 11,339,116,008 | 0.71 |
| vgg16 | 35.9 | 15,503,523,304 | 0.86 |
| vgg19 | 39.9 | 19,667,930,600 | 0.99 |

## Note:

Since the first execution of PyAXEngine was slow, I measured the execution time of the 2nd to 9th executions. See below.<br>
https://github.com/AXERA-TECH/pyaxengine/issues/17  
