"""Original-photo B06/BG06 composition; no chassis or brand generation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops, ImageCms
import json, hashlib, sys, shutil
P=Path(__file__).resolve().parent
ROOT=next((a for a in P.parents if (a/'scripts/gallery_engine.py').exists()),P.parents[1]/'tmp/listing-20744-20261013')
S=P/'sources'; O=P/'gallery'; U=O/'unbranded'; L=P/'layers'
for p in [O,U,L]:p.mkdir(parents=True,exist_ok=True)
icc_path=L/'sRGB.icc'
if not icc_path.exists():
 existing=Image.open(O/'MAIN-STRICT.jpg').info.get('icc_profile') if (O/'MAIN-STRICT.jpg').exists() else None
 icc_path.write_bytes(existing or ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
ICC=icc_path.read_bytes()
W=H=1254
NAVY='#0b2144'; BLUE='#1665ad'; TEAL='#008b97'; MUTED='#52677d'
FONT=Path('C:/Windows/Fonts')
def font(n,b=False):return ImageFont.truetype(str(FONT/('arialbd.ttf' if b else 'arial.ttf')),n)
def txt(im,xy,t,n=32,c=NAVY,b=False):ImageDraw.Draw(im).text(xy,t,font=font(n,b),fill=c,spacing=10)
def line(im,points,c=TEAL,width=3):ImageDraw.Draw(im).line(points,fill=c,width=width,joint='curve')
def rounded(im,box,fill,r=22,outline=None):ImageDraw.Draw(im).rounded_rectangle(box,r,fill=fill,outline=outline,width=2)
def load(p):return Image.open(p).convert('RGBA')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')

# Replace only LCD artwork; every exterior pixel remains from an official image.
QUADS={
 'front':[(389,414),(1611,414),(1611,1183),(389,1183)],
 'angle':[(274,646),(866,654),(1148,1104),(563,1149)],
 'stand':[(568,543),(1317,578),(1707,1157),(983,1285)],
 'tablet':[(321,461),(1226,520),(1696,1188),(850,1363)]}
FILE={'front':'CT2_04.png','angle':'CT1_04.png','stand':'CT1_06.png','tablet':'CT1_07.png'}
def warp_quad(art,quad,size):
 a=[];bb=[]
 for (x,y),(u,v) in zip(quad,[(0,0),(art.width,0),(art.width,art.height),(0,art.height)]):
  a += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]];bb += [u,v]
 matrix=[list(map(float,row))+[float(value)] for row,value in zip(a,bb)]
 for col in range(8):
  pivot=max(range(col,8),key=lambda r:abs(matrix[r][col]));matrix[col],matrix[pivot]=matrix[pivot],matrix[col]
  div=matrix[col][col];matrix[col]=[v/div for v in matrix[col]]
  for r in range(8):
   if r!=col:
    factor=matrix[r][col];matrix[r]=[v-factor*u for v,u in zip(matrix[r],matrix[col])]
 coeff=[matrix[r][-1] for r in range(8)]
 return art.transform(size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)
def screen_art(mode='plain'):
 art=ImageOps.fit(load(S/'screen-art.png'),(1200,750))
 if mode=='front':
  txt(art,(75,70),'Ready for your\nnext chapter',72,'white',True)
  txt(art,(80,270),'Work. Study. Create.',32,'#d7f6ff')
 elif mode=='angle':
  txt(art,(60,65),'Room for\nyour ideas',68,'white',True)
 else:
  # No software branding or specification text in ordinary PT screens.
  pass
 return art
def cut_white(im):
 # Preserve the solid chassis and enclosed light details. Outside that silhouette,
 # convert the OEM's white-matted neutral shadow into a transparent black shadow.
 r,g,b,a=im.split();level=ImageChops.darker(ImageChops.darker(r,g),b)
 inv=level.point(lambda v:255 if v>=230 else 0)
 ImageDraw.floodfill(inv,(0,0),128)
 solid=inv.point(lambda v:0 if v==128 else 255)
 shadow_alpha=level.point(lambda v:255-v)
 alpha=ImageChops.lighter(solid,shadow_alpha)
 out=Image.composite(im,Image.new('RGBA',im.size,(0,0,0,0)),solid)
 out.putalpha(alpha);return out
PRODUCTS={};META={}
def master(kind,mode='plain'):
 key=kind+'-'+mode
 if key in PRODUCTS:return PRODUCTS[key].copy(),META[key]
 im=load(S/FILE[kind]);art=screen_art(mode)
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(QUADS[kind],fill=255)
 im.paste(warp_quad(art,QUADS[kind],im.size),(0,0),mask)
 # Crop only whitespace/external campaign badge; no product content is cut.
 im=im.crop((0,0,2000,1780));im=cut_white(im)
 im.putalpha(ImageChops.lighter(im.getchannel('A'),mask.crop((0,0,2000,1780))))
 bbox=im.getchannel('A').getbbox();im=im.crop(bbox)
 im.save(L/(key+'.png'))
 meta={'source':FILE[kind],'sourceSha256':digest(S/FILE[kind]),'sourceCrop':bbox,'lcdQuadOriginalPixels':QUADS[kind],'mode':mode}
 PRODUCTS[key]=im;META[key]=meta
 return im.copy(),meta
def original_crop(name,box):
 im=load(S/name).crop(box);im=cut_white(im);bbox=im.getchannel('A').getbbox()
 return im.crop(bbox),{'source':name,'crop':box,'alphaCrop':bbox,'sourceSha256':digest(S/name)}
PLACES={};PLACEMENT={}
def place(im,product,box,slot,meta=None):
 x,y,w,h=box;scale=min(w/product.width,h/product.height)
 if scale>1.00001:raise ValueError('Refuse product upscaling')
 dims=(round(product.width*scale),round(product.height*scale));product=product.resize(dims,Image.Resampling.LANCZOS)
 px=round(x+(w-dims[0])/2);py=round(y+(h-dims[1])/2)
 im.alpha_composite(product,(px,py))
 rect={'label':'PRODUCT_SILHOUETTE_'+str(len(PLACES.get(slot,[]))+1),'x':px,'y':py,'width':dims[0],'height':dims[1]}
 PLACES.setdefault(slot,[]).append(rect)
 if meta:PLACEMENT.setdefault(slot,[]).append({**meta,'destination':rect,'scale':scale})
 return rect
def product(im,kind,box,slot,mode='plain'):
 p,m=master(kind,mode);return place(im,p,box,slot,m)
def base(bg=None):
 if bg:return ImageOps.fit(load(S/bg),(W,H),method=Image.Resampling.LANCZOS)
 im=Image.new('RGBA',(W,H),'#f5f8fc');d=ImageDraw.Draw(im)
 d.ellipse((780,100,1640,1000),fill='#e3eff6');d.ellipse((1030,280,1540,790),fill='#d3e9ee')
 return im
def header(im,kicker,title,sub=None):
 txt(im,(70,64),kicker,22,TEAL,True);txt(im,(66,112),title,63,NAVY,True)
 if sub:txt(im,(70,280),sub,29,MUTED)
def footer(im,slot):
 # Natural full-width navigation footer, not a logo card.
 d=ImageDraw.Draw(im);d.rectangle((0,1140,W,H),fill=NAVY)
 txt(im,(260,1181),'Yoga 7 2-in-1 16ILL10',24,'white')
 txt(im,(W-140,1183),slot[:4],20,'#bcd9e7')
def save(im,name):
 im=im.convert('RGB');im.save(U/name if name.startswith('PT') else O/name,quality=96,dpi=(96,96),icc_profile=ICC)

# MAIN alternatives: one actual computer, white exterior and product-only strict.
for name,kind,mode in [('MAIN-STRICT.jpg','front','plain'),('MAIN-ENHANCED-FRONT-CANDIDATE.png','front','front'),('MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png','angle','angle')]:
 mh=850 if kind=='angle' else 1100
 im=Image.new('RGBA',(W,mh),'white');r=product(im,kind,(45,20,1164,mh-40),name,mode)
 if mode!='plain':
  source=ROOT/'assets/branding'/('windows-11-pro-lockup.png' if mode=='front' else 'windows-11-pro-package.png')
  mark=load(source)
  pm=PLACEMENT[name][0];crop=pm['sourceCrop'];scale=pm['scale']
  sx,sy,sw=(700,880,380) if mode=='front' else (650,800,260)
  x=round(r['x']+(sx-crop[0])*scale);y=round(r['y']+(sy-crop[1])*scale);w=round(sw*scale)
  # Deterministic Windows graphic, no perspective distortion; verified inside LCD.
  h=round(w*mark.height/mark.width)
  lcd=Image.new('L',im.size);quad=[(round(r['x']+(a-crop[0])*scale),round(r['y']+(b-crop[1])*scale)) for a,b in QUADS[kind]]
  ImageDraw.Draw(lcd).polygon(quad,fill=255);lcd.save(L/(name+'.lcd-mask.png'))
  if lcd.crop((x,y,x+w,y+h)).getextrema()!=(255,255):raise ValueError('Windows artwork outside LCD')
  im.alpha_composite(mark.resize((w,h),Image.Resampling.LANCZOS),(x,y))
  PLACEMENT[name].append({'asset':str(source.relative_to(ROOT)),'sha256':digest(source),'x':x,'y':y,'width':w,'height':h,'mode':'WINDOWS_11_PRO_LOGO_LOCKUP' if mode=='front' else 'WINDOWS_11_PRO_PACKAGE'})
 save(im,name)

n='PT01.png';im=base('hero-background.png')
header(im,'READY FOR WHAT COMES NEXT','Ready for your\nnext chapter','Work. Study. Create.')
product(im,'front',(55,400,1144,680),n);footer(im,n);save(im,n)

n='PT02.png';im=base('lifestyle-background.png')
header(im,'YOUR EVERYDAY WORKSPACE','Make room\nfor focus','A calm space for coursework and everyday projects.')
product(im,'front',(140,495,974,620),n);footer(im,n);save(im,n)

n='PT03.png';im=base();header(im,'YOUR BASE CONFIGURATION','The essentials,\nclearly defined')
product(im,'angle',(575,330,620,435),n)
cards=[('PROCESSOR','Intel Core Ultra 5','226V'),('GRAPHICS','Integrated Intel Arc','130V'),('MEMORY','16GB LPDDR5x','Fixed memory'),('STORAGE','512GB SSD','PCIe NVMe'),('OPERATING SYSTEM','Windows 11 Pro','')]
for i,(label,a,b) in enumerate(cards):
 x,y=[(70,360),(635,700),(70,610),(70,860),(635,940)][i]
 rounded(im,(x,y,x+510,y+185),'white',24)
 txt(im,(x+28,y+22),label,20,TEAL,True);txt(im,(x+28,y+62),a,34,NAVY,True)
 if b:txt(im,(x+28,y+114),b,31,NAVY,True)
footer(im,n);save(im,n)

n='PT04.png';im=base();header(im,'TOUCH + CONVERTIBLE DESIGN','A bigger canvas.\nMore ways to use it.')
txt(im,(72,307),'16-inch IPS touch  |  1920 x 1200  |  16:10',31,BLUE,True)
product(im,'stand',(65,410,590,570),n);product(im,'tablet',(665,455,520,525),n)
txt(im,(90,1010),'Laptop  /  Tent  /  Stand  /  Tablet',34,NAVY,True)
footer(im,n);save(im,n)

n='PT05.png';im=base();header(im,'YOUR CREATIVE ROUTINE','From first thought\nto finished work')
product(im,'angle',(245,375,900,450),n)
for i,(a,b) in enumerate([('PLAN','Organize the next step'),('DRAFT','Shape your ideas'),('REVIEW','Refine the details')]):
 x=70+i*395
 rounded(im,(x,875,x+350,1060),'white')
 txt(im,(x+25,895),str(i+1).zfill(2),26,TEAL,True);txt(im,(x+25,938),a,35,NAVY,True)
 txt(im,(x+25,1002),b,23,MUTED)
 if i<2:line(im,[(x+360,965),(x+385,965)],TEAL,4)
footer(im,n);save(im,n)

n='PT06.png';im=Image.new('RGBA',(W,H),'white');header(im,'BUILT-IN INPUT','Comfort in\nevery keystroke')
kb,m=original_crop('CT2_05.png',(320,625,1680,1600))
r=place(im,kb,(95,345,1064,640),n,m)
txt(im,(90,1015),'Backlit numeric keyboard',31,NAVY,True)
txt(im,(715,1015),'Glass touchpad',31,NAVY,True)
footer(im,n);save(im,n)

n='PT07.png';im=base();header(im,'POWER FOR YOUR ROUTINE','Keep your\nideas moving')
txt(im,(85,350),'70Wh',145,BLUE,True);txt(im,(95,525),'Built-in battery',34,NAVY,True)
back,m=original_crop('CT1_08.png',(100,300,1860,1700))
place(im,back,(410,490,775,585),n,m)
txt(im,(85,1080),'Designed for everyday work and creativity.',27,MUTED)
footer(im,n);save(im,n)

n='PT08.png';im=Image.new('RGBA',(W,H),'white');header(im,'PHYSICAL PORTS + WIRELESS','Connect your way')
txt(im,(72,225),'Two actual sides. Clear connections.',30,MUTED)
left,ml=original_crop('CT2_01.png',(145,925,1840,1080))
right,mr=original_crop('CT2_02.png',(145,910,1840,1080))
rl=place(im,left,(70,445,1110,110),n,ml);rr=place(im,right,(70,795,1110,110),n,mr)
# Source connector centers are measured on the exact official side photographs.
def anchor(meta,rect,xy):
 crop=meta['crop'];ab=meta['alphaCrop'];sx=rect['width']/(crop[2]-crop[0]-(crop[2]-crop[0]-ab[2]+ab[0]));sy=rect['height']/(ab[3]-ab[1])
 return (round(rect['x']+(xy[0]-crop[0]-ab[0])*sx),round(rect['y']+(xy[1]-crop[1]-ab[1])*sy))
for i,(name,srcxy,end,label) in enumerate([('HDMI',(345,1002),(220,345),'HDMI 1.4b'),('TB4-L',(472,1002),(530,345),'Thunderbolt 4'),('AUDIO',(581,1002),(865,345),'3.5mm audio')]):
 a=anchor(ml,rl,srcxy);guide=end[1]+55+i*16;line(im,[a,(a[0],guide),(end[0],guide),(end[0],end[1]+35)]);txt(im,end,label,27,NAVY,True)
for i,(srcxy,end,label) in enumerate([((320,1023),(90,680),'USB-A 5Gbps'),((445,1024),(450,680),'Thunderbolt 4'),((568,1026),(820,680),'microSD')]):
 a=anchor(mr,rr,srcxy);guide=end[1]+55+i*16;line(im,[a,(a[0],guide),(end[0],guide),(end[0],end[1]+35)]);txt(im,end,label,27,NAVY,True)
txt(im,(85,1000),'Wi-Fi 7   +   Bluetooth 5.4',43,BLUE,True)
txt(im,(85,1075),'USB-A Always On  |  USB-C charging via Thunderbolt 4',25,MUTED)
footer(im,n);save(im,n)

# Preserve the unaltered official red rectangle and add only transparent padding.
logo=load(S/'lenovo-logo-red-official.png')
padded=Image.new('RGBA',(logo.width+8,logo.height+8));padded.alpha_composite(logo,(4,4));padded.save(L/'lenovo-logo-transparent.png')
plan={'schemaVersion':3,'brand':'Lenovo','logoRole':'OEM base-product identifier','logoVisibilityMode':'ASPECT_RATIO_WORDMARK','logoAssetSourceUrl':'https://media.lenovobrandworld.fiestic.com/2022/06/08010946/LenovoLogo_POS-Red-H.png','thumbnailReviewSizePx':200,'minimumClearancePx':32,'minimumComponentSeparationPx':32,'placements':{}}
for n in [f'PT{i:02}.png' for i in range(1,9)]:
 plan['placements'][n]={'style':'transparent','x':70,'y':1174,'width':128,'height':round(128*logo.height/logo.width),'protectedZones':PLACES[n]+[{'label':'FOOTER_PRODUCT_IDENTITY','x':260,'y':1170,'width':490,'height':45},{'label':'FOOTER_NAVIGATION','x':1110,'y':1170,'width':70,'height':45}]}
write(O/'logo-placement.json',plan)
recipe={'version':'vl1126-b06-v1','canvas':[W,H],'formFactor':'INTEGRATED_DISPLAY_LAPTOP','boundaryMode':'SCREEN_ONLY','productLayerMethod':'ORIGINAL_PHOTO','palette':['#FFFFFF','#0b2144','#1665ad','#008b97'],'layers':PLACEMENT,'productProtectedZones':PLACES,'sourceAssetInventory':json.loads((P/'source-inventory.json').read_text()),'fonts':['Arial','Arial Bold'],'renderCommand':'python build_gallery.py','finalBrandComposition':'gallery_engine.finalize; authentic original Lenovo logo with transparent padding','generation':'AI background and original screen art only; no generated chassis, ports, keys or logos','slotFactOwnership':{'PT01.png':['purchase-story-next-chapter'],'PT02.png':['use-case-focused-study'],'PT03.png':['base-cpu','base-gpu','base-ram','base-ssd','sold-os'],'PT04.png':['display-size','display-resolution','display-touch','display-aspect','hinge-modes'],'PT05.png':['task-plan','task-draft','task-review'],'PT06.png':['keyboard-backlight','numeric-keypad','glass-touchpad'],'PT07.png':['battery-capacity'],'PT08.png':['left-ports','right-ports','wifi-generation','bluetooth-version']}}
write(P/'recipe.json',recipe)
print('Rendered',len(list(O.glob('MAIN*'))),'MAIN and',len(list(U.glob('PT*'))),'PT clean compositions')
