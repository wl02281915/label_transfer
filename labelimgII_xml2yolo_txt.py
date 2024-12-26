from lxml import etree
import os, cv2
import numpy as np

ori_path = './img_save'
save_path = './img_save'
filenames = os.listdir(ori_path)
pic_files = [f for f in filenames if f.endswith('.png') and os.path.isfile(os.path.join(ori_path, f))]
classes = ['line','dirty','shadow']

for pic_file in pic_files :
    list_ = []
    xml_name = f'{ori_path}/{pic_file[:-4]}.xml'; aft_txt = open(f'{xml_name[:-4]}'+'.txt', 'a+')
    img = cv2.imread(f'{ori_path}/{pic_file}'); height, weight = img.shape[:2]
    print(pic_file)
    root = etree.parse(xml_name)
    for elem in root.iter():
        if elem.tag == 'name':
            dict_= {}; dict_['class'] = elem.text
        if elem.tag == 'bndbox':
            dict_['type'] = 'bndbox'
        if elem.tag == 'robndbox':
            dict_['type'] = 'robndbox'
        if elem.tag == 'xmin':
            dict_['xmin'] = float(elem.text)
        if elem.tag == 'ymin':
            dict_['ymin'] = float(elem.text)
        if elem.tag == 'xmax':
            dict_['xmax'] = float(elem.text)
        if elem.tag == 'ymax':
            dict_['ymax'] = float(elem.text); list_.append(dict_)
        if elem.tag == 'cx':
            dict_['cx'] = float(elem.text)
        if elem.tag == 'cy':
            dict_['cy'] = float(elem.text)
        if elem.tag == 'w':
            dict_['w'] = float(elem.text)
        if elem.tag == 'h':
            dict_['h'] = float(elem.text)
        if elem.tag == 'angle':
            dict_['angle'] = float(elem.text); list_.append(dict_)

    for box in list_ :
        obj_class = classes.index(box['class'])
        if box['type'] == 'bndbox':
            left_top = [box['xmin'],box['ymin']]; left_bottom = [box['xmin'],box['ymax']]
            right_top = [box['xmax'],box['ymin']]; right_bottom = [box['xmax'],box['ymax']]
            x1 = round(left_top[0]/weight,3); y1 = round(left_top[1]/height,3)
            x2 = round(right_top[0]/weight,3); y2 = round(right_top[1]/height,3)
            x3 = round(right_bottom[0]/weight,3); y3 = round(right_bottom[1]/height,3)
            x4 = round(left_bottom[0]/weight,3); y4 = round(left_bottom[1]/height,3)
            txt_content = f'{obj_class} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}\n'
            aft_txt.writelines(txt_content)
        if box['type'] == 'robndbox':
            center = (float(box['cx']),float(box['cy']))
            b_left_top = [center[0]-float(box['w'])/2,center[1]-float(box['h'])/2]
            b_left_bottom = [center[0]-float(box['w'])/2,center[1]+float(box['h'])/2]
            b_right_top = [center[0]+float(box['w'])/2,center[1]-float(box['h'])/2]
            b_right_bottom = [center[0]+float(box['w'])/2,center[1]+float(box['h'])/2]
            theta = float(box['angle'])*180/np.pi*(-1)
            if theta > 180 :
                theta -= 180
            rotate_matrix = cv2.getRotationMatrix2D(center, theta, 1.0)
            left_top_matrix = np.matrix(b_left_top+[1]) ;a_left_top = np.array((rotate_matrix*left_top_matrix.T).flatten().tolist(),float)
            left_bottom_matrix = np.matrix(b_left_bottom+[1]) ;a_left_bottom = np.array((rotate_matrix*left_bottom_matrix.T).flatten().tolist(),float)
            right_top_matrix = np.matrix(b_right_top+[1]) ;a_right_top = np.array((rotate_matrix*right_top_matrix.T).flatten().tolist(),float)
            right_bottom_matrix = np.matrix(b_right_bottom+[1]) ;a_right_bottom = np.array(((rotate_matrix*right_bottom_matrix.T).flatten().tolist()),float)
            x1 = np.clip(round(a_left_top[0][0]/weight,3),0,1); y1 = np.clip(round(a_left_top[0][1]/height,3),0,1)
            x2 = np.clip(round(a_right_top[0][0]/weight,3),0,1); y2 = np.clip(round(a_right_top[0][1]/height,3),0,1)
            x3 = np.clip(round(a_right_bottom[0][0]/weight,3),0,1); y3 = np.clip(round(a_right_bottom[0][1]/height,3),0,1)
            x4 = np.clip(round(a_left_bottom[0][0]/weight,3),0,1); y4 = np.clip(round(a_left_bottom[0][1]/height,3),0,1)
            txt_content = f'{obj_class} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}\n'
            aft_txt.writelines(txt_content)
            
            '''
            points = np.array([[int(x1*weight), int(y1*height)], [int(x2*weight), int(y2*height)],[int(x3*weight), int(y3*height)],[int(x4*weight), int(y4*height)]], np.int32)
            cv2.polylines(img, pts=[points], isClosed=True, color=(255,0,0), thickness=3)
import imutils
img = imutils.resize(img, width=200)
cv2.imshow('test',img)
cv2.waitKey()
            '''
