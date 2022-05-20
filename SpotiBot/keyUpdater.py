import gspread

sa = gspread.service_account()
sh = sa.open('SpotifyLogs')
wks = sh.worksheet("upCount")
wks2 = sh.worksheet("LogsTest")
wks3 = sh.worksheet("Keys")


with open('keys.txt') as input_file:
    long_list2 = [line.strip() for line in input_file]
keys = wks3.range('A2:A' + str(len(long_list2) + 1))
print(len(long_list2))
for i, val in enumerate(long_list2):
    keys[i].value = val
wks3.update_cells(keys)

with open('myKeys.txt') as input_file:
    long_list = [line.strip() for line in input_file]
myKey = wks3.range('B2:B202')
for i, val in enumerate(long_list):
    myKey[i].value = val
wks3.update_cells(myKey)