"""Frozen OEM layers + original generated art + deterministic typography.
Run with the project listing-testing Python 3.12 interpreter.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, PngImagePlugin
import math,json,hashlib,sys

P=Path(__file__).resolve().parent
ROOT=P.parents[1]
REPO=ROOT/'tmp/listing-VL1121-production'
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else REPO/'product generated photo/VL-1121'
S=P/'source-assets'; L=P/'layers'; L.mkdir(exist_ok=True)
OUT.mkdir(parents=True,exist_ok=True); (OUT/'unbranded').mkdir(exist_ok=True)
CY=(114,232,249); LIME=(201,255,43); WHITE=(245,248,250); MUTED=(168,186,198); INK=(13,20,25)
FONT='C:/Windows/Fonts/bahnschrift.ttf'; BODY='C:/Windows/Fonts/segoeui.ttf'
R=Image.Resampling.LANCZOS
placements={}; geometry={}; text_bounds=[]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def font(n,bold=True):return ImageFont.truetype(FONT if bold else BODY,round(n))
def txt(im,x,y,t,n=32,color=WHITE,maxw=None,bold=True):
 d=ImageDraw.Draw(im);f=font(n,bold)
 if maxw:
  while d.textbbox((0,0),t,font=f)[2]>maxw and n>12:n-=1;f=font(n,bold)
 d.text((int(x),int(y)),t,font=f,fill=color,stroke_width=0)
 b=d.textbbox((x,y),t,font=f);text_bounds.append({'text':t,'bbox':b,'fontSize':n})
 return b
def lines(im,x,y,ss,n=32,color=WHITE,gap=8,maxw=None):
 for t in ss:txt(im,x,y,t,n,color,maxw);y+=n+gap
def rect(im,b,fill,outline=None,width=1,radius=0):
 d=ImageDraw.Draw(im);d.rounded_rectangle(b,radius=radius,fill=fill,outline=outline,width=width)
def fit(im,w,h,up=False):
 q=min(w/im.width,h/im.height,1 if not up else 100);return im.resize((round(im.width*q),round(im.height*q)),R)
def icon(kind,size=100,color=CY):
 im=Image.new('RGBA',(size,size));d=ImageDraw.Draw(im);a=size/100
 def b(v):return tuple(round(x*a) for x in v)
 def line(v):d.line(b(v),fill=color,width=max(2,round(3*a)))
 if kind=='display':
  d.rounded_rectangle(b((8,17,92,72)),radius=4*a,outline=color,width=max(2,round(3*a)))
  line((6,79,94,79));line((8,81,92,81));line((16,65,85,25));line((78,25,85,25,85,32))
 elif kind=='ram':
  d.rectangle(b((5,28,95,65)),outline=color,width=max(2,round(3*a)))
  for x in [14,34,54,74]:d.rectangle(b((x,36,x+12,55)),outline=color,width=max(1,round(2*a)))
  for x in range(10,90,8):line((x,67,x,74))
 elif kind=='ssd':
  d.rounded_rectangle(b((27,8,73,89)),radius=6*a,outline=color,width=max(2,round(3*a)))
  for y in [26,49]:d.rectangle(b((37,y,63,y+15)),outline=color,width=max(1,round(2*a)))
  line((36,84,64,84));d.ellipse(b((46,15,53,22)),fill=color)
 elif kind in ('cpu','gpu'):
  asset=Image.open(S/(kind+'.png')).convert('RGBA');asset=asset.crop(asset.getchannel('A').getbbox());asset=fit(asset,size,size);im.alpha_composite(asset,((size-asset.width)//2,(size-asset.height)//2))
 elif kind=='flow':
  for x in [15,50,85]:d.ellipse(b((x-8,40,x+8,56)),outline=color,width=3)
  line((24,48,40,48));line((60,48,76,48))
 return im
def save(im,path):
 im=im.convert('RGB');im.save(path,quality=96,subsampling=0,dpi=(96,96))
def load(name):return Image.open(S/name).convert('RGBA')
def solve(A,b):
 m=[list(map(float,a))+[float(c)] for a,c in zip(A,b)]
 for col in range(len(m)):
  i=max(range(col,len(m)),key=lambda k:abs(m[k][col]));m[col],m[i]=m[i],m[col]
  s=m[col][col];m[col]=[v/s for v in m[col]]
  for k in range(len(m)):
   if k!=col:
    f=m[k][col];m[k]=[x-f*y for x,y in zip(m[k],m[col])]
 return [r[-1] for r in m]
def warp(src,corners,size):
 dest=[(0,0),(src.width-1,0),(src.width-1,src.height-1),(0,src.height-1)];A=[];b=[]
 for (x,y),(u,v) in zip(corners,dest):
  A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);b.extend([u,v])
 coeff=solve(A,b);return src.transform(size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)

# Exact-model front and sourced ordinary-touchpad angle; no generated hardware.
FRONT=[(388,419),(1609,419),(1609,1181),(388,1181)]
ANGLE=[(405,200),(942,219),(872,611),(336,549)]
def product(name,screen=None):
 im=load(name)
 if screen is not None:
  poly=FRONT if name=='exact-pr-official.png' else ANGLE
  mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
  warped=warp(screen.convert('RGBA'),poly,im.size);im.paste(warped,(0,0),mask)
 bbox=im.getchannel('A').getbbox();return im.crop(bbox),bbox

scene=Image.open(P/'screen-G07.png').convert('RGBA')
win=Image.open(S/'windows-11-pro-package.png').convert('RGBA')
win=win.crop(win.getchannel('A').getbbox())
def screen_cards(ram='16GB',angle=False):
 im=scene.resize((1220,762),R)
 d=ImageDraw.Draw(im)
 data=[('display','16-inch','165Hz'),('cpu','Ryzen 9','8940HX'),('gpu','RTX 5070 Ti','Laptop GPU'),('ram',ram,'DDR5'),('ssd','1TB','NVMe SSD'),('os','','')]
 if angle:data=[('display','16-inch','165Hz'),('cpu','Ryzen 9','8940HX'),('gpu','RTX','5070 Ti'),('ram',ram,'DDR5'),('ssd','1TB','SSD'),('os','','')]
 # Two side rails preserve the central crystal, C02 / A07.
 for j,(kind,a,b) in enumerate(data):
  x=30 if j<3 else 864;y=24+(j%3)*244;w=326;h=224
  rect(im,(x,y,x+w,y+h),(10,20,27,232),(82,146,162,255),2,12)
  d.line((x+16,y+2,x+85,y+2),fill=LIME,width=5)
  if kind=='os':
   mark=fit(win,170,194);im.alpha_composite(mark,(x+(w-mark.width)//2,y+(h-mark.height)//2))
  else:
   ico=icon(kind,50 if angle else 70);im.alpha_composite(ico,(x+16,y+22))
   txt(im,x+(83 if angle else 101),y+31,a,64 if angle else 43,CY if kind=='display' else WHITE,maxw=225 if angle else 210)
   txt(im,x+22,y+125 if angle else y+135,b,65 if angle else 49,WHITE,maxw=284)
  im.crop((x,y,x+w,y+h)).save(L/(f'card-{kind}-{ram}'+('-angle' if angle else '')+'.png'))
 im.save(L/(f'screen-cards-{ram}'+('-angle' if angle else '')+'.png'));return im

front,bf=product('exact-pr-official.png')
front.save(L/'front-original.rgba.png')
angle,ba=product('store-input.png');angle.save(L/'angle-original.rgba.png')
def paste_product(canvas,layer,x,y,width=None,shadow=True):
 if width:layer=fit(layer,width,9999)
 if shadow:
  sh=Image.new('RGBA',canvas.size);sd=ImageDraw.Draw(sh)
  sd.ellipse((x+layer.width*.08,y+layer.height*.94,x+layer.width*.92,y+layer.height*1.035),fill=(0,0,0,65));sh=sh.filter(ImageFilter.GaussianBlur(14));canvas.alpha_composite(sh)
 canvas.alpha_composite(layer,(int(x),int(y)))
 return {'x':int(x),'y':int(y),'width':layer.width,'height':layer.height,'label':'PRODUCT_SILHOUETTE'}

def main():
 # Long side follows actual sufficiently detailed source, without fixed square upscaling.
 c=Image.new('RGBA',(1664,1320),'white');bbox=paste_product(c,front,17,35,shadow=True);save(c,OUT/'MAIN-STRICT.jpg')
 f,b=product('exact-pr-official.png',screen_cards());f.save(L/'front-enhanced.rgba.png')
 c=Image.new('RGBA',(1664,1320),'white');paste_product(c,f,17,35);save(c,OUT/'MAIN-ENHANCED-FRONT-CANDIDATE.png')
 fm=Image.new('L',c.size);ImageDraw.Draw(fm).polygon([(x-b[0]+17,y-b[1]+35) for x,y in FRONT],fill=255);fm.save(L/'front-lcd-mask.png')
 # The screen scene/card layer is perspective mapped; Windows remains planar and proportional.
 art=screen_cards(angle=True);art_no_os=art.copy();art_no_os.paste(scene.resize((1220,762),R).crop((864,512,1190,736)),(864,512))
 rect(art_no_os,(864,512,1190,736),(10,20,27,232),(82,146,162,255),2,12)
 a,b=product('store-input.png',art_no_os);a.save(L/'angle-screen.rgba.png')
 c=Image.new('RGBA',(1000,760),'white');box=paste_product(c,a,49,70,shadow=True)
 # Once, wholly within real LCD; independently measured safe zone.
 mark=fit(win,80,88);wx,wy=782,371;c.alpha_composite(mark,(wx,wy))
 save(c,OUT/'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png')
 am=Image.new('L',c.size);ImageDraw.Draw(am).polygon([(x-b[0]+49,y-b[1]+70) for x,y in ANGLE],fill=255);am.save(L/'angle-lcd-mask.png')
 geometry['MAIN-STRICT.jpg']={'product':bbox,'canvas':[1664,1320],'upscaled':False}
 geometry['MAIN-ENHANCED-FRONT-CANDIDATE.png']={'product':bbox,'canvas':[1664,1320],'lcdMask':'front-lcd-mask.png','sixCategories':['DISPLAY','CPU','GPU','RAM','SSD','OS'],'windowsMode':'PACKAGE','boundary':'SCREEN_ONLY'}
 geometry['MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png']={'product':box,'canvas':[1000,760],'lcdMask':'angle-lcd-mask.png','windowsBox':[wx,wy,mark.width,mark.height],'sixCategories':['DISPLAY','CPU','GPU','RAM','SSD','OS'],'windowsMode':'PACKAGE','boundary':'SCREEN_ONLY'}

def base(slot,headline,sub=None,light=False):
 c=Image.new('RGBA',(1200,1200),(249,250,251) if light else INK);d=ImageDraw.Draw(c)
 if not light:
  # Subtle editorial measurement grid, not product or performance claims.
  for x in range(40,1200,80):d.line((x,0,x,1200),fill=(22,34,42),width=1)
  for y in range(40,1200,80):d.line((0,y,1200,y),fill=(22,34,42),width=1)
  d.line((58,225,1142,225),fill=(51,84,94),width=1)
 txt(c,60,44,'MEGAPC CUSTOM  /  ROG STRIX G16',20,(74,98,110) if light else MUTED,maxw=800)
 txt(c,60,98,headline,64,INK if light else WHITE,maxw=1050)
 if sub:txt(c,60,182,sub,26,(73,91,103) if light else MUTED,maxw=1060)
 d.rectangle((60,80,112,84),fill=CY)
 txt(c,60,1146,slot+'  /  VL-1121',18,(98,114,125) if light else MUTED)
 # The natural OEM wordmark space is at bottom-right, outside all product/copy.
 return c
def finish(c,slot,zones,light=False):
 path=OUT/'unbranded'/f'{slot}.png';save(c,path)
 logo=Image.open(S/'asus-logo.png').convert('RGBA');bb=logo.getchannel('A').getbbox();ar=(bb[2]-bb[0])/(bb[3]-bb[1]);w=132;h=round(w/ar)
 # Black original mark uses light native negative-space footer; no visible logo sticker.
 d=ImageDraw.Draw(c); # Footer already white for all PT canvases.
 placements[f'{slot}.png']={'x':1008,'y':1120,'width':w,'height':h,'style':'transparent','protectedZones':zones+[{'label':'COPY_FOOTER','x':60,'y':1135,'width':500,'height':35}]}
 geometry[f'{slot}.png']={'canvas':[1200,1200],'productZones':zones,'upscaled':False}

def footer(c):
 ImageDraw.Draw(c).rectangle((0,1080,1200,1200),fill=(248,250,251))
def gallery():
 clean,_=product('exact-pr-official.png',scene)
 angleclean,_=product('store-input.png',scene)
 clean.save(L/'front-scene.rgba.png');angleclean.save(L/'angle-scene.rgba.png')
 # PT01: purchase reason; no full specifications or Windows asset.
 c=base('PT01','GAMING POWER. STRIX STYLE.','Performance-focused design, customized by MegaPC.')
 bb=paste_product(c,clean,125,237,950)
 rect(c,(60,965,1140,1038),(22,36,44),outline=(51,99,112),radius=8)
 txt(c,86,982,'ECLIPSE GRAY  /  AURA SYNC LIGHT BAR',34,CY)
 footer(c);finish(c,'PT01',[bb,{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':190},{'label':'BENEFIT','x':60,'y':965,'width':1080,'height':73}])
 # PT02: real computer on original synthetic bare desk, no peripheral props.
 c=Image.open(P/'room-GG07.png').convert('RGBA').resize((1200,1200),R)
 shade=Image.new('RGBA',c.size);ImageDraw.Draw(shade).rectangle((0,0,1200,295),fill=(6,12,17,192));c.alpha_composite(shade)
 txt(c,60,48,'MEGAPC CUSTOM  /  ROG STRIX G16',20,MUTED)
 lines(c,60,105,['YOUR GAME.','YOUR SPACE.'],66,WHITE,3)
 txt(c,60,268,'A focused setup for immersive laptop gaming.',29,CY)
 bb=paste_product(c,angleclean,150,350,900)
 footer(c);finish(c,'PT02',[bb,{'label':'HEADLINE','x':60,'y':48,'width':1080,'height':270}])
 # PT03: sole full base configuration.
 c=base('PT03','THE POWER INSIDE','Your 16GB / 1TB base configuration.')
 bb=paste_product(c,clean,60,390,630)
 data=[('cpu','AMD RYZEN 9','8940HX','16 cores / 32 threads'),('gpu','NVIDIA GEFORCE','RTX 5070 Ti','12GB GDDR7 Laptop GPU'),('ram','MEMORY','16GB DDR5','Installed memory'),('ssd','STORAGE','1TB SSD','PCIe 4.0 NVMe'),('os','OPERATING SYSTEM','Windows 11 Pro','Seller-delivered OS')]
 for i,(kind,a,b,detail) in enumerate(data):
  x=738;y=275+i*151
  rect(c,(x,y,1140,y+135),(21,35,44),(48,83,96),1,10)
  if kind!='os':c.alpha_composite(icon(kind,54),(x+16,y+40))
  txt(c,x+86,y+15,a,18,MUTED,maxw=296);txt(c,x+86,y+44,b,33,WHITE,maxw=296);txt(c,x+86,y+92,detail,19,CY,maxw=296)
 txt(c,64,940,'Created using ASUS ROG Strix G16 G614',23,MUTED,maxw=635)
 footer(c);finish(c,'PT03',[bb,{'label':'SPECIFICATIONS','x':738,'y':275,'width':402,'height':740},{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':190}])
 # PT04: display/form; display panel evidence from exact configuration family.
 c=base('PT04','MORE ROOM TO PLAY','A 16:10 canvas for games and everyday multitasking.')
 bb=paste_product(c,clean,190,285,820)
 for x,value,label in [(62,'16-inch','WUXGA DISPLAY'),(438,'165Hz','REFRESH RATE'),(814,'100%','sRGB COLOR')]:
  txt(c,x,927,value,63,CY,maxw=320);txt(c,x,1000,label,22,MUTED)
 txt(c,60,241,'1920 x 1200  /  IPS-level  /  Anti-glare',29,WHITE)
 footer(c);finish(c,'PT04',[bb,{'label':'DISPLAY_FACTS','x':60,'y':927,'width':1080,'height':112},{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':240}])
 # PT05: practical relationships, no repeated numeric table.
 c=base('PT05','FROM PLAY TO PROJECT','Hardware that works together across demanding tasks.')
 task=Image.new('RGBA',(1220,762),(9,18,24));td=ImageDraw.Draw(task)
 rect(task,(35,35,1185,550),(14,29,38),(58,119,138),2,12)
 for step in range(0,12):
  x=370+step*36;td.line((x,120,x+230,450),fill=(72,184,202),width=2)
  td.line((390,120+step*28,920,120+step*28),fill=(38,95,113),width=2)
 td.polygon([(440,315),(660,130),(865,330),(663,470)],outline=CY,width=5)
 td.line((440,315,663,470,660,130,865,330,440,315),fill=CY,width=4)
 for j in range(4):
  y=585+j*36;td.line((65,y,1155,y),fill=(39,65,78),width=2)
  td.rounded_rectangle((180+j*90,y-10,600+j*110,y+9),radius=5,fill=CY if j%2==0 else (96,130,146))
 task.save(L/'task-viewport.png');task_product,_=product('store-input.png',task)
 bb=paste_product(c,task_product,200,325,800)
 labels=[('01','GAME','CPU + GPU','Run game logic and render your world.'),('02','CREATE','GPU + MEMORY','Build scenes and work across applications.'),('03','KEEP MOVING','SSD + MEMORY','Load projects and switch between tasks.')]
 for i,(n,title,rel,detail) in enumerate(labels):
  x=60+i*365;rect(c,(x,924,x+345,1043),(23,38,46),(51,88,102),1,10)
  txt(c,x+16,936,n,18,LIME);txt(c,x+57,930,title,27,WHITE);txt(c,x+16,972,rel,19,CY);txt(c,x+16,1004,detail,17,MUTED,maxw=313)
 footer(c);finish(c,'PT05',[bb,{'label':'TASK_FLOW','x':60,'y':924,'width':1075,'height':119},{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':190}])
 # PT06: source-native keyboard/touchpad detail, no guessed or relabelled keys.
 c=base('PT06','CONTROL AT YOUR FINGERTIPS','Backlit keyboard, dedicated hotkeys and a spacious touchpad.',light=True)
 k=load('store-angle.png');crop=k.crop((130,382,872,887));crop.save(L/'input-detail-original.rgba.png')
 bb=paste_product(c,crop,229,357,742,shadow=False)
 d=ImageDraw.Draw(c)
 for pts in [[(420,398),(140,398),(140,320)],[(718,817),(1040,817),(1040,920)],[(487,426),(487,289)]]:d.line(pts,fill=(73,135,154),width=2);d.ellipse((pts[0][0]-4,pts[0][1]-4,pts[0][0]+4,pts[0][1]+4),fill=(73,135,154))
 txt(c,62,282,'DEDICATED HOTKEYS',23,INK,maxw=350);txt(c,797,931,'MULTITOUCH TOUCHPAD',22,INK,maxw=340)
 txt(c,528,274,'4-ZONE RGB BACKLIT KEYBOARD',23,INK,maxw=600)
 footer(c);finish(c,'PT06',[bb,{'label':'INPUT_LABELS_TOP','x':60,'y':270,'width':1080,'height':63},{'label':'INPUT_LABELS_BOTTOM','x':795,'y':920,'width':345,'height':45},{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':190}],True)
 # PT07: one unique verified remaining capability; real exhaust view.
 c=base('PT07','ENGINEERED FOR AIRFLOW','ROG Intelligent Cooling supports demanding gaming sessions.')
 rear=load('rear.png');rear=rear.crop(rear.getchannel('A').getbbox())
 bb=paste_product(c,rear,165,285,870,shadow=False)
 rect(c,(60,948,1140,1039),(23,38,46),(51,88,102),1,10)
 txt(c,86,968,'PURPOSEFUL VENTILATION. PERFORMANCE IN FOCUS.',31,CY,maxw=1020)
 footer(c);finish(c,'PT07',[bb,{'label':'COOLING_CLAIM','x':60,'y':948,'width':1080,'height':91},{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':190}])
 # PT08: actual connector openings; two real sides, never conceptual network.
 c=base('PT08','CONNECT WITH CONFIDENCE','Physical ports on both sides. Wireless built in.')
 d=ImageDraw.Draw(c);zones=[]
 for name,y in [('ports-left.png',378),('ports-right.png',776)]:
  im=load(name);b=im.getchannel('A').getbbox();im=im.crop(b);zones.append(paste_product(c,im,60,y,1080,shadow=False))
 txt(c,60,280,'LEFT SIDE',22,LIME);txt(c,60,680,'RIGHT SIDE',22,LIME)
 # Source opening centers within alpha crop, scaled by actual width.
 q=1080/1318
 left=[('DC power',538,75,60,327),('RJ45 LAN',655,75,236,327),('HDMI',755,75,450,327),('2x USB4 Type-C',854,70,660,327),('3.5mm audio',1000,70,937,327)]
 for label,px,py,tx,ty in left:
  ex=60+px*q;ey=378+py*q;d.line((ex,ey,tx+70,ty+33),fill=CY,width=2);d.ellipse((ex-4,ey-4,ex+4,ey+4),fill=CY);txt(c,tx,ty,label,22,WHITE,maxw=210)
 ex=60+932*q;ey=378+70*q;d.line((ex,ey,730,360),fill=CY,width=2);d.ellipse((ex-4,ey-4,ex+4,ey+4),fill=CY)
 txt(c,60,565,'USB4: up to 40Gbps; DisplayPort on both USB-C ports.',24,MUTED,maxw=1080)
 txt(c,60,602,'Power Delivery supported on one USB-C port.',24,MUTED,maxw=1080)
 for px,tx in [(531,375),(662,690)]:
  ex=60+px*q;ey=776+73*q;d.line((ex,ey,ex,745,tx+40,745),fill=CY,width=2);d.ellipse((ex-4,ey-4,ex+4,ey+4),fill=CY)
 txt(c,375,711,'2x USB-A  /  USB 3.2 Gen 2',27,WHITE,maxw=650)
 txt(c,60,993,'Wi-Fi 6E   +   Bluetooth',36,CY)
 footer(c);finish(c,'PT08',zones+[{'label':'PORT_LABELS','x':60,'y':280,'width':1080,'height':70},{'label':'CONNECTIVITY_COPY','x':60,'y':560,'width':1080,'height':75},{'label':'USB_LABELS','x':375,'y':680,'width':650,'height':65},{'label':'WIRELESS','x':60,'y':990,'width':800,'height':50},{'label':'HEADLINE','x':60,'y':44,'width':1080,'height':190}])

if __name__=='__main__':
 main();gallery()
 plan={'schemaVersion':3,'brand':'ASUS','logoRole':'OEM base-product identifier','logoAssetSourceUrl':'https://www.asus.com/media/img/2017/images/n-logo-asus.svg','logoVisibilityMode':'ASPECT_RATIO_WORDMARK','minimumClearancePx':32,'minimumComponentSeparationPx':32,'thumbnailReviewSizePx':200,'placements':placements}
 write(OUT/'logo-placement.json',plan)
 write(P/'geometry.json',geometry)
 write(P/'text-bounds.json',text_bounds)
 used=['exact-pr-official.png','store-input.png','store-angle.png','ports-left.png','ports-right.png','rear.png','asus-logo.png','cpu.png','gpu.png','windows-11-pro-package.png']
 recipe={'schemaVersion':1,'version':'vl1121-g07-c02-a07-v1','formFactor':'LAPTOP','boundaryMode':'SCREEN_ONLY','configurationCardCategories':['DISPLAY','CPU','GPU','RAM','SSD','OS'],'styleApprovalQuote':'可以','soldConfigurationApprovalQuote':'可以','productLayerMethod':'ORIGINAL_PHOTO','sourceFront':'source-assets/exact-pr-official.png','sourceAngle':'source-assets/store-input.png','frontLcdCorners':FRONT,'angleLcdCorners':ANGLE,'font':FONT,'fontSha256':sha(FONT),'scriptSha256':sha(__file__),'assets':{str(p.relative_to(P)):sha(p) for p in [S/n for n in used]+[P/'screen-G07.png',P/'room-GG07.png']},'geometryRecord':'geometry.json','deterministicRender':'python -X utf8 production-pack/render_gallery.py <product-directory>','generatedHardware':False}
 write(P/'recipe.json',recipe)
 print('Rendered 3 MAIN and 8 unbranded PT masters; final OEM composition and actual visual review pending.')
