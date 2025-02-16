import os
from aiogram.types import FSInputFile

command_description= {'START': ('start','Нажмите для запуска бота'),
                      'HELP': ('help', 'Нажмите для просмотра доступных команд'),
                      'FACT': ('random', 'Рандомный факт','1','FACT_NEW','BACK'),
                      'AICHAT': ('gpt', 'ChatGPT интерфейс','2','BACK'),
                      'TALK': ('talk', 'Диалог с известной личностью','3','BACK'),
                      'QUIZ': ('quiz', 'Квиз','4','BACK'),
                      'TRANSLATION': ('translate', 'Переводчик','5.1','BACK'),
                      'VOICE_CHAT': ('voice', 'Голосовое общение','5.2','BACK'),
                      'RECOMMEND': ('recommend', 'Рекомендации по фильмам и книгам','5.3','BACK'),
                      'TRAIN': ('train', 'Словарный тренажёр','5.4','BACK'),
                      'IMAGE': ('image', 'Распознавание изображений','5.5','BACK'),
                      'SUMMARY': ('summary', 'Помощь с резюме','5.6','BACK')}

text_descriptions = {'BACK': ('Закончить'), 'FACT_NEW':('Хочу ещё факт')}
resource_list = {}
class Resource:
    photo = None
    prompt = None
    msg = None
    name_of_res = None
    def __init__(self, name, photo_, prompt_ = None,msg_ =None):
        self.photo = photo_
        self.prompt = prompt_
        self.msg = msg_
        self.name_of_res = name

class CelebrityResource(Resource):
    celebrity_name = None
    def __init__(self, name, photo_, prompt_ = None,msg_ =None):
        super().__init__(name, photo_, prompt_, msg_)
        self.celebrity_name = name

def init_resources():
    files_list = {}
    files_list['prompts'] = [file for file in os.listdir('resources/prompts')]
    files_list['images'] = [file for file in os.listdir('resources/images')]
    files_list['messages'] = [file for file in os.listdir('resources/messages')]
    #print(*files_list.items(), sep='\n')
    len_max = 0
    max_len_arr_key = ''
    for key, arr in files_list.items():
        arr_len = len(arr)
        if arr_len > len_max:
            max_len_arr_key = key
            len_max = arr_len
    res_list = {}
    #print(max_len_arr_key)
    another_keys = []
    for key in files_list.keys():
        if key == max_len_arr_key:
            continue
        another_keys.append(key)
    for file_name in files_list[max_len_arr_key]:
        #print(file_name)
        file_without_ext = os.path.splitext(os.path.basename(file_name))[0]
        prompt = None
        msg = None
        if max_len_arr_key == 'images':
            photo = FSInputFile(path=os.path.join(f'resources/{max_len_arr_key}', file_name))
        else:
            in_data = None
            with open(f'resources/{max_len_arr_key}/{file_name}', "r", encoding='UTF-8') as fin:
                in_data = fin.readlines()
            prompt = in_data if 'prompts' == max_len_arr_key else None
            msg = in_data if 'messages' == max_len_arr_key else None
        for key2 in another_keys:
            #print(key2)
            for file_name2 in files_list[key2]:
                file_without_ext2 = os.path.splitext(os.path.basename(file_name2))[0]
                #print(file_without_ext2, file_without_ext)
                if file_without_ext2 == file_without_ext:
                    #print(file_without_ext)
                    if key2 == 'images':
                        photo = FSInputFile(path=os.path.join(f'resources/{key2}', file_name2))
                    else:
                        in_data = None
                        with open(f'resources/{key2}/{file_name2}', "r", encoding='UTF-8') as fin:
                            in_data = fin.readlines()
                        prompt = in_data if 'prompts' == key2 else None
                        msg = in_data if 'messages' == key2 else None
        #print('combine')
        if file_name.startswith('talk_'):
            name_right = prompt[0].split(',')[0][5:]
            #print('name', name_right)
            res_list[file_without_ext] = CelebrityResource(name_right, photo, prompt, msg)
        else:
            res_list[file_without_ext] = Resource(file_without_ext, photo, prompt, msg)
        #print(*res_list.items(), sep='\n')
        global resource_list
        resource_list = res_list
