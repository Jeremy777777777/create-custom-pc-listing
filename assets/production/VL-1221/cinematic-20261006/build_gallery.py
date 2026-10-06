from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageCms
import hashlib, json, sys, shutil

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'
OUT=ROOT/'gallery'
OUT.mkdir(exist_ok=True)
(OUT/'unbranded').mkdir(exist_ok=True)
REPO=next((p for p in ROOT.parents if (p/'scripts/gallery_engine.py').exists()),ROOT.parents[1]/'tmp/business-laptop-redesign-20261005')
sys.path.insert(0,str(REPO/'scripts'))
import gallery_engine as ge
N=1254
FONT='C:/Windows/Fonts/bahnschrift.ttf'
WHITE=(246,243,240); MUTED=(195,183,182); RED=(228,76,85)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(n):return ImageFont.truetype(FONT,n)
def text(im,xy,s,size=48,color=WHITE):
    ImageDraw.Draw(im).text(xy,s,font=font(size),fill=color,spacing=12)
def solve(a,b):
    a=[list(map(float,r))+[float(v)] for r,v in zip(a,b)]
    for k in range(len(a)):
        j=max(range(k,len(a)),key=lambda j:abs(a[j][k]));a[k],a[j]=a[j],a[k]
        v=a[k][k];a[k]=[x/v for x in a[k]]
        for j in range(len(a)):
            if j!=k:
                v=a[j][k];a[j]=[x-v*y for x,y in zip(a[j],a[k])]
    return [r[-1] for r in a]
screen=[(23,125),(547,20),(643,400),(150,599)]
scene=Image.open(SRC/'original-game-scene.png').convert('RGB')
base=Image.open(SRC/'page0-Iabc20.jpg').convert('RGBA')
sw,sh=scene.size
A=[];B=[]
for (x,y),(u,v) in zip(screen,[(0,0),(sw,0),(sw,sh),(0,sh)]):
    A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);B.extend([u,v])
warped=scene.transform(base.size,Image.Transform.PERSPECTIVE,solve(A,B),Image.Resampling.BICUBIC)
mask=Image.new('L',base.size);ImageDraw.Draw(mask).polygon(screen,fill=255)
base.paste(warped,(0,0),mask)
base.save(SRC/'screen-replaced.png',dpi=(72,72))
mask.save(SRC/'lcd-mask.png')
ge.remove_background(SRC/'screen-replaced.png',SRC/'product-cutout.png',tolerance=55)
product=Image.open(SRC/'product-cutout.png').convert('RGBA')
product.putalpha(product.getchannel('A').filter(ImageFilter.MinFilter(3)))
product.save(SRC/'product-cutout.png')
profile_path=SRC/'sRGB.icc'
if not profile_path.exists():profile_path.write_bytes(ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
profile=profile_path.read_bytes()
recipes={};placements={}
def backdrop(white=False):
    if white:return Image.new('RGB',(N,N),'white')
    im=Image.new('RGB',(N,N));p=im.load()
    for y in range(N):
        for x in range(N):
            g=max(0,1-(((x-200)/1000)**2+((y-650)/850)**2))
            p[x,y]=(int(15+33*g),int(14+8*g),int(19+10*g))
    return im
def head(im,kicker,title,white=False):
    c=(32,30,33) if white else WHITE
    text(im,(64,54),kicker,24,(166,42,51) if white else RED)
    text(im,(64,107),title,64,c)
    ImageDraw.Draw(im).line((65,263,185,263),fill=RED,width=5)
def put(im,scale,x,y):
    assert scale<=1
    p=product.resize((round(product.width*scale),round(product.height*scale)),Image.Resampling.LANCZOS)
    im.paste(p,(x,y),p)
    return {'label':'PRODUCT_SILHOUETTE','x':x,'y':y,'width':p.width,'height':p.height,'scale':scale}
def finish(i,im,zones,notes,layers):
    name=f'PT{i:02}.png'
    # Logo is added by the repository's deterministic compositor from an original transparent asset.
    im.save(OUT/'unbranded'/name,dpi=(72,72),icc_profile=profile)
    zones.append({'label':'HEADLINE','x':64,'y':54,'width':900,'height':200})
    placements[name]={'x':1078,'y':54,'width':128,'height':128,'style':'transparent','protectedZones':[{k:v for k,v in z.items() if k!='scale'} for z in zones]}
    recipes[name]={'canvas':[N,N],'boundaryMode':'SCREEN_ONLY','notes':notes,'productProtectedZones':zones,'layers':layers,'font':FONT,'headlineSize':64,'bodyMinimumSize':32,'masterSha256':sha(OUT/'unbranded'/name)}

im=backdrop();head(im,'01 / GAMING EXPERIENCE','YOUR NEXT\nADVENTURE STARTS HERE')
z=put(im,.92,110,328)
finish(1,im,[z],'High-level gaming purchase reason only; no capacity grid or OS claim.',['original-game-scene.png','product-cutout.png'])

im=Image.open(SRC/'table-background.png').convert('RGB');im.thumbnail((N,N),Image.Resampling.LANCZOS)
if im.size!=(N,N):
    c=backdrop();c.paste(im,((N-im.width)//2,(N-im.height)//2));im=c
head(im,'02 / THE PLAY SESSION','SETTLE IN.\nSTART YOUR SESSION.')
z=put(im,.87,122,375)
finish(2,im,[z],'Original empty-table computer-use scene; no person or external equipment.',['table-background.png','product-cutout.png'])

im=backdrop();head(im,'03 / INSTALLED CONFIGURATION','KNOW YOUR HARDWARE')
z=put(im,.54,40,463)
for y,lab,val,sub in [(322,'PROCESSOR','AMD Ryzen 7 7445HS','6 cores / Up to 4.7 GHz'),(475,'GRAPHICS','GeForce RTX 4050','NVIDIA Laptop GPU / 6GB GDDR6'),(628,'MEMORY','16GB DDR5-5600','Installed memory'),(781,'STORAGE','512GB PCIe Gen 4 NVMe','Internal M.2 SSD'),(934,'OPERATING SYSTEM','Windows 11 Pro','Final delivered OS')]:
    text(im,(660,y),lab,23,RED);text(im,(660,y+39),val,40);text(im,(660,y+90),sub,29,MUTED)
finish(3,im,[z,{'label':'CONFIGURATION','x':655,'y':310,'width':550,'height':800}],'Only complete CPU/GPU/RAM/SSD/OS page. Display belongs to PT04.',['product-cutout.png'])

im=backdrop();head(im,'04 / DISPLAY','SEE THE GAME\nIN FULL DETAIL')
z=put(im,.76,300,438)
for y,a,b in [(330,'15.6-inch','IPS display'),(520,'144Hz','Refresh rate'),(710,'FHD','1920 × 1080'),(900,'ANTI-GLARE','Screen finish')]:
    text(im,(65,y),a,51);text(im,(65,y+65),b,32,MUTED)
finish(4,im,[z,{'label':'DISPLAY_COPY','x':64,'y':330,'width':240,'height':655}],'Display facts uniquely owned here; no input or port recap.',['product-cutout.png'])

im=backdrop();head(im,'05 / HOW THE SYSTEM WORKS','FROM GAME LOGIC\nTO ON-SCREEN ACTION')
for x,lab,sub in [(65,'PROCESS','Game logic'),(470,'RENDER','Scene rendering'),(875,'DISPLAY','On-screen motion')]:
    text(im,(x,333),lab,43,RED);text(im,(x,400),sub,32,MUTED)
    if x<875:
        d=ImageDraw.Draw(im);d.line((x+325,366,x+364,366),fill=WHITE,width=3);d.line((x+351,354,x+364,366,x+351,378),fill=WHITE,width=3)
z=put(im,.72,225,520)
finish(5,im,[z,{'label':'FLOW','x':64,'y':328,'width':1130,'height':125}],'Task relationships only; no repeated model names, clocks or capacities.',['product-cutout.png'])

im=backdrop(True);head(im,'06 / INPUT DETAILS','CONTROL AT\nYOUR FINGERTIPS',True)
# These are native, unwarped crops from the exact OEM photo. No keys are synthesized.
native=Image.open(SRC/'page0-Iabc20.jpg').convert('RGB')
keymask=Image.new('L',native.size);ImageDraw.Draw(keymask).polygon([(158,690),(686,465),(1116,590),(696,947),(155,720)],fill=255)
keyboard=Image.new('RGB',native.size,'white');keyboard.paste(native,(0,0),keymask);keyboard=keyboard.crop((176,478,1020,841))
touch=Image.open(SRC/'page0-Iabc20.jpg').convert('RGB').crop((615,634,963,841))
im.paste(keyboard,(200,366));im.paste(touch,(730,869))
text(im,(65,776),'FULL-SIZE KEYBOARD',43,(30,29,32));text(im,(65,839),'Backlit keys',34,(90,85,87));text(im,(65,887),'Numeric keypad',34,(90,85,87))
text(im,(65,1010),'HP IMAGEPAD',43,(30,29,32));text(im,(65,1070),'Precision touchpad input',34,(90,85,87))
finish(6,im,[{'label':'PRODUCT_SILHOUETTE_KEYBOARD','x':200,'y':366,'width':844,'height':343},{'label':'PRODUCT_SILHOUETTE_TOUCHPAD','x':730,'y':869,'width':348,'height':207},{'label':'INPUT_COPY','x':64,'y':775,'width':600,'height':340}],'White input-only composition with exact native OEM crops, no generated keys.',['page0-Iabc20.jpg'])

im=backdrop();head(im,'07 / CAMERA AND VOICE','READY FOR\nFACE-TO-FACE MOMENTS')
z=put(im,.7,365,510)
text(im,(65,328),'720p HD CAMERA',45);text(im,(65,395),'Temporal noise reduction',33,MUTED)
text(im,(65,449),'Dual-array digital microphones',33,MUTED)
# Leader ends on actual camera in the factory bezel, not an invented lens.
cx,cy=365+round(318*.7),510+round(53*.7)
ImageDraw.Draw(im).line([(650,465),(cx,490),(cx,cy)],fill=RED,width=3)
ImageDraw.Draw(im).ellipse((cx-4,cy-4,cx+4,cy+4),fill=RED)
finish(7,im,[z,{'label':'CAMERA_COPY','x':64,'y':327,'width':860,'height':155}],'Unused camera/call value, datasheet camera and microphone facts; no warranty or config recap.',['product-cutout.png'])

im=backdrop();head(im,'08 / PHYSICAL CONNECTIONS','CONNECT YOUR WAY')
ports=Image.open(SRC/'official-ports.jpg').convert('RGB')
# Two original side views remain proportionally downscaled. Original OEM anchor marks are retained.
zones=[]
for tag,box,y in [('LEFT',(100,770,1900,985),560),('RIGHT',(100,1120,1900,1335),925)]:
    part=ports.crop(box);part.save(SRC/f'ports-{tag.lower()}-native.png');ge.remove_background(SRC/f'ports-{tag.lower()}-native.png',SRC/f'ports-{tag.lower()}-cutout.png')
    part=Image.open(SRC/f'ports-{tag.lower()}-cutout.png').convert('RGBA');part.putalpha(part.getchannel('A').filter(ImageFilter.MinFilter(3)));part=part.resize((1098,131),Image.Resampling.LANCZOS);im.paste(part,(78,y),part)
    zones.append({'label':'PRODUCT_SILHOUETTE_'+tag,'x':78,'y':y,'width':1098,'height':131})
text(im,(65,318),'LEFT SIDE',26,RED)
for x,label,sub,end in [(65,'AC power','Smart pin',(184,604)),(382,'USB-A','5Gbps / Sleep & Charge',(271,604)),(865,'3.5mm audio','Headphone / mic',(334,607))]:
    text(im,(x,377),label,39);text(im,(x,433),sub,29,MUTED)
    start=(x+25,482);ImageDraw.Draw(im).line([start,end],fill=RED,width=3)
text(im,(65,735),'RIGHT SIDE',26,RED)
for x,label,sub,end in [(65,'USB-C','5Gbps / DP 1.4a',(777,1005)),(350,'RJ-45','Ethernet',(879,990)),(617,'USB-A','5Gbps',(967,1005)),(905,'HDMI 2.1','Display output',(1048,988))]:
    text(im,(x,786),label,39);text(im,(x,843),sub,28,MUTED)
    start=(x+25,890);ImageDraw.Draw(im).line([start,end],fill=RED,width=3)
text(im,(65,1084),'2 × USB-A  /  1 × USB-C',32)
text(im,(65,1130),'USB-C supports HP Sleep and Charge.',29,MUTED)
text(im,(65,1190),'Wi-Fi 6 (2×2)  /  Bluetooth 5.4',32,MUTED)
finish(8,im,zones+[{'label':'PORT_COPY_LEFT','x':64,'y':315,'width':1120,'height':170},{'label':'PORT_COPY_RIGHT','x':64,'y':735,'width':1120,'height':155},{'label':'WIRELESS_COPY','x':64,'y':1080,'width':1100,'height':155}],'Exact-model OEM two-sided physical port views; original connector anchors retained with deterministic leaders/types/count/function labels. Wireless uniquely owned here.',['official-ports.jpg'])

plan={'schemaVersion':3,'brand':'HP','logoRole':'OEM base-product identifier','minimumClearancePx':32,'minimumComponentSeparationPx':32,'thumbnailReviewSizePx':200,'placements':placements}
(OUT/'logo-placement.json').write_text(json.dumps(plan,indent=2))
recipe={'schemaVersion':1,'internalId':'VL-1221','version':'20261006-cinematic-correction','formFactor':'laptop','renderer':'build_gallery.py + repository gallery_engine.py badges','lcdPolygonSourcePixels':screen,'lcdMaskSha256':sha(SRC/'lcd-mask.png'),'sources':[{'file':p.name,'sha256':sha(p),'dimensions':list(Image.open(p).size)} for p in SRC.iterdir() if p.suffix.lower() in ['.png','.jpg'] and '-grid' not in p.name],'slots':recipes}
(ROOT/'recipe.json').write_text(json.dumps(recipe,indent=2))
ge.badges(OUT,REPO/'assets/branding/hp-logo-blue.png',OUT/'logo-placement.json',brand='HP',slots=list(recipes))
# gallery_engine preserves pixel data but does not add DPI/ICC. Re-export metadata and rebind final hashes.
qa=json.loads((OUT/'logo-qa.json').read_text())
for e in qa['images']:
    p=OUT/e['file'];im=Image.open(p).convert('RGB');im.save(p,dpi=(72,72),icc_profile=profile);e['finalImageSha256']=sha(p)
(OUT/'logo-qa.json').write_text(json.dumps(qa,indent=2))
sheet=Image.new('RGB',(840,460),'#dedddd');d=ImageDraw.Draw(sheet)
for i in range(8):
    im=Image.open(OUT/f'PT{i+1:02}.png');im.thumbnail((200,200));x=(i%4)*210+5;y=(i//4)*230+25
    sheet.paste(im,(x,y));d.text((x,y-21),f'PT{i+1:02}',font=font(18),fill='black')
sheet.save(ROOT/'contact-sheet.png')
print('Rendered eight exact-product composites, contact-sheet.png; manual review is still required.')
