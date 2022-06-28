# -*- coding:utf-8 -*-
# !/bin/sh
# !/usr/bin/python
# !/usr/bin/env
import os
import sys
import requests
import json
import time
# from PyQt5.QtGui import QFont

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from urllib import parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from apscheduler.schedulers.blocking import BlockingScheduler
from winsound import Beep


class Six(QWidget):
    def __init__(self):
        super().__init__()
        # 窗口标题
        self.setWindowTitle('iBox公告监控——未启动')
        # 窗口大小
        self.resize(720, 600)
        # 窗口居中
        self.center()
        # 二次添加
        self.table_view = None
        self.list_view = None
        self.content_browser = None
        self.key_label = None
        self.key_input = None
        self.send_label = None
        self.send_input = None
        self.pwd_label = None
        self.pwd_input = None
        self.rec_label = None
        self.rec_input = None
        self.rec_add_button = None
        self.delay_label = None
        self.delay_input = None
        self.start_button = None
        self.stop_button = None
        self.del_list = None
        self.emails = None
        self.send_email = None
        self.send_key = None
        self.delay_time = None
        self.job = None
        self.ip_arr = []
        self.start_flag = 0
        self.not_id = 0
        self.send_flag = 0
        self.main_show = self
        self.init_ui()

    # 设置窗口主要部件和信号
    def init_ui(self):
        # 创建窗口
        self.create_window()
        self.get_context()
        self.set_list_view()
        self.set_content_browser()
        self.set_key_label()
        self.set_key_input()
        self.set_send_label()
        self.set_send_input()
        self.set_pwd_label()
        self.set_pwd_input()
        self.set_rec_label()
        self.set_rec_input()
        self.set_delay_label()
        self.set_delay_input()

        # self.setWindowIcon(QIcon('logo.png'))

        # TODO 绑定信号槽
        self.rec_add_button.clicked.connect(self.add_rec)
        self.start_button.clicked.connect(self.start_action)
        self.stop_button.clicked.connect(self.stop_action)

        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.list_view_menu)

    def get_ip(self):
        try:
            if self.key_input.text() != "":
                response = requests.get(self.key_input.text())
                page_dict = json.loads(response.text)
                # 生成IP数组
                for i in page_dict["obj"]:
                    print(f'{i["ip"]}:{i["port"]}')
                    self.ip_arr.append(f'{i["ip"]}:{i["port"]}')
        except Exception as e:
            self.message_dialog("提示", "请检查IP余量")

    # 窗口居中
    def center(self):
        """
        窗口居中
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(round((screen.width() - size.width()) / 2), round((screen.height() - size.height()) / 2))

    # 窗口布局
    def create_window(self):
        # 输出内容
        self.content_browser = QTextBrowser()
        # 设置邮箱列表
        self.list_view = QListWidget()
        # 代理api文字
        self.key_label = QLabel()
        self.key_input = QLineEdit()
        # 发件人邮箱
        self.send_label = QLabel()
        self.send_input = QLineEdit()
        # 发件人密码
        self.pwd_label = QLabel()
        self.pwd_input = QLineEdit()
        # 收件人邮箱
        self.rec_label = QLabel()
        self.rec_input = QLineEdit()
        self.rec_add_button = QPushButton('添加')
        # 延迟
        self.delay_label = QLabel()
        self.delay_input = QLineEdit()
        self.start_button = QPushButton('启动')
        self.stop_button = QPushButton('停止')

        # 代理api
        key_layout = QHBoxLayout()
        key_layout.addWidget(self.key_label, 1)
        key_layout.addWidget(self.key_input, 3)

        # 发件人邮箱
        send_layout = QHBoxLayout()
        send_layout.addWidget(self.send_label, 1)
        send_layout.addWidget(self.send_input, 3)

        # 发件人密码
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(self.pwd_label, 1)
        pwd_layout.addWidget(self.pwd_input, 3)

        # 收件人邮箱
        rec_right_layout = QHBoxLayout()
        rec_right_layout.addWidget(self.rec_input)
        rec_right_layout.addWidget(self.rec_add_button)
        rec_layout = QHBoxLayout()
        rec_layout.addWidget(self.rec_label, 1)
        rec_layout.addLayout(rec_right_layout, 3)

        # 延迟
        delay_right_layout = QHBoxLayout()
        delay_right_layout.addWidget(self.delay_input)
        delay_right_layout.addWidget(self.start_button)
        delay_right_layout.addWidget(self.stop_button)
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(self.delay_label, 1)
        delay_layout.addLayout(delay_right_layout, 3)

        # 左下布局
        left_bottom_layout = QVBoxLayout()
        left_bottom_layout.addLayout(key_layout, 1)
        left_bottom_layout.addLayout(send_layout, 1)
        left_bottom_layout.addLayout(pwd_layout, 1)
        left_bottom_layout.addLayout(rec_layout, 1)
        left_bottom_layout.addLayout(delay_layout, 1)

        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_view, 5)
        left_layout.addLayout(left_bottom_layout, 2)

        # 右侧布局
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.content_browser)

        # 创建界面
        layout = QHBoxLayout(self)
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 1)
        self.setLayout(layout)

    # 获取服务器信息
    def get_context(self):
        # print("i am get_context")
        # page = requests.get("http://175.178.68.51:3000/context?userName=123")
        page = requests.get("http://175.178.68.51:3000/context?userName=" + user_name)
        page_dict = json.loads(page.text)

        if page_dict['emails'] is None:
            self.emails = 'xxx@qq.com'
        else:
            self.emails = json.loads(page_dict['emails'])

        if page_dict['sendEmail'] is None:
            self.send_email = 'xxx@qq.com'
        else:
            self.send_email = page_dict['sendEmail']

        if page_dict['sendKey'] is None:
            self.send_key = ''
        else:
            self.send_key = page_dict['sendKey']

        if page_dict['delayTime'] is None:
            self.delay_time = '30'
        else:
            self.delay_time = page_dict['delayTime']

        if isinstance(self.emails, str):
            self.emails = [self.emails]

        # if page_dict["status"] == 200:
        #     self.message_dialog("注册成功", page_dict["content"])
        # else:
        #     self.message_dialog(page_dict["content"], page_dict["content"])

    # TODO 输出内容
    def set_content_browser(self):
        # pass
        self.content_browser.setText("尚未启动\n发件人授权码在邮箱设置里面，不是软件密钥")
        # self.text_browser.horizontalScrollBar.setValue(0)

    # 收件人邮箱列表
    def set_list_view(self):
        self.list_view.addItems(self.emails)

    def list_view_menu(self, pos):
        menu = QtWidgets.QMenu()
        opt1 = menu.addAction("删除")
        opt2 = menu.addAction("清空")
        action = menu.exec_(self.mapToGlobal(pos))

        if action == opt1:
            self.del_list_action()
        elif action == opt2:
            self.del_all()

    # 删除
    def del_list_action(self):
        if self.start_flag == 1:
            self.message_dialog("提示", "请先停止检测！")
            return
        num_items = self.list_view.currentRow()  # 获取当前行
        self.emails.pop(num_items)
        self.list_view.clear()
        self.list_view.addItems(self.emails)

    def del_all(self):
        if self.start_flag == 1:
            self.message_dialog("提示", "请先停止检测！")
            return
        self.list_view.clear()

    # 代理api
    def set_key_label(self):
        self.key_label.setText("代理api：")  # 创建一个QLabel并写入文字

    def set_key_input(self):
        # pass
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.key_input.setFont(font)
        self.key_input.setText("")
        self.key_input.setTextMargins(5, 2, 0, 2)

    # 发件人邮箱
    def set_send_label(self):
        self.send_label.setText("发件人邮箱：")  # 创建一个QLabel并写入文字

    def set_send_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.send_input.setFont(font)
        self.send_input.setText(self.send_email)
        self.send_input.setTextMargins(5, 2, 0, 2)

    # 发件人密码
    def set_pwd_label(self):
        self.pwd_label.setText("发件人授权码：")  # 创建一个QLabel并写入文字

    def set_pwd_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.pwd_input.setFont(font)
        self.pwd_input.setText(self.send_key)
        self.pwd_input.setTextMargins(5, 2, 0, 2)

    # 收件人邮箱
    def set_rec_label(self):
        self.rec_label.setText("收件人邮箱：")  # 创建一个QLabel并写入文字

    def set_rec_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.rec_input.setFont(font)
        self.rec_input.setTextMargins(5, 2, 0, 2)

    def add_rec(self):
        if self.start_flag == 1:
            self.message_dialog("提示", "请先停止检测！")
            return
        self.emails.append(self.rec_input.text())
        self.list_view.addItem(self.rec_input.text())
        self.rec_input.setText("")

    # 延迟
    def set_delay_label(self):
        self.delay_label.setText("设置延迟/s：")  # 创建一个QLabel并写入文字

    def set_delay_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.delay_input.setFont(font)
        self.delay_input.setTextMargins(5, 2, 0, 2)
        self.delay_input.setText(str(self.delay_time))

    # TODO 启动
    def start_action(self):
        if self.start_flag == 0:
            self.start_flag = 1
            self.first_get()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.get_ip()
            try:
                self.job = GetThread(self)
                self.job.start()
            except Exception as e:
                print(e)
        else:
            self.message_dialog("检测已经启动", "检测已经启动")

    # TODO 停止
    def stop_action(self):
        if self.start_flag == 1:
            self.start_flag = 0
            print("exit")
            if self.job:
                self.job.sto()
                self.job.quit()
                self.job.exit(0)
                self.content_browser.append(f'停止运行！')
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
            self.setWindowTitle('iBox公告监控——未启动')
        else:
            self.message_dialog("检测已经停止", "检测已经停止")

    # 警告信息
    @staticmethod
    def message_dialog(title, text):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, text)
        msg_box.exec_()

    # 关闭窗口时弹出确认消息
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '是否退出', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            params = {
                "userName": user_name,
                "emails": self.emails,
                "sendEmail": self.send_input.text(),
                "sendKey": self.pwd_input.text(),
                "delayTime": self.delay_input.text()
            }
            requests.post("http://175.178.68.51:3000/close", params=params)
            # print(self.job)
            if self.job:
                self.job.quit()
            self.main_show.close()
        else:
            event.ignore()

    def first_get(self):
        try:
            list_page = requests.get(
                "https://api-h5.ibox.art/nft-mall-web/v1.2/nft/product/getCommonNoticeList?page=1&pageSize=20")
            list_dict = json.loads(list_page.text)
            pagelist = list_dict['data']['list']
            id_arr = []
            id_notice = []
            for i in pagelist:
                id_arr.append(i['id'])
                id_notice.append(i['noticeName'])
            self.not_id = max(id_arr)
            notice_name = "公告名"
            for i in pagelist:
                if i['id'] == self.not_id:
                    notice_name = i['noticeName']
            print("公告id", self.not_id)
            self.content_browser.moveCursor(QTextCursor.End)
            self.content_browser.append(f'启动成功，获取到最新公告是：{notice_name}')
            self.setWindowTitle('iBox公告监控——正在运行中....')
        except Exception as e:
            self.content_browser.append(f'启动成功')

        # self.content_browser.append("启动成功，获取到最新公告是", notice_name)


class GetThread(QThread):
    def __init__(self, my_app):
        super().__init__()
        self.my_app = my_app
        self.job = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'}
        self.index = 0
        self.id_arr = []
        self.id_notice = []

    def run(self):
        self.my_job()
        # print(111)
        # if self.my_app.key_input.text() == "":
        #     print(123)

        # sched = BlockingScheduler()
        # self.job = sched.add_job(self.my_job, 'interval', seconds=int(self.my_app.delay_input.text()))
        # # self.job = sched.add_job(self.my_job, 'interval', seconds=int(self.my_app.delay_input.text()), max_instances=1)
        # sched.start()

    def sto(self):
        self.job.remove()
        self.quit()
        self.exit(0)

    def no_in(self):
        try:
            list_page = requests.get(
                "https://api-h5.ibox.art/nft-mall-web/v1.2/nft/product/getCommonNoticeList?page=1&pageSize=20")
            list_dict = json.loads(list_page.text)
            pagelist = list_dict['data']['list']
            id_arr = []
            id_notice = []
            for i in pagelist:
                id_arr.append(i['id'])
                id_notice.append(i['noticeName'])
            print(max(id_arr))

            if max(id_arr) > self.my_app.not_id:
                self.my_app.not_id = max(id_arr)
                # self.content_browser.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                # print(id_notice)
                notice_name = "公告名"
                for i in pagelist:
                    if i['id'] == self.my_app.not_id:
                        notice_name = i['noticeName']
                # print(notice_name)
                self.my_app.content_browser.moveCursor(QTextCursor.End)
                self.my_app.content_browser.append(f'获取到最新公告是{notice_name}')
                print('获取到最新公告是', notice_name)

                # 发信方的信息：发信邮箱，QQ 邮箱授权码
                from_addr = self.my_app.send_email
                password = self.my_app.send_key

                # 收信方邮箱
                recer = self.my_app.emails

                # 发信服务器
                smtp_server = 'smtp.qq.com'

                # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码 https://www.ibox.art/zh-cn/notice/detail/?id=127
                msg = MIMEText(
                    "<div>手机QQ自带的邮箱可能查看不了</div><div>iBox已发送公告，前往 <a href='https://www.ibox.art/zh-cn/no"
                    "tice/detail/?id=" + str(self.my_app.not_id) + "'>iBox公告栏</a> 查看。</div>稍后可能会提醒第二次",
                    'html', 'utf-8')
                msg['From'] = Header('iBox公告第一次提示')
                msg['To'] = ",".join(recer)
                msg['Subject'] = Header(notice_name)

                try:
                    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                    s.login(from_addr, password)
                    s.sendmail(from_addr, recer, msg.as_string())
                    s.quit()
                    Beep(1000, 1000)
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append('发送成功！')
                    self.my_app.send_flag = 0
                except smtplib.SMTPException as e:
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append(f"发送失败,错误信息：{e}")
                try:
                    time.sleep(10)
                    page = requests.get("https://api-h5.ibox.art/nft-mall-web/v1.2/nft/product/getCommonNoticeInfo",
                                        params={'id': self.my_app.not_id})
                    notice_dict = json.loads(page.text)
                    notice_content = notice_dict['data']['noticeContent']
                    notice_html = parse.unquote(notice_content)
                    notice_html = notice_html.replace('src="', 'src="https://www.ibox.art')

                    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
                    msg = MIMEText(notice_html, 'html', 'utf-8')
                    msg['From'] = Header('iBox公告')
                    msg['To'] = ",".join(recer)
                    msg['Subject'] = Header(notice_name)

                    try:
                        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                        s.login(from_addr, password)
                        s.sendmail(from_addr, recer, msg.as_string())
                        s.quit()
                        self.my_app.content_browser.moveCursor(QTextCursor.End)
                        self.my_app.content_browser.append("发送成功！")
                        self.my_app.send_flag = 1
                    except smtplib.SMTPException as e:
                        self.my_app.content_browser.moveCursor(QTextCursor.End)
                        self.my_app.content_browser.append(f'发送失败,错误信息：{e}')
                except Exception as e:
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append("滑动模块，重新获取...")
                    if self.my_app.send_flag == 0:
                        time.sleep(30)
                        page = requests.get(
                            "https://api-h5.ibox.art/nft-mall-web/v1.2/nft/product/getCommonNoticeInfo",
                            params={'id': self.my_app.not_id})
                        notice_dict = json.loads(page.text)
                        notice_content = notice_dict['data']['noticeContent']
                        notice_html = parse.unquote(notice_content)
                        notice_html = notice_html.replace('src="', 'src="https://www.ibox.art')

                        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
                        msg = MIMEText(notice_html, 'html', 'utf-8')
                        msg['From'] = Header('iBox公告')
                        msg['To'] = ",".join(recer)
                        msg['Subject'] = Header(notice_name)

                        try:
                            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                            s.login(from_addr, password)
                            s.sendmail(from_addr, recer, msg.as_string())
                            s.quit()
                            self.my_app.content_browser.moveCursor(QTextCursor.End)
                            self.my_app.content_browser.append("发送成功！")
                            self.my_app.send_flag = 1
                        except smtplib.SMTPException as e:
                            self.my_app.content_browser.moveCursor(QTextCursor.End)
                            self.my_app.content_browser.append(f'发送失败,错误信息：{e}')
                if self.my_app.send_flag == 0:
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append("滑动模块，重新获取...")
            else:
                self.my_app.content_browser.moveCursor(QTextCursor.End)
                self.my_app.content_browser.append("没有公告发布，继续监听...")
                self.my_app.content_browser.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except Exception as e:
            print("???", e)
            self.my_app.content_browser.moveCursor(QTextCursor.End)
            self.my_app.content_browser.append("滑动模块，重新获取...")

    def quert_list(self):
        try:
            list_page = requests.get(
                "https://api-h5.ibox.art/nft-mall-web/v1.2/nft/product/getCommonNoticeList?page=1&pageSize=20",
                proxies={'https': self.my_app.ip_arr[self.index]}, headers=self.headers
            )
            list_dict = json.loads(list_page.text)
            pagelist = list_dict['data']['list']
            return pagelist
        except Exception as e:
            return e

    def query_content(self):
        try:
            page = requests.get(
                "https://api-h5.ibox.art/nft-mall-web/v1.2/nft/product/getCommonNoticeInfo",
                params={'id': self.my_app.not_id},
                proxies={'https': self.my_app.ip_arr[self.index]},
                headers=self.headers)
            notice_dict = json.loads(page.text)
            notice_content = notice_dict['data']['noticeContent']
            notice_html = parse.unquote(notice_content)
            notice_html = notice_html.replace('src="', 'src="https://www.ibox.art')
            return notice_html
        except Exception as e:
            return 1

    def has_in(self):
        pagelist = self.quert_list()
        print(type(pagelist))
        if type(pagelist) == "list":
            for i in pagelist:
                self.id_arr.append(i['id'])
                self.id_notice.append(i['noticeName'])
            max_notice = max(self.id_arr)
            if max_notice > self.my_app.not_id:
                for i in pagelist:
                    self.id_arr.append(i['id'])
                    self.id_notice.append(i['noticeName'])
                self.my_app.not_id = max_notice
                notice_name = "公告名"
                for i in pagelist:
                    if i['id'] == self.my_app.not_id:
                        notice_name = i['noticeName']
                # print(notice_name)
                self.my_app.content_browser.moveCursor(QTextCursor.End)
                self.my_app.content_browser.append(f'获取到最新公告是{notice_name}')
                print('获取到最新公告是', notice_name)

                # 发信方的信息：发信邮箱，QQ 邮箱授权码
                from_addr = self.my_app.send_email
                password = self.my_app.send_key

                # 收信方邮箱
                recer = self.my_app.emails

                # 发信服务器
                smtp_server = 'smtp.qq.com'

                # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码 https://www.ibox.art/zh-cn/notice/detail/?id=127
                msg = MIMEText(
                    "<div>手机QQ自带的邮箱可能查看不了</div><div>iBox已发送公告，前往 <a href='https://www.ibox.art/zh-cn/no"
                    "tice/detail/?id=" + str(self.my_app.not_id) + "'>iBox公告栏</a> 查看。</div>稍后可能会提醒第二次",
                    'html', 'utf-8')
                msg['From'] = Header('iBox公告第一次提示')
                msg['To'] = ",".join(recer)
                msg['Subject'] = Header(notice_name)

                # 第一次发邮件
                try:
                    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                    s.login(from_addr, password)
                    s.sendmail(from_addr, recer, msg.as_string())
                    s.quit()
                    Beep(1000, 1000)
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append('发送成功！')
                    index_flag = 1
                    self.my_app.send_flag = 0
                except smtplib.SMTPException as e:
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append(f"发送失败,请检查发件人授权码。错误信息：{e}")

                # 第二次发邮件
                notice_html = self.query_content()
                # 如果返回不是字符串，则一直执行
                while type(notice_html) != 'str':
                    if self.index == len(self.my_app.ip_arr) - 1:
                        self.index = 0
                    else:
                        self.index += 1
                    notice_html = self.query_content()
                # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
                msg = MIMEText(notice_html, 'html', 'utf-8')
                msg['From'] = Header('iBox公告')
                msg['To'] = ",".join(recer)
                msg['Subject'] = Header(notice_name)

                try:
                    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                    s.login(from_addr, password)
                    s.sendmail(from_addr, recer, msg.as_string())
                    s.quit()
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append("发送成功！")
                    self.my_app.send_flag = 1
                except smtplib.SMTPException as e:
                    self.my_app.content_browser.moveCursor(QTextCursor.End)
                    self.my_app.content_browser.append(f'发送失败,错误信息：{e}')
            else:
                if self.index == len(self.my_app.ip_arr) - 1:
                    self.index = 0
                else:
                    self.index += 1
                self.my_app.content_browser.moveCursor(QTextCursor.End)
                self.my_app.content_browser.append("没有公告发布，继续监听...")
                self.my_app.content_browser.append(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def my_job(self):
        if self.my_app.key_input.text() == "":
            sched = BlockingScheduler()
            self.job = sched.add_job(self.no_in, 'interval', seconds=int(self.my_app.delay_input.text()))
            sched.start()
        else:
            sched = BlockingScheduler()
            self.job = sched.add_job(self.has_in, 'interval', seconds=int(self.my_app.delay_input.text()))
            sched.start()
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


class RoundShadow(QWidget):
    """圆角边框类"""

    def __init__(self, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.border_width = 8
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

    # def paintEvent(self, event):
    #     # # 阴影
    #     # path = QPainterPath()
    #     # path.setFillRule(Qt.WindingFill)
    #     # pat = QPainter(self)
    #     # pat.setRenderHint(pat.Antialiasing)
    #     # pat.fillPath(path, QBrush(Qt.white))
    #     # color = QColor(155, 155, 155, 10)
    #     # for i in range(10):
    #     #     i_path = QPainterPath()
    #     #     i_path.setFillRule(Qt.WindingFill)
    #     #     ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
    #     #     # i_path.addRect(ref)
    #     #     i_path.addRoundedRect(ref, self.border_width, self.border_width)
    #     #     color.setAlpha(150 - i ** 0.7 * 50)
    #     #     pat.setPen(color)
    #     #     pat.drawPath(i_path)
    #     # 圆角
    #     pat2 = QPainter(self)
    #     pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
    #     pat2.setBrush(Qt.white)
    #     pat2.setPen(Qt.transparent)
    #     rect = self.rect()
    #     rect.setLeft(9)
    #     rect.setTop(9)
    #     rect.setWidth(rect.width() - 9)
    #     rect.setHeight(rect.height() - 9)
    #     pat2.drawRoundedRect(rect, 8, 8)


class Process(QWidget):
    def __init__(self, *args, **kwargs):
        super(Process, self).__init__(*args, **kwargs)
        self.root = os.getcwd()  # 获得当前路径 /home/dir1
        self.root = self.root.replace("\\", "/")
        self.main_show = self
        # self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("更新中")
        self.center()
        layout = QHBoxLayout(self)

        # 增加进度条
        self.progressBar = QProgressBar(self, minimumWidth=200)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.on_pushButton_clicked()

    # 下载按钮事件
    def on_pushButton_clicked(self):
        the_url = 'http://175.178.68.51:3000/update'
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        # the_filepath = "D:/sogou_pinyin_93e.exe"
        the_fileobj = open(f"{self.root}/iBox公告检测.exe", 'wb')
        #### 创建下载线程
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    # 设置进度条
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            reply = QMessageBox.information(self, "提示", "更新成功，点击确定重启应用！")
            if reply == QMessageBox.Ok:
                self.main_show.close()
                ex = self.root + "/iBox公告检测.exe"
                os.startfile(ex)
            return

    # 窗口居中
    def center(self):
        """
        窗口居中
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(round((screen.width() - size.width()) / 2), round((screen.height() - size.height()) / 2))


##################################################################
# 下载线程
##################################################################
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)  # 创建信号

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)  # 流下载模式
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)  # 设置指针位置
                self.fileobj.write(chunk)  # 写入文件
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))  # 发送信号
            #######################################################################
            self.fileobj.close()  # 关闭文件
            self.exit(0)  # 关闭线程
        except Exception as e:
            print(e)

    # def upgradeProgress(self):
    #     self.currentValue = (self.currentValue + 1) % 101
    #     self.progessBar.setValue(self.currentValue)


class Login(QWidget):
    # 自定义信号, 注意信号必须为类属性
    double_clicked = pyqtSignal()  # 自定义信号 两个类若想互传信号，必须定义此函数
    clicked = pyqtSignal(str)  # 表示单击qlabel标签，回传信号

    def __init__(self):
        super().__init__()
        self.setObjectName("login")
        # 窗口标题
        self.setWindowTitle('登录')

        # 窗口大小
        self.resize(350, 200)
        # 窗口居中
        self.center()
        # 图标
        self.user_label = None
        self.user_input = None
        self.pwd_label = None
        self.pwd_input = None
        self.key_label = None
        self.key_input = None
        self.reg_button = None
        self.login_button = None
        self.forget_label = None
        self.main_show = self
        self.init_ui()

    # 设置窗口主要部件和信号
    def init_ui(self):
        try:
            global level
            page = requests.get("http://175.178.68.51:3000/checknet")
            page_dict = json.loads(page.text)
            if level < float(page_dict['level']):
                # self.main_show.close()
                self.main_show = Process()
            self.main_show.show()

        except Exception as e:
            self.message_dialog("网络连接失败", f"请检查网络配置。{e}")
            sys.exit(0)

        # 创建窗口
        self.create_window()
        self.set_user_label()
        self.set_user_input()
        self.set_pwd_label()
        self.set_pwd_input()
        self.set_key_label()
        self.set_key_input()
        self.set_reg_button()
        # self.setWindowIcon(QIcon('logo.png'))

        # TODO 绑定信号槽
        self.reg_button.clicked.connect(self.to_reg)
        self.login_button.clicked.connect(self.login_app)

    def progress_bar(self):
        for i in range(1, 101):
            print("\r", end="")
            print("Download progress: {}%: ".format(i), "▋" * (i // 2), end="")
            sys.stdout.flush()
            time.sleep(0.01)

    # 窗口居中
    def center(self):
        """
        窗口居中
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(round((screen.width() - size.width()) / 2), round((screen.height() - size.height()) / 2))

    # 窗口布局
    def create_window(self):
        # 标题栏
        self.user_label = QLabel()
        self.user_input = QLineEdit()
        self.pwd_label = QLabel()
        self.pwd_input = QLineEdit()
        self.key_label = QLabel()
        self.key_input = QLineEdit()
        self.forget_label = QLabel("使用说明或忘记密码联系群主。")
        self.reg_button = QPushButton('没有账号，点这里注册...')
        self.login_button = QPushButton('登录')

        self.forget_label.setAlignment(Qt.AlignRight)

        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_label, 1)
        user_layout.addWidget(self.user_input, 3)

        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(self.pwd_label, 1)
        pwd_layout.addWidget(self.pwd_input, 3)

        key_layout = QHBoxLayout()
        key_layout.addWidget(self.key_label, 1)
        key_layout.addWidget(self.key_input, 3)

        # 创建界面
        layout = QVBoxLayout(self)
        layout.addLayout(user_layout)
        layout.addLayout(pwd_layout)
        layout.addWidget(self.forget_label)
        layout.addLayout(key_layout)
        layout.addWidget(self.reg_button)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    # TODO 登录用户
    def set_user_label(self):
        self.user_label.setText("用户名：")  # 创建一个QLabel并写入文字

    def set_user_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.user_input.setFont(font)
        self.user_input.setTextMargins(5, 2, 0, 2)
        self.user_input.setText("")

    # TODO 登录密码
    def set_pwd_label(self):
        self.pwd_label.setText("密码：")  # 创建一个QLabel并写入文字

    def set_pwd_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.pwd_input.setFont(font)
        self.pwd_input.setTextMargins(5, 2, 0, 2)
        self.pwd_input.setText("")

    # TODO 授权码
    def set_key_label(self):
        self.key_label.setText("软件密钥：")  # 创建一个QLabel并写入文字

    def set_key_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.key_input.setFont(font)
        self.key_input.setTextMargins(5, 2, 0, 2)
        self.key_input.setText("")

    # TODO 注册按钮
    def set_reg_button(self):
        self.reg_button.setObjectName("reg_in_login")
        self.reg_button.setCursor(QCursor(Qt.PointingHandCursor))

    def to_reg(self):
        self.main_show.close()
        self.main_show = AppReg()
        self.main_show.show()

    # TODO 登录验证
    def login_app(self):
        params = {
            "userName": self.user_input.text(),
            "userPwd": self.pwd_input.text(),
            "keyID": self.key_input.text()
        }
        page = requests.post("http://175.178.68.51:3000/login", params=params)
        page_dict = json.loads(page.text)
        global user_name
        if page_dict["status"] == 200:
            user_name = page_dict["userName"]
            self.message_dialog("登录成功", page_dict["content"])
            self.to_six()
        else:
            self.message_dialog(page_dict["content"], page_dict["content"])

    def to_six(self):
        self.main_show.close()
        self.main_show = Six()
        self.main_show.show()

    # 警告信息
    @staticmethod
    def message_dialog(title, text):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, text)
        msg_box.exec_()


class AppReg(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("login")
        # 窗口标题
        self.setWindowTitle('注册账号')

        # 窗口大小
        self.resize(350, 200)
        # 窗口居中
        self.center()
        # 图标
        self.user_label = None
        self.user_input = None
        self.pwd_label = None
        self.pwd_input = None
        self.reg_button = None
        self.login_button = None
        self.main_show = self
        self.init_ui()

    # 设置窗口主要部件和信号
    def init_ui(self):
        # 创建窗口
        self.create_window()
        self.set_user_label()
        self.set_user_input()
        self.set_pwd_label()
        self.set_pwd_input()
        # self.setWindowIcon(QIcon('logo.png'))
        # TODO 绑定信号槽
        self.reg_button.clicked.connect(self.reg_user)
        self.login_button.clicked.connect(self.to_login)

    # 窗口居中
    def center(self):
        """
        窗口居中
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(round((screen.width() - size.width()) / 2), round((screen.height() - size.height()) / 2))

    # 窗口布局
    def create_window(self):
        # 标题栏
        self.user_label = QLabel()
        self.user_input = QLineEdit()
        self.pwd_label = QLabel()
        self.pwd_input = QLineEdit()
        self.reg_button = QPushButton('注册')
        self.login_button = QPushButton('已注册，返回登陆')

        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_label, 1)
        user_layout.addWidget(self.user_input, 3)

        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(self.pwd_label, 1)
        pwd_layout.addWidget(self.pwd_input, 3)

        # 创建界面
        layout = QVBoxLayout(self)
        layout.addLayout(user_layout)
        layout.addLayout(pwd_layout)
        layout.addWidget(self.reg_button)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    # TODO 登录用户
    def set_user_label(self):
        self.user_label.setText("邮箱账号：")  # 创建一个QLabel并写入文字

    def set_user_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.user_input.setFont(font)
        self.user_input.setTextMargins(5, 2, 0, 2)

    # TODO 登录密码
    def set_pwd_label(self):
        self.pwd_label.setText("设置密码：")  # 创建一个QLabel并写入文字

    def set_pwd_input(self):
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Times New Roman")
        self.pwd_input.setFont(font)
        self.pwd_input.setTextMargins(5, 2, 0, 2)

    def reg_user(self):
        if len(self.user_input.text()) == 0:
            self.message_dialog('需要输入邮箱', "需要输入邮箱")
        elif len(self.user_input.text()) > 32:
            self.message_dialog('邮箱名过长', "邮箱名过长")
        elif len(self.pwd_input.text()) >= 6:
            params = {
                "userName": self.user_input.text(),
                "userPwd": self.pwd_input.text()
            }
            page = requests.post("http://175.178.68.51:3000/reg", params=params)
            page_dict = json.loads(page.text)
            if page_dict["status"] == 200:
                self.message_dialog("注册成功", page_dict["content"])
                self.to_login()
            else:
                self.message_dialog(page_dict["content"], page_dict["content"])
        else:
            self.message_dialog('密码位数过少', "密码必须大于6位")

    def to_login(self):
        self.main_show.close()
        self.main_show = Login()
        self.main_show.show()

    # 警告信息
    @staticmethod
    def message_dialog(title, text):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, text)
        msg_box.exec_()


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r', encoding="UTF-8") as file:
            return file.read()


if __name__ == '__main__':
    level = 1.2
    user_name = ""
    # 创建 QApplication 类的实例
    app = QApplication(sys.argv)
    # 创建窗体
    mainWindow = Login()
    # mainWindow = Six()
    # 样式
    # style_file = './main.qss'
    # style_sheet = QSSLoader.read_qss_file(style_file)
    # mainWindow.setStyleSheet(style_sheet)
    # # 关联login
    # ui = Ui_widget()
    # ui.setupUi(mainWindow)
    # 打开窗体
    # mainWindow.show()
    # 退出窗体
    sys.exit(app.exec_())
