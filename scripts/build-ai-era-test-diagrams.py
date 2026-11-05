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

# 1) E2E first. Non-E2E is for high-volume combinations that cannot run economically in E2E.
im,d=canvas(1800,1200)
txt(d,(74,50),"THE IDEA  /  ユーザーに近いテストを厚くします",29,BLUE,True)
txt(d,(74,120),"原則はE2E。ユーザーに最も近いからです。",63,INK,True)
txt(d,(78,214),"ただし大量の組み合わせだけは、非画面のスクリプトで検証します。",36,SUB)
rect(d,(80,308,1720,442),WHITE,LINE,21)
center(d,900,346,"実装前に決める",27,BLUE,True)
center(d,900,400,"ユーザー操作・UX・受入条件  →  テストケース・期待結果・組み合わせ",38,INK,True)
down(d,900,443,510,BLUE,6)

rect(d,(83,535,1167,1008),BLUE_L,"#9AB3EA",26,5)
rect(d,(111,565,442,629),BLUE,BLUE,16)
center(d,275,598,"基本方針",30,WHITE,True)
txt(d,(132,663),"まず、E2Eでテストします。",48,BLUE,True)
txt(d,(137,751),"画面操作　・　ユーザビリティ",34,INK,True)
txt(d,(137,808),"API / DB / 画面への結果反映",34,INK,True)
txt(d,(137,908),"実行可能なケースは、E2Eで確認",32,BLUE,True)

line(d,[(1169,760),(1221,760)],AMBER,6)
right(d,1221,760,1260,AMBER,6)
rect(d,(1285,536,1718,1008),WHITE,AMBER,26,5)
center(d,1500,595,"例外",36,AMBER,True)
center(d,1500,662,"画面では回せない",30,INK,True)
center(d,1500,710,"大量パターン",34,INK,True)
rect(d,(1310,777,1690,850),TEAL_L,"#8ACCC0",14)
center(d,1500,812,"非E2Eのスクリプト",30,TEAL,True)
down(d,1500,851,894,TEAL)
center(d,1500,938,"副作用なし・疎結合",31,TEAL,True)
center(d,1500,976,"実装前に設計する",27,SUB)

rect(d,(80,1060,1720,1156),INK,INK,21)
center(d,900,1108,"E2Eを主役にするために、テストケースからモジュールを設計する。",42,WHITE,True)
save(im,"hero.png")

# 2) Practical flow: E2E default, exception based on feasibility, then design before coding.
im,d=canvas(1800,1795)
txt(d,(80,46),"HOW TO  /  実装前に判断するためのフローチャート",29,TEAL,True)
txt(d,(80,111),"まずE2E。回しきれないケースだけ非E2E。",62,INK,True)
txt(d,(80,208),"例外が判明したら、その時点で副作用のない疎結合モジュールを設計します。",34,SUB)

rect(d,(360,310,1440,430),WHITE,LINE,18)
center(d,900,350,"STEP 1  /  テストケースを設計",28,BLUE,True)
center(d,900,393,"ユーザー操作・UX・期待結果を整理",36,INK,True)
down(d,900,431,479,BLUE)
rect(d,(360,490,1440,608),WHITE,LINE,18)
center(d,900,526,"STEP 2  /  組み合わせを洗い出す",28,BLUE,True)
center(d,900,573,"因子・水準・境界値・想定実行時間",36,INK,True)
down(d,900,610,671,BLUE)

d.polygon([(900,678),(1240,807),(900,936),(560,807)],fill=BLUE_L)
line(d,[(900,678),(1240,807),(900,936),(560,807),(900,678)],BLUE,5)
center(d,900,778,"E2Eで現実的に",37,BLUE,True)
center(d,900,827,"実行できる？",37,BLUE,True)

line(d,[(560,807),(438,807),(438,977)],BLUE,5)
down(d,438,974,998,BLUE)
center(d,403,769,"YES",29,BLUE,True)
line(d,[(1240,807),(1360,807),(1360,977)],AMBER,5)
down(d,1360,974,998,AMBER)
center(d,1407,769,"NO",29,AMBER,True)

rect(d,(87,1010,790,1187),BLUE_L,"#A6B7E8",20)
center(d,440,1050,"E2Eテスト",43,BLUE,True)
center(d,440,1109,"画面・操作・UX・API・DB",31,INK,True)
center(d,440,1154,"ユーザーに近い振る舞いを確認",27,SUB)
rect(d,(1005,1010,1713,1187),"#FFF3D7","#E2B968",20)
center(d,1359,1050,"非E2Eに配分",43,AMBER,True)
center(d,1359,1110,"大量の組み合わせを直接検証",31,INK,True)
center(d,1359,1154,"画面の繰り返しは避ける",27,SUB)
down(d,1359,1189,1239,AMBER)
rect(d,(1005,1250,1713,1380),TEAL_L,"#8DC9BE",20)
center(d,1359,1293,"STEP 3  /  実装前の設計",29,TEAL,True)
center(d,1359,1341,"副作用のない疎結合モジュール",33,INK,True)
down(d,1359,1381,1436,TEAL)
rect(d,(1005,1448,1713,1568),TEAL_L,"#8DC9BE",20)
center(d,1359,1489,"スクリプトでルールを網羅",33,TEAL,True)
center(d,1359,1534,"入力 × 期待結果を直接照合",29,INK)
line(d,[(440,1188),(440,1676),(892,1676)],BLUE,5)
line(d,[(1359,1569),(1359,1643),(892,1643)],TEAL,5)
down(d,892,1643,1676,TEAL)
rect(d,(465,1693,1695,1772),INK,INK,17)
center(d,1080,1732,"E2Eで利用者の価値を、非E2Eで例外の大量条件を確かめる",31,WHITE,True)
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

txt(d,(83,1202),"※ 各マスが1テストケース。画面操作を54回繰り返す必要はありません。",31,TEAL,True)
save(im,"case-matrix.png")