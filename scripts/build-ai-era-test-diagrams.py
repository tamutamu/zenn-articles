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

# 1) Why the order matters: design for testability BEFORE implementation.
im,d=canvas(1800,1170)
txt(d,(72,48),"THE IDEA  /  テスト可能性を設計に組み込む",29,TEAL,True)
txt(d,(72,110),"実装前のテストケース設計が、モジュールの境界を決める",56,INK,True)
txt(d,(75,204),"E2Eかユニットかを先に決めつけず、組み合わせと実行負荷を見て判断します。",34,SUB)

rect(d,(75,296,787,998),WHITE,LINE,23,3)
rect(d,(824,296,1725,998),WHITE,TEAL,23,5)
center(d,430,341,"実装してから考えると",38,SUB,True)
center(d,1269,341,"実装前に考えておけば",38,TEAL,True)

for i,(label,desc) in enumerate([
    ("① 先に実装する","判定とDB操作を一緒に書く"),
    ("② 大量のケースに気付く","スクリプトから直接テストしたい"),
    ("③ 構造を見直す","密結合な処理を分離し直す")
]):
    y=411+i*174
    rect(d,(115,y,745,y+130),GRAY_L,"#D1D9E2",14,2)
    txt(d,(146,y+15),label,34,INK,True)
    txt(d,(146,y+72),desc,27,SUB)
    if i<2: down(d,430,y+132,y+170,SUB,4)
rect(d,(115,940,745,983),RED_L,RED,12,2)
center(d,430,961,"テストのために手戻りが発生",25,RED,True)

for i,(label,desc) in enumerate([
    ("① テストケースを洗い出す","因子・水準・組み合わせ・期待結果"),
    ("② 実行可能性を見積もる","E2Eで回せるか / 直接検証が必要か"),
    ("③ テスト可能な構造を設計","必要な処理を副作用なし・疎結合に")
]):
    y=411+i*174
    rect(d,(860,y,1685,y+130),TEAL_L,"#A0D4C8",14,2)
    txt(d,(890,y+15),label,34,TEAL,True)
    txt(d,(890,y+72),desc,28,INK)
    if i<2: down(d,1272,y+132,y+170,TEAL,4)
rect(d,(860,940,1685,983),TEAL_L,TEAL,12,2)
center(d,1272,961,"テスト可能な構造のまま実装に進める",25,TEAL,True)

rect(d,(75,1041,1725,1138),INK,INK,18)
center(d,900,1089,"テストケースを先に決めることが、開発段階の品質の作り込みにつながる。",39,WHITE,True)
save(im,"hero.png")

# 2) Pre-implementation DESIGN ONLY: no test execution steps appear in this flow.
im,d=canvas(1800,1710)
txt(d,(80,45),"DESIGN FLOW  /  実装前に決めること",30,TEAL,True)
txt(d,(80,110),"テストケースの配分から、モジュール設計まで",61,INK,True)
txt(d,(80,206),"この図は設計工程です。テストの実装や実行は、この後に行います。",34,SUB)

rect(d,(360,304,1440,426),WHITE,LINE,19)
center(d,900,345,"STEP 1  /  テストケース設計",29,BLUE,True)
center(d,900,394,"ユーザー操作・UX・受入条件と期待結果を整理",34,INK,True)
down(d,900,428,477,BLUE)
rect(d,(360,489,1440,615),WHITE,LINE,19)
center(d,900,528,"STEP 2  /  因子と組み合わせを洗い出す",29,BLUE,True)
center(d,900,581,"条件数・想定実行時間・データ準備の負荷を見積もる",32,INK,True)
down(d,900,617,677,BLUE)

d.polygon([(900,681),(1240,808),(900,935),(560,808)],fill=BLUE_L)
line(d,[(900,681),(1240,808),(900,935),(560,808),(900,681)],BLUE,5)
center(d,900,778,"E2Eで現実的に",37,BLUE,True)
center(d,900,828,"実行できる？",37,BLUE,True)
line(d,[(560,808),(438,808),(438,980)],BLUE,5)
down(d,438,977,1002,BLUE)
center(d,388,771,"YES",30,BLUE,True)
line(d,[(1240,808),(1360,808),(1360,980)],AMBER,5)
down(d,1360,977,1002,AMBER)
center(d,1408,771,"NO",30,AMBER,True)

rect(d,(90,1014,790,1221),BLUE_L,"#A6B7E8",21)
center(d,440,1057,"E2Eのテストケースを確定",36,BLUE,True)
center(d,440,1123,"画面操作・UX・API・DB連携",29,INK,True)
center(d,440,1179,"対象ケースと期待結果を設計",29,SUB)
rect(d,(1008,1014,1710,1221),"#FFF3D7","#E2B968",21)
center(d,1359,1057,"非E2Eの対象ケースを確定",35,AMBER,True)
center(d,1359,1123,"大量パターンの組み合わせ",30,INK,True)
center(d,1359,1179,"直接入力するケースと期待結果を設計",27,SUB)
down(d,1359,1223,1270,AMBER)

rect(d,(1008,1282,1710,1469),TEAL_L,"#8DC9BE",21)
center(d,1359,1330,"STEP 3  /  テスト可能なモジュール設計",29,TEAL,True)
center(d,1359,1388,"副作用なし・疎結合の境界を定義",31,INK,True)
center(d,1359,1433,"入力・出力・責務を決定",27,SUB)
line(d,[(440,1222),(440,1584),(890,1584)],BLUE,5)
line(d,[(1359,1471),(1359,1551),(890,1551)],TEAL,5)
down(d,890,1551,1584,TEAL)
rect(d,(320,1600,1720,1681),INK,INK,18)
center(d,1020,1641,"設計完了：E2E・非E2Eのケース配分とモジュール構造が確定",33,WHITE,True)
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