
'''
This script used for transfering segmentation data format : yolo txt to labelme json
You need to put image file and yolo txt file in same path
only work on linux
'''

import base64, os, glob, json
from PIL import Image

### manual setting
txt_path ='./img_save/' # image/txt file path
class_ = ['Fall' , 'Stand'] # list element ordered by yolo classes


### script begin 
files = glob.glob( txt_path + '/*.txt')
json_ = {"version":"1.0.0", "flags":{}, "shapes":None,
             "imagePath":None, "imageData":None, "imageHeight":None, "imageWidth":None}
for txt_ in files :
    ### read Image
    image_path = txt_[:-4]+'.png'
    file_name = os.path.basename(image_path)
    img = Image.open(image_path)
    width, height = img.size
    encoded = base64.b64encode(open(image_path, "rb").read())
    #print(encoded)
    
    ### read txt
    with open(txt_, 'r') as contents:
        file_contents = contents.read()
        #print(file_contents)
        
    ### convert yolo points to labelme
    file_contents = file_contents.replace('\n',' ')
    yolopoints_ = file_contents.split(' ')
    cls_points_all = []; count_= 0
    for i in range(len(yolopoints_)) :
        if yolopoints_[i] == '' :
            continue
        if '.' not in yolopoints_[i] :
            label_ = class_[int(yolopoints_[i])]
            points_all = []; points_each = []
            cls_points_all.append([label_,points_all])
            count_ = 1 
        else :
            if count_%2 != 0 :
                points_each.append(round(width * float(yolopoints_[i]),3))
                count_ += 1
            else :
                points_each.append(round(height * float(yolopoints_[i]),3))
                points_all.append(points_each)
                points_each = []
                count_ += 1
    shape_content = []
    for j in cls_points_all :
        shape_content.append({"label":j[0], "points":j[1],"group_id":None,
            "description": "","shape_type": "polygon","flags": {}})
    
    ### write into json
    json_['shapes'] = shape_content
    json_['imagePath'] = file_name
    json_["imageHeight"] = height
    json_['imageWidth'] = width
    json_['imageData'] = str(encoded,encoding='utf-8')
    with open(txt_path + file_name[:-4] + '.json', 'w') as json_file:
        json.dump(json_, json_file, indent=2)

