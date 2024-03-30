from datetime import datetime
import calendar

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def get_week_days(day:int, month:int, year:int) -> list[tuple[int,int,int]]:
    dayWeek = datetime(year, month, day).isoweekday()
    MonthDays = calendar.monthrange(year=year, month=month)[1]
    if month == 1: 
        PreviousMonth = 12
        PreviousMonthYear = year - 1
        NextMonthYear = year
    else: 
        PreviousMonth = month - 1
        PreviousMonthYear = year
        if month == 12: 
            nextMonth = 1
            nextMonthYear = year+1
        else: 
            nextMonth = month + 1
            nextMonthYear = year


    PreviousMonthDays = calendar.monthrange(year=year-1, month=PreviousMonth)[1]

    days = []
    forwardMonth = False

    for i in range(7):
        temp = day+i-dayWeek+1
        if temp >= 0:
            days.append( (temp % (MonthDays+1), month, year))
            if forwardMonth or (days[i][0] == 0 and day > 7):
                days[i] = (days[i][0] % MonthDays + 1, nextMonth, nextMonthYear)
                forwardMonth = True
            elif days[i][0] == 0:
                days[i] = (PreviousMonthDays, PreviousMonth, PreviousMonthYear)
        else:
            days.append((PreviousMonthDays - abs(temp), PreviousMonth, PreviousMonthYear))

    return days