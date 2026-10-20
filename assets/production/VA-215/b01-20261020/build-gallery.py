"""Compose VA-215 from authorized OEM layers; AI is used only for original art plates.
No generated hardware, logo, key, connector or specification is used in final files.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageCms
import json, hashlib, shutil, sys, math
from datetime import datetime, timezone

WORK=Path(__file__).resolve().parent
IN_PACK=WORK.name=='b01-20261020'
REPO=WORK.parents[3] if IN_PACK else WORK.parents[1]/'tmp/listing-20744-20261013'
PACK=REPO/'assets/production/VA-215/b01-20261020'
SRC=PACK/'sources'
OUT=REPO/'product generated photo/VA-215'
W=H=2000
NAVY='#102E55'; BLUE='#1265C7'; INK='#102A47'; MUTED='#536C88'
REG='C:/Windows/Fonts/arial.ttf'; BOLD='C:/Windows/Fonts/arialbd.ttf'
NOW=datetime.now(timezone.utc).isoformat()
if IN_PACK and (OUT/'product-facts.json').exists():
    # Rebuilds retain the original research/approval recording time; rendering
    # alone is neither a new ERP lookup nor a new user style approval.
    NOW=json.loads((OUT/'product-facts.json').read_text(encoding='utf-8-sig')).get('updatedAtUtc',NOW)
for p in (PACK,SRC,OUT,OUT/'unbranded',PACK/'layers',PACK/'masks'):
    p.mkdir(parents=True,exist_ok=True)
if not IN_PACK:
    for n in ['official-01.png','official-02.png','official-03.png','official-06.png','official-07.png','office-background.png','screen-art.png','official-image-urls.txt']:
        shutil.copyfile(WORK/'sources'/n,SRC/n)
    shutil.copyfile(WORK/'VA-215-style-preview-v1.png',PACK/'approved-style-preview.png')
    shutil.copyfile(WORK/'generation-prompt.txt',PACK/'preview-prompt.txt')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def font(s,b=False): return ImageFont.truetype(BOLD if b else REG,s)
def text(im,xy,s,size=48,color=INK,b=False,spacing=12):
    ImageDraw.Draw(im).multiline_text(xy,s,font=font(size,b),fill=color,spacing=spacing)
def save(im,p):
    kw={'dpi':(96,96),'icc_profile':ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()}
    im.convert('RGB').save(p,quality=97,subsampling=0,**kw) if str(p).endswith('.jpg') else im.convert('RGBA').save(p,**kw)
def layer(n): return Image.open(SRC/n).convert('RGBA')
def fit(im,box):
    x,y,w,h=box; k=min(w/im.width,h/im.height,1)
    z=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.LANCZOS)
    return z,(round(x+(w-z.width)/2),round(y+(h-z.height)/2))
def paste(im,z,box,shadow=False):
    z,(x,y)=fit(z,box)
    if shadow:
        sh=Image.new('RGBA',im.size); d=ImageDraw.Draw(sh)
        d.ellipse((x+z.width*.07,y+z.height*.94,x+z.width*.95,y+z.height*1.01),fill=(15,32,50,38))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    im.alpha_composite(z,(x,y)); return [x,y,z.width,z.height]
def canvas():
    im=Image.new('RGBA',(W,H),'#F4F8FD');d=ImageDraw.Draw(im)
    for y in range(420,H):
        a=(y-420)/(H-420);d.line((0,y,W,y),fill=(round(244-15*a),round(248-12*a),round(253-5*a),255))
    d.line((100,445,1900,445),fill='#D5E2F2',width=2)
    return im
def header(im,kicker,title,sub=''):
    text(im,(100,70),kicker,30,BLUE,True)
    text(im,(100,135),title,86,INK,True,10)
    if sub:text(im,(103,350 if '\n' in title else 310),sub,36,MUTED)
def pill(im,xy,s,w=500):
    x,y=xy; ImageDraw.Draw(im).rounded_rectangle((x,y,x+w,y+100),radius=24,fill='white',outline='#D2E2F4',width=2)
    text(im,(x+25,y+24),s,40,INK,True)
def solve(mat,rhs):
    a=[list(map(float,row))+[float(v)] for row,v in zip(mat,rhs)]
    for c in range(len(rhs)):
        r=max(range(c,len(rhs)),key=lambda r:abs(a[r][c]));a[c],a[r]=a[r],a[c]
        s=a[c][c];a[c]=[v/s for v in a[c]]
        for r in range(len(rhs)):
            if r!=c:
                s=a[r][c];a[r]=[v-s*t for v,t in zip(a[r],a[c])]
    return [r[-1] for r in a]
def warp(art,points,size):
    # Inverse destination-to-source homography, with a measured LCD polygon mask.
    src=[(0,0),(art.width,0),(art.width,art.height),(0,art.height)]
    m=[];v=[]
    for (x,y),(u,z) in zip(points,src):
        m += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-z*x,-z*y]];v += [u,z]
    z=art.transform(size,Image.Transform.PERSPECTIVE,solve(m,v),Image.Resampling.BICUBIC)
    mask=Image.new('L',size);ImageDraw.Draw(mask).polygon(points,fill=255);z.putalpha(mask)
    return z,mask

front=layer('official-06.png');angle=layer('official-07.png');art=layer('screen-art.png')
LCD={'front':[(43,159),(2780,159),(2780,1702),(43,1702)],
     'angle':[(66,72),(2530,240),(2595,1687),(136,1807)]}
masters={};lcd_masks={}
for name,base in [('front',front),('angle',angle)]:
    z,mask=warp(art,LCD[name],base.size);base=base.copy();base.alpha_composite(z)
    masters[name]=base;lcd_masks[name]=mask
    base.save(PACK/'layers'/f'{name}-blue.png');mask.save(PACK/'masks'/f'{name}-lcd.png')

placements={};recipe_slots={}
def pt(n,im,zones):
    name=f'PT{n:02}.png';save(im,OUT/'unbranded'/name)
    protected=[{'label':label,'x':int(x),'y':int(y),'width':int(w),'height':int(h)} for label,x,y,w,h in zones]
    placements[name]={'style':'transparent','x':1680,'y':85,'width':220,'height':220,'protectedZones':protected}
    recipe_slots[name]={'protectedZones':protected,'logoVisibleBox':[1680,85,220,220]}

# Strict choice uses an untouched official front photo, including its original screen.
im=Image.new('RGBA',(W,H),'white');bbox=paste(im,front,(40,80,1920,1840),True);save(im,OUT/'MAIN-STRICT.jpg')
recipe_slots['MAIN-STRICT.jpg']={'productBox':bbox,'method':'ORIGINAL_PHOTO','screen':'OEM original'}

for name,key,asset,wid in [('MAIN-ENHANCED-FRONT-CANDIDATE.png','front','windows-11-pro-lockup.png',650),('MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png','angle','windows-11-pro-package.png',440)]:
    base=masters[key].copy();identity=Image.open(REPO/'assets/branding'/asset).convert('RGBA')
    shade=Image.new('RGBA',art.size);ds=ImageDraw.Draw(shade)
    for x in range(art.width):
        a=round(215*max(0,1-x/(art.width*.78)))
        ds.line((x,0,x,art.height),fill=(5,25,57,a))
    shaded=art.copy();shaded.alpha_composite(shade)
    shaded_lcd,_=warp(shaded,LCD[key],base.size);base.alpha_composite(shaded_lcd)
    identity.thumbnail((wid,550),Image.Resampling.LANCZOS)
    # All marketing text and identity pixels remain within the real screen.
    if key=='front':
        pos=(1850,1130);text(base,(180,380),'WORK,\nBEAUTIFULLY\nIN VIEW.',170,'white',True,20)
    else:
        pos=(1880,1130);text(base,(240,420),'ROOM FOR\nYOUR NEXT\nBIG IDEA.',145,'white',True,18)
    base.alpha_composite(identity,pos)
    footprint=Image.new('L',base.size);footprint.paste(identity.getchannel('A'),pos)
    from PIL import ImageChops
    assert ImageChops.subtract(footprint,lcd_masks[key]).getbbox() is None,'Windows outside LCD'
    base.save(PACK/'layers'/f'{key}-enhanced.png')
    im=Image.new('RGBA',(W,H),'white');bbox=paste(im,base,(40,80,1920,1840),True);save(im,OUT/name)
    recipe_slots[name]={'productBox':bbox,'lcdPolygon':LCD[key],'windowsSource':asset,'windowsPositionInMaster':list(pos),'windowsSizeInMaster':list(identity.size),'windowsLcdBoundary':'PIXEL_MASK_CONTAINED'}

im=canvas();header(im,'DELL PRO 24 ALL-IN-ONE','One computer.\nA clearer desk.','An integrated desktop for an organized workspace.')
b=paste(im,masters['angle'],(100,520,1800,1390),True)
pt(1,im,[('PRODUCT_SILHOUETTE_SET',*b),('HEADLINE',100,60,1450,305)])

im=Image.open(SRC/'office-background.png').convert('RGBA').resize((W,H),Image.Resampling.LANCZOS)
veil=Image.new('RGBA',im.size);dv=ImageDraw.Draw(veil)
for y in range(540):dv.line((0,y,W,y),fill=(245,250,255,round(230*(1-y/540))))
im.alpha_composite(veil)
header(im,'YOUR EVERYDAY WORKSPACE','Make room\nfor your work.')
b=paste(im,masters['angle'],(150,520,1700,1430),True)
pt(2,im,[('PRODUCT_SILHOUETTE_SET',*b),('HEADLINE',100,60,1450,305)])

im=canvas();header(im,'BASE CONFIGURATION','The essentials, together.','Dell Pro 24 All-in-One QC24251')
b=paste(im,masters['front'],(90,540,1050,1320),True)
for j,(label,val) in enumerate([('PROCESSOR','Intel Core i5-14500T'),('GRAPHICS','Intel Integrated Graphics'),('MEMORY','8GB DDR5'),('STORAGE','256GB Gen 4 SSD')]):
    y=540+j*220;ImageDraw.Draw(im).rounded_rectangle((1200,y,1900,y+185),radius=22,fill='white')
    text(im,(1230,y+25),label,28,BLUE,True)
    text(im,(1230,y+80),val,52 if j<2 else 62,INK,True)
win=Image.open(REPO/'assets/branding/windows-11-pro-lockup.png').convert('RGBA');win.thumbnail((600,260));im.alpha_composite(win,(1240,1470))
pt(3,im,[('PRODUCT_SILHOUETTE_SET',*b),('HEADLINE',100,60,1450,305),('SPECIFICATIONS',1200,540,700,1220)])

im=canvas();header(im,'DISPLAY','Room to focus.','A 23.8-inch Full HD display, built into your desktop.')
b=paste(im,masters['front'],(140,475,1720,1310),True)
for x,s,w in [(130,'1920 × 1080',610),(790,'60Hz',360),(1200,'Non-touch',670)]:pill(im,(x,1810),s,w)
pt(4,im,[('PRODUCT_SILHOUETTE_SET',*b),('HEADLINE',100,60,1450,305),('DISPLAY_FACTS',130,1810,1740,100)])

im=canvas();header(im,'AN ORIGINAL WORKFLOW','From ideas to action.','Plan. Create. Review. Keep your day moving.')
for x,num,s in [(160,'01','PLAN'),(800,'02','CREATE'),(1440,'03','REVIEW')]:
    d=ImageDraw.Draw(im);d.rounded_rectangle((x,520,x+400,790),radius=28,fill='white',outline='#D0E2F7',width=2)
    text(im,(x+35,550),num,40,BLUE,True);text(im,(x+35,650),s,56,INK,True)
    if x<1400:d.line((x+420,655,x+590,655),fill=BLUE,width=5);d.polygon([(x+590,655),(x+565,640),(x+565,670)],fill=BLUE)
b=paste(im,masters['front'],(400,880,1200,1030),True)
pt(5,im,[('PRODUCT_SILHOUETTE_SET',*b),('HEADLINE',100,60,1450,305),('WORKFLOW',160,520,1680,270)])

im=Image.new('RGBA',(W,H),'white');header(im,'INPUT DETAILS','A familiar way to work.','Classic Dell keyboard and mouse styling.')
keys=front.crop((0,2390,3277,2725));b=paste(im,keys,(80,820,1840,600),True)
text(im,(140,610),'FULL-SIZE KEYBOARD',40,BLUE,True)
text(im,(140,1480),'Number pad',47,INK,True);text(im,(780,1480),'Wireless input',47,INK,True);text(im,(1430,1480),'Mouse',47,INK,True)
pt(6,im,[('PRODUCT_SILHOUETTE_INPUTS',*b),('HEADLINE',100,60,1450,305),('INPUT_COPY',140,1480,1660,100)])

im=canvas();header(im,'CAMERA DESIGN','There when you need it.','An integrated pop-up camera above the display.')
b=paste(im,masters['angle'],(700,650,1200,1200),True)
cam=masters['front'].crop((1150,0,1670,380));ImageDraw.Draw(im).rounded_rectangle((110,620,690,1220),radius=30,fill='white')
cb=paste(im,cam,(140,680,520,380))
text(im,(150,1130),'Pop-up camera',40,INK,True)
pt(7,im,[('PRODUCT_SILHOUETTE_SET',*b),('PRODUCT_SILHOUETTE_CAMERA',*cb),('HEADLINE',100,60,1450,305)])

im=canvas();header(im,'PHYSICAL CONNECTIVITY','Connect your workday.','Real QC24251 ports, shown from the official product views.')
# Rear crop retains native connector geometry; leaders terminate on real openings.
rear=layer('official-01.png');crop=(800,1100,2460,1600);r=rear.crop(crop)
rb=paste(im,r,(170,600,1660,500));rx,ry,rw,rh=rb;scale=rw/r.width
def lead(label,pos,endpoint):
    text(im,pos,label,36,INK,True);d=ImageDraw.Draw(im)
    tx=pos[0]+60;ty=pos[1]+55;ex,ey=endpoint
    d.line([(tx,ty),(tx,(ty+ey)/2),(ex,(ty+ey)/2),(ex,ey)],fill=BLUE,width=3);d.ellipse((ex-6,ey-6,ex+6,ey+6),fill=BLUE)
def rear_point(x,y):return (rx+(x-crop[0])*scale,ry+(y-crop[1])*scale)
lead('DisplayPort',(170,455),rear_point(1365,1350))
lead('4 × USB-A',(740,455),rear_point(1490,1350))
lead('RJ45 Ethernet',(1320,455),rear_point(1950,1350))
right=layer('official-02.png').crop((1460,2300,1910,2660));left=layer('official-03.png').crop((740,2300,1130,2630))
br=paste(im,right,(150,1280,450,360));bl=paste(im,left,(780,1280,390,330))
text(im,(125,1160),'Right: USB-A',36,INK,True);text(im,(720,1160),'Left: headset jack',36,INK,True)
bottom=rear.crop((100,1600,780,1791));bb=paste(im,bottom,(1240,1310,680,191))
text(im,(1230,1160),'Below display',36,INK,True)
text(im,(1240,1560),'USB-C + SD card slot',34,INK,True)
pill(im,(130,1800),'Wi-Fi',650);pill(im,(850,1800),'Bluetooth',1020)
pt(8,im,[('PRODUCT_SILHOUETTE_REAR',*rb),('PRODUCT_SILHOUETTE_RIGHT',*br),('PRODUCT_SILHOUETTE_LEFT',*bl),('PRODUCT_SILHOUETTE_BOTTOM',*bb),('HEADLINE',100,60,1450,305)])

plan={'schemaVersion':3,'brand':'Dell','logoRole':'OEM base-product identifier','minimumClearancePx':50,'minimumComponentSeparationPx':50,'thumbnailReviewSizePx':200,'logoVisibilityMode':'STANDARD','logoAssetSourceUrl':'https://www.dell.com/','placements':placements}
write(OUT/'logo-placement.json',plan)
facts={'internalId':'VA-215','identity':{'internalId':'VA-215','oemBrand':'Dell','oemModel':'Dell Pro 24 All-in-One QC24251','formFactor':'AIO','color':'Black'},
       'selectedBaseConfiguration':{'configurationId':'VA-215-PA-222-base','cpu':'Intel Core i5-14500T','graphics':'Intel Integrated Graphics','ram':{'value':8,'unit':'GB','type':'DDR5'},'internalSsd':{'value':256,'unit':'GB','interface':'Gen 4'},'os':'Windows 11 Pro','soldApplicabilityBasis':'Image-only base selection: exact VA-215 linked current physical SKU PA-222; user directed ERP lookup; no upgrade variant selected.'},
       'display':{'diagonalInches':23.8,'resolution':'1920x1080','refreshRateHz':60,'touch':False},'wireless':{'wifi':True,'bluetooth':True,'generation':'UNSPECIFIED'},
       'inputDevices':{'keyboard':'Dell classic full-size black representative reference','mouse':'Dell classic black representative reference','wireless':True,'sku':'UNSPECIFIED','basis':'User explicitly approved corresponding-brand classic treatment; VA-215 product comment states WIRELESS KEYBOARD & MOUSE.'},
       'sources':[{'url':'https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/products/40215','scope':'Exact VA-215 identity, display, wireless, input and stand comment','checkedAtUtc':NOW},{'url':'https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/computers?q=QC24251','scope':'VA-215 → PA-222 current physical SKU; 8GB DDR5, 256GB GEN 4, Windows 11 Pro; non-touch. VA-223/PA-223 touch SKU excluded.','checkedAtUtc':NOW},{'url':'https://www.dell.com/en-us/shop/Desktop/spd/DellPro24AllinOne35WQC24251/qc24251_reg_01','scope':'Exact-model official chassis, display, ports, camera; configurable capacities not imported as sold values.','checkedAtUtc':NOW}],
       'serial_research':{'outcome':'NOT_REQUIRED','reason':'Image-only work: current exact ERP physical configuration PA-222 and official views establish all depicted facts. No FCC, radio model, per-unit warranty, upgrade history or as-built serial claims are made.','checkedAtUtc':NOW},'oem_brand_authorization_status':'USER_CONFIRMED_CATALOG_WIDE','updatedAtUtc':NOW}
write(OUT/'product-facts.json',facts)
recipe={'version':'VA-215-b01-v1','canvas':[W,H],'formFactor':'AIO','boundaryMode':'SCREEN_ONLY','method':'ORIGINAL_PHOTO_WITH_ORIGINAL_AI_ART_AND_DETERMINISTIC_TYPE','productGeometryRedrawn':False,'font':{'regular':REG,'bold':BOLD},'lcdPolygonsInSourcePixels':LCD,'slots':recipe_slots,'sourceHashes':{p.name:sha(p) for p in SRC.glob('*.png')},'renderCommand':'python assets/production/VA-215/b01-20261020/build-gallery.py','artNotes':'Built-in imagegen original office background and LCD abstract art. No generated hardware or final logos.'}
write(PACK/'recipe.json',recipe)
write(OUT/'style-lock.json',{'style_approval_status':'APPROVED','approved_style_id':'B01','approved_supporting_gallery_pack':'BG01','profile':'navy-technical-v1','palette':['navy','white','sky blue'],'approvalSource':'Direct user reply: 采用这个风格，继续制作整套','approvalRecordedAtUtc':NOW,'approvedPreviewSha256':sha(PACK/'approved-style-preview.png'),'recipePath':'assets/production/VA-215/b01-20261020/recipe.json','recipeStatus':'BUILT','mainContentBoundary':'SCREEN_ONLY','requiredMotifs':['office workflow','classic Dell keyboard and mouse'],'forbiddenMotifs':['other external devices','invented ports','unverified capacity variants']})
write(OUT/'delivery-status.json',{'internalId':'VA-215','galleryState':'AWAITING_VISUAL_REVIEW','deliveryState':'LOCAL_PRODUCTION','deliveryScope':'FULL_GALLERY','currentQaPass':False,'publicationEligibility':'NOT_ASSESSED','reason':'New source-bound images require current-byte manual review and remote delivery.'})
write(PACK/'source-rights.json',{'oemAuthorization':'USER_CONFIRMED_CATALOG_WIDE','officialPage':facts['sources'][2]['url'],'officialGalleryUrls':(SRC/'official-image-urls.txt').read_text().splitlines(),'assets':recipe['sourceHashes'],'inputDeviceTreatment':'USER_APPROVED_CLASSIC_SAME_BRAND_REPRESENTATIVE','syntheticPeople':False,'generationMode':'built-in image_gen','generatedAssets':['office-background.png','screen-art.png'],'checkedAtUtc':NOW})
sys.path.insert(0,str(REPO/'scripts'))
import gallery_engine as g
g.finalize(OUT,REPO/'assets/branding/dell-logo-blue-transparent.png','Dell',PACK/'gallery-contact.png')
thumb=Image.new('RGB',(4*240,3*275),'#E7EDF5')
for i,n in enumerate(g.NAMES):
    z=Image.open(OUT/n).convert('RGB');z.thumbnail((200,200));x=(i%4)*240+20;y=(i//4)*275+12
    thumb.paste(z,(x,y));ImageDraw.Draw(thumb).text((x,y+210),n.replace('MAIN-ENHANCED-','').replace('-CANDIDATE',''),font=font(13,True),fill=INK)
thumb.save(PACK/'thumbnails-200px.png')
write(PACK/'output-hashes.json',{n:sha(OUT/n) for n in g.NAMES})
print(json.dumps({'output':str(OUT),'images':len(g.NAMES),'contact':str(PACK/'gallery-contact.png')},indent=2))
