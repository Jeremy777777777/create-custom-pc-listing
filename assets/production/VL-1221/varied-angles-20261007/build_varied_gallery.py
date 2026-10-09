"""Measured original-photo composition; no mirrored hardware or generated angles."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import hashlib, json, sys, shutil
ROOT=Path(__file__).resolve().parent
REPO=next((p for p in ROOT.parents if (p/'scripts/gallery_engine.py').exists()),ROOT.parents[1]/'tmp/business-laptop-redesign-20261005')
SRC=ROOT/'sources'; OUT=ROOT/'gallery'; OUT.mkdir(exist_ok=True); (OUT/'unbranded').mkdir(exist_ok=True)
OLD=REPO/'product generated photo/VL-1221'
sys.path.insert(0,str(REPO/'scripts')); import gallery_engine as ge
N=1254; FONT='C:/Windows/Fonts/bahnschrift.ttf'; WHITE=(246,243,240); RED=(228,76,85); MUTED=(195,183,182)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
font=lambda n:ImageFont.truetype(FONT,n)
def text(im,xy,s,size=48,color=WHITE): ImageDraw.Draw(im).text(xy,s,font=font(size),fill=color,spacing=12)
def backdrop():
    im=Image.new('RGB',(N,N)); pix=im.load()
    for y in range(N):
        for x in range(N):
            g=max(0,1-(((x-200)/1000)**2+((y-650)/850)**2));pix[x,y]=(int(15+33*g),int(14+8*g),int(19+10*g))
    return im
def head(im,kicker,title):
    text(im,(64,54),kicker,24,RED);text(im,(64,107),title,64);ImageDraw.Draw(im).line((65,263,185,263),fill=RED,width=5)
def solve(a,b):
    a=[list(map(float,r))+[float(v)] for r,v in zip(a,b)]
    for k in range(len(a)):
        j=max(range(k,len(a)),key=lambda j:abs(a[j][k]));a[k],a[j]=a[j],a[k]
        v=a[k][k];a[k]=[x/v for x in a[k]]
        for j in range(len(a)):
            if j!=k:
                v=a[j][k];a[j]=[x-v*y for x,y in zip(a[j],a[k])]
    return [r[-1] for r in a]
def replace_screen(im,quad,art):
    a=[];b=[];sw,sh=art.size
    for (x,y),(u,v) in zip(quad,[(0,0),(sw,0),(sw,sh),(0,sh)]):
        a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);b.extend([u,v])
    w=art.transform(im.size,Image.Transform.PERSPECTIVE,solve(a,b),Image.Resampling.BICUBIC)
    mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(quad,fill=255);im.paste(w,(0,0),mask)
    return mask
art=Image.open(SRC/'original-game-scene.png').convert('RGB')
front=Image.open(SRC/'official-front.jpg').convert('RGBA');front.putalpha(Image.open(SRC/'main-product-mask.png').convert('L'))
front.paste(ImageOps.fit(art,(773,435),method=Image.Resampling.LANCZOS),(627,578))
front=front.crop((480,540,1555,1490));front.save(SRC/'front-clean.png')
# Opposite three-quarter source is a different official camera view, never a horizontal flip.
op=Image.open(SRC/'official-right-angle.jpg').convert('RGBA')
grid=op.convert('RGB').crop((350,475,1400,1550));gd=ImageDraw.Draw(grid)
for x in range(350,1400,50):
    gd.line((x-350,0,x-350,1075),fill=(0,200,255),width=1);gd.text((x-349,2),str(x),font=font(16),fill='white',stroke_width=1,stroke_fill='black')
for y in range(475,1550,50):
    gd.line((0,y-475,1050,y-475),fill=(0,200,255),width=1);gd.text((0,y-473),str(y),font=font(16),fill='white',stroke_width=1,stroke_fill='black')
grid.save(ROOT/'opposite-measurement-grid.png')
outline=[(794,532),(1355,505),(1362,511),(1365,1120),(1362,1129),(1353,1128),(1356,1142),(1373,1149),(1380,1167),(1371,1198),(1205,1338),(835,1518),(826,1518),(374,1298),(371,1287),(739,1027),(750,1020),(771,1013),(784,1010),(782,549),(787,538)]
alpha=Image.new('L',op.size);ImageDraw.Draw(alpha).polygon(outline,fill=255)
# Campaign pixels in the measured body outline are excluded; neutral factory metal is retained.
ap=alpha.load();sp=op.load()
for y in range(475,1530):
    for x in range(350,1400):
        if ap[x,y] and max(sp[x,y][:3])-min(sp[x,y][:3])>28:ap[x,y]=0
alpha=alpha.filter(ImageFilter.MinFilter(3));op.putalpha(alpha)
quad=[(798,552),(1342,520),(1342,1026),(797,947)]
lcdmask=replace_screen(op,quad,art);lcdmask.save(SRC/'opposite-lcd-mask.png');alpha.save(SRC/'opposite-product-mask.png')
op=op.crop((350,475,1400,1550));op.save(SRC/'opposite-clean.png')
ge.remove_background(SRC/'official-rear.jpg',SRC/'rear-clean.png',tolerance=35)
rear=Image.open(SRC/'rear-clean.png').convert('RGBA');rear.putalpha(rear.getchannel('A').filter(ImageFilter.MinFilter(3)));rear.save(SRC/'rear-clean.png')
plan=json.loads((OLD/'logo-placement.json').read_text()); recipes={}
def put(im,p,scale,x,y,label='PRODUCT_SILHOUETTE'):
    assert 0<scale<=1
    q=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS);assert x>=0 and y>=0 and x+q.width<=N and y+q.height<=N
    im.paste(q,(x,y),q);return dict(label=label,x=x,y=y,width=q.width,height=q.height)
def finish(n,im,zones,view):
    name=f'PT{n:02}.png'; im.save(OUT/'unbranded'/name,dpi=(72,72),icc_profile=(SRC/'sRGB.icc').read_bytes())
    zones.append(dict(label='HEADLINE',x=64,y=54,width=900,height=200));plan['placements'][name]['protectedZones']=zones
    recipes[name]={'canvas':[N,N],'cameraView':view,'productLayerMethod':'ORIGINAL_PHOTO','protectedZones':zones,'masterSha256':sha(OUT/'unbranded'/name)}
im=backdrop();head(im,'01 / GAMING EXPERIENCE','YOUR NEXT\nADVENTURE STARTS HERE')
z=put(im,front,.9,143,335);finish(1,im,[z],'Straight front hero, large centered placement; no specs or OS')
im=Image.open(SRC/'table-background.png').convert('RGB');im=ImageOps.fit(im,(N,N),method=Image.Resampling.LANCZOS)
head(im,'02 / THE PLAY SESSION','SETTLE IN.\nSTART YOUR SESSION.')
z=put(im,op,.79,215,375);finish(2,im,[z],'Opposite three-quarter view on original empty tabletop; screen rises to the right')
im=backdrop();head(im,'04 / DISPLAY','SEE THE GAME\nIN FULL DETAIL')
for x,a,b in [(65,'15.6-inch','IPS display'),(375,'144Hz','Refresh rate'),(665,'FHD','1920 × 1080'),(945,'ANTI-GLARE','Screen finish')]:
    text(im,(x,335),a,43);text(im,(x,397),b,29,MUTED)
z=put(im,front,.76,217,480);finish(4,im,[z,dict(label='DISPLAY_COPY',x=64,y=330,width=1140,height=110)],'Centered frontal display, four facts across top, full product below')
im=backdrop();head(im,'05 / HOW THE SYSTEM WORKS','FROM GAME LOGIC\nTO ON-SCREEN ACTION')
for y,lab,sub in [(385,'PROCESS','Game logic'),(625,'RENDER','Scene rendering'),(865,'DISPLAY','On-screen motion')]:
    text(im,(65,y),lab,43,RED);text(im,(65,y+65),sub,32,MUTED)
    if y<865:
        d=ImageDraw.Draw(im);d.line((95,y+135,95,y+190),fill=WHITE,width=3);d.line((83,y+177,95,y+190,107,y+177),fill=WHITE,width=3)
z=put(im,rear,.475,338,495);finish(5,im,[z,dict(label='FLOW',x=64,y=380,width=260,height=610)],'Original rear three-quarter product; vertical workflow at left; no additional capacities')
im=backdrop();head(im,'07 / CAMERA AND VOICE','READY FOR\nFACE-TO-FACE MOMENTS')
text(im,(65,333),'720p HD CAMERA',45)
# Genuine original front bezel, native-resolution detail strip. No new camera hardware.
strip=front.crop((130,10,935,92));im.paste(strip,(65,438),strip);strip.save(SRC/'camera-bezel-native.png')
ImageDraw.Draw(im).line([(470,418),(470,438)],fill=RED,width=3)
z=put(im,front,.52,65,685)
text(im,(700,735),'CLEANER CAMERA INPUT',32,RED);text(im,(700,795),'Temporal noise\nreduction',39)
text(im,(700,945),'VOICE PICKUP',32,RED);text(im,(700,1005),'Dual-array digital\nmicrophones',39)
finish(7,im,[z,dict(label='PRODUCT_BEZEL_DETAIL',x=65,y=438,width=805,height=82),dict(label='CAMERA_COPY',x=65,y=330,width=800,height=70),dict(label='CAMERA_BODY',x=700,y=735,width=500,height=370)],'Native frontal webcam/bezel detail above lower-left front product; proof copy at right')
selected=list(recipes)
(OUT/'logo-placement.json').write_text(json.dumps(plan,indent=2)+'\n')
ge.badges(OUT,REPO/'assets/branding/hp-logo-blue.png',OUT/'logo-placement.json',brand='HP',slots=selected)
qa=json.loads((OUT/'logo-qa.json').read_text())
for e in qa['images']:
    p=OUT/e['file']; Image.open(p).convert('RGB').save(p,dpi=(72,72),icc_profile=(SRC/'sRGB.icc').read_bytes());e['finalImageSha256']=sha(p)
(OUT/'logo-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
record={'schemaVersion':1,'internalId':'VL-1221','version':'20261007-varied-angles','scope':selected,'renderer':'build_varied_gallery.py + repository gallery_engine.py badges','font':FONT,'fontSha256':sha(FONT),'sources':[{'file':p.name,'sha256':sha(p)} for p in sorted(SRC.iterdir()) if p.is_file()],'oppositeSourceOutline':outline,'oppositeSourceLCD':quad,'frontCrop':[480,540,1555,1490],'slots':recipes,'transformPolicy':'Native hardware or proportional downscale only; never mirror, simulate perspective or synthesize a new product angle'}
(ROOT/'recipe.json').write_text(json.dumps(record,indent=2)+'\n')
sheet=Image.new('RGB',(1280,700),'#e5e2e2');d=ImageDraw.Draw(sheet)
for i in range(8):
    name=f'PT{i+1:02}.png'; p=OUT/name if (OUT/name).exists() else OLD/name
    tile=Image.open(p);tile.thumbnail((300,300));x=i%4*320+10;y=i//4*350+35;sheet.paste(tile,(x,y));d.text((x,y-28),f'PT{i+1:02}',font=font(23),fill='black')
sheet.save(ROOT/'contact-sheet.png')
small=Image.new('RGB',(840,460),'#e5e2e2');sd=ImageDraw.Draw(small)
for i in range(8):
    name=f'PT{i+1:02}.png';p=OUT/name if (OUT/name).exists() else OLD/name
    tile=Image.open(p);tile.thumbnail((200,200));x=i%4*210+5;y=i//4*230+25;small.paste(tile,(x,y));sd.text((x,y-21),f'PT{i+1:02}',font=font(18),fill='black')
small.save(ROOT/'contact-sheet-200px.png')
print('Rendered five varied-angle replacements; native and 200px visual review still required.')
