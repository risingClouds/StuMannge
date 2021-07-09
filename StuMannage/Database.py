# -*- coding:utf-8 -*-
"""
作者：智科类1班  罗涛（学号：222020335220012）
日期：2021年07月07日
"""


import pymysql
from tkinter.messagebox import *


class Database:
    """数据库工具类"""

    # 类变量
    db = None # 数据库
    cursor = None # 游标

    def condatabase(self, user, password):
        """ 连接数据库"""
        # 打开数据库连接
        try:
            self.db = pymysql.connect(host="127.0.0.1", user=user, password=password, database="stu")
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cursor = self.db.cursor()
            return True
        except Exception as e:
            print(e)
            return False

    def addstudent(self, user, passwd, name, gender, id):
        """添加学生"""
        self.condatabase(self, user, passwd)
        # 检查学号是否重复,是的话函数结束
        if self.determinestudent(self, user, passwd, id):
            return
        sql = "insert into student values(%s,%s,%s);"
        sql2 = "insert into grade(id) values (%s);"%id
        try:
            # 使用 execute()  方法执行 SQL,在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql, (name, gender, id))
            self.cursor.execute(sql2)
            self.db.commit()
            # 消息提示
            showinfo(title="提示界面", message="添加学生信息成功！！！")
        except Exception as e:
            print(e)
            showerror(title="错误界面", message="数据库异常！！！\n加入失败！！！")
            self.db.rollback()
        # 关闭数据库连接
        self.db.close()

    def determinestudent(self, user, passwd, id):
        """判断学号重复"""
        self.condatabase(self, user, passwd)
        sql = "select * from student where id = %s;" % id
        try:
            # 在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is not None:
                showerror(title="错误界面", message="学号重复！！！")
                self.db.rollback()
                return True
        except:
            self.db.rollback()
            return False
        self.db.close()

    def showstudent(self, user, passwd):
        """输出学生信息"""
        self.condatabase(self, user, passwd)
        sql = "select s.name,s.sex,s.id,g.cn,g.mh,g.en,g.cn+g.mh+g.en from student s left join grade g on g.id=s.id order by s.id;"
        try:
            # 在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
        self.db.close()

    # order by
    def sortstudent(self, user, passwd, target):
        """
            排序
            target == 0,1,2,3分别代表按总分，语文，数学，英语排序
        """
        self.condatabase(self, user, passwd)
        if target == 0:
            st = "zongfen"
        elif target == 1:
            st = "g.cn"
        elif target == 2:
            st = "g.mh"
        elif target == 3:
            st = "g.en"
        else:
            st = "g.id"
        sql = "select s.name,s.sex,s.id,g.cn,g.mh,g.en,g.cn+g.mh+g.en as zongfen from student s left join grade g on g.id=s.id order by %s desc;" % (
            st)
        try:
            # 在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
        self.db.close()

    def deletestu(self, user, passwd, id):
        """按学号删除学生和成绩"""
        self.condatabase(self, user, passwd)
        sql1 = 'delete from student where id=%s;' % (id)
        sql2 = 'delete from grade where id=%s;' % (id)

        try:
            # 在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.db.commit()
        except:
            self.db.rollback()
        self.db.close()

    def find_stu(self, user, passwd, inx, info):
        """按条件找到符合的学生"""
        self.condatabase(self, user, passwd)
        columns = ['s.id', 's.name']
        target = columns[inx]
        sql = "select s.name,s.sex,s.id,g.cn,g.mh,g.en,g.cn+g.mh+g.en as zongfen from student s left join grade g on g.id=s.id where %s=%s" % (
            target, info)
        try:
            # 在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
        self.db.close()

    def find_sco(self, user, passwd, type, min, max):
        """
            找到符合分数区间的学生
            参数type==0,1,2,3分别代表按语文、数学、英语、总分查找
        """
        self.condatabase(self, user, passwd)
        if type == 0:
            way = 'g.cn'
        elif type == 1:
            way = 'g.mh'
        elif type == 2:
            way = 'g.en'
        elif type == 3:
            way = 'g.cn+g.mh+g.en'
        sql = "select s.name,s.sex,s.id,g.cn,g.mh,g.en,g.cn+g.mh+g.en as zongfen from student s left join grade g on g.id=s.id where %s between %s and %s" % (
            way, min, max)
        try:
            # 在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            self.db.rollback()
        self.db.close()

    def update_stu_info(self, user, passwd, row_info, inx, new_info, all=False):
        """更新学生基本信息、all表明是否要更新所有信息"""
        self.condatabase(self, user, passwd)
        if inx == 2:
            # 该学号需要查重
            if self.determinestudent(self, user, passwd, new_info):
                return
        if 0 <= inx <= 2:
            # 改学生表
            colunms = ['name', 'sex', 'id']
            sql = "update student set %s=%s where id=%s;" % (colunms[inx], new_info, row_info[2])
        elif 3 <= inx <= 5:
            # 改成绩表
            colunms = ['cn', 'mh', 'en']
            sql = "update grade set %s=%s where id=%s;" % (colunms[inx - 3], new_info, row_info[2])

        try:
            # 使用 execute()  方法执行 SQL,在每次运行sql之前，ping一次，如果连接断开就重连。
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            if inx == 2:
                # 学号需要改两个表
                sql1 = 'update grade set id=%s where id=%s;' % (new_info, row_info[2])
                self.cursor.execute(sql1)
            self.db.commit()
            # 消息提示
            if not all:
                showinfo(title="提示界面", message="修改信息成功！！！")
            else:
                if inx == 5:
                    showinfo(title="提示界面", message="录入成绩成功！！！")
        except Exception as e:
            print(e)
            showerror(title="错误界面", message="数据库异常！！！\n修改失败！！！")
            self.db.rollback()
        # 关闭数据库连接
        self.db.close()