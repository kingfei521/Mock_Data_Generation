import json
import threading
from do.data_template import *
from loguru import logger

class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance


class File(object):
    def __init__(self, file_name):
        self.name = file_name

    def save_data_json(self, rows, fields, status):
        """
        生成SON文件格式
        :param rows:
        :param fields:
        :param status:
        :return:
        """
        data = {}
        if status:
            file = []
            with open(self.name + '.json', 'w+', encoding='utf-8') as f:  # 以列表形式存入导出
                for i in range(0, int(rows)):
                    for k, v in fields.items():
                        data[k] = data_generator(v)
                    file.append(data)
                    data = {}
                json.dump(file, f, indent=4, ensure_ascii=False)
        else:
            with open(self.name + '.json', 'w+', encoding='utf-8') as f:  # 以原始字典形式存入导出
                for i in range(0, int(rows)):
                    for k, v in fields.items():
                        data[k] = data_generator(v)
                    json.dump(data, f, ensure_ascii=False)
                    f.write(',')
                    if i == int(rows) - 1:
                       return
                    f.write('\n')
                    data = {}

    def create_table_and_open_sql(self, rows, fields, status):
        """
        生成SQL文件格式
        :param rows: 行数
        :param fields: 字段
        :param status: 是否需要创建表
        :return:
        """
        with open(self.name + '.sql', 'w+', encoding='utf-8') as f:
            if status:
                self._table_sql(self.name, f, fields)
                self._sql(self.name, f, rows, fields)
            else:
                self._sql(self.name, f, rows, fields)

        return 'Download Successful'




    def _table_sql(self, name, f, fields):
        """
        支持SQL文件，所需的创建表字段格式
        :param f:
        :param fields:
        :return:
        """
        title = 'CREATE TABLE {}('.format(name) + '\r'
        logger.debug(title)
        f.write(title)
        i = 0
        for field_name, type_name in fields.items():
            model = '\t' * 2 + '{} {}'.format(field_name, TEMPLATES[type_name])
            f.write(model)
            if i != len(fields) - 1:
                f.write(',\r')
            else:
                f.write('\r')
            i += 1
        f.write(');\r')

    def _sql(self,name, f, rows, fields):
        """
        仅插入数据 "INSERT INTO XXXXXXXX"
        :param f:
        :param rows:
        :param fields:
        :return:
        """
        _field_name = [k for k in fields.keys()]
        _type_name = [v for v in fields.values()]

        for row in range(int(rows)):
            ing = []
            for i in _type_name:
                ing.append(data_generator(i))
            sql = 'INSERT INTO {} ('.format(name) + ', '.join(_field_name) + ') VALUES {};'.format(tuple(ing))
            f.write(sql)
            f.write('\r')









