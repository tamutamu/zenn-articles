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

# 1) Core proposal: start from required quality, not a test-level quota.
im,d=canvas(1800,1180)
txt(d,(75,43),"THE IDEA  /  先に必要な検証を定義する",29,TEAL,True)
txt(d,(75,112),"テストの量ではなく、必要な品質から考える",60,INK,True)
txt(d,(78,208),"テスト方法は結論です。実装前のテスト設計がモジュール構造を決めます。",35,SUB)

rect(d,(75,300,762,1025),WHITE,LINE,24,3)
rect(d,(815,300,1725,1025),WHITE,TEAL,24,5)
center(d,419,347,"テスト方法から始める",39,SUB,True)
center(d,1270,347,"必要な検証から始める",39,TEAL,True)

for i,(label,desc) in enumerate([
    ("① 手段を先に決める","E2Eを厚くする／ユニットを増やす"),
    ("② 後から条件を洗い出す","重要な観点や組み合わせに気付く"),
    ("③ 実装後に構造を調整","直接テストしづらい処理を修正"),
]):
    y=421+i*181
    rect(d,(108,y,733,y+136),GRAY_L,"#CCD6DF",15,2)
    txt(d,(136,y+15),label,33,INK,True)
    txt(d,(136,y+76),desc,25,SUB)
    if i<2:down(d,420,y+139,y+178,SUB,4)

for i,(label,desc) in enumerate([
    ("① 必要な品質を定義","ユーザーの期待・業務ルール・リスク"),
    ("② 検証ケースを洗い出す","操作・条件の組み合わせ・期待結果"),
    ("③ 手法を配分し、境界を設計","E2E／ユニット／その他の検証"),
]):
    y=421+i*181
    rect(d,(851,y,1685,y+136),TEAL_L,"#95CBC0",15,2)
    txt(d,(878,y+15),label,36,TEAL,True)
    txt(d,(878,y+78),desc,28,INK)
    if i<2:down(d,1270,y+139,y+178,TEAL,4)
rect(d,(75,1055,1725,1150),INK,INK,19)
center(d,900,1100,"テストケースから必要なモジュール境界を導出し、設計段階で品質を作り込む",38,WHITE,True)
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