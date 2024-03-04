import tkinter as tk
from tkinter import messagebox
import os
import sys
import calendar
from datetime import datetime,timedelta
import time

#ZK
#不过，蔡勒公式只适合于1582年（中国明朝万历十年）10月15日之后的情形。
def day_of_week(year, month, day):
    # 判断月份是否为1月或2月，如果是，则将年份和月份分别减1
    if month < 3:
        month += 12
        year -= 1

    # 计算世纪数和年份在世纪中的年数
    century = year // 100
    year_of_century = year % 100

    # 根据蔡勒（Zeller）公式计算星期几
    day_of_week = (day + (
                13 * (month + 1)) // 5 + year_of_century + year_of_century // 4 + century // 4 - 2 * century) % 7

    # 将结果转换为星期几的字符串表示
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    return days[day_of_week]

def find_next_birthday(today,birthday=None):
    if birthday is None:
        return "2024-05-08"
    month, day = (int(i) for i in birthday.split("-")[1:])
    
    next_year = today.year  # 默认下一次生日的年份为今年
    for year in range(today.year , 9999):  # 遍历从明年开始直到最大值的所有年份
        try:
            date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            
            if date > today:  # 如果找到了比今天更近的生日日期
                next_year = year
                break
                
        except ValueError:
            pass  # 若该年不存在指定的生日日期则会引发ValueError错误，此时pass表示无视该错误

    next_birthday = datetime.strptime(f"{next_year}-{month}-{day}", "%Y-%m-%d")
    return f"{next_year}-{month}-{day}"

#ZK
def next_birthday_plan(birthday_date, days_until_birthday, ahead_days):
    # 提示用户输入提前多少天做聚会计划
    # ahead_days = int(input("请输入希望提前多少天做聚会计划："))
    # ahead_days = input("请输入希望提前多少天做聚会计划：")
    # isinstance(ahead_days,int)==False
    # if(ahead_days<1 or ahead_days> days_until_birthday):
    #     #print("聚会计划日期请勿早于今天的日期，请重新选择")
    #     print("请合理选择提前天数")
    #     return next_birthday_plan(birthday_date,days_until_birthday)


    # 计算计划日期
    plan_date = birthday_date - timedelta(days=ahead_days)
    prompt = ""
    weekday=day_of_week(plan_date.year, plan_date.month, plan_date.day)
    labor_National=False
    # 如果计划日期是五一假期和国庆假期
    if plan_date.month == 5 and plan_date.day >= 1 and plan_date.day <= 3:
        # plan_date = plan_date - timedelta(days=7)
        # prompt = "It's a holiday, I schedule to the latest Saturday: " + str(plan_date.year) + '-' + str(
        #     plan_date.month) + '-' + str(plan_date.day)
        labor_National = True
    if plan_date.month == 10 and plan_date.day >= 1 and plan_date.day <= 7:
        # plan_date = plan_date - timedelta(days=7)
        # prompt = "It's a holiday, I schedule to the latest Saturday: " + str(plan_date.year) + '-' + str(
        #     plan_date.month) + '-' + str(plan_date.day)
        labor_National = True
    if(labor_National==False):
        if weekday == "Monday":
            plan_date = plan_date - timedelta(days=2)
            prompt = "It's a working day, I schedule to the latest Saturday: " + str(plan_date.year) + '-' + str(
                plan_date.month) + '-' + str(plan_date.day)
        elif weekday == "Tuesday":
            plan_date = plan_date - timedelta(days=3)
            prompt = "It's a working day, I schedule to the latest Saturday: " + str(plan_date.year) + '-' + str(
                plan_date.month) + '-' + str(plan_date.day)
        elif weekday == "Wednesday":
            plan_date = plan_date + timedelta(days=3)
            prompt = "It's a working day, I schedule to the latest Saturday: " + str(plan_date.year) + '-' + str(
                plan_date.month) + '-' + str(plan_date.day)
        elif weekday == "Thursday":
            plan_date = plan_date + timedelta(days=2)
            prompt = "It's a working day, I schedule to the latest Saturday: " + str(plan_date.year) + '-' + str(
                plan_date.month) + '-' + str(plan_date.day)
        elif weekday == "Friday":
            plan_date = plan_date + timedelta(days=1)
        else:
            plan_date = plan_date + timedelta(days=0)

    # # 如果计划日期是工作日，则改为最近的一个周六
    # "Return day of the week, where Monday == 0 ... Sunday == 6."
    # if plan_date.weekday()==0:
    #     plan_date = plan_date - datetime.timedelta(days=2)
    # elif plan_date.weekday()==1:
    #     plan_date = plan_date - datetime.timedelta(days=3)
    # elif plan_date.weekday()==2:
    #     plan_date = plan_date + datetime.timedelta(days=3)
    # elif plan_date.weekday()==3:
    #     plan_date = plan_date + datetime.timedelta(days=2)
    # elif plan_date.weekday()==4:
    #     plan_date = plan_date + datetime.timedelta(days=1)
    # else:
    #     plan_date = plan_date + datetime.timedelta(days=0)

    today_date=birthday_date - timedelta(days=days_until_birthday)
    # if(plan_date < today_date):
    #     plan_date=plan_date+timedelta(days=7)
    while(plan_date < today_date):
        plan_date=plan_date+timedelta(days=7)
    # # 输出结果给用户确认
    # print("下次生日日期：", birthday_date)
    # print("下次生日距离今天的天数：", days_until_birthday)
    # print("今天的日期：",today_date)
    # print("聚会计划日期：", plan_date)


    # # 用户确认后返回计划日期
    # confirm = input("是否确认以上日期为聚会计划日期？(是/否)：")
    # if confirm.lower() == "是":
    #     return plan_date
    # else:
    #     return None

    return plan_date, prompt

#Please write your own path!!
birthdaytxt_path='F:\PycharmProjects\BirthdayPlanner\\birthday.txt'

#ZYL
class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Birthday Plan')
        self.window.geometry('800x600')
        self.f=open(birthdaytxt_path,'w') if not os.path.exists(birthdaytxt_path) else open(birthdaytxt_path,'a')
        self.namelist = [i.split(' ')[0] for i in open(birthdaytxt_path).read().split('\n') if i != '']
        self.list = tk.StringVar()
        self.list.set(self.namelist)
        self.listbox = tk.Listbox(self.window, listvariable=self.list, font=('Arial', 20))
        self.listbox.grid(row=0, column=0,rowspan=3)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.info = tk.Text(self.window,bg='silver')
        self.info.grid(row=0, column=1, rowspan=3,columnspan=3)
        self.info.insert(tk.END, "Welcome to Birthday Plan\nPress any key to start")
        #按任意键开始的操作
        self.window.bind('<Key>', self.next)
        self.window.mainloop()
    
    def on_select(self, event):
        value = self.listbox.get(self.listbox.curselection()[0])
        with open(birthdaytxt_path, 'r') as f:
            for i in f.readlines():
                if value in i.split(' '):
                    self.info.insert(tk.END, '\n'+ i.split(' ')[0] + ' is ' + i.split(' ')[1] + ', the birthday is ' + i.split(' ')[2] )
                    self.birthdate = i.split(' ')[2].split('\n')[0]
                    self.cand_name = i.split(' ')[0]
                    self.cand_rel = i.split(' ')[1] 
                    break
    
    def register(self, event=None):
        try:
            self.button.destroy()
            self.regbut.destroy()
        except:
            pass
        self.window.unbind('<Key>')
        self.info.delete(1.0, tk.END)
        self.info.insert(tk.END, "Please enter the name & relationship of the person whose birthday you want to plan")
        self.name = tk.Entry(self.window, font=('Arial', 25))
        self.relationship = tk.Entry(self.window, font=('Arial', 25))
        self.birth = tk.Entry(self.window, font=('Arial', 25)) 
        self.blabel = tk.Label(self.window, text='birthday', font=('Arial', 25))
        self.nlabel = tk.Label(self.window, text='name', font=('Arial', 25))
        self.rlabel = tk.Label(self.window, text='relationship', font=('Arial', 25))
        self.nlabel.grid(row=3, column=0)
        self.rlabel.grid(row=4, column=0)
        self.blabel.grid(row=5,column=0)
        self.name.grid(row=3, column=1,columnspan=3)
        self.relationship.grid(row=4, column=1,columnspan=3)
        self.birth.grid(row=5, column=1,columnspan=3)
        self.button = tk.Button(self.window, text='submit', font=('Arial', 25), command=self.register_info)
        self.button.grid(row=6,column=2,columnspan=2)

    def register_info(self, event=None):
        #读写文件
        if os.path.exists(birthdaytxt_path):
            with open(birthdaytxt_path, 'a') as f:
                f.write(self.name.get() + ' ' + self.relationship.get() + ' '+ self.birth.get() + '\n')
        else:
            with open(birthdaytxt_path, 'w') as f:
                f.write(self.name.get() + ' ' + self.relationship + ' '+ self.birth.get() + '\n')
        self.next()

    def next(self, event=None):
        try:
            self.blabel.destroy()
            self.nlabel.destroy()
            self.rlabel.destroy()
            self.name.destroy()
            self.relationship.destroy()
            self.birth.destroy()
            self.button.destroy()
        except:
            pass
        self.window.unbind('<Key>')
        self.info.delete(1.0, tk.END)
        self.namelist = [i.split(' ')[0] for i in open(birthdaytxt_path).read().split('\n') if i != '']
        self.list.set(self.namelist)
        self.info.insert(tk.END, "Please select name and input today's date")
        self.tlabel = tk.Label(self.window, text='today', font=('Arial', 25))
        self.today = tk.Entry(self.window, font=('Arial', 25))
        self.tlabel.grid(row=3, column=0)
        self.today.grid(row=3, column=1,columnspan=3)
        self.button = tk.Button(self.window, text='submit', font=('Arial', 25), command=self.showdays)
        self.regbut = tk.Button(self.window, text='register_info', font=('Arial', 25), command=self.register)
        self.button.grid(row=4,column=2,columnspan=2)
        self.regbut.grid(row=4,column=0,columnspan=2)
    
    def showdays(self, event=None):
        # try:
        #     self.tlabel.destroy()
        #     self.today.destroy()
        # except:
        #      pass
        try:
            self.window.unbind('<Key>')
        except:
            pass
        try:
            self.todaynum = self.today.get().split('-')
            self.todaydate = self.today.get()
        except ValueError:
            messagebox.showinfo('Warning', 'Please enter the correct date format')
            self.todaynum = self.today.get().split('-')
            self.todaydate = self.today.get()
        try:
            self.birthnum = self.birthdate.split('-')
        except AttributeError:
            self.info.insert(tk.END, "\nPlease select name")
        self.nextbirth= find_next_birthday(datetime.strptime(self.todaydate, "%Y-%m-%d"), self.birthdate)
        self.info.insert(tk.END, "\nThe next birthday is: " + self.nextbirth + "\n")
        try:
            self.todaynum = [int(i) for i in self.todaynum]
            self.nextnum =  [int(i) for i in self.nextbirth.split('-') ]
        except ValueError:
            messagebox.showinfo('Warning', 'Please enter the correct date format')
            self.todaynum = [int(i) for i in self.todaynum]
            self.nextnum =  [int(i) for i in self.nextbirth.split('-') ]
            

        ####
        self.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d")
        self.todaydate = datetime.strptime(self.todaydate, "%Y-%m-%d")
        # if (self.birthdate.date()-self.todaydate.date()).days>0:
        #     self.datelabel.insert(tk.END, "You haven't been born yet\nPress any key to continue")
        #     self.window.bind('<Key>', self.showdays)
        # self.button.destroy()
        self.nextbirth = datetime.strptime(self.nextbirth, "%Y-%m-%d")
        if (self.nextbirth.date()-self.todaydate.date()).days<0:
            self.nextbirth = datetime.strptime(str(self.nextnum[0]+1)+'-'+str(self.nextnum[1])+'-'+str(self.nextnum[2]), "%Y-%m-%d")
        self.daytobirthday = (self.nextbirth.date()-self.todaydate.date()).days
        ####
        self.info.insert(tk.END, "\nThe  next birthday is: " + str(self.daytobirthday) + " days later\nPress any key to continue")
        # self.window.bind('<Key>', self.setdate)
        try:
            if (self.birthdate.date()-self.todaydate.date()).days>0:
                self.info.insert(tk.END, "You haven't been born yet\nPress any key to continue")
                self.window.bind('<Key>', self.showdays)
            else:
                self.info.insert(tk.END, "The date of your next birthday is: " + str(self.daytobirthday) + " days later\nPress any key to continue")
                self.window.bind('<Key>', self.setdate)
                self.button.destroy()
        except AttributeError:
            self.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d")
            if (self.birthdate.date()-self.todaydate.date()).days>0:
                self.info.insert(tk.END, "You haven't been born yet\nPress any key to continue")
                self.window.bind('<Key>', self.showdays)
            else:
                self.info.insert(tk.END, "The date of your next birthday is: " + str(self.daytobirthday) + " days later\nPress any key to continue")
                self.window.bind('<Key>', self.setdate)
                self.button.destroy()

    def setdate(self, event=None):
        self.window.unbind('<Key>')
        try:
            self.confirm.destroy()
            self.reject.destroy()
            self.days.destroy()
        except AttributeError:
            pass
        
        try:
            self.tlabel.destroy()
            self.today.destroy()
            self.regbut.destroy()
        except AttributeError:
            pass
        try:
            self.tlabel.destroy()
        except:
            pass
        self.info.delete(1.0, tk.END)
        self.info.insert(tk.END, "Please enter ? days you'd like to arrange party ahead of birthday\n")
        self.info.insert(tk.END, "The date of your next birthday is: " + str(self.daytobirthday) + " days later\n")
        self.days = tk.Entry(self.window, font=('Arial', 25)) 
        self.days.grid(row=3, column=1,columnspan=3)
        self.button = tk.Button(self.window, text='submit', font=('Arial', 25), command=self.checkdate)
        self.button.grid(row=4,column=2,columnspan=2)

    def checkdate(self):
        try:
            self.daysnum = int(self.days.get())
            #nextbirth下一次生日日期，daysnum提前天数
            self.plandate, prompt = next_birthday_plan(self.nextbirth, self.daytobirthday, self.daysnum)
            try:
                self.info.insert(tk.END,"Person: " + self.cand_name + "\nRelationship: " + self.cand_rel + "\nBirthday: " + self.birthdate.strftime("%Y-%m-%d") + "\nToday: " + self.todaydate.strftime("%Y-%m-%d") + "\nNext birthday: " + self.nextbirth.strftime("%Y-%m-%d") + "\nDays to next birthday: " + str(self.daytobirthday) + "\nPlan date: " + self.plandate.strftime("%Y-%m-%d") + "\n")
            except AttributeError:
                self.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d")
                self.info.insert(tk.END,"Person: " + self.cand_name + "\nRelationship: " + self.cand_rel + "\nBirthday: " + self.birthdate.strftime("%Y-%m-%d") + "\nToday: " + self.todaydate.strftime("%Y-%m-%d") + "\nNext birthday: " + self.nextbirth.strftime("%Y-%m-%d") + "\nDays to next birthday: " + str(self.daytobirthday) + "\nPlan date: " + self.plandate.strftime("%Y-%m-%d") + "\n")
            self.plannum = [int(self.plandate.year),int(self.plandate.month),int(self.plandate.day)]
            self.info.insert(tk.END, "\n"+prompt)

        except ValueError:
            messagebox.showinfo('Warning', 'Please enter the correct date format')
            self.daysnum = int(self.days.get())
            #nextbirth下一次生日日期，daysnum提前天数
            self.plandate, prompt = next_birthday_plan(self.nextbirth, self.daytobirthday, self.daysnum)
            try:
                self.info.insert(tk.END,"Person: " + self.cand_name + "\nRelationship: " + self.cand_rel + "\nBirthday: " + self.birthdate.strftime("%Y-%m-%d") + "\nToday: " + self.todaydate.strftime("%Y-%m-%d") + "\nNext birthday: " + self.nextbirth.strftime("%Y-%m-%d") + "\nDays to next birthday: " + str(self.daytobirthday) + "\nPlan date: " + self.plandate.strftime("%Y-%m-%d") + "\n")
            except AttributeError:
                self.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d")
                self.info.insert(tk.END,"Person: " + self.cand_name + "\nRelationship: " + self.cand_rel + "\nBirthday: " + self.birthdate.strftime("%Y-%m-%d") + "\nToday: " + self.todaydate.strftime("%Y-%m-%d") + "\nNext birthday: " + self.nextbirth.strftime("%Y-%m-%d") + "\nDays to next birthday: " + str(self.daytobirthday) + "\nPlan date: " + self.plandate.strftime("%Y-%m-%d") + "\n")
            self.plannum = [int(self.plandate.year),int(self.plandate.month),int(self.plandate.day)]
            self.info.insert(tk.END, "\n"+prompt)
        self.button.destroy()
        self.confirm = tk.Button(self.window, text='Confirm', font=('Arial', 25), command=self.result)
        self.confirm.grid(row=5,column=0,columnspan=2)
        self.reject = tk.Button(self.window, text='Redetermine', font=('Arial', 25), command=self.setdate)
        self.reject.grid(row=5,column=2,columnspan=2)
    

    def result(self):
        self.confirm.destroy()
        self.days.destroy()
        self.reject.destroy()
        self.info.delete(1.0,tk.END)
        with open(birthdaytxt_path, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if self.cand_name in lines[i]:
                    if len(lines[i].split(' ')) == 4:
                        lines[i] = lines[i].split(' ')[0] +' '+ lines[i].split(' ')[1] +' '+ lines[i].split(' ')[2] + ' ' + str(self.plandate.year) + '-' + str(self.plandate.month) + '-' + str(self.plandate.day) + '\n'
                        self.info.insert(tk.END,"Plan date has been updated\n")
                    else:
                        lines[i] = lines[i].split('\n')[0] + ' ' + str(self.plandate.year) + '-' + str(self.plandate.month) + '-' + str(self.plandate.day) + '\n'
        with open(birthdaytxt_path, 'w') as f:
            for line in lines:
                f.write(line)
        with open(birthdaytxt_path, 'r') as f:
            for i in f.readlines():
                self.cand_name = i.split(' ')[0]
                self.cand_rel = i.split(' ')[1]
                self.birthdate = i.split(' ')[2].split('\n')[0]
                try:
                    self.plandate = i.split(' ')[3].split('\n')[0]
                    self.info.insert(tk.END,"Person: " + self.cand_name + "\nRelationship: " + self.cand_rel + "\nBirthday: " + self.birthdate  + "\nPlan date: " + self.plandate + "\n"+"\n")
                except IndexError:
                    self.info.insert(tk.END,"Person: " + self.cand_name + "\nRelationship: " + self.cand_rel + "\nBirthday: " + self.birthdate  + "\n"+"\n")
        self.info.insert(tk.END,"\nPress any key to exit")
        self.window.bind('<Key>', self.end)
    
    def end(self, event=None):
        self.window.destroy()
        sys.exit(0)

if __name__ == "__main__":
    GUI()