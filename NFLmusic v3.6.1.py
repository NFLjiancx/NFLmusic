from tkinter import *
import time
import threading
import requests
import os
from arcade import load_sound, play_sound, stop_sound
from ttkbootstrap import *
import tkinter.messagebox
import sys
import json


def make_jsondata():
    if not os.path.exists("./NFLmusic.json"):
        with open("NFLmusic.json", "w") as f:
            jsondata = {
                "theme": "darkly",
                "repo": {
                    "QQ": ["https://api.xingzhige.com/API/QQmusicVIP",
                           {
                               "标准音质": 9,
                               "有损音质": 4
                           }
                           ],
                    "KUWO": ["https://api.xingzhige.com/API/Kuwo_BD_new",
                             {
                                 "SQ音质": 3,
                                 "HQ音质": 2,
                                 "标准音质": 1
                             }
                             ],
                    "KUGOU": ["https://api.xingzhige.com/API/Kugou_GN_new",
                              {
                                  "SQ音质": 3,
                                  "HQ音质": 2,
                                  "标准音质": 1
                              }
                              ],
                    "WANGYIYUN": ["https://api.xingzhige.com/API/NetEase_CloudMusic_new",
                                  {
                                      "标准": 1,
                                      "较高": 2,
                                      "极高": 3,
                                      "无损": 4,
                                      "Hi-Res": 5,
                                      "高清环绕声": 6,
                                      "沉浸环绕声": 7,
                                      "超清母带": 8
                                  }
                                  ]
                },
                "choice": "KUGOU"
            }
            f.write(json.dumps(jsondata))


version = "3.6.1"
make_jsondata()
with open('NFLmusic.json', 'r') as file:
    jsondata = json.loads(file.read())
    theme = jsondata["theme"]
    choice = jsondata["choice"]
    url = jsondata["repo"][choice][0]
    br_dict = jsondata["repo"][choice][1]
    br_list = [br for br in br_dict]

style = Style(theme=theme)
root = style.master
root.resizable(0, 0)
root.geometry("810x520")
root.title(f"NFLmusic v{version}")
var = StringVar()
var0 = StringVar()
var0.set("输入你想搜的...(￣▽￣)／")
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()
OptionMenu = ttk.OptionMenu
Button = ttk.Button
Scrollbar = ttk.Scrollbar
Progressbar = ttk.Progressbar
showed = False


def change_theme(tm):
    style.theme = tm
    tkinter.messagebox.showinfo(message='更改主题后需要重新启动程序！', title='提示')
    with open("NFLmusic.json", "r") as f:
        jsondata = json.loads(f.read())
        jsondata["theme"] = tm
    with open("NFLmusic.json", "w") as f:
        f.write(jsondata)
    restart0()


def display(window, text, x, y, ltime=3):
    a = Label(window, text=text)
    a.place(x=x, y=y)
    time.sleep(ltime)
    a.destroy()


def download_music(songname, br, choose):
    button['state'] = 'disabled'
    try:
        progressbar = Progressbar(mode='determinate', length=230)
        progressbar.place(x=290, y=460)
        resp = requests.get(f"{url}/?name={songname}&n={choose}&br={br}&max=60")
        resp.close()
        music_name = resp.json()["data"]["songname"]
        singer = resp.json()["data"]["name"]
        music_url = resp.json()["data"]["src"]
        level = resp.json()["data"]["quality"]
        response = requests.get(music_url, stream=True)
        formated = music_url.split("?")[0].rsplit(".", 1)[1]
        if os.path.exists("./music"):
            pass
        else:
            os.makedirs("./music")
        filename = f"{music_name}_{singer}_{level}.{formated}"
        filename = filename.replace("\\", "#").replace("/", "#")
        filename = filename.replace(":", "#").replace("*", "#")
        filename = filename.replace("?", "#").replace("\"", "#")
        filename = filename.replace("<", "#").replace(">", "#").replace("|", "#")
        with open("music/" + filename, "wb") as f:
            total_length = int(response.headers.get('content-length'))
            downloaded = 0
            for data in response.iter_content(chunk_size=1024):
                downloaded += len(data)
                f.write(data)
                progress = int((downloaded / total_length) * 100)
                progressbar['value'] = progress
        button['state'] = 'normal'
        refresh()
        progressbar.destroy()
        response.close()
        display(lableFrame2, f"{music_name} - {singer} 下载成功~", x=10, y=420)
    except KeyError:
        button['state'] = 'normal'
        progressbar.destroy()
        response.close()
        display(lableFrame2, "抱歉没有找到该歌曲哦 (*_*)!!! 换一首吧", x=10, y=420)
    except PermissionError:
        button['state'] = 'normal'
        progressbar.destroy()
        response.close()
        display(lableFrame2, "正在播放该音频哦~不能重复下载罒ω罒", x=10, y=420)
    except Exception as e:
        print(type(e), e)
        button['state'] = 'normal'
        progressbar.destroy()
        response.close()
        display(lableFrame2, "连接服务器失败 (>_<)!!! 请检查网络或稍后再试吧", x=10, y=420)


def run(task, *args):
    t = threading.Thread(target=task, args=args, daemon=True)
    t.start()


def playsound(music):
    global player
    try:
        stopsound()
    except:
        pass
    sound = load_sound(music)
    player = play_sound(sound)


def stopsound():
    stopsoundButton['state'] = 'disabled'
    stop_sound(player)


def refresh():
    global music_dir
    listbox1.delete(0, "end")
    music_dir = os.listdir("./music")
    for musics in music_dir:
        listbox1.insert("end", musics)


def get_data_non_blocking(song_name):
    def search_and_update_list():
        try:
            button0["state"] = "disabled"
            songlist.delete(0, "end")
            url1 = f"{url}/?name={song_name}&max=60"
            resp = requests.get(url1)
            jsondata = resp.json()["data"]
            resp.close()
            for index in range(len(jsondata)):
                full_name = jsondata[index]["songname"] + " - " + jsondata[index]["name"]
                songlist.insert("end", full_name)
        except:
            tkinter.messagebox.showinfo(title='搜索失败', message='没有搜索到你想要的结果~(╯°Д°)╯︵┻━┻')
        finally:
            button0["state"] = "normal"

    search_thread = threading.Thread(target=search_and_update_list)
    search_thread.start()


def playsoundButtonSet():
    playsoundButton['state'] = 'disabled'
    time.sleep(1.5)
    playsoundButton['state'] = 'normal'


def playsounds():
    global music_dir
    run(playsoundButtonSet)
    try:
        playsound(f"./music/{music_dir[listbox1.curselection()[0]]}")
    except IndexError:
        tkinter.messagebox.showwarning(title='播放失败(▼ヘ▼#)', message='请先选择你要听的歌吧(•́へ•́╬)')
    except:
        tkinter.messagebox.showerror(title='播放失败(▼ヘ▼#)', message='源文件不存在或已损坏！ヽ(#`Д´)ﾉ')
        refresh()
    stopsoundButton["state"] = "normal"


def restart0():
    root.destroy()
    python = sys.executable
    os.execl(python, python, *sys.argv)


def update_log():
    def reset():
        global showed
        showed = False
        updateLogButton['text'] = '查看'
        updateWindow.destroy()

    global showed, updateWindow
    if not showed:
        showed = True
        updateWindow = Toplevel()
        updateWindow.protocol('WM_DELETE_WINDOW', reset)
        updateWindow.title("更新日志")
        updateWindow.geometry('300x400')
        updateWindow.resizable(False, False)
        text = '''NFLmusic更新日志
        v1.2.7
        第一个正式版出现
        v1.5.7
        歌曲可选择索引
        v1.9.2
        更新了UI组件
        v2.0.0
        新增播放与停止功能
        v2.2.3
        音质可自由选择
        下载格式优化
        v2.4.1
        大幅度更改函数并添加了大量组件
        v3.0.0
        大幅度更新了UI组件
        v3.1.0
        修复了大部分已知bug
        优化搜索函数
        增加了更新日志
        v3.1.5
        修复未联网时二次弹窗问题
        修复参数错误导致下载失败的问题
        v3.5.1
        更新下载进度条
        修复搜索函数阻塞问题
        v3.5.2
        更换下载源
        修复已知问题
        v3.6.0
        修复音质参数错误问题
        v3.6.1
        整合下载源
        优化数据格式'''
        data = Text(updateWindow, width=38, height=20)
        data.place(x=10, y=20)
        data.insert('end', text)
        data["state"] = "disabled"
        updateLogButton['text'] = '关闭'
        updateWindow.mainloop()
    else:
        showed = False
        updateLogButton['text'] = '查看'
        updateWindow.destroy()


def settings():
    with open("NFLmusic.json", "r") as f:
        jsondata = json.loads(f.read())

    def save_settings():
        response = tkinter.messagebox.askquestion("保存设置", "是否保存设置？")
        if response == 'yes':
            jsondata["choice"] = repo_dict[var4.get()]
            with open("NFLmusic.json", "w") as f:
                f.write(json.dumps(jsondata))
            settingsWindow.destroy()
            tkinter.messagebox.showinfo(message='更改设置后需要重新启动程序！', title='提示')
            restart0()
        else:
            pass

    settingsWindow = Toplevel()
    settingsWindow.protocol('WM_DELETE_WINDOW', save_settings)
    settingsWindow.title("更多设置")
    settingsWindow.geometry('300x400')
    settingsWindow.geometry('+500+400')
    settingsWindow.attributes('-topmost', True)
    settingsWindow.resizable(False, False)

    repo_dict = {
        "QQ音乐": "QQ",
        "酷我音乐": "KUWO",
        "酷狗音乐": "KUGOU",
        "网易云音乐": "WANGYIYUN"
    }
    repo_dict_reverse = {
        "QQ": "QQ音乐",
        "KUWO": "酷我音乐",
        "KUGOU": "酷狗音乐",
        "WANGYIYUN": "网易云音乐"
    }
    repo_list = [repo for repo in repo_dict]

    label0 = Label(settingsWindow, text="下载源:")
    label0.place(x=10, y=20)

    menu0 = OptionMenu(settingsWindow, var4, repo_dict_reverse[jsondata["choice"]],
                       repo_list[0], repo_list[1], repo_list[2], repo_list[3])
    menu0.place(x=140, y=20)

    button0 = Button(settingsWindow, text="完成", width=20, command=save_settings)
    button0.place(x=40, y=80)

    settingsWindow.mainloop()


if os.path.exists("./music"):
    pass
else:
    os.makedirs("./music")

lableFrame0 = ttk.Labelframe(root, text='播放设置', width=250, height=70)
lableFrame0.place(x=20, y=430)

playsoundButton = Button(lableFrame0, text="▶", command=playsounds)
playsoundButton.place(x=20, y=7)

stopsoundButton = Button(lableFrame0, text="■", command=stopsound, state='disabled')
stopsoundButton.place(x=100, y=7)

Button(lableFrame0, text="↻", command=refresh).place(x=180, y=7)

lableFrame1 = ttk.Labelframe(root, text='歌曲列表', width=250, height=404)
lableFrame1.place(x=20, y=20)
listbox1 = Listbox(lableFrame1, width=29, height=19, listvariable=var3)
listbox1.place(x=20, y=15)
music_dir = os.listdir("./music")
for files in music_dir:
    listbox1.insert("end", files)

lableFrame2 = ttk.Labelframe(root, text='下载音乐', height=480, width=250)
lableFrame2.place(x=280, y=20)

songlist = Listbox(lableFrame2, width=32, height=15)
songlist.place(x=10, y=135)

button0 = Button(lableFrame2, text="搜索",
                 command=lambda: get_data_non_blocking(var0.get()))
button0.place(x=70, y=90)

button = Button(lableFrame2, text="下载",
                command=lambda: run(download_music, var0.get(), br_dict[var.get()], songlist.curselection()[0] + 1))
button.place(x=150, y=90)

Label(lableFrame2, text="歌名:").place(x=10, y=10)
entry = Entry(lableFrame2, textvariable=var0)
entry.place(x=70, y=10)

Label(lableFrame2, text="音质:").place(x=10, y=50)

if choice == "QQ":
    menu0 = OptionMenu(lableFrame2, var, br_list[0], br_list[0], br_list[1])
elif choice == "WANGYIYUN":
    menu0 = OptionMenu(lableFrame2, var, br_list[1], br_list[0], br_list[1], br_list[2], br_list[3], br_list[4],
                       br_list[5], br_list[6], br_list[7])
else:
    menu0 = OptionMenu(lableFrame2, var, br_list[1], br_list[0], br_list[1], br_list[2])

menu0.place(x=70, y=50)

lableFrame3 = ttk.Labelframe(root, text='设置', width=250, height=140)
lableFrame3.place(x=540, y=20)

themeLable = Label(lableFrame3, text='主题:')
themeLable.place(x=10, y=10)

updateLogLable = Label(lableFrame3, text='日志:')
updateLogLable.place(x=10, y=70)

updateLogButton = Button(lableFrame3, text='查看', width=5,
                         command=lambda: run(update_log()))
updateLogButton.place(x=70, y=70)

settingsButton = Button(lableFrame3, text="更多设置", width=8,
                        command=lambda: run(settings()))
settingsButton.place(x=158, y=70)

menu1 = OptionMenu(lableFrame3, var1, theme, 'alt', 'yeti', 'superhero', 'darkly',
                   'xpnative', 'vista', 'cyborg', 'default', 'litera', 'solar',
                   'journal', 'lumen', 'flatly', 'united', 'clam', 'pulse',
                   'morph', 'winnative', 'cosmo', 'minty', 'sandstone', 'classic', )
menu1.place(x=70, y=10)

themeButton = Button(lableFrame3, text='确定', command=lambda: change_theme(var1.get()))
themeButton.place(x=190, y=10)

lableFrame4 = ttk.LabelFrame(root, text='关于', height=330, width=250)
lableFrame4.place(x=540, y=170)

try:
    resp = requests.get("https://oiapi.net/API/AWord")
    text = resp.text
    resp.close()
except:
    tkinter.messagebox.showinfo(title='联网失败(╥╯^╰╥)',
                                message='服务器连接失败╮(╯﹏╰）╭\n请检查网络设置或稍后再试吧~')
    text = ""

lable0 = Label(lableFrame4, text="应用版本:" + version + "\n函数编写:白松霖\n"
                                 "GUI设计:白松霖\n源码维护:白松霖\n"
                                 "版权声明:歌曲来源QQ音乐\n\n--致敬我们伟大的电教委员--\n\n"
                                 + text[:12] + "\n" + text[12:24] + "\n" + text[24:]
                                 + '\n\n' + '请勿将从NFLmusic中下载的\n音频文件用于商业或盈利\n'
                                            '本应用未经允许请勿发布或传播')
lable0.place(x=35, y=10)

root.mainloop()
