# googlemeetbot
This can be used to attend all online classes with a single command. 

## Main features of googlemeetbot
    1. It can automatically fetch link from google classroom from both meetlink or from announcement tab.
    2. It can differenciate the link posted in announcement tab. Then joins the class if link is posted today. 
    3. It can join the class when the members count is greater than minCountToJoin(defined in data.json). If members count is not available, then it joins automatically.
    4. Leaves the class when the class strenght reaches minCountToLeave.
    5. If the classes ended early, then it will wait until next class.
    6. Sends the joining and leaving time in discord server.
    7. Plays alert sound when someone calls you.
    7. Auto responds with responseMessage when someone calls you. (can be turned off if not required).
    8. Fetches the class schedule from timetable.xlsx and updates when you want to change timetable.


