# coding=utf-8
from tkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from DATA import BG_PNG
from fake import TEMPLATES
from file import File, Messagebox
from ttkbootstrap.scrolled import ScrolledFrame

__author__ = "屈永飞"
__copyright__ = "Copyright (C) 2004 屈永飞"
__license__ = "Public Domain"
__version__ = "1.1"

language_list = ['en_US', 'zh_CN', 'it_IT', 'ja_JP',
                 'en_CA', 'en_PH', 'en_TH', 'uk_UA']

type_list = [k for k in TEMPLATES.keys()]


fake_lan = "en-US"
i = 0
rows = []
val = []
rowss = []


class CommanStyle(object):
    """
    通用样式设计
    """

    def __init__(self, frame):
        self.frame = frame
        # -----通用样式-----
        s = ttk.Style()
        s.configure('TFrame', background='white')
        s.configure('Frame1.TFrame', background='white')
        s.configure('Frame2.TFrame', background='white')
        s.configure('Frame3.TFrame', background='white')
        s.configure('Frame4.TFrame', background='white')
        s.configure(
            'TCombobox',
            padding=[
                5,
                3,
                0,
                6],  # 决定Type文字宽度
            selectbackground='white',
            selectforeground='red')  # Type输入选中文字颜色
        s.configure(
            'TEntry',
            padding=[
                0,
                0,
                0,
                0],
            selectbackground='#98d2eb',
            selectforeground='white')  # Field Name输入选中文字颜色
        s.configure('TLabel', background='white')
        s.configure('TButton', padding=[6, 6, 6, 6])

    def set_text(self):
        """
        右边文字标题部分
        """
        field_name = ttk.Label(
            self.frame, text='Name:', font=(
                'Devanagari MT', 25), foreground='#7189ff')
        type = ttk.Label(
            self.frame,
            text='Type:',
            font=(
                'Devanagari MT',
                25),
            foreground='#7189ff')
        field_name.grid(row=1, column=1, ipady=18)  # 字段名位置
        type.grid(row=1, column=2, padx=90, ipady=18)
        # -----------------


class Add_Del_Row(object):

    def __init__(self, scrollable_body):
        self.scrollable_body = scrollable_body

    def add_row(self, name='', types=None):

        global i
        i = i + 1
        items = []

        l = ttk.Label(self.scrollable_body, text=i)
        items.append(l)
        field = ttk.Entry(
            self.scrollable_body, font=(
                'Weibei TC', 12), width=20, bootstyle='secondary')  # field 输入框相关信息
        field.insert(0, name)

        # type相关信息
        type = ttk.Combobox(
            self.scrollable_body,
            font=('STFangsong', 12),
            width=18,
            state='readonly',
            values=type_list)
        # Windows & OSX 禁用滚轮对type值得改变
        type.unbind_class("TCombobox", "<MouseWheel>")

        # # Linux and other *nix systems:
        # type.unbind_class("TCombobox", "<ButtonPress-4>")
        # type.unbind_class("TCombobox", "<ButtonPress-5>")
        if types is not None:
            type.current(types)
        clear = ttk.Button(
            self.scrollable_body,
            text='Clear',
            width=6,
            bootstyle="warning-outline",
            command=lambda: self.clear_one_row_txt(
                l.cget('text')))
        pop = ttk.Button(
            self.scrollable_body,
            text='X',
            width=2,
            bootstyle="danger-outline",
            command=lambda: self.delete_row(
                l.cget('text')))
        items.append(field)
        items.append(type)
        items.append(clear)
        items.append(pop)
        field.grid(row=i, column=1, pady=8)
        type.grid(row=i, column=2, padx=10)
        clear.grid(row=i, column=3)
        pop.grid(row=i, column=4, padx=8)
        self.scrollable_body.update()
        rows.append(items)

    def delete_row(self, lab):
        for rowno, row in reversed(list(enumerate(rows))):
            if row[0].cget("text") == lab:
                for i in row:
                    i.destroy()
                    self.scrollable_body.update()
                rows.pop(rowno)

    def clear_one_row_txt(self, lab):
        for rowno, row in reversed(list(enumerate(rows))):
            if row[0].cget("text") == lab:
                row[1].delete(0, END)
                row[2].set('')
                self.scrollable_body.update()
                # rows.pop(rowno)

    def delete_all_row(self):
        for rowno, row in reversed(list(enumerate(rows))):
            for i in row:
                i.destroy()
            rows.pop(rowno)

    def down_data_save_file(self, total, type_f):
        POSITION = (850, 450)
        save_dict = {}
        for row in rows:
            fieled_name = row[1].get()
            type_name = row[2].get()
            if fieled_name and type_name:
                if save_dict.get(fieled_name):
                    Messagebox.show_warning(
                        title="Waring",
                        message="Column '{}' is specified more than once.Column names must be unique.(Name, Type必须唯一)".format(
                            fieled_name), position=POSITION,
                        alert=False)
                    return
                save_dict[fieled_name] = type_name
        if save_dict == {}:
            Messagebox.show_warning(title='Warning',
                                    alert=False,
                                    message="Name Type不能为空至少有一组对应关系/Enter Correct column", position=(800, 450))
            return

        total_row_num = total.get()

        file_type = type_f.get()

        try:
            if int(total_row_num) > 0:
                if int(total_row_num) > 20_0000:
                    INFO = "The maximum download size is 20,0000 rows.(最大下载大小为 20,0000 行)"
                    Messagebox.show_warning(
                        title='警告', message=INFO, position=POSITION)
                else:
                    if file_type == 'JSON':
                        File("MOCK_JSON", fake_lan).save_data_json_thread(
                            total_row_num, save_dict)  # 保存为json
                    elif file_type == 'SQL':
                        status = val[-1].state()
                        table_name, _table_status = val[1].get(), status
                        if len(_table_status) > 0:
                            File(table_name, fake_lan).create_table_and_open_sql(
                                total_row_num, save_dict, status=True)
                        else:
                            File(table_name, fake_lan).create_table_and_open_sql(
                                total_row_num, save_dict, status=False)
                    elif file_type == "CSV":  # 保存为csv
                        File("MOCK_CSV", fake_lan).save_data_csv(
                            total_row_num, save_dict)
            else:
                INFO = 'Number must be greater than "0".(请输入有效数字)'
                Messagebox.show_warning(
                    title='警告', message=INFO, position=POSITION)
        except ValueError as e:
            Messagebox.show_error(
                title='错误', message='"{}"是无效字符'.format(e), position=POSITION)


class Func_Data(object):
    def __init__(self, frame):
        self.frame = frame
        self.get_dwn_args()

    def get_dwn_args(self):
        # ---------Rows Num:-----------
        ttk.Label(
            self.frame,
            text='Rows Num:',
            font=(
                "times new roman",
                14,
                'bold'),
            foreground='#7189ff').grid(
            row=1,
            column=1,
            padx=5)
        row_num = ttk.Entry(Frame4, font=('times new roman', 15), width=10)
        row_num.insert(0, 1000)
        row_num.grid(row=1, column=2, padx=5)
        # ----------Format--------------
        ttk.Label(
            self.frame,
            text='Format Type:',
            font=(
                "times new roman",
                14,
                'bold'),
            foreground='#7189ff').grid(
            row=1,
            column=3,
            padx=14)
        select_file_type = ttk.Combobox(
            self.frame,
            font=(
                'times new roman',
                15),
            state='readonly',
            justify=CENTER,
            width=10)
        select_file_type['values'] = ('JSON', 'SQL', 'CSV')
        select_file_type.grid(row=1, column=4)
        select_file_type.current(0)
        select_file_type.bind(
            '<<ComboboxSelected>>',
            lambda event: self.callback(
                select_file_type,
                event))
        return row_num, select_file_type

    # def add_csv_status(self):
    #     # ---------CSV-------------------
    #     csv_status = self.model_status('header', 1, 5, 15)
    #     val.append(csv_status)

    def model_status(self, text, row, column, padx):
        var = IntVar()
        status = ttk.Checkbutton(self.frame, text=text, variable=var, bootstyle="primary")
        status.val = var
        status.state(['selected'])
        status.grid(row=row, column=column, padx=padx)
        return status

    def add_sql_status(self):
        # -----------SQL------------------
        tab_name = ttk.Label(
            self.frame,
            text='Table Name:',
            font=(
                "times new roman",
                14,
                'bold'),
            foreground='#7189ff')
        tab_name.grid(row=2, column=1)
        name = ttk.Entry(self.frame, font=('times new roman', 15), width=10)
        name.insert(0, 'mock_data')
        name.grid(row=2, column=2, pady=5)
        sql_status = self.model_status('include create table', 2, 3, 5)
        val.append(tab_name)
        val.append(name)
        val.append(sql_status)

    def callback(self, select_file_type, event):

        one_status = select_file_type.get()
        self.remove_widget(val)
        if one_status == "SQL":
            self.add_sql_status()
        else:
            return None

    def remove_widget(self, val):
        for num, i in reversed(list(enumerate(val))):
            i.destroy()
            val.pop(num)


class Menu_toolbar(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = Menu(menubar, tearoff="off")
        submenu = Menu(fileMenu, tearoff="off")

        language_ = self.language_generator(language_list)
        for i in language_:
            submenu.add_radiobutton(
                label=i, command=lambda lan=i: self.option(lan))

        fileMenu.add_cascade(label='Language', underline=0, menu=submenu)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
        menubar.add_cascade(label="关于", underline=0, command=self.about_me)
        fileMenu.add_separator()  # 添加分隔条
        fileMenu.add_command(label="Exit", underline=0, command=self.onExit)

    def language_generator(self, language_list):
        for i in language_list:
            yield i

    def onExit(self):

        self.quit()

    def about_me(self):
        Messagebox.ok(message="         作者：屈永飞\n"
                              "         邮箱: 923464541@qq.com\n"
                              "         介绍：一名底层的测试人员", position=(850, 450))

    def option(self, arg0):
        global fake_lan
        fake_lan = arg0


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
    root.update()


if __name__ == '__main__':


    # root = ttk.Window()
    root = tk.Tk()

    root.resizable(width=False, height=False)  # 禁止改变窗口大小
    style = ttk.Style("cosmo")  # litera cosmo  lumen   minty   pulse  flatly  不友好（journal）
    # root.geometry('1100x700+0+0')
    center_window(root, 1100, 720)
    # root.resizable(0, 0)
    root.title('MockTool-win')


    # Logo = PhotoImage(data=LOGO_PNG)
    # root.call('wm', 'iconphoto', root._w, Logo)
    root.iconbitmap(default=r'F://Mock_Data_Generation-main//foursquare.ico')
    Menu_toolbar()

    # ----背景图片----
    left = ttk.PhotoImage(data=BG_PNG)
    ttk.Label(root, image=left).place(x=50, y=30)
    root.config(bg='#ffffff')

    # ----name type标题文字块部分整体位置---------
    Frame1 = ttk.Frame(root, style='Frame1.TFrame')
    Frame1.place(x=600)
    CommanStyle(Frame1).set_text()

    '''输入框整体部分'''
    Frame2 = ttk.Frame(root, style='Frame2.TFrame')
    Frame2.place(x=590, y=70)  # name和type输入框整体位置
    scrollable_body = ScrolledFrame(Frame2, autohide=True, height=370, width=500)
    scrollable_body.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    """动态添加/删除部分"""
    Frame3 = ttk.Frame(root, style='Frame3.TFrame')
    Frame3.place(x=605, y=513)

    add_data = Add_Del_Row(scrollable_body)
    add_btn = ttk.Button(
        Frame3,
        text='Add Field',
        bootstyle="success-outline",
        command=add_data.add_row).grid(
        row=1,
        column=2,
        padx=255, ipadx=20)

    # Add Field 提示
    # ToolTip.show_tip(ADD)
    ttk.Button(
        Frame3,
        text='Del All',
        bootstyle="danger-outline",
        command=add_data.delete_all_row).grid(
        row=1,
        column=1, ipadx=20)

    """最底部下载相关字段"""
    Frame4 = ttk.Frame(root, style='Frame4.TFrame')
    Frame4.place(x=490, y=560)  # 底部相关输入选择框整体位置
    f = Func_Data(Frame4)
    total, type_f = f.get_dwn_args()
    # --------Download-----------
    down = ttk.Button(
        root,
        text='Download',
        width=50,
        command=lambda: add_data.down_data_save_file(
            total,
            type_f))
    down.grid(row=0, column=0, pady=660, padx=600)

    # -------Copyright © 2021 屈永飞. All rights reserved.
    copyright = ttk.Label(root, text='Copyright © 2021 屈永飞. All rights reserved.').place(x=0, y=682)

    root.mainloop()
