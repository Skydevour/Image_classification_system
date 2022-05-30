from utils import log, httpserver, database, mysqlDB, exception, tools
import os
import json
import torch
from PIL import Image
from torchvision.models.resnet import resnet50
from torchvision.models.vgg import vgg16
from torchvision.models.alexnet import alexnet
import numpy as np
from torchvision import transforms
import cv2
import base64
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image, preprocess_image

labels = []
with open('imagenet-simple-labels.json') as f:
    labels = json.load(f)


@exception.exception_handler('contract')
async def _get_model_list(request):
    sql = "select id, model_type, filename,acc,param,model_size,in_use from classify_model where id>-1;"
    args = ()
    res = await mysqlDB.db_select(sql, args)
    data = {}
    if len(res) > 0:
        data['data'] = res
    log.logger.info(data)
    return httpserver.web_response(True, data)


@exception.exception_handler('contract')
async def _switch_use_status(request):
    res = json.loads(await request.text())
    model_id = res.get('id')
    sql = "update classify_model set in_use=0 where in_use=1;"
    args = ()
    await mysqlDB.db_exec(sql, args)
    sql = "update classify_model set in_use=1 where id=%s;"
    args = (model_id,)
    await mysqlDB.db_exec(sql, args)
    data = {}
    return httpserver.web_response(True, data)


@exception.exception_handler('contract')
async def _process_img(request):
    reader = await request.multipart()
    reader = await reader.next()
    filename = 'images/' + str(len(os.listdir('images'))) + '.jpg'
    with open(filename, 'wb') as f:
        while True:
            chunk = await reader.read_chunk()  # 默认是8192个字节。
            if not chunk:
                break
            f.write(chunk)
    sql = "select model_type, filename from classify_model where in_use=1;"
    res = await mysqlDB.db_select(sql, ())
    data = {}
    if res and len(res) > 0:
        model_filename = 'models/' + res[0].get('filename')
        model_type = res[0].get('model_type')
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )])
        if model_type == 0:
            net = vgg16(pretrained=False)
            target_layer = [net.features]
        elif model_type == 1:
            net = resnet50(pretrained=False)
            target_layer = [net.layer4]
        else:
            net = alexnet(pretrained=False)
            target_layer = [net.features]
        weight = torch.load(model_filename)
        net.load_state_dict(weight)
        net.eval()
        img = Image.open(filename)
        img_t = preprocess(img)
        batch_t = torch.unsqueeze(img_t, 0)
        out = net(batch_t)
        _, predicted = torch.topk(out, 5, 1)
        data['result'] = []
        img_cv = cv2.imread(filename, 1)[:, :, ::-1]
        img_cv = np.float32(img_cv) / 255
        input_tensor = preprocess_image(img_cv, mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
        cam = GradCAM(model=net, target_layers=target_layer, use_cuda=False)
        grayscale_cam = cam(input_tensor=input_tensor)
        grayscale_cam = grayscale_cam[0]
        visualization = show_cam_on_image(img_cv, grayscale_cam)  # (224, 224, 3)
        image = cv2.imencode('.jpg', visualization)[1]
        image_code = str(base64.b64encode(image))[2:-1]
        for item in predicted[0]:
            data['result'].append({'name': labels[int(item)]})
        data['model_type'] = model_type
        data['model_name'] = res[0].get('filename')
        data['heatmap'] = image_code
    return httpserver.web_response(True, data)


@exception.exception_handler('contract')
async def _upload_model(request):
    acc = float(request.headers.get('acc'))
    param = int(request.headers.get('paramCount'))
    model_type = int(request.headers.get('modelType'))
    filename = request.headers.get('filename')
    # model_size = int(request.headers.get('modelSize'))
    reader = await request.multipart()
    reader = await reader.next()
    filepath = 'models/' + filename
    with open(filepath, 'wb') as f:
        while True:
            chunk = await reader.read_chunk()  # 默认是8192个字节。
            if not chunk:
                break
            f.write(chunk)
    sql = "insert into classify_model (model_type, filename, acc, param, model_size, in_use) values (%s, %s, %s, %s, %s, %s);"
    args = (model_type, filename, acc, param, 0, 0)
    await mysqlDB.db_exec(sql, args)
    return httpserver.web_response(True, {})


def add_route(webapp):
    webapp.router.add_route('POST', '/get_model_list', _get_model_list)
    webapp.router.add_route('POST', '/upload_model', _upload_model)
    webapp.router.add_route('POST', '/process_img', _process_img)
    webapp.router.add_route('POST', '/switch_use_status', _switch_use_status)
