import json
import pickle
import os
import re

def load_json(jsonfile):
    #输入json文件名，返回[{"group":name,"pic_name":path}]形式的列表
    with open(jsonfile, 'r',encoding='utf-8') as f:
        images = json.load(f)
    return images

def sort_by_group(images):
    #输入[{"group":name,"pic_name":path}]形式的列表，返回{name:[paths]}形式的字典
    groups = {}
    for image in images:
        path = image['pic_name']
        name = image['class']
        if name not in groups:#添加新分类
            groups[name] = []
        groups[name].append(path)
    return groups

def get_groups(jsonfile):
    #输入json文件名，返回{name:[paths]}形式的字典，整合了上面两个的意思
    images = load_json(jsonfile)
    groups = sort_by_group(images)
    return groups
'''
def get_groups_more(groups):
    #输入{name:[paths]}形式的字典，去除paths个数小于等于3的节点，返回{name:[paths]}形式的字典
    group_to_delete = []
    for name, paths in list(groups.items()):
        if name == "未命名":
            continue
        if len(paths) <= 3 or name == "错误分类":
            group_to_delete.append(name)
    for group in group_to_delete:
        groups.pop(group)
    return groups
    '''
def write_json(groups):
    #输入{name:[paths]}形式的字典，以[{"group":name,"pic_name":path}]的形式写入output.json中
    images = []
    for name, paths in groups.items():
        for path in paths:
            image_dic = {}
            image_dic['pic_name'] = os.path.basename(path)
            #print(image_dic['pic_name'])
            image_dic['group'] = name
            images.append(image_dic)
    images.sort(key=lambda x: [int(s) if s.isdigit() else s for s in re.findall(r'\D+|\d+', x['group'])])
    with open('output.json','w',encoding='utf-8') as f:
        f.write(json.dumps(images,indent=4,ensure_ascii=False,sort_keys=True))

def print_by_group(groups):
    #将{name:[paths]}形式的字典按"人名:图片组"的形式格式化输出
    for name, paths in groups.items():
        print("------------------------------")
        print()
        print("Name:{}".format(name))
        for count,path in enumerate(paths):
            index = path.rfind('\\',0,len(path))
            print("{}:{}".format(count,path[index+1:]))
        print()
    print("------------------------------")

def edit_group_name(new_group_name,old_group_name, groups):
    #输入新名称、旧名称、{name:[paths]}形式的字典，返回更名后的{name:[paths]}形式的字典
    if new_group_name not in groups:
        groups[new_group_name] = groups.pop(old_group_name)
    else:
        groups[new_group_name].extend(groups.pop(old_group_name))
    return groups

def edit_single_group_name(new_group_name, path, groups):
    #输入新名称、图片路径、{name:[paths]}形式的字典，返回更名后的{name:[paths]}形式的字典
    name_to_delete = -1
    for name, paths in groups.items():
        if path in paths:
            paths.remove(path)
        if len(paths)==0:
            name_to_delete = name
    if name_to_delete != -1:
        groups.pop(name_to_delete)
    if new_group_name in groups:
        persons[new_group_name].append(path)
    else:
        persons[new_group_name] = [path]
    return groups

def load_pickle(picklefile):
    #输入embeddings.pickle的路径，返回[{"path":path,"embedding":np_array}]类型的列表
    datas = pickle.load(open(picklefile,"rb"))
    return datas

def write_pickle(datas):
    #输入[{"path":path,"embedding":np_array}]类型的列表，写入embeddings.pickle
    with open("embeddings.pickle", "wb") as f: 
        pickle.dump(datas, f)

def delete_single_pic(target_path, groups):
    # 输入图片路径target_path和{name:[paths]}形式的字典
    # 将target_path对应的图片从embeddings.pickle中删除，
    # 将target_path对应的图片从{name:[paths]}形式的字典中删除，返回修改过的{name:[paths]}形式的字典
    #从groups里删除单张照片
    empty_names =[]
    for name, paths in groups.items():
        if target_path in paths:
            paths.remove(target_path)
            groups[name] = paths
            try:
                os.remove(target_path)
            except FileNotFoundError:
                pass
        if len(paths) == 0:
            empty_names.append(name)
    for name in empty_names:
        groups.pop(name)

    #从embeddings.pickle里删除单张照片
    pickle_datas = load_pickle("embeddings.pickle")
    pickle_to_delete = []
    for index, pickle_data in enumerate(pickle_datas):
        if target_path == pickle_data["path"]:
            pickle_to_delete.append(index)
    for index in pickle_to_delete:
        pickle_datas.pop(index)
    write_pickle(pickle_datas)

    return groups

def delete_multi_pic(rootdir, target_paths, groups):
    pickle_datas = load_pickle("embeddings.pickle")

    for target_path in target_paths:
        target_path = target_path
        empty_names =[]
        for name, paths in groups.items():
            if target_path in paths:
                paths.remove(target_path)
                groups[name] = paths
                try:
                    os.remove(os.path.join(rootdir, target_path))
                except FileNotFoundError:
                    print("Not Found: {}".format(target_path))
                    pass
                #print(groups[name])
            if len(paths) == 0:
                empty_names.append(name)
        for name in empty_names:
            groups.pop(name)

        pickle_to_delete = []
        for index, pickle_data in enumerate(pickle_datas):
            if target_path == os.path.basename(pickle_data["path"]):
                pickle_to_delete.append(index)
        for index in pickle_to_delete:
            pickle_datas.pop(index)
        
    write_pickle(pickle_datas)
    return groups

if __name__ == "__main__":
    jsonfile = 'output.json'
    images = load_json(jsonfile)
    groups = sort_by_group(images)
    #print(groups)
    #print_by_group(groups)
    '''
    更改人脸名测试
    groups = edit_group_name("TEST_2","Person 8",groups)
    write_json(groups)
    '''
    #删除人脸测试
    #persons = delete_pic("./image\\08.jpg",persons)
    #print_by_person(persons)
    #groups = edit_single_group_name("Person 46","./image\\08.jpg",groups)
    print_by_group(groups)