from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path("images/ai-era-e2e-module-test-design")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "C:/Windows/Fonts/meiryo.ttc"
INK = "#192D40"
SUB = "#50647B"
LINE = "#B9C8D5"
BG = "#F7F9FC"
WHITE = "#FFFFFF"
TEAL = "#007F73"
TEAL_L = "#E5F5F0"
BLUE = "#3159BA"
BLUE_L = "#EAF0FD"
RED = "#B14B45"
RED_L = "#FCEDEB"
GRAY_L = "#EDF1F5"
AMBER = "#D58B14"

def f(sz, bold=False):
    return ImageFont.truetype(FONT, sz, index=1 if bold else 0)

def canvas(w,h):
    im=Image.new("RGB",(w,h),BG)
    return im,ImageDraw.Draw(im)

def txt(d, xy, s, sz=32, color=INK, bold=False, anchor=None, spacing=8):
    d.multiline_text(xy,s,font=f(sz,bold),fill=color,anchor=anchor,spacing=spacing,align="center" if anchor and "m" in anchor else "left")

def rect(d,box,fill=WHITE,outline=LINE,r=22,width=3):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def line(d,points,fill=LINE,width=5):
    d.line(points,fill=fill,width=width,joint="curve")

def down(d,x,y1,y2,color=SUB,width=5):
    d.line([(x,y1),(x,y2-13)],fill=color,width=width)
    d.polygon([(x-11,y2-20),(x+11,y2-20),(x,y2)],fill=color)

def right(d,x1,y,x2,color=SUB,width=5):
    d.line([(x1,y),(x2-14,y)],fill=color,width=width)
    d.polygon([(x2-19,y-11),(x2-19,y+11),(x2,y)],fill=color)

def center(d,x,y,s,sz=36,color=INK,bold=False):
    txt(d,(x,y),s,sz,color,bold,anchor="mm")

def save(im,name):
    im.save(OUT/name,optimize=True)
    print(str(OUT/name),im.size)

# 1) Hero concept: same validation needs, different architecture outcomes.
# The thesis is testability designed BEFORE implementation, not a fixed E2E/Unit ratio.
im,d=canvas(1800,1510)
txt(d,(70,40),"CONCEPT  /  テスト設計からアーキテクチャを考える",30,TEAL,True)
txt(d,(70,120),"「どうテストするか」で、設計は変わる",69,INK,True)
txt(d,(72,220),"検証方法を実装前に決めると、必要なモジュール境界が見えてきます。",34,SUB)

# Input: shared, required verification for a task management system
rect(d,(76,294,1724,574),WHITE,LINE,22,3)
center(d,900,337,"システムには、次のような検証が必要",40,INK,True)
rect(d,(116,399,848,535),BLUE_L,"#A0B6EB",15,3)
center(d,482,443,"操作・連携をE2Eで確認",33,BLUE,True)
center(d,482,494,"タスク編集 → 保存 → 画面への反映",28,INK)
rect(d,(950,399,1683,535),TEAL_L,"#8ECBBE",15,3)
center(d,1316,443,"大量の条件を直接確認",33,TEAL,True)
center(d,1316,494,"権限 × 操作 × 状態 × 担当者（54ケース）",28,INK)

# Contrast what changes in architecture when testing is considered before implementation
down(d,900,574,618,TEAL,6)
rect(d,(519,628,1281,697),INK,INK,16)
center(d,900,663,"この検証を、実装前の設計に反映したか？",37,WHITE,True)

# Comparison panels, no conflation of testing phase and design phase
rect(d,(75,740,866,1361),WHITE,LINE,23,3)
rect(d,(935,740,1725,1361),WHITE,TEAL,23,4)
rect(d,(108,770,833,843),GRAY_L,GRAY_L,12)
rect(d,(967,770,1692,843),TEAL_L,TEAL_L,12)
center(d,470,806,"A  実装後にテストを検討",36,SUB,True)
center(d,1329,806,"B  実装前にテストを設計",36,TEAL,True)

center(d,470,883,"権限判定がRepositoryに依存",31,INK,True)
center(d,1329,883,"権限判定を独立させる",31,INK,True)

# A: Service contains the decision logic and database dependency
rect(d,(300,928,745,1130),GRAY_L,LINE,17,3)
center(d,522,967,"TaskService",34,INK,True)
line(d,[(325,999),(722,999)],LINE,2)
center(d,522,1046,"権限判定",32,INK,True)
center(d,522,1092,"Repositoryアクセス",27,SUB)
rect(d,(107,980,272,1075),BLUE_L,"#A6BCEB",13,2)
center(d,189,1027,"E2E",31,BLUE,True)
right(d,275,1027,295,BLUE,3)
rect(d,(106,1167,342,1255),"#FFF4DD","#E3BC80",13,3)
center(d,224,1206,"54ケース",31,AMBER,True)
center(d,224,1240,"直接検証",24,SUB)
line(d,[(345,1208),(522,1208),(522,1134)],AMBER,4)
d.polygon([(511,1152),(533,1152),(522,1132)],fill=AMBER)
rect(d,(370,1166,747,1255),"#FFF4DD","#E3BC80",13,3)
center(d,558,1196,"模擬Repositoryが必要",28,INK,True)
center(d,558,1232,"ケースごとにデータを準備",25,SUB)
center(d,471,1310,"後から構造の見直しが発生する場合も",27,RED)

# B: integration path is preserved, direct scripted access to a policy is possible
rect(d,(972,942,1126,1027),BLUE_L,"#A6BCEB",12,2)
center(d,1049,984,"画面",30,BLUE,True)
rect(d,(1214,942,1434,1027),GRAY_L,LINE,12,2)
center(d,1324,983,"TaskService",29,INK,True)
rect(d,(1527,942,1692,1027),GRAY_L,LINE,12,2)
center(d,1609,983,"DB",29,INK,True)
right(d,1130,983,1208,BLUE,4)
right(d,1437,983,1520,BLUE,4)
txt(d,(985,900),"E2E：操作のつながりを確認",25,BLUE,True)

rect(d,(979,1133,1207,1230),TEAL_L,"#84CDBE",12,3)
center(d,1093,1171,"54ケース",31,TEAL,True)
center(d,1093,1208,"直接検証",25,SUB)
rect(d,(1385,1122,1691,1248),TEAL_L,TEAL,14,4)
center(d,1538,1166,"PermissionPolicy",30,TEAL,True)
center(d,1538,1211,"判定専用・副作用なし",25,INK)
right(d,1211,1184,1379,TEAL,5)
line(d,[(1324,1031),(1324,1090),(1538,1090),(1538,1118)],TEAL,4)
d.polygon([(1528,1106),(1548,1106),(1538,1122)],fill=TEAL)
center(d,1329,1310,"必要な判定だけを独立して検証できる",27,TEAL,True)

rect(d,(75,1401,1725,1480),INK,INK,17)
center(d,900,1441,"先にテストを考え、テスト可能な構造を設計してから実装する",43,WHITE,True)
save(im,"hero.png")

# 2) Flowchart, DESIGN PHASE ONLY. Selection is driven by required tests.
im,d=canvas(1800,1700)
txt(d,(80,52),"DESIGN FLOW  /  実装前に決める",29,TEAL,True)
txt(d,(80,115),"必要な検証から、テスト可能な設計へ",64,INK,True)
txt(d,(80,210),"E2E・ユニット・その他を目的と負荷で選び、必要な境界だけを設計します。",33,SUB)
rect(d,(355,305,1445,435),WHITE,LINE,19)
center(d,900,348,"STEP 1  /  必要な品質とリスク",29,BLUE,True)
center(d,900,401,"受入条件・操作・非機能・重要なリスクを整理",34,INK,True)
down(d,900,436,487,BLUE)

rect(d,(355,497,1445,627),WHITE,LINE,19)
center(d,900,538,"STEP 2  /  テストケースと期待結果",29,BLUE,True)
center(d,900,594,"条件・組み合わせ・境界値・確認方法を洗い出す",33,INK,True)
down(d,900,629,680,BLUE)

rect(d,(275,692,1525,938),BLUE_L,"#98B2E5",19,3)
center(d,900,741,"STEP 3  /  テスト方法と実行負荷を比較",33,BLUE,True)
for i,(kind,desc) in enumerate([
    ("E2E","操作・連携の確認"),
    ("ユニット","大量の条件判定"),
    ("その他","性能・UX・安全性"),
]):
    x=315+i*405
    rect(d,(x,801,x+380,903),WHITE,"#B6C7DF",14,2)
    center(d,x+190,829,kind,30,INK,True)
    center(d,x+190,879,desc,24,SUB)
down(d,900,939,996,BLUE)

d.polygon([(900,1010),(1260,1119),(900,1228),(540,1119)],fill=TEAL_L)
line(d,[(900,1010),(1260,1119),(900,1228),(540,1119),(900,1010)],TEAL,5)
center(d,900,1091,"直接テスト用の",34,TEAL,True)
center(d,900,1139,"独立モジュールが必要？",32,TEAL,True)

line(d,[(540,1119),(415,1119),(415,1273)],BLUE,5)
down(d,415,1270,1296,BLUE)
center(d,378,1081,"NO",27,BLUE,True)
line(d,[(1260,1119),(1387,1119),(1387,1273)],TEAL,5)
down(d,1387,1270,1296,TEAL)
center(d,1420,1081,"YES",27,TEAL,True)
rect(d,(93,1308,765,1480),BLUE_L,"#9BAFE0",19)
center(d,430,1360,"既存の構造で検証",36,BLUE,True)
center(d,430,1422,"追加の分離は不要",30,INK)
rect(d,(1040,1308,1715,1480),TEAL_L,"#87C5BA",19)
center(d,1377,1360,"モジュール境界を設計",36,TEAL,True)
center(d,1377,1422,"責務・入出力・依存を決める",27,INK)
line(d,[(430,1482),(430,1572),(903,1572)],BLUE,5)
line(d,[(1377,1482),(1377,1545),(903,1545)],TEAL,5)
down(d,903,1545,1575,TEAL)
rect(d,(330,1595,1715,1676),INK,INK,18)
center(d,1022,1635,"設計完了：必要なテストと実装構造が決まった状態",36,WHITE,True)
save(im,"workflow.png")

# 3) Case map: every cell corresponds to 1 exact combination.
im,d=canvas(1800,1270)
txt(d,(75,52),"EXAMPLE  /  タスクの操作権限",29,TEAL,True)
txt(d,(75,118),"54ケースは、具体的に何を網羅するのか",63,INK,True)
txt(d,(80,211),"役割 3 × 操作 3 × 状態 3 × 担当者本人かどうか 2 = 54通り",35,SUB)
stats=[("54","全組み合わせ",BLUE_L,BLUE),("26","許可",TEAL_L,TEAL),("28","拒否",RED_L,RED)]
for i,(n,label,fill,col) in enumerate(stats):
    x=80+i*560
    rect(d,(x,292,x+532,400),fill,fill,18)
    txt(d,(x+26,302),n,59,col,True)
    txt(d,(x+154,336),label,31,INK,True)

x0=80; labelw=465; cellw=202; top=474; rowh=69
roles=["管理者","一般ユーザー","閲覧専用"]
center(d,80+labelw/2,top+39,"操作 / タスク状態",29,INK,True)
for k,role in enumerate(roles):
    bx=x0+labelw+k*2*cellw
    rect(d,(bx,top,bx+2*cellw-8,top+84),GRAY_L,"#CFD9E1",12,2)
    center(d,bx+cellw-4,top+27,role,29,INK,True)
    center(d,bx+cellw/2-4,top+64,"担当外",24,SUB)
    center(d,bx+1.5*cellw-4,top+64,"担当本人",24,SUB)

actions=[("閲覧","view"),("編集","edit"),("削除","delete")]
statuses=[("未着手","todo"),("進行中","doing"),("完了","done")]
role_ids=["admin","member","viewer"]
for ai,(action,aid) in enumerate(actions):
    for si,(status,sid) in enumerate(statuses):
        row=ai*3+si
        y=top+101+row*rowh
        fill=WHITE if si%2==0 else "#F2F5F9"
        rect(d,(x0,y,x0+labelw-12,y+rowh-6),fill,fill,8,1)
        txt(d,(x0+26,y+17),action if si==0 else " ",30,INK,si==0)
        txt(d,(x0+215,y+18),status,27,SUB)
        for ri,role in enumerate(role_ids):
            for ass in range(2):
                good = aid=="view" or (aid=="edit" and sid!="done" and (role=="admin" or (role=="member" and ass==1))) or (aid=="delete" and role=="admin" and sid=="todo")
                x=x0+labelw+(ri*2+ass)*cellw
                c=TEAL if good else RED
                fill=TEAL_L if good else RED_L
                rect(d,(x,y,x+cellw-10,y+rowh-6),fill,fill,8,1)
                center(d,x+(cellw-10)/2,y+(rowh-6)/2,"許可" if good else "拒否",27,c,True)
    if ai<2:
        yy=top+101+(ai+1)*3*rowh-3
        line(d,[(x0,yy),(x0+labelw+cellw*6-10,yy)],LINE,3)

txt(d,(83,1202),"※ 各マスが1ケース。E2Eで回せるかは実行負荷と必要な頻度で判断します。",31,TEAL,True)
save(im,"case-matrix.png")