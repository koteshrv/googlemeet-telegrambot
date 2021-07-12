#https://www.geeksforgeeks.org/python-schedule-library/

import schedule, time
from dependencies.meetbot import meetbot
from dependencies.others import data


def dailySchedule():

    startupTime = data["otherData"]["startuptime"]
    # Every day at 8.45 AM meetbot() is called.
    schedule.every().day.at(startupTime).do(meetbot)

    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
    
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)



    
    
