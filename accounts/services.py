
from datetime import date, timedelta, datetime
from accounts.models import CustomUser, Calendar
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
        start_date = start_date #'2018-6-15'
        end_date = end_date #'2019-3-20'
        dtrange = len(pd.date_range(start=start_date, end=end_date, freq='d'))

    for i in range(dtrange):
        current_date = date.today() + timedelta(days=i)
        day_of_week = current_date.strftime('%a').upper()

        if day_of_week in days_of_week:
            schedule_date = current_date
            #if schedule_date == schedule_date
            # start_time= datetime.strptime(start_time, '%Y-%m-%d').time()
            # existing_slot= Calendar.objects.filter(user=user.id,
            #                                        schedule_date = schedule_date,start_time_gte=start_time+timedelta(hours=1))
            # if existing_slot:
            #     return "Already Schedule "
            slot =Calendar.objects.create(
                user=user,
                frequency=freq,
                days_of_week=day_of_week,
                start_time=start_time,  # Adjust the start time as needed
                schedule_date = schedule_date   # Adjust the end time as needed
            )

    return slot

