# googlemeetbot
This bot can be used to attend all online classes with a single command. 

## Some features of googlemeetbot  

1. It can automatically fetch link from google classroom from both meetlink or from announcement tab.
2. No need to login to google account every time we use googlemeetbot.
3. It can differenciate the link posted in announcement tab. Then joins the class if link is posted today. 
4. It can join the class when the members count is greater than minCountToJoin(defined in data.json). 
5. If members count is not available, then it joins automatically.
6. Leaves the class when the class strenght reaches minCountToLeave.
7. If the classes ended early, then it will wait until next class.
8. Sends the joining and leaving time in discord server.
9. Plays alert sound when someone calls you.
10. Auto responds with responseMessage when someone calls you. (can be turned off if not required).
11. Fetches the class schedule from timetable.xlsx and updates when you want to change timetable.
12. Update the timetable temporarily, if the class schedule is changed only for that day.
13. Linux users can use **crontab** for scheduling the googlemeetbot daily and windows users can also configure task in **Windows Task Scheduler**.

## googlemeetbot commands
![commands](https://github.com/koteshrv/googlemeetbot/blob/main/images/3.png)

## Steps required to use googlemeetbot
   
1. Clone the repository.
2. Run `pip3 install -r requirements.txt` to install all dependencies.
3. Now create a new chrome profile and copy the profile path as shown [here](https://stackoverflow.com/questions/52394408/how-to-use-chrome-profile-in-selenium-webdriver-python-3#answer-61336851).
4. Now copy the profile path to `profilePath` present in data.json.
5. Modify the timetable.xlsx with your class timetable and use 24 hour format for class time.
6. For example, if you have class from `9:30 AM to 10:30 AM` then change it as `09:30 : 10:30`. 
7. In `classroomLinks` present in data.json, paste all your classroom links with subject as keys and url as value.
8. If some class links are posted in announcement tab, add the subjects in `linkPostedSeperatelyInAnnouncementTab` present in data.json.
9. Create a discord webhook. If you dont know how to create a discord webhook, then follow the steps [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).
10. Now, copy the `Webhook URL` and paste the url to `discordURL` present in data.json.
11. Change `minCountToJoin` and `minCountToLeave` according to your requirement. If the members count before joining the class is more than `minCountToJoin`,  
    then the bot joins the class. Similarly, when the members count falls less than `minCountToLeave`, then it detects it's time to leave the class and leaves 
    class.
12. Update the alertwords present in data.json according to your choice.
13. Set `autoReply` to `1`, if you want autoreply feature when someone calls you.
14. After completing the setup, If you are using linux, then move all the files of the repository to `/home/username/.local/bin/`.  
    If you are using windows, then add the repository to path.
15. Now change dir path of `pathToChromeDriver` that is present in the repository and `classTimeTableLocation` path in the data.json.  
16. If you are a linux user and if you moved the dir to `/home/username/.local/bin/`, then `pathToChromeDriver` is `/home/username/.local/bin/chromedriver` and `classTimeTableLocation` is `/home/username/.local/bin/timetable.xlsx`.  
17. If you are a windows user and if the repository is in `C:\Users\username\Desktop`, then `pathToChromeDriver` is  `C:\Users\username\Desktop\googlemeetbot\chromedriver` and `classTimeTableLocation` is `C:\Users\username\Desktop\googlemeetbot\timetable.xlsx`.  
18. Now the setup is complete!


## Some command previews

### Discord Notifications
![discord](https://github.com/koteshrv/googlemeetbot/blob/main/images/7.png)  

### Schedule of today's classes  
![classtimetable](https://github.com/koteshrv/googlemeetbot/blob/main/images/5.png)  

### Scheduling a class manually
![manualschedule](https://github.com/koteshrv/googlemeetbot/blob/main/images/6.png)  

### googlemeetbot waiting for the next class after leaving the class
![waitingfornextclass](https://github.com/koteshrv/googlemeetbot/blob/main/images/1.png)  



