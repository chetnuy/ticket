#!/bin/bash
import  time
from datetime import  datetime
from pytz import timezone

mtime = [1539153000,1539156600,1539160200,1539163800,1539167400,1539171000,1539174600,1539178200,1539181800,1539185400,1539239400,1539243000,1539246600,1539250200,1539253800,1539257400,1539261000,1539264600,1539268200,1539271800]

# for tt in mtime:
#     time_tuple = time.localtime(tt)
#     print(time.strftime("%D %H:%M", time_tuple))



timestamp = 1539272971
time_tuple = time.localtime(timestamp)
print(time.strftime("%D %H:%M", time_tuple))

#now_utc = datetime.now(timezone('Europe/Moscow'))
#now_utc = datetime.astimezone(timezone('Europe/Berlin'))

#print(now_utc.strftime("%H:%M"))
























