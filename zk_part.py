import datetime

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




def next_birthday_plan(birthday_date, days_until_birthday):
    # 提示用户输入提前多少天做聚会计划
    ahead_days = int(input("请输入希望提前多少天做聚会计划："))
    #ahead_days = input("请输入希望提前多少天做聚会计划：")
    #isinstance(ahead_days,int)==False
    if(ahead_days<1 or ahead_days> days_until_birthday):
        #print("聚会计划日期请勿早于今天的日期，请重新选择")
        print("请合理选择提前天数")
        return next_birthday_plan(birthday_date,days_until_birthday)


    # 计算计划日期
    plan_date = birthday_date - datetime.timedelta(days=ahead_days)

    weekday=day_of_week(plan_date.year, plan_date.month, plan_date.day)
    if weekday=="Monday":
        plan_date = plan_date - datetime.timedelta(days=2)
    elif weekday=="Tuesday":
        plan_date = plan_date - datetime.timedelta(days=3)
    elif weekday=="Wednesday":
        plan_date = plan_date + datetime.timedelta(days=3)
    elif weekday=="Thursday":
        plan_date = plan_date + datetime.timedelta(days=2)
    elif weekday=="Friday":
        plan_date = plan_date + datetime.timedelta(days=1)
    else:
        plan_date = plan_date + datetime.timedelta(days=0)

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

    today_date=birthday_date - datetime.timedelta(days=days_until_birthday)
    if(plan_date < today_date):
        plan_date=plan_date+datetime.timedelta(days=7)

    # 输出结果给用户确认
    print("下次生日日期：", birthday_date)
    print("下次生日距离今天的天数：", days_until_birthday)
    print("今天的日期：",today_date)
    print("聚会计划日期：", plan_date)


    # 用户确认后返回计划日期
    confirm = input("是否确认以上日期为聚会计划日期？(是/否)：")
    if confirm.lower() == "是":
        return plan_date
    else:
        return None



# # 示例用法
# year = int(input("请输入年份："))
# month = int(input("请输入月份："))
# day = int(input("请输入日期："))
#
# result = day_of_week(year, month, day)
# print(f"{year}年{month}月{day}日是{result}.")

# 示例用法
next_birthday_date = datetime.date(2024, 3, 6)  # 下次生日日期
days_until_next_birthday = 8  # 下次生日距离今天的天数
plan_date = next_birthday_plan(next_birthday_date, days_until_next_birthday)
if plan_date:
    print("聚会计划日期已确认：", plan_date)
else:
    print("用户取消了聚会计划。")
