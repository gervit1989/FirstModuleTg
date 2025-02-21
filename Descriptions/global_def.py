import os
from aiogram.types import FSInputFile

command_description= {'START': ('start','Нажмите для запуска бота'),
                      'HELP': ('help', 'Нажмите для просмотра доступных команд'),
                      'FACT': ('random', 'Рандомный факт','-','FACT_NEW','BACK'),
                      'AICHAT': ('gpt', 'ChatGPT интерфейс','-','BACK'),
                      'TALK': ('talk', 'Диалог с известной личностью','-','BACK'),
                      'QUIZ': ('quiz', 'Квиз','-','BACK'),
                      'TRANSLATION': ('translate', 'Переводчик','-','BACK'),
                      'VOICE_CHAT': ('voice', 'Голосовое общение','-','BACK'),
                      'RECOMMEND': ('recommend', 'Рекомендации по фильмам и книгам','-','BACK'),
                      'TRAIN': ('train', 'Словарный тренажёр','-','BACK'),
                      'IMAGE': ('image', 'Распознавание изображений','-','BACK'),
                      'SUMMARY': ('summary', 'Помощь с резюме','-','BACK')}

text_descriptions = {'FACT_NEW':('Хочу ещё факт',), 'BACK': ('Закончить',)}

class Resource:
    photo = None
    prompt = None
    msg = None
    name_of_res = None
    def __init__(self, name, photo_, prompt_ = None,msg_ =None):
        self.photo = photo_
        #print("class:", name, prompt_, msg_)
        self.prompt = prompt_
        self.msg = msg_
        self.name_of_res = name

class CelebrityResource(Resource):
    celebrity_name = None
    def __init__(self, name, photo_, prompt_ = None,msg_ =None):
        super().__init__(name, photo_, prompt_, msg_)
        self.celebrity_name = name

class ResHolder:
    resource_list = []

    def __init__(self):
        self.resource_list = []
        self.init_resources()

    async def get_resource(self, _name):
        for item in self.resource_list:
            if item.name_of_res == _name:
                return item
        return None

    async def get_celebrity_resource(self, _name):
        for item in self.resource_list:
            if isinstance(item, CelebrityResource):
                if item.celebrity_name == _name:
                    return item
        return None

    def init_resources(self):
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
                    in_data = fin.read()
                prompt = in_data if 'prompts' == max_len_arr_key else prompt
                msg = in_data if 'messages' == max_len_arr_key else msg
            for key2 in another_keys:
                #print('\t',key2)
                for file_name2 in files_list[key2]:
                    file_without_ext2 = os.path.splitext(os.path.basename(file_name2))[0]
                    #print('\t','\t',file_without_ext2, file_name2, key2)
                    if file_without_ext2 == file_without_ext:
                        #print('\t','\t','\t',file_without_ext)
                        if key2 == 'images':
                            photo = FSInputFile(path=os.path.join(f'resources/{key2}', file_name2))
                        else:
                            in_data = None
                            with open(f'resources/{key2}/{file_name2}', "r", encoding='UTF-8') as fin:
                                in_data = fin.read()
                            #print('\t','\t','\t',"file:", in_data)
                            prompt = in_data if 'prompts' == key2 else prompt
                            #print(prompt)
                            msg = in_data if 'messages' == key2 else msg
                        break
            #print('combine')
            if file_name.startswith('talk_'):
                name_right = prompt[0].split(',')[0][5:]
                #print('name', name_right)
                self.resource_list.append( CelebrityResource(name_right, photo, prompt, msg))
            else:
                self.resource_list.append( Resource(file_without_ext, photo, prompt, msg))
            #print(*res_list.items(), sep='\n')
