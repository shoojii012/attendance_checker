import csv
import datetime

# tstr = "2024年04月10日 10:15:02"
with open("log.csv") as f:
    reader = csv.reader(f)
    log = [row for row in  reader]
del log[0]
for l in log:
    l[1] = datetime.datetime.strptime(l[1],"%Y年%m月%d日 %H:%M:%S")
    l[2] = datetime.datetime.strptime(l[2],"%Y年%m月%d日 %H:%M:%S")
print(l)
init_date = datetime.datetime.strptime("2024年4月1日 00:00:00","%Y年%m月%d日 %H:%M:%S")
loop_date = init_date
output_date = []
while (loop_date <= log[-1][2]):#specifig_date loop
    clipped_log = []
    for i in range(len(log)):
        #日付を跨って研究室に存在する人はいない想定
        if log[i][1].strftime('%Y %m %d') == loop_date.strftime('%Y %m %d'):
            clipped_log.append(log[i])
    clear_log = []
    skip_list = []
    for i in range(len(clipped_log)):
        if (i in skip_list) is False:
            clear_log.append(log[i])
            for j in range(i+1,len(clipped_log)):
                if clear_log[-1][0] == log[j][0]:
                    skip_list.append(j)
                    clear_log[-1][2] = log[j][2]
    output_date = output_date + clear_log
    loop_date = loop_date + datetime.timedelta(days=1)

for entry in output_date:
    print(entry[1])
    entry[1] = datetime.datetime.strftime(entry[1], "%Y年%m月%d日 %H:%M:%S")
    entry[2] = datetime.datetime.strftime(entry[2], "%Y年%m月%d日 %H:%M:%S")
with open("log_for_lab.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(output_date)