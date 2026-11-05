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

# 1) Eye-catching opening: testing allocation creates a testable boundary.
im,d=canvas(1800,1100)
txt(d,(75,55),"THE IDEA  /  テスト設計からアーキテクチャを決める",28,TEAL,True)
txt(d,(75,115),"E2Eを増やす前に、テストケースを決める。",65,INK,True)
txt(d,(77,214),"54通りの判定を「どこで確かめるか」が、モジュールの境界を決めます。",36,SUB)

rect(d,(75,315,672,870),WHITE,LINE,22)
rect(d,(725,315,1725,870),WHITE,TEAL,22,4)
txt(d,(116,342),"E2Eだけを増やすと…",43,RED,True)
txt(d,(760,342),"提案：テストケースを先に配分",43,TEAL,True)
for i,(t,sub) in enumerate([
    ("仕様から実装","コード中心に作り始める"),
    ("画面から54条件を確認","セットアップが何度も必要"),
    ("ルールの問題が埋もれる","失敗原因を切り分けづらい")]):
    y=432+i*140
    rect(d,(115,y,630,y+100),RED_L,"#F4CFC9",15,2)
    txt(d,(141,y+10),t,35,INK,True)
    txt(d,(141,y+60),sub,26,SUB)
    if i!=2: down(d,374,y+101,y+132,RED,4)

rect(d,(765,424,1680,520),GRAY_L,"#CBD5DF",15)
center(d,1222,469,"① 仕様・受入条件から、期待結果つきのケースを作る",34,INK,True)
down(d,1222,522,558,TEAL)
rect(d,(765,565,1680,653),TEAL_L,"#8ACCC0",15)
center(d,1222,609,"② 3 × 3 × 3 × 2 ＝ 54ケースを確定",40,TEAL,True)
line(d,[(1222,656),(1222,690),(1005,690),(1005,714)],TEAL,4)
line(d,[(1222,690),(1470,690),(1470,714)],TEAL,4)
rect(d,(765,720,1205,794),BLUE_L,"#A8BCE9",15)
center(d,985,755,"E2E：代表的な操作",32,BLUE,True)
rect(d,(1250,720,1680,794),TEAL_L,"#8ACCC0",15)
center(d,1465,755,"非E2E：条件の全網羅",30,TEAL,True)
line(d,[(985,795),(985,814),(1222,814)],TEAL,4)
line(d,[(1465,795),(1465,814),(1222,814)],TEAL,4)
down(d,1222,814,854,TEAL)
rect(d,(75,912,1725,1037),INK,INK,22)
center(d,900,957,"③ 非E2Eで直接検証できる「テスト可能なモジュール」を設計",41,WHITE,True)
center(d,900,1010,"E2Eはシステムの接続を、非E2Eは判定ルールの組み合わせを確認",29,"#DAEEF0")
save(im,"hero.png")

# 2) Flowchart: practical decisions and testable-module feedback.
im,d=canvas(1800,1770)
txt(d,(80,55),"HOW TO  /  実践の判断フロー",30,TEAL,True)
txt(d,(80,113),"テストの配分 → テスト可能な設計",66,INK,True)
txt(d,(82,211),"同じ機能をE2E・非E2Eの両方で検証しても構いません。目的で役割を分けます。",32,SUB)

rect(d,(375,313,1425,433),WHITE,LINE,18)
center(d,900,353,"STEP 1",26,TEAL,True)
center(d,900,398,"仕様・受入条件から、テストケースと期待結果を定義",34,INK,True)
down(d,900,435,484,TEAL)
rect(d,(375,490,1425,610),WHITE,LINE,18)
center(d,900,531,"STEP 2",26,TEAL,True)
center(d,900,576,"条件・組み合わせ・境界値を整理する",35,INK,True)
down(d,900,612,669,TEAL)
# branching question diamond
d.polygon([(900,675),(1220,775),(900,875),(580,775)],fill=TEAL_L)
line(d,[(900,675),(1220,775),(900,875),(580,775),(900,675)],TEAL,4)
center(d,900,750,"何を確かめる",36,TEAL,True)
center(d,900,798,"テストか？",36,TEAL,True)
line(d,[(580,775),(398,775),(398,911)],BLUE,5)
down(d,398,909,938,BLUE)
line(d,[(1220,775),(1400,775),(1400,911)],TEAL,5)
down(d,1400,909,938,TEAL)
center(d,313,735,"操作・連携",29,BLUE,True)
center(d,1518,735,"判定・計算",29,TEAL,True)

rect(d,(90,951,818,1147),BLUE_L,"#9AAFE0",20)
center(d,454,998,"E2E",44,BLUE,True)
center(d,454,1057,"画面 → API → DB の一連の動作",30,INK,True)
center(d,454,1106,"代表的な成功・拒否・反映を検証",29,SUB)
rect(d,(980,951,1710,1147),TEAL_L,"#80C5BA",20)
center(d,1345,998,"非E2E",44,TEAL,True)
center(d,1345,1057,"判定を直接呼び、全54ケースを確認",29,INK,True)
center(d,1345,1106,"速く・独立して期待結果と照合",29,SUB)
down(d,1345,1148,1201,TEAL)

d.polygon([(1345,1212),(1573,1292),(1345,1372),(1117,1292)],fill=WHITE)
line(d,[(1345,1212),(1573,1292),(1345,1372),(1117,1292),(1345,1212)],TEAL,4)
center(d,1345,1272,"直接テスト",31,INK,True)
center(d,1345,1313,"できる？",31,INK,True)
line(d,[(1117,1292),(926,1292),(926,1426)],AMBER,5)
down(d,926,1424,1452,AMBER)
txt(d,(963,1261),"NO",28,AMBER,True)
line(d,[(1573,1292),(1680,1292),(1680,1426)],TEAL,5)
down(d,1680,1424,1452,TEAL)
txt(d,(1592,1251),"YES",27,TEAL,True)
rect(d,(790,1460,1245,1548),"#FFF4D9","#E3BE6A",15)
center(d,1017,1504,"副作用から判定を分離",31,INK,True)
rect(d,(1270,1460,1740,1548),TEAL_L,"#80C5BA",15)
center(d,1505,1504,"既存の境界で直接検証",29,INK,True)
# link E2E and modules into verification step
line(d,[(454,1149),(454,1631),(900,1631)],BLUE,5)
line(d,[(1017,1549),(1017,1601),(1330,1601)],TEAL,5)
line(d,[(1505,1549),(1505,1601),(1330,1601)],TEAL,5)
down(d,1330,1602,1631,TEAL)
rect(d,(525,1651,1725,1732),INK,INK,18)
center(d,1125,1691,"E2Eで接続を確認し、非E2Eでルールを網羅",34,WHITE,True)
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
