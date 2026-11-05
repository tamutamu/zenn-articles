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

# 1) The article's ONE core concept: compare when test design is considered.
# Keep concrete E2E/unit examples in the later diagrams, not this opening concept.
im,d=canvas(1800,1280)
txt(d,(72,38),"CONCEPT  /  テスト可能なシステムをどう設計するか",30,TEAL,True)
txt(d,(72,105),"テストを考える順序で、設計の進め方が変わる",61,INK,True)
txt(d,(75,206),"同じシステムでも「いつテスト方法を考えるか」によって、手戻りを防げる場合があります。",31,SUB)

# Two distinct approaches side-by-side, with the same number of stages.
panels=[
    (70,859,LINE,WHITE,"テストの検討を後回しにすると",SUB),
    (942,1730,TEAL,WHITE,"実装前にテストを考えると",TEAL),
]
for x0,x1,border,background,heading,hcolor in panels:
    rect(d,(x0,294,x1,1089),background,border,23,4)
    rect(d,(x0+23,318,x1-23,402),GRAY_L if x0==70 else TEAL_L,GRAY_L if x0==70 else TEAL_L,12,2)
    center(d,(x0+x1)//2,359,heading,39,hcolor,True)

left_steps=[
    ("①  システムを設計・実装","モジュール構造を決めて作り始める"),
    ("②  テストケースを検討","必要な組み合わせ・期待結果を洗い出す"),
    ("③  テストしづらい箇所に気付く","直接テストしたい処理が他と密結合"),
]
right_steps=[
    ("①  必要なテストを設計","システム全体の検証方法と期待結果"),
    ("②  テスト可能な構造を設計","責務・入出力・モジュール境界を決める"),
    ("③  システムを実装","必要なテストを実行できる構造で開発"),
]
for x0,x1,steps,color,fill,border in [
    (112,816,left_steps,INK,GRAY_L,"#D4DEE8"),
    (984,1687,right_steps,TEAL,TEAL_L,"#9CCFC3"),
]:
    cx=(x0+x1)//2
    for i,(heading,desc) in enumerate(steps):
        y=450+i*183
        rect(d,(x0,y,x1,y+139),fill,border,16,2)
        center(d,cx,y+42,heading,36,color,True)
        center(d,cx,y+100,desc,27,INK if i!=2 else SUB)
        if i<2:down(d,cx,y+140,y+181,SUB if x0==112 else TEAL,5)

# Outcome of each approach
rect(d,(112,1004,816,1068),"#FFF2E8","#E9BCA9",15,2)
center(d,464,1035,"必要なら、後から構造を見直す",30,RED,True)
rect(d,(984,1004,1687,1068),TEAL_L,"#80C5B7",15,2)
center(d,1335,1035,"最初からテスト可能な構造で進める",30,TEAL,True)

rect(d,(70,1131,1730,1248),INK,INK,20)
center(d,900,1170,"テストケースは、実装後の確認だけでなく",34,WHITE,True)
center(d,900,1214,"実装前の設計材料にもなる",41,WHITE,True)
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