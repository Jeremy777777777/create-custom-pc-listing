from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import json, hashlib, shutil, sys, math
from datetime import datetime, timezone
P=Path(__file__).resolve().parent
OUT=P.parent
ROOT=OUT.parents[1]
S=P/'sources';M=P/'masters'
(OUT/'unbranded').mkdir(exist_ok=True)
W=1254; WHITE='#f5f7fc'; MUTED='#b5bfd5'; BLUE='#a9baff'
def js(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n,bold=False): return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
def text(im,xy,s,n=30,c=WHITE,b=False):
    d=ImageDraw.Draw(im);d.multiline_text(xy,s,font=font(n,b),fill=c,spacing=5)
def base(kind='dark'):
    if kind=='studio': return Image.open(S/'b10-studio.png').convert('RGBA')
    if kind=='office':
        im=Image.open(S/'b10-office.png').convert('RGBA'); layer=Image.new('RGBA',im.size)
        d=ImageDraw.Draw(layer)
        for y in range(600): d.line((0,y,W,y),fill=(6,10,22,max(0,200-int(y/3))))
        im.alpha_composite(layer);return im
    if kind=='white':return Image.new('RGBA',(W,W),'white')
    im=Image.new('RGBA',(W,W));d=ImageDraw.Draw(im)
    for y in range(W):
        t=y/W;d.line((0,y,W,y),fill=(int(12+8*t),int(17+9*t),int(30+24*t)))
    glow=Image.new('RGBA',(W,W));g=ImageDraw.Draw(glow);g.ellipse((600,400,1450,1370),fill=(73,62,155,55));glow=glow.filter(ImageFilter.GaussianBlur(90));im.alpha_composite(glow)
    return im
def head(im,k,title,sub=None,dark=True):
    text(im,(64,62),'MEGAPC CUSTOM  /  YOGA SLIM 7x',20,MUTED if dark else '#56627a')
    text(im,(64,139),k.upper(),23,BLUE if dark else '#5860a8',True)
    text(im,(60,186),title,66,WHITE if dark else '#172038')
    if sub:text(im,(64,352),sub,28,MUTED if dark else '#556078')
def save(im,n,pt=True):
    path=OUT/'unbranded'/n if pt else OUT/n
    im.convert('RGB').save(path,quality=96,dpi=(96,96))
def plate(n):
    im=Image.open(S/n).convert('RGBA');return im
def fit(im,size):
    im=im.copy();im.thumbnail(size,Image.Resampling.LANCZOS);return im
def put(im,product,box,shadow=False):
    product=product.crop(product.getchannel('A').getbbox());p=fit(product,(box[2],box[3]));x=box[0]+(box[2]-p.width)//2;y=box[1]+(box[3]-p.height)//2
    if shadow:
        sh=Image.new('RGBA',im.size);ImageDraw.Draw(sh).ellipse((x+40,y+p.height-50,x+p.width-30,y+p.height+35),fill=(0,0,0,120));im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))
    im.alpha_composite(p,(x,y));return [x,y,p.width,p.height]
def abstract(w,h,task=0):
    im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im)
    for y in range(h):d.line((0,y,w,y),fill=(int(13+18*y/h),int(22+14*y/h),int(43+38*y/h)))
    for i in range(5):
        x=int(w*.55+i*w*.035);d.arc((x-w*.1,-h*.3,x+w*.65,h*1.2),90,270,fill=(92+i*15,113+i*13,210+i*8),width=max(3,int(w*.025)))
    # Original abstract task cards; no app identity, realistic data or entitlement.
    for i in range(3):
        x=int(w*.08);y=int(h*(.40+i*.17));d.rounded_rectangle((x,y,int(w*.46),y+int(h*.13)),radius=10,fill=(31+i*3,43+i*4,78+i*8),outline=(81,103,158),width=1)
        d.line((x+18,y+18,int(w*.38),y+18),fill=(181,197,236),width=3)
        d.line((x+18,y+30,int(w*(.28+.04*((task+i)%3))),y+30),fill=(91,119,193),width=3)
    return im
def solve(a,b):
    m=[list(x)+[v] for x,v in zip(a,b)];n=len(b)
    for i in range(n):
        pivot=max(range(i,n),key=lambda r:abs(m[r][i]));m[i],m[pivot]=m[pivot],m[i]
        v=m[i][i];m[i]=[x/v for x in m[i]]
        for r in range(n):
            if r!=i:
                v=m[r][i];m[r]=[x-v*y for x,y in zip(m[r],m[i])]
    return [r[-1] for r in m]
FRONT=[(192,234),(1006,234),(1006,742),(192,742)]
ANGLE=[(121,66),(648,226),(694,692),(167,632)]
def with_screen(name,quad,task=0,mode=None):
    im=plate(name);screen=abstract(900,560,task)
    if task==3 and (S/'oled-art.png').exists():screen=Image.open(S/'oled-art.png').convert('RGBA').resize((900,560),Image.Resampling.LANCZOS)
    target=[(0,0),(899,0),(899,559),(0,559)];a=[];b=[]
    for (x,y),(u,v) in zip(quad,target):
        a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);b.extend([u,v])
    warped=screen.transform(im.size,Image.Transform.PERSPECTIVE,solve(a,b),Image.Resampling.BICUBIC)
    mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(quad,fill=255)
    im.paste(warped,(0,0),mask)
    if mode:
        d=ImageDraw.Draw(im)
        if name=='front.png':
            text(im,(250,275),'Focus. Create. Move.',47,WHITE)
            text(im,(253,342),'YOGA SLIM 7x',24,MUTED)
            asset=plate('windows-11-pro-lockup.png');asset=fit(asset,(300,140));pos=(630,555)
        elif name=='angle.png':
            # Axis-aligned package, never perspective-warped. All corners inside LCD.
            asset=plate('windows-11-pro-package.png');asset=fit(asset,(170,190));pos=(400,360)
        else:
            asset=fit(plate('windows-11-pro-package.png'),(250,278));pos=(1320,760)
        markmask=Image.new('L',im.size);markmask.paste(asset.getchannel('A'),pos)
        assert not ImageChops.subtract(markmask,mask).getbbox(), 'Windows outside actual LCD'
        im.alpha_composite(asset,pos)
    return im,mask
front,fmask=with_screen('front.png',FRONT)
angle,amask=with_screen('angle.png',ANGLE)
front_art,_=with_screen('front.png',FRONT,task=3)
for name,im in [('front-clean.png',front),('angle-clean.png',angle)]:im.save(M/name)
fmask.save(M/'front-lcd-mask.png');amask.save(M/'angle-lcd-mask.png')
# MAIN strict retains complete exact official rendering and original screen.
save(Image.open(S/'Yoga_Slim_7_14Q8X9_CT1_01.png').convert('RGB'),'MAIN-STRICT.jpg',False)
for name,src,q,mode in [('MAIN-ENHANCED-FRONT-CANDIDATE.png','front.png',FRONT,'lockup'),('MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png','angle.png',ANGLE,'package')]:
    if src=='angle.png':
        im,mask=with_screen('Yoga_Slim_7_14Q8X9_CT1_01.png',[(1000,414),(1805,466),(1600,1240),(822,1003)],mode=mode)
        mask.save(M/'enhanced-angle-lcd-mask.png');save(im,name,False)
    else:
        im=base('white');p,mask=with_screen(src,q,mode=mode);put(im,p,(45,85,1164,1084),True);save(im,name,False)
zones={}
# PT01: one overarching purchase narrative; no factual configuration table.
im=base('studio');head(im,'AI Focus Workspace','A clearer space for\nyour next idea.');zones['PT01.png']=put(im,front_art,(60,430,1134,750),True);save(im,'PT01.png')
# PT02: workspace context, no external device or accessory.
im=base('office');head(im,'Make room for focus','Your ideas.\nYour workspace.');zones['PT02.png']=put(im,front,(150,450,954,690),True);save(im,'PT02.png')
# PT03: only complete sold configuration, with one OS identity graphic.
im=base();head(im,'Your base configuration','Built around\nSnapdragon X Elite.');zones['PT03.png']=put(im,front,(60,420,550,650),True)
text(im,(64,1088),'Windows on ARM',29,WHITE,True);text(im,(64,1133),'Check compatibility for specialized apps.',20,MUTED)
specs=[('PROCESSOR','Snapdragon X Elite','X1E-78-100  /  12 cores'),('GRAPHICS','Qualcomm Adreno','Integrated graphics'),('MEMORY','16GB LPDDR5x','Fixed, soldered memory'),('STORAGE','512GB NVMe SSD','PCIe 4.0 x4')]
d=ImageDraw.Draw(im)
for i,(label,value,note) in enumerate(specs):
    y=390+i*152;text(im,(666,y),label,19,BLUE,True);text(im,(666,y+29),value,35,WHITE,True);text(im,(666,y+79),note,23,MUTED);d.line((666,y+126,1180,y+126),fill='#33425f')
osasset=fit(plate('windows-11-pro-lockup.png'),(310,140));im.alpha_composite(osasset,(666,1021));save(im,'PT03.png')
# PT04: display and form, unique factual ownership.
im=base();head(im,'See more in every detail','OLED brilliance.\nA lighter footprint.')
for x,a,b in [(64,'14.5"  3K OLED','2944 x 1840  /  Touch'),(465,'90Hz','Smooth display refresh'),(850,'12.9mm','Thin aluminum chassis')]:
    text(im,(x,390),a,35,WHITE,True);text(im,(x,444),b,23,MUTED)
zones['PT04.png']=put(im,front_art,(82,535,1090,650),True);save(im,'PT04.png')
# PT05: original generic task flow, no software bundle or duplicate capacity.
im=base();head(im,'From thought to finished','Keep your creative\nflow in view.')
flow=[('01','ORGANIZE','Give each idea a place.'),('02','CREATE','Move the work forward.'),('03','REVIEW','Bring the details together.')]
for i,(num,title,note) in enumerate(flow):
    x=64+i*400;ImageDraw.Draw(im).rounded_rectangle((x,410,x+370,584),radius=20,fill='#202b45',outline='#3b4c76');text(im,(x+22,430),num,22,BLUE,True);text(im,(x+22,473),title,28,WHITE,True);text(im,(x+22,526),note,21,MUTED)
zones['PT05.png']=put(im,angle,(225,610,805,580),True);save(im,'PT05.png')
# PT06: genuine OEM keyboard crop and touchpad, kept on white.
im=base('white');head(im,'Made for the hands-on work','A comfortable place\nto start.',dark=False)
text(im,(64,392),'Backlit US keyboard',32,'#172038',True);text(im,(64,444),'Clear layout. Familiar controls.',24,'#556078')
text(im,(700,392),'Glass precision touchpad',32,'#172038',True);text(im,(700,444),'A spacious 80 x 135mm surface.',24,'#556078')
keyboard=plate('keyboard.png').crop((160,451,1041,1050));zones['PT06.png']=put(im,keyboard,(110,550,1034,640));save(im,'PT06.png')
# PT07: remaining verified privacy/collaboration capability.
im=base();head(im,'A more personal sign-in','Face the day.\nKeep privacy close.')
for x,a,b in [(64,'FHD + IR','1080p camera'),(470,'Windows Hello','Facial sign-in'),(880,'E-shutter','Camera privacy control')]:
    text(im,(x,390),a,34,WHITE,True);text(im,(x,442),b,23,MUTED)
zones['PT07.png']=put(im,front,(130,545,994,650),True);save(im,'PT07.png')
# PT08: exact body-edge crops of both official sides; labels end at real holes.
im=base();head(im,'Connections, kept simple','Three USB4 ports.\nOne versatile standard.')
text(im,(64,367),'USB-C  /  Up to 40Gbps  /  USB PD 3.1  /  DisplayPort 1.4',27,MUTED)
left=plate('left.png').crop((50,1050,1150,1160));right=plate('right.png').crop((50,1050,1150,1160))
im.alpha_composite(left,(77,482));im.alpha_composite(right,(77,818))
d=ImageDraw.Draw(im)
text(im,(77,437),'LEFT SIDE',22,BLUE,True);text(im,(77,773),'RIGHT SIDE',22,BLUE,True)
for x in [250,341]:
    d.line((x,531,x,640),fill=BLUE,width=3);d.ellipse((x-5,526,x+5,536),fill=BLUE)
d.line((250,640,341,640),fill=BLUE,width=3);text(im,(77,663),'2 x USB-C USB4',33,WHITE,True)
d.line((1004,867,1004,976,885,976),fill=BLUE,width=3);d.ellipse((999,862,1009,872),fill=BLUE);text(im,(725,999),'1 x USB-C USB4',33,WHITE,True)
d.line((64,1091,1190,1091),fill='#3b4c76',width=2);text(im,(64,1130),'Wi-Fi 7',35,WHITE,True);text(im,(660,1130),'Bluetooth 5.4',35,WHITE,True)
zones['PT08.png']=[77,482,1100,110]
save(im,'PT08.png')
