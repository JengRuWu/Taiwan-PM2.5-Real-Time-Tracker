def rbＣity():
    global site_list, list_radio
    site_list.clear()
    for r in list_radio:
        r.destroy()
    n=0
    for c1 in data["County"]:
        if c1 == city.get():
            site_list.append(data.iloc[n, 0])
        n+=1
    site_make()
    rb_site()


def site_make():
    global site_list, list_radio
    for sitename in site_list:
        rbtem = tk.Radiobutton(frame02, text=sitename, variable=site, value=sitename, command=rb_site)
        list_radio.append(rbtem)
        if sitename == site_list[0]:
            rbtem.select()
        rbtem.pack(side="left")


def click_fresh():
    global data
    data = pd.read_csv("http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=csv")
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    update_time.set("更新時間：" + dt_string)
    rb_site()

def rb_site():
    n=0
    for s in data.iloc[:,0]:
        if s == site.get():
            pm = data.iloc[n, 11]
            if not pm.isnumeric():
                result1.set("目前無" + s + "站的PM2.5資料")
            else:
                pm = int(pm)
                if pm <= 35:
                    grade1 = "低"
                elif pm <= 53:
                    grade1 = "中"
                elif pm <= 70:
                    grade1 = "高"
                else:
                    grade1 = "非常高"
                result1.set(s + "站的PM2.5值為「" + str(pm) + "」：「" + grade1 + "」等級")
            break
        n+=1

import tkinter as tk
from datetime import datetime
import pandas as pd

data = pd.read_csv("http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=csv")

win = tk.Tk()
win.geometry("640x270")
win.title("PM2.5 即時監測")

city = tk.StringVar()
site = tk.StringVar()
result1 = tk.StringVar()
update_time = tk.StringVar()
city_list = []
site_list = []
list_radio = []

for c1 in data["County"]:
    if c1 not in city_list:
        city_list.append(c1)

count = 0
for c1 in data["County"]:
    if c1 == city_list[0]:
        site_list.append(data.iloc[count, 0])
    count += 1

label1 = tk.Label(win, text="縣市：", pady=6, fg="blue", font=("新細明體",12))
label1.pack()
frame01 = tk.Frame(win)
frame01.pack()

for i in range(0,3):
    for j in range(0,8):
        n = i*8 + j
        if n<len(city_list):
            city01 = city_list[n]
            rbtem = tk.Radiobutton(frame01, text=city01, variable=city, value=city01, command=rbCity)
            rbtem.grid(row=i, column=j)
            if n == 0:
               rbtem.select()

label2 = tk.Label(win, text="測站：", pady=6, fg="blue", font =("新細明體", 12))
label2.pack()
frame02 = tk.Frame(win)
frame02.pack()

site_make()

btn_down = tk.Button(win, text="更新資料", font=("新細明體", 12), command=click_fresh)
btn_down.pack(pady=6)

time_label = tk.Label(win, textvariable=update_time, font=("新細明體", 10))
time_label.pack(pady=1)

now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
update_time.set("更新時間：" + dt_string)

result_label = tk.Label(win, textvariable=result1, fg="red", font=("新細明體", 16))
result_label.pack(pady=6)
rb_site()

win.mainloop()


