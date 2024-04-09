import csv
import datetime
import platform
import subprocess as sp
import threading


# ping総当たりのためのスレッド処理クラス
class PingThreading(threading.Thread):
    def __init__(self, ip_address):
        self.ip_address = ip_address
        threading.Thread.__init__(self)

    def run(self):
        if platform.system() == "Linux":
            # Linux用のコマンド
            sp.run(["ping", "-c", "1", "-w", "1", "192.168.10." + str(self.ip_address)])
        elif platform.system() == "Darwin":
            # MacOS（Darwin）用のコマンド
            sp.run(["ping", "-c", "1", "-W", "1", "192.168.10." + str(self.ip_address)])
        else:
            print("Unsupported OS")


# 別ファイルに保存したmacアドレス-個人名テーブルの取得
def main(mac_address_list="/home/attendance_checker/mac_address_list.csv"):
    with open(mac_address_list) as f:
        reader = csv.reader(f)
        mac_address = [row for row in reader]
    # エクセルの一番上の名前行の削除
    del mac_address[0]

    # arpによるWi-Fi環境下のデバイスの取得
    thread_list = []
    for i in range(2, 255):
        thread = PingThreading(ip_address=i)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    output = (sp.run(["arp", "-a"], capture_output=True, text=True)).stdout
    # 存在した場合の名前の出力
    now_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    save_data = [now_time]
    for i in range(len(mac_address)):
        if (
            output.find(mac_address[i][1]) != -1
            or output.find(mac_address[i][2]) != -1
            or output.find(mac_address[i][3]) != -1
            or output.find(mac_address[i][4]) != -1
        ):
            print(mac_address[i][0])
            save_data.append(mac_address[i][0])

    with open(".attendance_data.csv") as f:
        reader = csv.reader(f)
        attendance_data = [row for row in reader]
    pre_attendance_data = []
    for name in save_data[1:]:
        with open("now_attendance.csv") as f:
            reader = csv.reader(f)
            attendance__ = [row for row in reader]
        flag = False
        for i in range(len(attendance__)):
            if name == attendance__[i][0]:
                flag = True
        if flag is False:
            user_enter(name, now_time)
    while len(attendance_data) > 10:
        pre_attendance_data = attendance_data[0]
        del attendance_data[0]
    attendance_data.append(save_data)
    with open(".attendance_data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(attendance_data)
    for name in pre_attendance_data:
        flag = False
        for i in range(len(attendance_data)):
            if name in attendance_data[i]:
                flag = True
                break
        if flag is False:
            user_exit(name)

    # template.htmlからテンプレート内容を読み込む
    with open("template.html", "r") as template_file:
        template_content = template_file.read()

    # file.txtから内容を読み込む
    with open("now_attendance.csv", "r") as attendance_file:
        file_content = attendance_file.read()

    # 改行を<br/>で置換
    file_content = file_content.replace("\n", "<br/>\n")

    # テンプレート内のプレースホルダーをfile.txtの内容で置換
    html_content = template_content.replace("{{content}}", file_content)

    # 結果をindex.htmlに保存
    with open("index.html", "w") as output_file:
        output_file.write(html_content)


def user_enter(name, now_time):
    with open("now_attendance.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([name, now_time])


def user_exit(name):
    with open("now_attendance.csv") as f:
        reader = csv.reader(f)
        attendance = [row for row in reader]
    with open(".attendance_data.csv") as f:
        reader = csv.reader(f)
        attendance_data = [row for row in reader]
    for i in range(len(attendance)):
        if attendance[i][0] == name:
            with open("log.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [attendance[i][0], attendance[i][1], attendance_data[0][0]]
                )
            del attendance[i]
            with open("now_attendance.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerows(attendance)
            break


if __name__ == "__main__":
    main("./mac_address_list.csv")
