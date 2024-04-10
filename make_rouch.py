import csv
import datetime

# tstr = "2024年04月10日 10:15:02"
with open("log.csv") as f:
    reader = csv.reader(f)
    log = [row for row in  reader]
clipped_log = []
for i in range(len(log)):
    if log[i] == ["*","*","*"]:
        clipped_log.append(log[i])
print("test", clipped_log)
# tdatetime = datetime.datetime.strptime(tstr,"%Y年%m月%d日 %H:%M:%S")
# print(tdatetime, type(tdatetime))