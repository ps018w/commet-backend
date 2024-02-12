
from datetime import date, timedelta, datetime
from accounts.models import CustomUser, Calendar, BookingSlot, Timeslot, DayOfWeek, CalendarSlot
import pandas as pd

def create_slot(request):
    data= request.data
    freq = data["frequency"]
    start_time = data['start_time']
    start = datetime.strptime(start_time, '%H:%M')
    end = start + timedelta(hours=3)
    end_time = end.strftime('%H:%M')
    slot=None
    if freq == "M":
        dtrange =30
    elif freq == 'H':
        dtrange= 180
    elif freq == 'C':
        start_date = request.data['start_date'] #'2018-6-15'
        end_date = request.data['start_date'] #'2019-3-20'
        dtrange = len(pd.date_range(start=start_date, end=end_date, freq='d'))
    calendar_slot=[]
    for i in range(dtrange):
        current_date = date.today() + timedelta(days=i)
        day = current_date.strftime('%a').upper()
        obj_day = DayOfWeek.objects.get(name=day)
        if obj_day.id in data["days_of_week"]:
            slot =CalendarSlot.objects.create(
                start_time=start_time,
                end_time=end_time,
                schedule_date=current_date,
                weekday=obj_day
            )
            calendar_slot.append(slot.id)
    return calendar_slot


def booked_teaching_slot(user_data,request =None):
    email= user_data['email']
    tutor = CustomUser.objects.get()
    print(tutor)
    student = CustomUser.objects.get(email=email)
    slot = Timeslot.objects.create(start_time=user_data['start_time'] , end_time=user_data['end_time'])
    if Calendar.objetcs.filter(user=2,start_time=user_data['start_time']):
        scheduled_calender = Calendar.objects.get(user=2)
    else:
        print("Teacher schedule not available")
    booked_slot = BookingSlot.objects.create(
        tutor=tutor,
        student=student,
        time_slot =slot,
        scheduled_calender=scheduled_calender,
        approved =True,


    )
    pass

