#! usr/bin/python
# coding=utf-8

import os

class QtTool:

    def exeCmd(self, cmd):
        '''根据终端命令获取内容'''
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text

    def ui2py(self):
        '''ui文件转py文件，这里需要系统安装pyuic5'''
        #获取当前目录下的ui文件
        UI_FileList = self.exeCmd('ls | grep .ui').split('\n')
        path = os.getcwd()
        for ui in UI_FileList:
            if len(ui)>0:
                cmd = 'pyuic5 -o %s/%s %s/%s' % (path,ui.split('.')[0]+'.py',path,ui)
                # print(cmd)
                try:
                    os.system(cmd)
                    print('%s   转换为  %s  成功'%(ui,ui.split('.')[0]+'.py'))
                except Exception as e:
                    print(e)

tool = QtTool()
tool.ui2py()
# #ui文件转py文件，这里要安装pyuic5
# path_ui = '/home/xiong/PycharmProjects/nt_test/Dialog_Task.ui'
# paty_py = '/home/xiong/PycharmProjects/nt_test/Dialog_Task.py'
# os.system('pyuic5 -o %s %s'%(paty_py,path_ui))

#添加一个模块

#第二次