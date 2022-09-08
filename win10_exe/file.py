import os
import json
from tkinter import messagebox as mbox, filedialog

from faker import Faker
from ttkbootstrap.dialogs import Messagebox

from fake import *
import csv, time

import threading

threadLock = threading.Lock()


def print_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print('current Function [%s] run time is %.2f' % (func.__name__ ,time.time() - local_time))
    return wrapper

# ---------------------------------------

class Json_Thread(threading.Thread):
    def __init__(self, count, fields, fake, f_path):
        threading.Thread.__init__(self)
        self.fake = fake
        self.count = count
        self.fields = fields
        self.f_path = f_path

    def run(self):
        num = 0
        try:
            with open(self.f_path, 'w+', encoding='utf-8') as f:  # 以列表形式存入导出
                files = []
                while True:
                    # 获得锁
                    threadLock.acquire()
                    if num >= self.count:
                        # 释放锁
                        threadLock.release()
                        break
                    num += 1
                    dic = {k: data_generator(v, self.fake) for k, v in self.fields.items()}
                    files.append(dic)
                    # 释放锁
                    threadLock.release()
                json.dump(list(files), f, ensure_ascii=False)
        except Exception as e:
            return e



# -----------------------------------

class File(object):
    def __init__(self, file_name, lan='zh_CN'):
        self.name = file_name
        self.file_type = [[("JSON", ".json")], [("SQL", "*.sql")], [("CSV", "*.csv")], [("All File", "*.*")]]
        self.fake = Faker([lan])

    # @print_run_time
    def save_data_csv(self, rows, fields):
        """
        生成CSV文件格式
        :param rows:
        :param fields:
        :param status:
        :return:
        """
        f_path = self.save_box(2)
        try:
            with open(f_path, "w+", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(fields.keys())
                for i in range(0, int(rows)):
                    iterobj = (data_generator(name, self.fake) for name in fields.values())
                    writer.writerow(iterobj)

            return self.onInfo()
        except FileNotFoundError as e:
            return e


    # def iter_list(self, rows, fields):
    #     for _ in range(0, int(rows)):
    #         dic = {k: data_generator(v, self.fake) for k, v in fields.items()}
    #         yield dic
    #
    #
    # @print_run_time
    # def save_data_json(self, rows, fields):
    #     """
    #     生成JSON文件格式
    #     :param rows:
    #     :param fields:
    #     :return:
    #     """
    #
    #     try:
    #         f_path = self.save_box(0)
    #         with open(f_path, 'w+', encoding='utf-8') as f:  # 以列表形式存入导出
    #             res = self.iter_list(rows, fields)
    #             json.dump(list(res), f, ensure_ascii=False)
    #         return self.onInfo()
    #     except FileNotFoundError as e:
    #         return e

    # @print_run_time
    def save_data_json_thread(self, rows, fields):
        """
        生成JSON文件格式
        :param rows:
        :param fields:
        :return:
        """

        f_path = self.save_box(0)
        try:
            if f_path != "":
                thread1 = Json_Thread(int(rows), fields, self.fake, f_path)
                thread1.start()
                thread1.join()
                return self.onInfo()
        except FileNotFoundError as e:
            return self.onError(e)

    def create_table_and_open_sql(self, rows, fields, status):
        """
        生成SQL文件格式
        :param rows: 行数
        :param fields: 字段
        :param status: 是否需要创建表
        :return:
        """

        try:
            f_path = self.save_box(1)
            with open(f_path, 'w+', encoding='utf-8') as f:
                if status:
                    self._table_sql(self.name, f, fields)
                    self._sql(self.name, f, rows, fields)
                else:
                    self._sql(self.name, f, rows, fields)
            return self.onInfo()
        except FileNotFoundError as e:
            return self.onError(e)


    def _table_sql(self, name, f, fields):
        """
        支持SQL文件，所需的创建表字段格式
        :param f:
        :param fields:
        :return:
        """
        title = 'CREATE TABLE {}('.format(name) + '\r'
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
                ing.append(data_generator(i, self.fake))
            sql = 'INSERT INTO {} ('.format(name) + ', '.join(_field_name) + ') VALUES {};'.format(tuple(ing))
            f.write(sql)
            f.write('\r')

    def save_box(self, i):
        file_path = filedialog.asksaveasfilename(title=u"下载路径",
                                                 filetypes=self.file_type[i],
                                                 confirmoverwrite=False,
                                                 initialdir=(os.path.expanduser(__file__)), initialfile=self.name,
                                                 defaultextension=".json")
        return file_path

    def onInfo(self):

        Messagebox.show_info(title="Information", message="Download completed", icon='info', position=(850, 450))

    def onError(self, e):

        Messagebox.show_error(title="ErrrInfo", message="! ERROR: {}".format(e), icon='info',position=(850, 450))
