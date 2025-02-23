import os
from aiogram.types import FSInputFile

# описание команд и допов
command_description= {'START': ('start','Нажмите для запуска бота'),
                      'HELP': ('help', 'Нажмите для просмотра доступных команд'),
                      'FACT': ('random', 'Рандомный факт','-','FACT_NEW','BACK'),
                      'AICHAT': ('gpt', 'ChatGPT интерфейс','-','BACK'),
                      'TALK': ('talk', 'Диалог с известной личностью','-','BACK_THIS', 'BACK'),
                      'QUIZ': ('quiz', 'Квиз','-','BACK'),
                      'TRANSLATION': ('translate', 'Переводчик','-','BACK'),
                      'VOICE_CHAT': ('voice', 'Голосовое общение','-','BACK'),
                      'RECOMMEND': ('recommend', 'Рекомендации по фильмам и книгам','-','BACK'),
                      'TRAIN': ('train', 'Словарный тренажёр','-','BACK'),
                      'IMAGE': ('image', 'Распознавание изображений','-','BACK'),
                      'SUMMARY': ('summary', 'Помощь с резюме','-','BACK')}
# кнопки описание
text_descriptions = {'FACT_NEW':('Хочу ещё факт',), 'BACK_THIS': ('К списку звезд',), 'BACK': ('Закончить',)}

# класс ресурс
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

# ресурс знаменитости
class CelebrityResource(Resource):
    celebrity_name = None
    def __init__(self, name_of_res, name, photo_, prompt_ = None,msg_ =None):
        super().__init__(name_of_res, photo_, prompt_, msg_)
        self.celebrity_name = name

# хранилище ресурсов
class ResHolder:
    resource_list = []

    def __init__(self):
        self.resource_list = []
        self.init_resources()

    # дай мне ресурс команды
    async def get_resource(self, _name):
        for item in self.resource_list:
            if item.name_of_res == _name:
                return item
        return None

    # список имен звезд
    def get_celebrity_names(self):
        names_lst =[]
        for item in self.resource_list:
            if isinstance(item, CelebrityResource):
                names_lst.append(item.celebrity_name)
        return names_lst

    # по имени отдай ресурс звезды
    def get_celebrity_resource(self, _name):
        for item in self.resource_list:
            if isinstance(item, CelebrityResource):
                if item.celebrity_name == _name:
                    return item
        return None

    # инициализация ресурса
    def init_resources(self):
        print('init resources...')
        files_list = {}
        res_dir_name = 'resources'
        img_key='images'
        prompt_key='prompts'
        msg_key ='messages'
        dir_lst = os.listdir(res_dir_name)
        for dir_var in dir_lst:
            files_list[dir_var] = [file for file in os.listdir(f'{res_dir_name}/{dir_var}')]
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
            if max_len_arr_key == img_key:
                photo = FSInputFile(path=os.path.join(f'{res_dir_name}/{max_len_arr_key}', file_name))
            else:
                in_data = None
                with open(f'{res_dir_name}/{max_len_arr_key}/{file_name}', "r", encoding='UTF-8') as fin:
                    in_data = fin.read()
                prompt = in_data if prompt_key == max_len_arr_key else prompt
                msg = in_data if msg_key == max_len_arr_key else msg
            for key2 in another_keys:
                #print('\t',key2)
                for file_name2 in files_list[key2]:
                    file_without_ext2 = os.path.splitext(os.path.basename(file_name2))[0]
                    #print('\t','\t',file_without_ext2, file_name2, key2)
                    if file_without_ext2 == file_without_ext:
                        #print('\t','\t','\t',file_without_ext)
                        if key2 == img_key:
                            photo = FSInputFile(path=os.path.join(f'{res_dir_name}/{key2}', file_name2))
                        else:
                            in_data = None
                            with open(f'{res_dir_name}/{key2}/{file_name2}', "r", encoding='UTF-8') as fin:
                                in_data = fin.read()
                            #print('\t','\t','\t',"file:", in_data)
                            prompt = in_data if prompt_key == key2 else prompt
                            #print(prompt)
                            msg = in_data if msg_key == key2 else msg
                        break
            celebrity_start_str=command_description['TALK'][0].lower()+'_'
            if file_name.startswith(celebrity_start_str):
                name_right = prompt.split(',')[0][5:]
                self.resource_list.append( CelebrityResource(file_without_ext, name_right, photo, prompt, msg))
            else:
                self.resource_list.append( Resource(file_without_ext, photo, prompt, msg))
