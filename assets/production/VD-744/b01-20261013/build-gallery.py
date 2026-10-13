"""Deterministic composition from exact official product layers, approved fixed brand assets and an AI scene background. No generated hardware."""
import json,hashlib,math,shutil
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
OUT=Path(__file__).resolve().parent
REPO=next((p for p in OUT.parents if (p/'SKILL.md').exists() and (p/'scripts/gallery_engine.py').exists()),OUT.parents[1]/'tmp/listing-20744-20261013')
DEST=REPO/'product generated photo/VD-744'
PACK=REPO/'assets/production/VD-744/b01-20261013'
PACK.mkdir(parents=True,exist_ok=True)
(DEST/'unbranded').mkdir(parents=True,exist_ok=True)
for f in (OUT/'source-assets').glob('*.png'):
 if f.resolve()!=(PACK/f.name).resolve():shutil.copy2(f,PACK/f.name)
generated=Path('C:/Users/jerem/.codex/generated_images/01a136b6-3514-7821-b183-c701bb3907eb')
if not (PACK/'office-background.png').exists():shutil.copy2(generated/'exec-c7adbc64-251f-4da3-a457-cdc95d1049f6.png',PACK/'office-background.png')
if not (PACK/'approved-style-preview.png').exists():shutil.copy2(generated/'exec-7efcdfe1-e15e-49a5-972f-6b181568bdc1.png',PACK/'approved-style-preview.png')
FONT=Path('C:/Windows/Fonts/arial.ttf'); BOLD=Path('C:/Windows/Fonts/arialbd.ttf')
NAVY='#10243A'; BLUE='#246DDB'; INK='#172C43'; GRAY='#526174'; LIGHT='#EDF3F9'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):Path(p).write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
def font(n,bold=False):return ImageFont.truetype(str(BOLD if bold else FONT),n)
def photo(name):
 im=Image.open(PACK/name).convert('RGBA');return im.crop(im.getchannel('A').getbbox())
angle=photo('dell-qcm1250-angle.png');left=photo('dell-qcm1250-left.png');front=photo('dell-qcm1250-front-native.png');rear=photo('dell-qcm1250-rear.png')
package=Image.open(REPO/'assets/branding/windows-11-pro-package.png').convert('RGBA')
lockup=Image.open(REPO/'assets/branding/windows-11-pro-lockup.png').convert('RGBA')
layout={}; facts={}; logo={}
def blank(s=1600):return Image.new('RGBA',(s,s),'white')
def text(im,xy,lines,size=52,color=INK,bold=False,leading=1.18):
 d=ImageDraw.Draw(im);x,y=xy
 for line in lines.split('\n'):
  d.text((x,y),line,font=font(size,bold),fill=color,stroke_width=0)
  y+=round(size*leading)
 return {'label':'TEXT','x':x,'y':xy[1],'width':math.ceil(max((d.textlength(t,font=font(size,bold)) for t in lines.split('\n')),default=0)),'height':round(y-xy[1])}
def rect(im,box,fill,r=0,outline=None,width=1):
 d=ImageDraw.Draw(im)
 if r:d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
 else:d.rectangle(box,fill=fill,outline=outline,width=width)
def product(im,p,xy,wh,label='PRODUCT_SILHOUETTE'):
 scale=min(wh[0]/p.width,wh[1]/p.height)
 assert scale<=1.0001,('Source detail cannot be upscaled',p.size,wh)
 q=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS)
 im.alpha_composite(q,xy)
 return {'label':label,'x':xy[0],'y':xy[1],'width':q.width,'height':q.height,'sourceSize':list(p.size),'scale':scale}
def asset(im,p,xy,wh):
 scale=min(wh[0]/p.width,wh[1]/p.height);q=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS);im.alpha_composite(q,xy)
 return {'x':xy[0],'y':xy[1],'width':q.width,'height':q.height}
def shadow(im,box):
 layer=Image.new('RGBA',im.size);ImageDraw.Draw(layer).ellipse(box,fill=(10,20,30,55));im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(22)))
def grid(im,box):
 x0,y0,x1,y1=box;rect(im,box,NAVY)
 d=ImageDraw.Draw(im)
 for i in range(7):
  x=x0+i*70;d.line((x,y0,x,y1),fill='#17334F',width=2)
 for y in range(y0,y1,110):d.line((x0,y,x1,y),fill='#17334F',width=2)
def header(im,kicker,title,s=1600):
 zones=[text(im,(70,65),kicker.upper(),25,BLUE,True),text(im,(70,125),title,60 if s==1600 else 49,INK,True)]
 ImageDraw.Draw(im).line((70,255 if s==1600 else 235,s-70,255 if s==1600 else 235),fill='#BDD0E4',width=2)
 return zones
def save(im,name,zones,ids,main=False):
 s=im.width
 rgb=im.convert('RGB')
 file=DEST/name if main else DEST/'unbranded'/name
 rgb.save(file,quality=96,subsampling=0) if name.endswith('.jpg') else rgb.save(file)
 layout[name]={'canvas':[s,s],'protectedZones':[{k:v for k,v in z.items() if k in ('label','x','y','width','height')} for z in zones],'productLayers':[z for z in zones if z['label'].startswith('PRODUCT_SILHOUETTE')]}
 facts[name]=ids
 if not main:
  edge=round(s*.11);logo[name]={'x':s-round(s*.045)-edge,'y':round(s*.045),'width':edge,'height':round(edge*249/250),'style':'transparent','protectedZones':layout[name]['protectedZones']}

# MAIN: pure white product-only choice plus two independently fitted safe zones.
im=blank();shadow(im,(410,1430,1190,1510));z=product(im,angle,(316,80),(1000,1420));save(im,'MAIN-STRICT.jpg',[z],[],True)
im=blank(1000);shadow(im,(110,910,410,955));z=product(im,front,(120,55),(280,880));grid(im,(470,200,940,810));tz=[]
tz.append(text(im,(505,240),'Compact office\ncomputing',41,'white',True));tz.append(text(im,(505,365),'Core Ultra 7 265T',30,'white'));tz.append(text(im,(505,420),'16GB DDR5 RAM\n256GB SSD',29,'white'))
win=asset(im,package,(640,545),(170,200));layout['enhancedFrontWindows']=win
save(im,'MAIN-ENHANCED-FRONT-CANDIDATE.png',[z]+tz,['base.cpu','base.ram','base.ssd','base.os'],True)
im=blank();shadow(im,(130,1430,950,1515));z=product(im,angle,(70,90),(1000,1420));grid(im,(1090,310,1530,1270));tz=[]
tz.append(text(im,(1130,355),'Workday\nready',58,'white',True));tz.append(text(im,(1130,530),'Core Ultra 7\n265T',41,'white'));tz.append(text(im,(1130,690),'16GB DDR5\n256GB SSD',37,'white'));win=asset(im,package,(1180,900),(230,260));layout['enhancedAngleWindows']=win
save(im,'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png',[z]+tz,['base.cpu','base.ram','base.ssd','base.os'],True)

# PT01: a purchase narrative, distinct from the configuration and dimension pages.
im=blank();zones=header(im,'Dell Pro Micro QCM1250','A focused look for your workspace')
rect(im,(70,330,800,1510),LIGHT,26);shadow(im,(190,1370,880,1450));zones.append(product(im,left,(120,360),(800,1100)))
zones.append(text(im,(930,495),'Black. Clean.\nUnderstated.',69,INK,True));zones.append(text(im,(930,740),'A restrained exterior\nfor professional spaces.',39,GRAY));zones.append(text(im,(930,1170),'MegaPC Custom\nCreated Using Dell Pro Micro',28,BLUE))
save(im,'PT01.png',zones,['appearance.black','appearance.restrained'])

# PT02: original empty office scene, exact product composite, no extra equipment.
im=ImageOps.fit(Image.open(PACK/'office-background.png').convert('RGBA'),(1200,1200),method=Image.Resampling.LANCZOS)
zones=header(im,'Office use','A place for everyday work',1200);shadow(im,(300,1000,850,1070));zones.append(product(im,angle,(350,340),(600,700)))
save(im,'PT02.png',zones,['use.officeScene'])

# PT03: sole full base configuration; fixed OS lockup is placed once.
im=blank();zones=header(im,'Base configuration','The essentials, precisely specified')
rect(im,(70,330,540,1510),LIGHT,24);zones.append(product(im,front,(170,480),(300,900)))
items=[('PROCESSOR','Intel Core Ultra 7 265T','20 cores · up to 5.3 GHz'),('GRAPHICS','Intel Graphics','Integrated graphics'),('MEMORY','16GB DDR5 RAM','Installed base memory'),('STORAGE','256GB SSD','Installed internal storage')]
for i,(k,v,sub) in enumerate(items):
 y=355+i*235;rect(im,(620,y,1520,y+205),'#F5F8FC',18);zones.append(text(im,(655,y+23),k,23,BLUE,True));zones.append(text(im,(655,y+62),v,46,INK,True));zones.append(text(im,(655,y+125),sub,31,GRAY))
zones.append(text(im,(655,1340),'OPERATING SYSTEM',23,BLUE,True));win=asset(im,lockup,(1020,1310),(450,200));zones.append({'label':'WINDOWS_IDENTITY',**win})
save(im,'PT03.png',zones,['base.cpu','base.gpu','base.ram','base.ssd','base.os'])

# PT04: authoritative chassis dimensions, without treating weight range as exact.
im=blank();zones=header(im,'Form and dimensions','A small footprint, measured clearly')
zones.append(product(im,angle,(540,340),(760,1100)));d=ImageDraw.Draw(im)
d.line((430,340,430,1440),fill=BLUE,width=4);d.line((415,340,445,340),fill=BLUE,width=4);d.line((415,1440,445,1440),fill=BLUE,width=4)
zones.append(text(im,(80,790),'182 mm\nheight',42,INK,True))
zones.append(text(im,(80,1390),'178 mm depth',35,INK,True));zones.append(text(im,(1040,1460),'36 mm width',35,INK,True))
save(im,'PT04.png',zones,['chassis.height','chassis.depth','chassis.width'])

# PT05: original abstract office task relationships, no duplicated capacity table.
im=blank();zones=header(im,'Work flow','Prepare. Compare. Deliver.')
grid(im,(70,340,1530,940));cards=[(110,'01','PREPARE','Organize your documents'),(610,'02','COMPARE','Review information together'),(1110,'03','DELIVER','Bring the work to completion')]
for x,num,k,sub in cards:
 rect(im,(x,420,x+370,800),'#183653',24);zones.append(text(im,(x+30,450),num,30,'#84B5FF',True));zones.append(text(im,(x+30,525),k,39,'white',True));
 words=sub.split();lines=[];line=''
 for word in words:
  if len(line+' '+word)>19:lines.append(line);line=word
  else:line=(line+' '+word).strip()
 lines.append(line);zones.append(text(im,(x+30,620),'\n'.join(lines),30,'#DDEBFA'))
zones.append(product(im,left,(650,1000),(400,500)));save(im,'PT05.png',zones,[])

# PT06: source-accurate physical power control, white background; ports belong to PT08.
im=blank();zones=header(im,'Physical control','Power control at the front')
zones.append(product(im,front,(315,440),(300,900)))
detail=angle.crop((480,0,850,700));zones.append(product(im,detail,(980,410),(370,700),'PRODUCT_SILHOUETTE_CONTROL_DETAIL'))
zones.append(text(im,(100,1390),'Front view',32,GRAY));zones.append(text(im,(950,1390),'Original control detail',32,GRAY))
d=ImageDraw.Draw(im);d.line((425,510,820,510,1128,510),fill=BLUE,width=3)
save(im,'PT06.png',zones,['input.powerButton'])

# PT07: unused, independently verified NPU capability, not a spec recap.
im=blank();zones=header(im,'On-chip AI capability','A dedicated neural processor')
grid(im,(70,340,1530,960));zones.append(text(im,(120,405),'Intel AI Boost',70,'white',True));zones.append(text(im,(120,540),'Up to 13 TOPS',88,'white',True));zones.append(text(im,(120,680),'NPU peak performance (INT8)',35,'#DDEBFA'));zones.append(text(im,(120,785),'For supported AI workloads',37,'white'))
zones.append(product(im,angle,(1040,430),(400,550)));zones.append(text(im,(100,1130),'Integrated into the processor',48,INK,True));zones.append(text(im,(100,1240),'Application support and workload determine\nhow on-device AI acceleration is used.',38,GRAY))
save(im,'PT07.png',zones,['npu.intelAiBoost','npu.peak13Tops'])

# PT08: leaders end on exact photographed standard openings; optional module is blank.
im=blank();zones=header(im,'Physical connections','Front and rear, clearly mapped')
zf=product(im,front,(420,420),(250,840));zr=product(im,rear,(1000,420),(260,840));zones.extend([zf,zr]);d=ImageDraw.Draw(im)
zones.append(text(im,(420,330),'FRONT',27,BLUE,True));zones.append(text(im,(1000,330),'REAR',27,BLUE,True))
def leader(label,xy,endpoint,right=False):
 x,y=xy;zones.append(text(im,(x,y),label,46,INK,True));start=(x if right else x+280,y+25);elbow=(endpoint[0]+60 if right else endpoint[0]-60,start[1]);d.line([start,elbow,endpoint],fill=BLUE,width=3);d.ellipse((endpoint[0]-5,endpoint[1]-5,endpoint[0]+5,endpoint[1]+5),fill=BLUE)
fw,fh=zf['width'],zf['height'];rw,rh=zr['width'],zr['height']
leader('Headset\ncombo',(70,540),(420+int(fw*.38),420+int(fh*.20)))
leader('USB-A\n5 Gbps',(70,710),(420+int(fw*.38),420+int(fh*.29)))
leader('USB-C\n10 Gbps',(70,880),(420+int(fw*.38),420+int(fh*.39)))
leader('Ethernet\n1 Gbps',(1290,450),(1000+int(rw*.68),420+int(rh*.17)),True)
leader('2 × USB 2.0',(1290,610),(1000+int(rw*.65),420+int(rh*.36)),True)
leader('2 × USB-A\n5 Gbps',(1290,765),(1000+int(rw*.65),420+int(rh*.46)),True)
leader('HDMI 2.1',(1290,930),(1000+int(rw*.66),420+int(rh*.66)),True)
leader('DisplayPort\n1.4a',(1290,1080),(1000+int(rw*.66),420+int(rh*.80)),True)
zones.append(text(im,(80,1430),'Wi-Fi and Bluetooth support',42,INK,True));save(im,'PT08.png',zones,['ports.standard','wireless.support'])

write(DEST/'logo-placement.json',{'schemaVersion':3,'brand':'Dell','logoRole':'OEM base-product identifier','minimumClearancePx':32,'minimumComponentSeparationPx':32,'thumbnailReviewSizePx':200,'logoVisibilityMode':'STANDARD','placements':logo})
write(DEST/'style-lock.json',{'internalId':'VD-744','style_approval_status':'APPROVED','approved_style_id':'B01','approved_supporting_gallery_pack':'BG01','profile':'navy-technical-v1','palette':[NAVY,'#FFFFFF',BLUE],'approvalSource':'Direct user reply: 批准这个风格','approvalDate':'2026-10-13','recipeVersion':'vd744-b01-v1','recipeStatus':'BUILT_PENDING_CURRENT_BYTE_REVIEW','boundaryMode':'DESKTOP_GRAPHIC_SAFE_ZONE','formFactor':'STANDALONE_DESKTOP','forbidden':['External devices/accessories','Invented LCD','Office/paid software entitlement','Seller warranty advertising in gallery'],'recipePath':'../../assets/production/VD-744/b01-20261013/recipe.json'})
write(PACK/'recipe.json',{'version':'vd744-b01-v1','method':'ORIGINAL_PHOTO + deterministic typography/approved brand assets; AI empty office background only','fonts':{'regular':str(FONT),'regularSha256':digest(FONT),'bold':str(BOLD),'boldSha256':digest(BOLD),'fontFilesUploaded':False},'sources':{p.name:{'sha256':digest(p),'dimensions':list(Image.open(p).size)} for p in PACK.glob('*.png')},'layout':layout,'primaryFactOwnership':facts,'rebuild':'Run build-gallery.py in the listing-testing environment, then gallery_engine.py finalize; identical frozen fonts and source layers required.','publication':'Enhanced MAIN are candidates; no Amazon acceptance claimed.'})
write(DEST/'delivery-status.json',{'internalId':'VD-744','galleryState':'AWAITING_CURRENT_BYTE_VISUAL_REVIEW','deliveryState':'LOCAL_PRODUCTION','deliveryScope':'FULL_GALLERY','currentQaPass':False,'amazonEligibility':'NOT_ASSESSED','factsCompleteness':'REVIEW_REQUIRED'})
if Path(__file__).resolve()!=(PACK/'build-gallery.py').resolve():shutil.copy2(Path(__file__),PACK/'build-gallery.py')
write(PACK/'source-rights.json',{'oem':'Dell','authorizationStatus':'USER_CONFIRMED_CATALOG_WIDE','holder':'MegaPC / J-Tech Digital','officialPage':'https://www.dell.com/en-us/shop/desktops/spd/dellpromicroqcm1250','date':'2026-10-13','physicalLayers':'Original exact-model OEM photos; alpha trim and proportional downsize only, factory marks preserved.','sourceNativeFront':'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/page/landing-page/windows-11/2025/windows-11-update-desktop-pro-qcm1250-micro-black.png?fmt=png-alpha&qlt=100','rearSource':'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/desktops/dell-pro/qcm1250/media-gallery/desktop-pro-qcm1250-micro-black-gallery-2.psd','sideSource':'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/desktops/dell-pro/qcm1250/media-gallery/desktop-pro-qcm1250-micro-black-gallery-3.psd','angleSource':'https://i.dell.com/assetlink/img/global/desktop-pro-qcm1250-micro-black-gallery-1-dl11avy1-original.png','AI':'Built-in imagegen; empty synthetic office background only. No synthetic performer. Style preview is reference only, not reused as product pixels.','fixedAssets':'Repository active Dell transparent logo, Windows 11 Pro package and lockup; hashes in recipe/QA.','verificationLimit':'Exact sold-unit optional rear module has not been photographed; standard OEM chassis ports only. Do not infer an optional module from these images.'})
print(json.dumps({'output':str(DEST),'images':list(layout),'facts':facts},indent=2))
