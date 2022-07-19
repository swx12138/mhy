from datetime import datetime

start = datetime.strptime("2020.09.15 09", "%Y.%m.%d %H")
print(start)

s = datetime.now() - start
print(s.days)

code = datetime.now().month * 100 + datetime.now().day + 1000
print(f"{'0'+str(code) if code<1000 else code}.genshin")
