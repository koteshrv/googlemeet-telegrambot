#https://www.geeksforgeeks.org/python-schedule-library/

import schedule, time
from dependencies.meetbot import meetbot

def dailySchedule():

    # Every day at 8.45 AM meetbot() is called.
    schedule.every().day.at("08:55").do(meetbot)

    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
    
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)



    
    
