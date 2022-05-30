# import sys
import torch
# import torch.nn as nn
from PIL import Image
# import numpy as np
# import cv2
# from torchvision.models.resnet import resnet50
# from torchvision.models.vgg import vgg16
# from torchvision.models.alexnet import alexnet
from torchvision import transforms
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)])
#
# net = alexnet(pretrained=True)
# # weight = torch.load('models/densenet121-a639ec97.pth')
# # net.load_state_dict(weight)
# net.eval()
# img = Image.open('images/1.jpg')
# img_t = preprocess(img)
# batch_t = torch.unsqueeze(img_t, 0)
# out = net(batch_t)
# _, predicted = torch.max(out, 1)
# # print('pred :',out, predicted)
# print('pred :', predicted)

from pytorch_grad_cam import GradCAM, ScoreCAM, GradCAMPlusPlus, AblationCAM, XGradCAM, EigenCAM
from pytorch_grad_cam.utils.image import show_cam_on_image, \
                                         deprocess_image, \
                                         preprocess_image
from torchvision.models import resnet50
import cv2
import numpy as np
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# 1.加载模型
model = resnet50(pretrained=True) #预先训练
# 2.选择目标层
# target_layer = model.layer4[-1]
target_layer = [model.layer4]
image_path = 'images/1.jpg'
rgb_img = cv2.imread(image_path, 1)[:, :, ::-1]   # 1是读取rgb
                                                 #imread返回从指定路径加载的图像
# rgb_img = cv2.imread(image_path, 1) #imread()读取的是BGR格式
rgb_img = np.float32(rgb_img) / 255

input_tensor = preprocess_image(rgb_img, mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])


#----------------------------------------
'''
3)初始化CAM对象，包括模型，目标层以及是否使用cuda等
'''
# Construct the CAM object once, and then re-use it on many images:
cam = GradCAM(model=model, target_layers=target_layer, use_cuda=False)
'''
4)选定目标类别，如果不设置，则默认为分数最高的那一类
'''
# If target_category is None, the highest scoring category
# will be used for every image in the batch.
# target_category can also be an integer, or a list of different integers
# for every image in the batch.
target_category = None
#指定类：target_category = 281

'''
5)计算cam
'''
# You can also pass aug_smooth=True and eigen_smooth=True, to apply smoothing.
grayscale_cam = cam(input_tensor=input_tensor)  # [batch, 224,224]

#----------------------------------
'''
6)展示热力图并保存
'''
# In this example grayscale_cam has only one image in the batch:
# 7.展示热力图并保存, grayscale_cam是一个batch的结果，只能选择一张进行展示
grayscale_cam = grayscale_cam[0]
visualization = show_cam_on_image(rgb_img, grayscale_cam)  # (224, 224, 3)
cv2.imwrite(f'first_try.jpg', visualization)