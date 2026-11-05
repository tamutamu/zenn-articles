from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from math import atan2, cos, sin, pi

OUT=Path("images/ai-era-e2e-module-test-design")
OUT.mkdir(parents=True,exist_ok=True)
FONT="C:/Windows/Fonts/NotoSansJP-VF.ttf"
MONO="C:/Windows/Fonts/CascadiaCode.ttf"
S=2

paper="#FBFCFD"
ink="#1C2A38"
muted="#536375"
rule="#B9C5CD"
teal="#12766E"
teal_pale="#EAF5F2"
light="#EDF1F4"

def font(size, mono=False):
    ff=ImageFont.truetype(MONO if mono else FONT,size*S)
    if not mono: ff.set_variation_by_axes([660 if size>=35 else 440])
    return ff

def canvas(w,h):
    im=Image.new("RGB",(w*S,h*S),paper)
    d=ImageDraw.Draw(im)
    return im,d

def txt(d,x,y,s,size=34,color=ink,mono=False,anchor="lt",weight=None):
    ff=font(size,mono)
    if weight is not None and not mono: ff.set_variation_by_axes([weight])
    d.text((int(x*S),int(y*S)),s,font=ff,fill=color,anchor=anchor)

def rect(d,x1,y1,x2,y2,fill=None,stroke=None,width=1,radius=0):
    box=(x1*S,y1*S,x2*S,y2*S)
    if radius:d.rounded_rectangle(box,radius=radius*S,fill=fill,outline=stroke,width=width*S)
    else:d.rectangle(box,fill=fill,outline=stroke,width=width*S)

def line(d,points,fill=rule,width=2,dash=None):
    points=[(int(x*S),int(y*S)) for x,y in points]
    if not dash: d.line(points,fill=fill,width=width*S,joint="curve");return
    for p,q in zip(points,points[1:]):
        L=((q[0]-p[0])**2+(q[1]-p[1])**2)**.5
        k=(q[0]-p[0])/L if L else 0;l=(q[1]-p[1])/L if L else 0
        a=0
        while a<L:
            b=min(a+dash[0]*S,L)
            d.line((p[0]+a*k,p[1]+a*l,p[0]+b*k,p[1]+b*l),fill=fill,width=width*S)
            a=b+dash[1]*S

def arrow(d,points,fill=rule,width=2,dash=None):
    line(d,points,fill,width,dash)
    (x1,y1),(x2,y2)=points[-2],points[-1]
    a=atan2(y2-y1,x2-x1)
    L=10;W=5
    d.polygon([(x2*S,y2*S),
        ((x2-L*cos(a)+W*sin(a))*S,(y2-L*sin(a)-W*cos(a))*S),
        ((x2-L*cos(a)-W*sin(a))*S,(y2-L*sin(a)+W*cos(a))*S)],fill=fill)

def save(im,name):
    path=OUT/name
    im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS).save(path,optimize=True)
    print(f"{path}: {path.stat().st_size} bytes")

# --- Intro figure: one source, two responsibilities, design follows the cases
im,d=canvas(1560,708)
txt(d,70,48,"テストケースから、検証方法と設計を決めます",48)
line(d,[(70,120),(1490,120)],ink,2)

# source & spec — straight editorial band with an angled arrow
txt(d,92,172,"仕様・受入条件",39)
txt(d,92,230,"利用者にとって正しい振る舞い",27,muted)
arrow(d,[(508,213),(620,213)],ink,2)
txt(d,660,172,"テストケースと期待結果",39)
txt(d,660,230,"因子・水準・組み合わせを先に確定",27,muted)

# one branch line
line(d,[(1005,280),(1005,323)],rule,2)
line(d,[(340,323),(1192,323)],rule,2)
arrow(d,[(340,323),(340,364)],rule,2)
arrow(d,[(1192,323),(1192,364)],rule,2)

# E2E column and nonE2E column
line(d,[(70,378),(738,378)],ink,2)
line(d,[(816,378),(1490,378)],teal,3)
txt(d,85,397,"E2E",44)
txt(d,831,397,"非E2E",44)
txt(d,85,461,"利用者の一連の操作を確認",31)
txt(d,831,461,"多数の条件を直接検証",31)
txt(d,85,519,"画面 → API → DB",33,muted)
txt(d,831,519,"条件 → 判定 → 結果",33,muted)

# the output only for non-E2E cases requiring a boundary
arrow(d,[(1192,567),(1192,603)],teal,2)
rect(d,816,613,1490,680,teal_pale,None,radius=2)
rect(d,816,613,822,680,teal,None)
txt(d,849,631,"必要なら、判定を独立モジュールにします",30,teal)
save(im,"concept.png")

# --- UML component diagram: one comparison plate
im,d=canvas(1560,905)
txt(d,65,49,"2つの設計案を比較します",49)
txt(d,68,111,"UMLコンポーネント図",27,muted)
line(d,[(66,161),(1494,161)],ink,2)

def comp(d,x,y,w,h,name,detail="",accent=False):
    fill=teal_pale if accent else paper
    stroke=teal if accent else rule
    rect(d,x,y,x+w,y+h,fill,stroke,2,6)
    txt(d,x+24,y+20,"«component»",24,muted)
    txt(d,x+24,y+57,name,32 if name == "TaskRepository" else 35,ink,weight=660)
    if detail:
        txt(d,x+24,y+106,detail,27,muted)

txt(d,68,185,"案A",31,teal)
txt(d,185,184,"権限判定とDB操作を同じ処理に置く",33)
comp(d,73,272,331,151,"権限判定テスト")
comp(d,594,272,408,151,"TaskService","権限判定 + タスク操作")
comp(d,1210,272,295,151,"TaskRepository")
arrow(d,[(404,350),(594,350)],ink,2,dash=(10,7))
arrow(d,[(1002,350),(1210,350)],ink,2,dash=(10,7))
txt(d,427,309,"操作処理を経由",21,muted)
txt(d,1020,309,"データ操作",23,muted)

line(d,[(66,458),(1494,458)],rule,2)
txt(d,68,484,"案B",31,teal)
txt(d,185,483,"権限判定を独立させ、直接テストできるようにする",33)

# layout B test top, policy top; service bottom and repository bottom
comp(d,73,567,331,134,"権限判定テスト")
comp(d,612,553,442,166,"PermissionPolicy","canOperate() を公開",True)
comp(d,73,762,331,125,"TaskService")
comp(d,1210,762,295,125,"TaskRepository")
arrow(d,[(404,630),(612,630)],teal,3,dash=(10,7))
txt(d,435,588,"直接テスト",24,teal)
arrow(d,[(404,822),(547,822),(547,692),(612,692)],ink,2,dash=(9,7))
txt(d,426,742,"判定",23,muted)
arrow(d,[(404,858),(1210,858)],ink,2,dash=(10,7))
txt(d,726,813,"データ操作",23,muted)

save(im,"architecture.png")