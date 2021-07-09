# -*- coding:utf-8 -*-
"""
作者：智科类1班  陈思宇（学号：222020335220002）
作者：智科类1班  黄越鸣（学号：222020335220009）
作者：智科类1班  罗  涛（学号：222020335220012）

日期：2021年07月05日
"""

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.messagebox import *

from Database import Database

# 全局变量防止图片被GC回收
bm = None

class ManagerUI(object):
    """管理系统界面和后台"""

    def __init__(self):
        # 数据库的用户名和密码，从self.entry_1和self.entry_2中获得
        self.user = None
        self.password = None
        # # 建立列表用于清除函数的参数传送
        self.list_1 = []
        self.root = Tk()
        self.root.resizable(0, 0)  # 禁止调节大小
        self.screen_width = self.root.winfo_screenwidth()  # 获得屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  # 获得屏幕高度
        # 容器,添加各种组件
        self.frame_1 = Frame(self.root)
        # # 以place的形式添加到root中

        self.frame_1.place(x=0, y=0)

        # 用户名和密码的文本框, show="*"，防止密码泄露
        self.entry_1 = Entry(self.frame_1, bd=5, width=30)
        self.entry_2 = Entry(self.frame_1, bd=5, width=30, show="*")

    # 成绩管理系统主界面
    def init_1(self, target=-1, condition=False, constu=[]):
        """
            主页面，展示信息target与表格的显示有关，为-1是数据库中table的先后顺序
            为0，1，2，3分别是总分、语文、数学、英语降序排序
            condition是展示条件，默认按学号排序全部展示
            constu是符合条件的学生学生列表，condition为False则无效
        """
        # 清除组件避免重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 设置窗口标题
        self.root.title("学生成绩管理系统")
        # 设置窗口大小
        self.root.geometry("550x600")

        # frame_func = Frame(self.frame_1, width=200)  # 功能按钮的容器
        frame_func = Frame(self.root, width=200)  # 功能按钮的容器

        frame_func.pack(expand=YES, fill=BOTH)
        frame_table = Frame(self.root, width=300)  # tree表的容器
        # frame_table.pack()

        # 8个功能

        button_1 = Button(frame_func, text="添加学生", command=lambda: self.addstudent())
        row_info = []  # 传参用的变量
        button_2 = Button(frame_func, text="删除学生", command=lambda: self.delete_win(row_info))
        button_3 = Button(frame_func, text="信息修改", command=lambda: self.update_win(row_info))
        button_4 = Button(frame_func, text="查找学生", command=lambda: self.find_win())
        button_5 = Button(frame_func, text="总分降序", command=lambda: self.sort(0))
        button_6 = Button(frame_func, text="语文降序", command=lambda: self.sort(1))
        button_7 = Button(frame_func, text="数学降序", command=lambda: self.sort(2))
        button_8 = Button(frame_func, text="英语降序", command=lambda: self.sort(3))

        # 功能容器布局
        Label(frame_func, width=20).grid(row=0, column=0)
        button_1.grid(row=1, column=2)
        button_2.grid(row=1, column=3)
        button_3.grid(row=1, column=4)
        button_4.grid(row=1, column=5)
        button_5.grid(row=2, column=2)
        button_6.grid(row=2, column=3)
        button_7.grid(row=2, column=4)
        button_8.grid(row=2, column=5)

        # 建表
        columns = ['姓名', '性别', '学号', '语文成绩', '数学成绩', '英语成绩', '总分']  # 表的索引
        tree = ttk.Treeview(frame_table, show="headings", height=18, columns=columns)
        tree.column(columns[0], width=50, anchor='center')
        tree.column(columns[1], width=50, anchor='center')
        tree.column(columns[2], width=70, anchor='center')
        tree.column(columns[3], width=70, anchor='center')
        tree.column(columns[4], width=70, anchor='center')
        tree.column(columns[5], width=70, anchor='center')
        tree.column(columns[6], width=70, anchor='center')

        # 显示头索引
        for i in columns:
            tree.heading(i, text=i)

        # 将数据库中的数据再表中排序显示
        if (target == -1):
            student = Database.showstudent(Database, self.user, self.password)
        else:
            student = Database.sortstudent(Database, self.user, self.password, target=target)
        if condition:
            student = constu
        for row in student:
            tree.insert("", END, value=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        tree.pack(anchor='w', ipadx=100, side=LEFT, expand=False, fill=BOTH)
        vbar1 = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vbar1.set)
        vbar1.pack(side=RIGHT, fill=Y)

        vbar2 = ttk.Scrollbar(orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=vbar2.set)
        vbar2.pack(side=BOTTOM, fill=X)
        frame_table.pack(expand=YES, fill=BOTH)

        def click(event, tree=tree):
            """闭包，获取对表点击的坐标"""
            row = tree.identify_row(event.y)
            # 使用非局部变量row_info获取鼠标点击的表的数据，防止被GC回收，用来传参
            nonlocal row_info
            row_info = list(tree.item(row, "values"))

        tree.bind('<Button-1>', click)

        # 进入事件循环
        self.root.mainloop()

    # 登录界面
    def login(self):
        """登录界面"""
        self.root.title("登录界面")
        # 设置窗口大小
        self.root.geometry("280x240+%d+%d" % (self.screen_width / 4, self.screen_height / 7))
        # 在root_2中添加登录信息
        global bm
        img = Image.open('./swu.jpg')
        img = img.resize((120, 100))
        bm = ImageTk.PhotoImage(img)
        label_img = Label(self.frame_1, image=bm)
        label_1 = Label(self.frame_1, text="用户名:")
        label_2 = Label(self.frame_1, text="密码:")
        # 以网格布局的形式加入到root_2中
        label_img.grid(row=0, column=1)
        label_1.grid(row=1, column=0)
        self.entry_1.grid(row=1, column=1)
        label_2.grid(row=3, column=0)
        self.entry_2.grid(row=3, column=1)

        # 添加用户名和密码的文本框
        self.list_1.append(self.entry_1)
        self.list_1.append(self.entry_2)

        # 添加按钮
        button_1 = Button(self.frame_1, text="登录", command=lambda: self.judge(), width=10)
        button_2 = Button(self.frame_1, text="清除", command=lambda: self.clearentry(), width=10)
        button_1.grid(row=4, column=1)
        button_2.grid(row=5, column=1)

        self.root.mainloop()

    def judge(self):
        """判断用户名和密码是否正确"""
        # 如果用户名和密码正确
        if Database.condatabase(Database, self.entry_1.get(), self.entry_2.get()):
            self.user = self.entry_1.get()
            self.password = self.entry_2.get()
            # 消息提示
            showinfo(title="提示界面", message="登录成功！！！\n欢迎使用学成绩管理系统")
            # 清除登陆界面的组件
            for widget in self.frame_1.winfo_children():
                widget.destroy()
            self.init_1()
        else:
            showerror(title="错误界面", message="用户名或密码错误！！！\n请重新输入！！！")

    def clearentry(self):
        """清除文本框内容"""
        for i in range(len(self.list_1)):
            self.list_1[i].delete(0, 'end')

    def addstudent(self):
        """添加学生信息"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        # 窗口大小
        self.root.geometry("550x200")
        # 在容器frame中添加学生的各种信息
        label_1 = Label(self.root, text="姓名:", width=30)
        label_2 = Label(self.root, text="性别:")
        label_3 = Label(self.root, text="学号:")

        entry_1 = Entry(self.root, bd=5)
        entry_2 = Entry(self.root, bd=5)
        entry_3 = Entry(self.root, bd=5)

        # 以网格布局的形式加入到frame中
        label_1.grid(row=0, column=0)
        entry_1.grid(row=0, column=1)
        label_2.grid(row=1, column=0)
        entry_2.grid(row=1, column=1)
        label_3.grid(row=2, column=0)
        entry_3.grid(row=2, column=1)

        # 将文本框添加到列表中
        self.list_1.append(entry_1)
        self.list_1.append(entry_2)
        self.list_1.append(entry_3)

        # 添加按钮
        # 若要给函数传递参数，需要利用lambda表达式
        # 绑定添加功能
        button_1 = Button(self.root, text="提交",
                          command=lambda: Database.addstudent(Database, self.user,
                                                              self.password, entry_1.get(), entry_2.get(),
                                                              entry_3.get()
                                                              )
                          )
        button_2 = Button(self.root, text="清除", command=lambda: self.clearentry())
        button_3 = Button(self.root, text="返回", command=lambda: self.init_1())
        button_1.grid(row=6, column=0)
        button_2.grid(row=6, column=1)
        button_3.grid(row=6, column=2)

    def sort(self, target=0):
        """对成绩进行排序target=0，1，2，3分别表示按总分、语文、数学、英语成绩降序排序"""
        return self.init_1(target=target)

    def delete_win(self, row_info):
        """删除学生的窗口"""
        if row_info == []:
            messagebox.showinfo('提示', '请选中一个学生')
            return
        flag = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if (flag == True):
            self.deletestu(row_info)

    def deletestu(self, row_info):
        """确认删除后调用数据库工具类的删除，用学号删（设置了学号非重）"""
        id = row_info[2]
        Database.deletestu(Database, self.user, self.password, id)
        return self.init_1()

    def find_win(self):
        """查询窗口"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        self.root.title('查询学生')
        self.root.geometry('250x390')
        Button(self.root, text='按学号查询', command=lambda: self.id_name_seek(0)).pack(pady=45)
        Button(self.root, text='按姓名查询', command=lambda: self.id_name_seek(1)).pack(pady=45)
        Button(self.root, text='按成绩查询', command=lambda: self.sco_win()).pack(pady=45)
        Button(self.root, text='返回', width=20, command=lambda: self.init_1()).pack(anchor='s', side=RIGHT)

    def id_name_seek(self, type):
        """查询学生信息，type=0为按学号查询，type=1为按姓名查询"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        way = '学号' if type == 0 else '姓名'
        self.root.title('%s查询' % way)
        self.root.geometry('300x360')
        Label(self.root, text='输入学生%s' % way, font=('Verdana', 15)).pack(pady=20)
        anser = Entry(self.root)
        anser.pack()
        Button(self.root, text='确认', width=10, command=lambda: self.find_stu(type, info=repr(anser.get()))).pack(
            side=LEFT, padx=25)
        Button(self.root, text='返回', width=10, command=lambda: self.find_win()).pack(side=RIGHT, padx=25)

    def sco_win(self):
        """按分数查询的窗口"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        self.root.title('按成绩查询')
        self.root.geometry('250x390')
        Button(self.root, text='按语文成绩查询', command=lambda: self.sco_seek(0)).pack(pady=25)
        Button(self.root, text='按数学成绩查询', command=lambda: self.sco_seek(1)).pack(pady=25)
        Button(self.root, text='按英语成绩查询', command=lambda: self.sco_seek(2)).pack(pady=25)
        Button(self.root, text='按成绩总和查询', command=lambda: self.sco_seek(3)).pack(pady=25)
        Button(self.root, text='返回', width=20, command=lambda: self.find_win()).pack(anchor='s', side=RIGHT)

    def sco_seek(self, type):
        """           查询学生信息，
            type=0为按语文成绩查询，type=1为按数学成绩查询，
            tpye=2为按英语成绩查询，type=3为按成绩总和查询
        """
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        if type == 0:
            way = '语文成绩'
        elif type == 1:
            way = '数学成绩'
        elif type == 2:
            way = '英语成绩'
        elif type == 3:
            way = '总成绩'
        self.root.title('%s查询' % way)
        self.root.geometry('300x360')
        Label(self.root, text='输入学生最低%s' % way, font=('Verdana', 15)).pack(pady=20)
        min = Entry(self.root)
        min.pack()
        Label(self.root, text='输入学生最高%s' % way, font=('Verdana', 15)).pack(pady=20)
        max = Entry(self.root)
        max.pack()
        self.list_1.append(min)
        self.list_1.append(max)
        Button(self.root, text='提交', width=20,
               command=lambda: self.find_sco(type, float(min.get()), float(max.get()))).pack(pady=20)
        Button(self.root, text='清除', width=20, command=lambda: self.clearentry()).pack(anchor='s', side=LEFT)
        Button(self.root, text='返回', width=20, command=lambda: self.sco_win()).pack(anchor='s', side=RIGHT)

    def find_stu(self, inx, info):
        """查找学生实现方法，调用Database的查找返回的对象当初条件传入init_1"""
        a = Database.find_stu(Database, self.user, self.password, inx, info)
        self.init_1(target=-1, condition=True, constu=a)

    def find_sco(self, type, min, max):
        """按分数查找实现方法，调用Database的查找返回的对象当初条件传入init_1"""
        a = Database.find_sco(Database, self.user, self.password, type, min, max)
        self.init_1(target=-1, condition=True, constu=a)

    def update_win(self, row_info):
        """更改更新形象的窗口"""
        if row_info == []:
            messagebox.showinfo('提示', '请选中一个学生')
            return
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title('%s的信息' % row_info[0])
        self.root.geometry('250x430')
        Button(self.root, text='学生信息修改', command=lambda: self.update_stu_info_win(row_info)).pack(pady=25)
        Button(self.root, text='学生成绩录入', command=lambda: self.insert_sco_win(row_info)).pack(pady=25)
        Button(self.root, text='语文成绩修改', command=lambda: self.update_sco_info_win(row_info, 3)).pack(pady=25)
        Button(self.root, text='数学成绩修改', command=lambda: self.update_sco_info_win(row_info, 4)).pack(pady=25)
        Button(self.root, text='英语成绩修改', command=lambda: self.update_sco_info_win(row_info, 5)).pack(pady=25)
        Button(self.root, text='返回', width=20, command=lambda: self.init_1()).pack(anchor='s', side=RIGHT)

    def update_stu_info_win(self, row_info):
        """更改学生基本信息的窗口"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        self.root.title('%s的基本信息修改' % row_info[0])
        self.root.geometry('250x430')
        Button(self.root, text='修改姓名', command=lambda: self.update_stu_info(row_info, 0)).pack(pady=25)
        Button(self.root, text='修改性别', command=lambda: self.update_stu_info(row_info, 1)).pack(pady=25)
        Button(self.root, text='修改学号', command=lambda: self.update_stu_info(row_info, 2)).pack(pady=25)
        Button(self.root, text='返回', width=20, command=lambda: self.update_win(row_info)).pack(anchor='s', side=RIGHT)

    def update_stu_info(self, row_info, inx):
        """更改学生信息的方法实现"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        info = ['姓名', '性别', '学号']
        self.root.title('%s的%s修改' % (row_info[0], info[inx]))
        self.root.geometry('300x260')
        Label(self.root, text='输入更改后的%s' % info[inx], font=('Verdana', 15)).pack(pady=20)
        entry = Entry(self.root)
        entry.pack()
        self.list_1.append(entry)
        Button(self.root, text='提交', width=20,
               command=lambda: Database.update_stu_info(Database, self.user, self.password, row_info, inx,
                                                        repr(entry.get()))).pack(pady=20)
        Button(self.root, text='清除', width=20, command=lambda: self.clearentry()).pack(anchor='s', side=LEFT)
        Button(self.root, text='返回', width=20, command=lambda: self.update_stu_info_win(row_info)).pack(anchor='s',
                                                                                                        side=RIGHT)

    def update_sco_info_win(self, row_info, inx):
        """修改成绩的窗口"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        info = ['语文', '数学', '英语']
        self.root.title('%s的成绩修改' % row_info[0])
        self.root.geometry('250x230')
        Label(self.root, text='输入更改后的%s成绩' % info[inx - 3], font=('Verdana', 15)).pack(pady=20)
        entry = Entry(self.root)
        entry.pack()
        self.list_1.append(entry)
        Button(self.root, text='提交', width=20,
               command=lambda: Database.update_stu_info(Database, self.user, self.password, row_info, inx,
                                                        float(entry.get()))).pack()
        Button(self.root, text='返回', width=20, command=lambda: self.update_win(row_info)).pack(anchor='s', side=RIGHT)

    def insert_sco_win(self, row_info):
        """录入成绩窗口"""
        # 清空组件,防止组件重叠
        for widget in self.root.winfo_children():
            widget.destroy()
        # 清空list_1
        self.list_1.clear()
        self.root.title('录入%s的成绩' % (row_info[0]))
        self.root.geometry('300x180')
        Label(self.root, text='录入语文成绩：').grid(row=0, padx=10, pady=5)
        cn = Entry(self.root)
        cn.grid(row=0, column=1)
        Label(self.root, text='录入数学成绩：').grid(row=1, padx=10, pady=5)
        mh = Entry(self.root)
        mh.grid(row=1, column=1)
        Label(self.root, text='录入英语成绩：').grid(row=2, padx=10, pady=5)
        en = Entry(self.root)
        en.grid(row=2, column=1)
        Button(self.root, text='返回', width=10, command=lambda: self.update_win(row_info)).grid(row=3, sticky=W)
        Button(self.root, text='确认', width=10,
               command=lambda: self.insert_all_sco(row_info, float(cn.get()), float(mh.get()), float(en.get()))).grid(
            row=3, column=1, sticky=E)

    def insert_all_sco(self, row_info, cn, mh, en):
        """录入成绩方法调用三次Databse的方法分别将三科成绩录入"""
        li = [cn, mh, en]
        for inx in range(3, 6):
            Database.update_stu_info(Database, self.user, self.password, row_info, inx, li[inx - 3], all=True)
