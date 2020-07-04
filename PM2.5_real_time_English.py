def rbCity():
    global site_list, list_radio
    site_list.clear()
    for r in list_radio:
        r.destroy()
    n=0
    for c1 in data["County"]:
        if c1 == city.get():
            site_list.append(pinyin.get(data.iloc[n, 0], format="strip").title())
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
    english_name()
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    update_time.set("Last update：" + dt_string)
    rb_site()

def rb_site():
    n=0
    for s in data.iloc[:,0]:
        if pinyin.get(s, format="strip").title() == site.get():
            pm = str(data.iloc[n, 11])
            try:
                pm = float(pm)
                test = True
            except:
                test = False
            if test == False:
                result1.set( "There is no data in " + pinyin.get(s, format="strip").title() + " for now." )
            else:
                if pm <= 35:
                    grade1 = "low"
                elif pm <= 53:
                    grade1 = "medium"
                elif pm <= 70:
                    grade1 = "high"
                else:
                    grade1 = "very high"
                result1.set("The PM2.5 index in " + pinyin.get(s, format="strip").title() + " is currently " + str(pm) + " (" + grade1 + ").")
            break
        n+=1

def english_name():
    global data
    data.loc[data['County'] == "臺北市", 'County'] = 'Taipei City'
    data.loc[data['County'] == "新北市", 'County'] = 'New Taipei City'
    data.loc[data['County'] == "桃園市", 'County'] = 'Taoyuan City'
    data.loc[data['County'] == "新竹縣", 'County'] = 'Hsinchu County'
    data.loc[data['County'] == "新竹市", 'County'] = 'Hsinchu City'
    data.loc[data['County'] == "苗栗縣", 'County'] = 'Miaoli County'
    data.loc[data['County'] == "臺中市", 'County'] = 'Taichung County'
    data.loc[data['County'] == "彰化縣", 'County'] = 'Changhua County'
    data.loc[data['County'] == "雲林縣", 'County'] = 'Yunlin County'
    data.loc[data['County'] == "嘉義縣", 'County'] = 'Chiayi County'
    data.loc[data['County'] == "嘉義市", 'County'] = 'Chiayi City'
    data.loc[data['County'] == "臺南市", 'County'] = 'Tainan City'
    data.loc[data['County'] == "高雄市", 'County'] = 'Kaohsiung City'
    data.loc[data['County'] == "屏東縣", 'County'] = 'Pingtung County'
    data.loc[data['County'] == "宜蘭縣", 'County'] = 'Yilan County'
    data.loc[data['County'] == "花蓮縣", 'County'] = 'Hualien County'
    data.loc[data['County'] == "臺東縣", 'County'] = 'Taitung County'
    data.loc[data['County'] == "澎湖縣", 'County'] = 'Penghu County'
    data.loc[data['County'] == "基隆市", 'County'] = 'Keelung County'
    data.loc[data['County'] == "金門縣", 'County'] = 'Kinmen County'
    data.loc[data['County'] == "連江縣", 'County'] = 'Lianjiang County'
    data.loc[data['County'] == "南投縣", 'County'] = 'Nantou County'

import tkinter as tk
from datetime import datetime
import pandas as pd
import pinyin

data = pd.read_csv("http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=csv")
english_name()

win = tk.Tk()
win.geometry("640x270")
win.title("PM2.5 Real-time Tracker of Taiwan")

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
        site_list.append(pinyin.get(data.iloc[count, 0],format="strip").title())
    count += 1

label1 = tk.Label(win, text="Region：", pady=6, fg="blue", font=("Arial",12))
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

label2 = tk.Label(win, text="Site：", pady=6, fg="blue", font =("Arial", 12))
label2.pack()
frame02 = tk.Frame(win)
frame02.pack()

site_make()

btn_down = tk.Button(win, text="Update Data", font=("Arial", 12), command=click_fresh)
btn_down.pack(pady=6)

time_label = tk.Label(win, textvariable=update_time, font=("Arial", 10))
time_label.pack(pady=1)

now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
update_time.set("Last update：" + dt_string)

result_label = tk.Label(win, textvariable=result1, fg="red", font=("Arial", 16))
result_label.pack(pady=6)
rb_site()

win.mainloop()


