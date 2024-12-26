import os
import json

folder_path = './img_save'
classes = {'123':0,'567':1}



files = os.listdir(folder_path)
json_files = [file for file in files if file.endswith('.json')]
for json_file in json_files:
    json_path = os.path.join(folder_path, json_file)
    txt_path = os.path.join(folder_path, json_file.replace('.json','.txt'))
    with open(json_path, 'r') as file:
        data = json.load(file)
        height = data['imageHeight']
        width = data['imageWidth']

        for object_ in range(len(data['shapes'])) :
            content_ = str(classes[data['shapes'][object_]['label']])
            for xpoint, ypoint in data['shapes'][object_]['points'] :
                content_ = content_ + f' {round(xpoint/width,3)}'
                content_ = content_ + f' {round(ypoint/height,3)}'
            
            with open(txt_path, 'a') as txt_file :
                txt_file.write(content_)
                txt_file.write('\n')
        

