from datetime import datetime
import calendar

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def get_week_days(day:int, month:int, year:int) -> list[int]:
    dayWeek = datetime(year, month, day).isoweekday()
    MonthDays = calendar.monthrange(year=year, month=month)[1]
    if month == 1:
        PreviousMonthDays = calendar.monthrange(year=12, month=12)[1]
    else: PreviousMonthDays = calendar.monthrange(year=year-1, month=month-1)[1]

    days = []
    nextMonth = False

    for i in range(7):
        temp = day+i-dayWeek+1
        if temp >= 0:
            days.append( temp % (MonthDays+1))
            if nextMonth or (days[i] == 0 and day > 7):
                days[i] = days[i] % MonthDays + 1
                nextMonth = True
            elif days[i] == 0:
                days[i] = PreviousMonthDays
        else:
            days.append(PreviousMonthDays - abs(temp))

    return days