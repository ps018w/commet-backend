
from datetime import date, timedelta, datetime
from accounts.models import CustomUser, Calendar, BookingSlot, Timeslot
import pandas as pd

def create_slot(request):
    freq = request.data["frequency"]
    days_of_week = request.data['days_of_week']
    start_time = request.data['start_time']
    user = CustomUser.objects.get(email=request.data['email'])
    start_date = request.data['start_date']
    end_date = request.data['end_date']


    slot=None
    if freq == "M":
        dtrange =30
    elif freq == 'H':
        dtrange= 180
    elif freq == 'C':
        start_date = start_date #'2018-6-15'6
        end_date = end_date #'2019-3-20'
        dtrange = len(pd.date_range(start=start_date, end=end_date, freq='d'))

    for i in range(dtrange):
        current_date = date.today() + timedelta(days=i)
        day_of_week = current_date.strftime('%a').upper()

        if day_of_week in days_of_week:
            schedule_date = current_date

            slot =Calendar.objects.create(
                user=user,
                frequency=freq,
                days_of_week=day_of_week,
                start_time=start_time,  # Adjust the start time as needed
                schedule_date = schedule_date   # Adjust the end time as needed
            )

    return slot


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

