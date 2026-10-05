#!/usr/bin/env python3
"""Portable deterministic image operations; review evidence is supplied by humans, never inferred."""
import argparse, hashlib, json, math, os, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone
from collections import deque
from PIL import Image, ImageChops, ImageFilter, ImageDraw, PngImagePlugin
MAIN=['MAIN-STRICT.jpg','MAIN-ENHANCED-FRONT-CANDIDATE.png','MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png']
PT=[f'PT{i:02}.png' for i in range(1,9)]
NAMES=MAIN+PT

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); tmp=p.with_name(p.name+'.tmp'); tmp.write_text(json.dumps(obj,indent=2)+'\n'); tmp.replace(p)
def save(im,path,fmt='PNG',metadata=None):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); tmp=p.with_name(p.name+'.tmp')
    if fmt.upper() in ('JPEG','JPG'): im=im.convert('RGB')
    extra={}
    if metadata and fmt.upper()=='PNG':
        info=PngImagePlugin.PngInfo()
        for k,v in metadata.items(): info.add_text(k,str(v))
        extra['pnginfo']=info
    im.save(tmp,format=fmt.upper(),**extra,**({'quality':95} if fmt.upper()=='JPEG' else {})); tmp.replace(p)
def load(path):
    with Image.open(path) as im: im.load(); return im.convert('RGBA')
def check_image_size(size):
    """Amazon US general pixel range only; never a publication/visual PASS."""
    if min(size)<=0 or not 500<=max(size)<=10000:
        raise ValueError(f'Image longest side must be 500–10000 pixels; got {size}')
    return {'width':size[0],'height':size[1],'zoomEligibleBySize':max(size)>=1000}

def normalize(src,out,size=None,fmt='PNG'):
    im=load(src); size=max(im.size) if size is None else size
    check_image_size((size,size)); scale=size/max(im.size)
    if scale>1: raise ValueError('Low-resolution input cannot be upscaled; regenerate the source.')
    wh=tuple(max(1,round(x*scale)) for x in im.size); im=im.resize(wh,Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(size,size),'white'); canvas.alpha_composite(im,((size-wh[0])//2,(size-wh[1])//2)); save(canvas,out,fmt)
def remove_background(src,out,tolerance=8,full=42):
    im=load(src); px=im.load(); w,h=im.size
    # Infer neutral background from the majority corner color; flood only connected,
    # similarly colored pixels. Thus black ink on white and white ink on black survive.
    corners=[px[x,y] for x,y in ((0,0),(w-1,0),(0,h-1),(w-1,h-1))]
    opaque_neutral=[c[:3] for c in corners if c[3] and max(c[:3])-min(c[:3])<=tolerance]
    background=max(opaque_neutral,key=opaque_neutral.count) if opaque_neutral else None
    def eligible(x,y):
        r,g,b,a=px[x,y]
        return a==0 or (background is not None and max(r,g,b)-min(r,g,b)<=tolerance and max(abs(v-base) for v,base in zip((r,g,b),background))<=max(tolerance,20))
    seen=set(); q=deque()
    for x,y in [(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]:
        if eligible(x,y) and (x,y) not in seen: seen.add((x,y)); q.append((x,y))
    while q:
        x,y=q.popleft(); r,g,b,a=px[x,y]; px[x,y]=(r,g,b,0)
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<w and 0<=yy<h and (xx,yy) not in seen and eligible(xx,yy): seen.add((xx,yy)); q.append((xx,yy))
    save(im,out)
def overlay(src,asset,out,x,y,w,h,style='Flat',padding=18,mask=None):
    with Image.open(src) as original:
        if original.info.get('galleryOverlayApplied')=='true': raise ValueError('Already composited: use clean source')
    im=load(src); mark=load(asset)
    if min(w,h)<=0 or x<0 or y<0 or x+w>im.width or y+h>im.height: raise ValueError('Overlay outside canvas')
    if abs(w/h-mark.width/mark.height)/(mark.width/mark.height)>.02: raise ValueError('Overlay distorts official asset aspect ratio')
    provenance=Path(str(src)+'.overlay.json')
    if provenance.exists() and read(provenance).get('outputSha256')==digest(src): raise ValueError('Already composited: use clean source')
    clip=None
    if style=='ScreenGlow':
        if not mask: raise ValueError('ScreenGlow requires LcdMaskPath')
        clip=load(mask).convert('L')
        if clip.size!=im.size or sum(clip.histogram()[1:255]) != 0: raise ValueError('LCD mask must be binary and match canvas')
        area=Image.new('L',im.size); area.paste(mark.resize((w,h),Image.Resampling.LANCZOS).getchannel('A'),(x,y))
        if ImageChops.subtract(area,clip).getbbox(): raise ValueError('Windows asset extends outside LCD')
    layer=Image.new('RGBA',im.size)
    if style=='ScreenGlow':
        glow=Image.new('RGBA',im.size); ImageDraw.Draw(glow).rounded_rectangle((x-padding,y-padding,x+w+padding,y+h+padding),radius=20,fill=(90,130,220,65)); glow=glow.filter(ImageFilter.GaussianBlur(max(1,padding/2)))
        glow.putalpha(ImageChops.multiply(glow.getchannel('A'),clip)); layer.alpha_composite(glow)
    layer.alpha_composite(mark.resize((w,h),Image.Resampling.LANCZOS),(x,y))
    if clip: layer.putalpha(ImageChops.multiply(layer.getchannel('A'),clip))
    input_hash=digest(src); im.alpha_composite(layer); save(im,out,metadata={'galleryOverlayApplied':'true','galleryOverlayAssetSha256':digest(asset)})
    write(str(out)+'.overlay.json',{'schemaVersion':3,'inputSha256':input_hash,'outputSha256':digest(out),'assetSha256':digest(asset),'lcdMaskSha256':digest(mask) if mask else None})
def rect(p):
    x,y,w,h=(int(p[k]) for k in ('x','y','width','height'))
    if min(w,h)<=0: raise ValueError('Invalid rectangle')
    return x,y,x+w,y+h

def check_separation(box,zones,size,requested):
    gap=max(32,math.ceil(.025*min(size)),requested)
    x,y,r,b=box
    if x<gap or y<gap or r+gap>size[0] or b+gap>size[1]: raise ValueError('Logo canvas clearance violation')
    for z in zones:
        zx,zy,zr,zb=rect(z)
        if x-gap<zr and r+gap>zx and y-gap<zb and b+gap>zy: raise ValueError('Logo protected-zone separation violation')
    return gap

def badges(directory,asset,planpath,out=None,brand=None,slots=None):
    p=Path(directory); dest=Path(out or directory); plan=read(planpath)
    if not plan.get('brand') or (brand and plan['brand']!=brand): raise ValueError('Unverified brand')
    if plan.get('logoRole')!='OEM base-product identifier': raise ValueError('Invalid logo role')
    mark=load(asset); bbox=mark.getchannel('A').getbbox()
    if not bbox: raise ValueError('Empty logo')
    if mark.getchannel('A').getextrema()[0]==255: raise ValueError('Use approved transparent asset')
    mark=mark.crop(bbox); entries={}
    old=dest/'logo-qa.json'
    if slots and old.exists(): entries={e['file']:e for e in read(old).get('images',[])}
    prepared=[]
    for name in slots or PT:
        if name not in PT: raise ValueError('Badges apply only to PT slots')
        source=p/'unbranded'/name; im=load(source); cfg=plan['placements'][name]
        if cfg.get('style')!='transparent': raise ValueError('Portable compositor requires transparent treatment; badge exception needs separate approved renderer')
        zones=cfg.get('protectedZones',[])
        if not zones or not any(z.get('label','').startswith('PRODUCT_SILHOUETTE') for z in zones): raise ValueError('Missing product silhouette protection')
        box=rect(cfg); x,y,r,b=box; w,h=r-x,b-y
        if abs(w/h-mark.width/mark.height)/(mark.width/mark.height)>.02: raise ValueError('Logo aspect ratio mismatch after alpha trimming')
        gap=check_separation(box,zones,im.size,max(int(plan.get('minimumClearancePx',0)),int(plan.get('minimumComponentSeparationPx',0))))
        thumb=int(plan.get('thumbnailReviewSizePx',200))
        if thumb!=200: raise ValueError('Thumbnail review must be exactly 200px')
        factor=thumb/max(im.size)
        long=max(w,h)*factor; short=min(w,h)*factor
        if long<20 or max(w,h)>.12*min(im.size): raise ValueError('Logo visible long edge threshold')
        wide=plan.get('logoVisibilityMode')=='ASPECT_RATIO_WORDMARK'
        if wide and not plan.get('logoAssetSourceUrl'): raise ValueError('Wordmark requires official source URL')
        if wide and max(mark.size)/min(mark.size)<=2.4: raise ValueError('Wide-wordmark mode requires measured aspect ratio >2.4')
        if short<(20*min(mark.size)/max(mark.size) if wide else 10): raise ValueError('Logo visible short edge threshold')
        im.alpha_composite(mark.resize((w,h),Image.Resampling.LANCZOS),(x,y)); prepared.append((name,im,source,gap))
    for name,im,source,gap in prepared:
        save(im,dest/name); entries[name]={'file':name,'finalImageSha256':digest(dest/name),'unbrandedSourceSha256':digest(source),'separationPx':gap,'geometryGate':'PASS','sourceVerification':'LOCAL_BYTES_VERIFIED','commandRecord':'gallery_engine.py badges (from clean unbranded master)'}
    # Geometry cannot prove visual quality. A human must supply hash-bound evidence for final PASS.
    write(dest/'logo-qa.json',{'schemaVersion':3,'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'brand':plan['brand'],'result':'AWAITING_VISUAL_REVIEW','logoAssetSha256':digest(asset),'logoAssetPath':os.path.relpath(Path(asset).resolve(),dest.resolve()),'visibleLogoAspectRatio':mark.width/mark.height,'placementPlanSha256':digest(planpath),'images':list(entries.values())})

def evidence(path,names,directory):
    report=read(path)
    if report.get('schemaVersion',0)<3 or report.get('result')!='PASS' or not report.get('reviewer') or not report.get('reviewedAtUtc'): raise ValueError(f'Missing current human review evidence: {path}')
    entries=report.get('images',[])
    if len(entries)!=len(names) or {e.get('file') for e in entries}!=set(names): raise ValueError(f'Incomplete evidence: {path}')
    for name in names:
        entry=next(e for e in entries if e['file']==name)
        if entry.get('sha256','').lower()!=digest(Path(directory)/name) or entry.get('result')!='PASS' or not entry.get('notes'): raise ValueError(f'Stale or incomplete evidence: {name}')
    return report

def validate(directory,brand=None,legacy=False,require_final=True,allow_quarantined=False):
    p=Path(directory)
    sizes={}
    status=p/'delivery-status.json'
    if not allow_quarantined and status.exists() and read(status).get('galleryState')=='LEGACY_QUARANTINED': raise ValueError('Gallery is LEGACY_QUARANTINED; regenerate and supply current review evidence before delivery')
    for name in NAMES:
        with Image.open(p/name) as original:
            original.load()
            expected_format='JPEG' if name.endswith('.jpg') else 'PNG'
            if original.format!=expected_format or original.mode not in ('RGB','RGBA'): raise ValueError(f'{name}: expected actual {expected_format} RGB/RGBA image')
            if original.mode=='RGBA' and original.getchannel('A').getextrema()[0]!=255: raise ValueError('All final images must have an opaque background')
        im=load(p/name)
        check_image_size(im.size); sizes[name]=im.size
    unexpected=[f.name for f in p.iterdir() if f.is_file() and f.suffix.lower() in ('.png','.jpg','.jpeg','.gif','.tif','.tiff') and f.name not in NAMES]
    if unexpected: raise ValueError(f'Unexpected canonical images: {unexpected}')
    qa=read(p/'logo-qa.json')
    if qa.get('schemaVersion',0)<3:
        if legacy:
            print('LEGACY_SCHEMA_DIAGNOSTIC_ONLY: schema2 cannot authorize current delivery')
        raise ValueError('Legacy QA is historical only; schema3 current hash-bound evidence is required')
    if brand and qa.get('brand')!=brand: raise ValueError('Brand mismatch')
    if not qa.get('generatedAtUtc'): raise ValueError('Missing QA generation time')
    entries=qa.get('images',[])
    if len(entries)!=8 or {e['file'] for e in entries}!=set(PT): raise ValueError('Incomplete logo QA')
    for e in entries:
        if e.get('geometryGate')!='PASS' or e.get('finalImageSha256','').lower()!=digest(p/e['file']): raise ValueError('Stale logo QA')
        source=p/'unbranded'/e['file']
        if not e.get('unbrandedSourceSha256') or not e.get('commandRecord'): raise ValueError('Missing source provenance')
        if source.exists() and e['unbrandedSourceSha256'].lower()!=digest(source): raise ValueError('Stale unbranded source')
        if not source.exists(): print(f"SOURCE_HASH_RECORDED_NOT_LOCALLY_REPLAYED: {e['file']}")
    plan=read(p/'logo-placement.json')
    if plan.get('brand')!=qa.get('brand'): raise ValueError('Plan/QA brand mismatch')
    if qa.get('placementPlanSha256','').lower()!=digest(p/'logo-placement.json'): raise ValueError('Stale placement plan')
    asset=(p/qa['logoAssetPath']).resolve()
    if digest(asset)!=qa.get('logoAssetSha256'): raise ValueError('Stale logo asset')
    logo=load(asset); bbox=logo.getchannel('A').getbbox()
    if not bbox: raise ValueError('Empty visible logo')
    vw,vh=bbox[2]-bbox[0],bbox[3]-bbox[1]
    for n in PT:
        cfg=plan['placements'][n]; box=rect(cfg)
        check_separation(box,cfg['protectedZones'],sizes[n],max(int(plan.get('minimumClearancePx',0)),int(plan.get('minimumComponentSeparationPx',0))))
        w,h=box[2]-box[0],box[3]-box[1]
        if abs(w/h-vw/vh)/(vw/vh)>.02: raise ValueError('Current logo geometry distorts asset')
        scale=200/max(sizes[n])
        if int(plan.get('thumbnailReviewSizePx',200))!=200: raise ValueError('Thumbnail review must be exactly 200px')
        wide=plan.get('logoVisibilityMode')=='ASPECT_RATIO_WORDMARK'
        if max(w,h)*scale<20 or max(w,h)>.12*min(sizes[n]) or (wide and max(vw,vh)/min(vw,vh)<=2.4) or min(w,h)*scale<(20*min(vw,vh)/max(vw,vh) if wide else 10): raise ValueError('Current logo visibility threshold failed')
    evidence(p/'visual-review.json',NAMES,p); evidence(p/'semantic-review.json',PT,p)
    if require_final:
        report=read(p/'final-image-qa.json')
        if report.get('schemaVersion',0)<3 or report.get('result')!='PASS': raise ValueError('Missing final QA')
        expected={n:digest(p/n) for n in NAMES}; actual={e['file']:e['sha256'].lower() for e in report.get('images',[])}
        if actual!=expected or len(report.get('images',[]))!=11: raise ValueError('Stale final QA image hashes')
        for filename,key in [('logo-qa.json','logoQaSha256'),('visual-review.json','visualReviewSha256'),('semantic-review.json','semanticReviewSha256')]:
            if report.get(key)!=digest(p/filename): raise ValueError('Stale final review binding')
    return [{'file':n,**check_image_size(sizes[n]),'sha256':digest(p/n)} for n in NAMES]

def finalize(directory,asset,brand,contact,size=None,skip=False,slots=None):
    p=Path(directory); selected=slots or NAMES
    if any(n not in NAMES for n in selected): raise ValueError('Unknown slot')
    # Preflight every selected source before changing any bytes.
    for n in selected:
        src=p/'unbranded'/n if n in PT else p/n
        dimensions=load(src).size; check_image_size(dimensions)
        if size is not None:
            check_image_size((size,size))
            if max(dimensions)<size: raise ValueError('Regenerate low-resolution source before finalization')
    # Native dimensions by default; resizing is explicitly opt-in.
    if not skip and size is not None:
        for n in selected: normalize(p/'unbranded'/n if n in PT else p/n,p/'unbranded'/n if n in PT else p/n,size,'JPEG' if n.endswith('.jpg') else 'PNG')
    selected_pt=[n for n in selected if n in PT]
    if selected_pt: badges(p,asset,p/'logo-placement.json',brand=brand,slots=selected_pt)
    contact_sheet(p,contact)
    print('PREPARED: supply current hash-bound visual-review.json and semantic-review.json, then run accept; no delivery PASS claimed.')

def accept(directory,brand=None,slots=None):
    p=Path(directory)
    if slots: return accept_partial(p,slots,brand)
    images=validate(p,brand,require_final=False,allow_quarantined=True)
    qa=read(p/'logo-qa.json'); qa.update(result='PASS',visualReviewSha256=digest(p/'visual-review.json')); write(p/'logo-qa.json',qa)
    write(p/'final-image-qa.json',{'schemaVersion':3,'result':'PASS','generatedAtUtc':datetime.now(timezone.utc).isoformat(),'images':images,'logoQaSha256':digest(p/'logo-qa.json'),'visualReviewSha256':digest(p/'visual-review.json'),'semanticReviewSha256':digest(p/'semantic-review.json')})
    if (p/'delivery-status.json').exists():
        status=read(p/'delivery-status.json')
        status.update(galleryState='CURRENT_REVIEWED',deliveryState='READY_FOR_GITHUB_DELIVERY',
                      deliveryScope='FULL_GALLERY',currentQaPass=True,
                      reason='Current full-gallery bytes and supplied hash-bound reviews passed local acceptance; remote delivery remains unverified.',
                      nextRun='Commit/push, await applicable CI and verify remote file hashes before claiming GITHUB_DELIVERY_VERIFIED.')
        for key in ('verifiedRemoteCommit','githubDeliveryVerifiedAtUtc','remoteDeliveryRecord'):
            status.pop(key,None)
        write(p/'delivery-status.json',status)

def partial_checks(p,slots,brand=None):
    if not slots or any(n not in NAMES for n in slots) or len(set(slots))!=len(slots): raise ValueError('Invalid partial scope')
    evidence(p/'visual-review.json',slots,p); evidence(p/'semantic-review.json',slots,p)
    inventory={n:digest(p/n) for n in NAMES}
    if read(p/'semantic-review.json').get('galleryInventorySha256')!=inventory: raise ValueError('Partial semantic review must bind all current gallery bytes')
    selected_pt=[n for n in slots if n in PT]
    if selected_pt:
        qa=read(p/'logo-qa.json'); plan=read(p/'logo-placement.json')
        if qa.get('schemaVersion',0)<3 or qa.get('brand')!=plan.get('brand') or (brand and qa.get('brand')!=brand): raise ValueError('Partial logo brand/schema mismatch')
        if qa.get('placementPlanSha256')!=digest(p/'logo-placement.json'): raise ValueError('Partial logo plan stale')
        logo=load(p/qa['logoAssetPath']); box=logo.getchannel('A').getbbox()
        if not box or digest(p/qa['logoAssetPath'])!=qa.get('logoAssetSha256'): raise ValueError('Partial logo asset stale')
        vw,vh=box[2]-box[0],box[3]-box[1]
        for n in selected_pt:
            entries=[e for e in qa['images'] if e['file']==n]
            if len(entries)!=1 or entries[0].get('geometryGate')!='PASS' or entries[0].get('finalImageSha256')!=inventory[n] or not entries[0].get('commandRecord') or not entries[0].get('unbrandedSourceSha256'): raise ValueError('Partial logo evidence incomplete')
            src=p/'unbranded'/n
            if src.exists() and digest(src)!=entries[0]['unbrandedSourceSha256']: raise ValueError('Partial source stale')
            cfg=plan['placements'][n]; bounds=rect(cfg); w,h=bounds[2]-bounds[0],bounds[3]-bounds[1]
            with Image.open(p/n) as image: dimensions=image.size
            check_separation(bounds,cfg['protectedZones'],dimensions,max(int(plan.get('minimumClearancePx',0)),int(plan.get('minimumComponentSeparationPx',0))))
            wide=plan.get('logoVisibilityMode')=='ASPECT_RATIO_WORDMARK'
            scale=200/max(dimensions)
            if int(plan.get('thumbnailReviewSizePx',200))!=200 or abs(w/h-vw/vh)/(vw/vh)>.02 or max(w,h)*scale<20 or max(w,h)>.12*min(dimensions) or min(w,h)*scale<(20*min(vw,vh)/max(vw,vh) if wide else 10): raise ValueError('Partial visible logo size/aspect violation')
            if wide and (max(vw,vh)/min(vw,vh)<=2.4 or not plan.get('logoAssetSourceUrl')): raise ValueError('Invalid official wordmark branch')
    for n in slots:
        with Image.open(p/n) as im:
            im.load()
            check_image_size(im.size)
            if im.mode not in ('RGB','RGBA') or im.format!=('JPEG' if n.endswith('.jpg') else 'PNG'): raise ValueError('Partial image format mismatch')
            if im.mode=='RGBA' and im.getchannel('A').getextrema()[0]!=255: raise ValueError('Partial final image must have an opaque background')
    return inventory

def accept_partial(p,slots,brand=None):
    inventory=partial_checks(p,slots,brand)
    write(p/'partial-update-qa.json',{'schemaVersion':3,'result':'PARTIAL_UPDATE_REVIEWED','deliveryScope':'PARTIAL_UPDATE','retainedLegacyGallery':True,'fullGalleryPass':False,'selectedSlots':slots,'images':[{'file':n,'sha256':inventory[n]} for n in slots],'galleryInventorySha256':inventory,'visualReviewSha256':digest(p/'visual-review.json'),'semanticReviewSha256':digest(p/'semantic-review.json'),'logoQaSha256':digest(p/'logo-qa.json') if any(n in PT for n in slots) else None})

def validate_partial(p,changed):
    report=read(p/'partial-update-qa.json'); slots=report.get('selectedSlots',[])
    if report.get('schemaVersion',0)<3 or report.get('result')!='PARTIAL_UPDATE_REVIEWED' or report.get('deliveryScope')!='PARTIAL_UPDATE' or report.get('retainedLegacyGallery')!=True or report.get('fullGalleryPass')!=False or not set(changed).issubset(set(slots)): raise ValueError('Missing current partial update receipt')
    inventory=partial_checks(p,slots)
    if report.get('galleryInventorySha256')!=inventory or {e['file']:e['sha256'] for e in report.get('images',[])}!={n:inventory[n] for n in slots}: raise ValueError('Partial receipt stale')
    for filename,key in [('visual-review.json','visualReviewSha256'),('semantic-review.json','semanticReviewSha256')]:
        if report.get(key)!=digest(p/filename): raise ValueError('Partial review binding stale')
    if any(n in PT for n in slots) and report.get('logoQaSha256')!=digest(p/'logo-qa.json'): raise ValueError('Partial logo binding stale')
    print('PARTIAL_UPDATE_REVIEWED: overall legacy gallery remains quarantined; no full gallery PASS')

def contact_sheet(directory,out):
    canvas=Image.new('RGB',(1200,1664),(238,244,251)); draw=ImageDraw.Draw(canvas)
    for i,n in enumerate(NAMES):
        im=load(Path(directory)/n); im.thumbnail((370,370)); x=(i%3)*400+15; y=(i//3)*416+10
        canvas.paste(im.convert('RGB'),(x,y)); draw.text((x,y+378),n,fill=(15,35,70))
    save(canvas,out)

def crop(src,out,x,y,w,h):
    im=load(src)
    if min(w,h)<=0 or min(x,y)<0 or x+w>im.width or y+h>im.height: raise ValueError('Crop outside canvas')
    save(im.crop((x,y,x+w,y+h)),out)

def gallery_directories(root,changed,full=False):
    if full or any(s in ('SKILL.md','README.md') or s.startswith(('scripts/','.github/','references/','assets/')) or s=='product generated photo/image-manifest-template.md' for s in changed):
        return list((root/'product generated photo').glob('VL-*'))
    return sorted({root/Path(*Path(s).parts[:2]) for s in changed if s.startswith('product generated photo/VL-')})

def validate_approved_import(root,p,changed):
    receipt=read(p/'approved-slot-exception.json'); name=receipt.get('file')
    if receipt.get('schemaVersion')!=1 or receipt.get('internalId')!=p.name or name!=MAIN[1] or set(changed)!={name}:
        raise ValueError('Approved import exception does not cover this scope')
    if receipt.get('exceptionType')!='USER_APPROVED_EXACT_ASSET_IMPORT' or not receipt.get('authorizationSource') or receipt.get('fullGalleryPass') is not False:
        raise ValueError('Missing scoped user import authorization')
    expected=receipt.get('sha256')
    reference=(root/receipt['referencePath']).resolve()
    if not reference.is_relative_to(root.resolve()) or digest(p/name)!=expected or digest(reference)!=expected or receipt.get('referenceSha256')!=expected:
        raise ValueError('Approved import bytes/reference changed')
    with Image.open(p/name) as im:
        im.load()
        if im.format!='PNG' or list(im.size)!=receipt.get('dimensions') or im.mode!=receipt.get('mode'):
            raise ValueError('Approved import format differs from supplied asset')
    unchanged={n:digest(p/n) for n in NAMES if n!=name}
    if receipt.get('unchangedCanonicalSha256')!=unchanged or not receipt.get('visualReview',{}).get('notes'):
        raise ValueError('Untouched slots changed or import review missing')
    print('USER_APPROVED_EXACT_ASSET_IMPORT: one scoped native-size file; remaining gallery NOT PASS; Amazon acceptance user-reported')

def validate_ai_effect_import(root,p,changed):
    """Narrow VL-1326 user-authorized byte import, not product/brand QA."""
    receipt=read(p/'approved-ai-effect-import.json')
    if p.name!='VL-1326' or receipt.get('internalId')!=p.name or receipt.get('schemaVersion')!=1:
        raise ValueError('AI import authorization is product-specific')
    if receipt.get('exceptionType')!='USER_APPROVED_AI_EFFECT_IMPORT' or set(changed)!=set(PT):
        raise ValueError('AI import authorization covers these eight PT files only')
    if receipt.get('fullGalleryPass') is not False or receipt.get('publicationReadiness')!='NOT_ASSESSED' or not receipt.get('limitations'):
        raise ValueError('AI import must retain review/publication limitations')
    authorization=receipt.get('authorization',{})
    if not all(authorization.get(k) for k in ('aiMethodQuote','replacementQuote','sizePolicyQuote')):
        raise ValueError('Missing explicit AI/replacement/size authorization')
    source=p/'ai-gallery-silver-blue-20261005'
    for name,key in [('approval-and-review.json','sourceReviewSha256'),('native-file-checks.json','sourceFileChecksSha256')]:
        if receipt.get(key)!=digest(source/name): raise ValueError('AI source review binding stale')
    checks=read(source/'native-file-checks.json')
    expected={e['file']:e['sha256'] for e in checks['files']}
    if set(expected)!=set(PT) or receipt.get('images')!=expected: raise ValueError('Incomplete AI image inventory')
    for n in PT:
        if digest(p/n)!=expected[n] or digest(source/n)!=expected[n]: raise ValueError('AI approved bytes changed')
        with Image.open(p/n) as im:
            im.load(); check_image_size(im.size)
            if im.mode!='RGB' or im.format!='PNG': raise ValueError('AI import format mismatch')
    if receipt.get('unchangedMainSha256')!={n:digest(p/n) for n in MAIN}: raise ValueError('AI import changed MAIN')
    print('USER_APPROVED_AI_EFFECT_IMPORT: eight hash-bound images imported; full product/brand QA and Amazon readiness NOT certified')

def validate_vl1276_ai_gallery_import(root,p,changed):
    """Exact eleven-file user approval, never strict QA or general AI permission."""
    if p.name!='VL-1276' or set(changed)!=set(NAMES):
        raise ValueError('VL-1276 approval covers exactly eleven slots')
    receipt=read(p/'approved-ai-gallery-import.json')
    expected={
    "MAIN-STRICT.jpg": "a8168d6adad3eb7d72f683946004c900fcd955022877216103163009b7d87197",
    "MAIN-ENHANCED-FRONT-CANDIDATE.png": "60e8cf761bf817a90791e154beb50c99e8fc4bf8b04a65d5d7d1f17c93ff0e1a",
    "MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png": "51fc0a579c5bcb976bccf38f3037371d91b23d7d0e2bd5793c2e3ef2a484593c",
    "PT01.png": "9b1694585db0300428d91a2bdfb18f6f78c27aa0160a7b8cf08fb2babb2e1a72",
    "PT02.png": "72f2cc5de3d818ae11a1b68cae71450b95a27602ebbc2e2ebda9e634c986ba73",
    "PT03.png": "882e853c9b5d7d7e814e910d182110eba1a242f8d04cad933127fcf74878f0c7",
    "PT04.png": "879bfbf7f13d29ab70621471c226d001f9640ffe81423af6793ec3a7e7c4a323",
    "PT05.png": "0832dade56d2c9300fe41db1dd73d53d732af0f1be3bc4ce97bf07991b685eb0",
    "PT06.png": "6ab3c90fbf9bec3ff1a0d38cd3f9b78ffd43773d8397e75794016afe62f7003f",
    "PT07.png": "704e68ce663a82fb75be365eafffdb5497f9471922324ed144a09156afd914e8",
    "PT08.png": "cd9f524e2ff91d9738b6dc2b1299671602795bc892b66923b179838229436a38"
}
    if receipt.get('schemaVersion')!=1 or receipt.get('internalId')!='VL-1276' or receipt.get('exceptionType')!='USER_APPROVED_VL1276_ELEVEN_AI_IMPORT':
        raise ValueError('Missing VL-1276-specific import receipt')
    if receipt.get('images')!=expected or receipt.get('sourceCommit')!='2fa9845ee8a8a2594c4e443377ff5962358b3ac0':
        raise ValueError('Approval is frozen to the previously delivered eleven files')
    if receipt.get('fullGalleryPass') is not False or receipt.get('strictProductBrandQaPass') is not False or receipt.get('publicationReadiness')!='NOT_ASSESSED' or not receipt.get('limitations'):
        raise ValueError('AI import cannot confer QA or publication clearance')
    auth=receipt.get('authorization',{})
    if not all(auth.get(k) for k in ('aiMethodQuote','replacementQuote','scopeClarificationQuote')):
        raise ValueError('Missing explicit method, replacement or eleven-file approval')
    source=p/'ai-gallery-architectural-20261005'
    for filename,key in [('effect-review.json','sourceReviewSha256'),('native-file-checks.json','sourceFileChecksSha256')]:
        # Git text checkout may use CRLF on Windows and LF on Linux.
        evidence_hash=hashlib.sha256((source/filename).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        if receipt.get('sourceReviewEncoding')!='UTF8_LF_NORMALIZED' or evidence_hash!=receipt.get(key):
            raise ValueError('AI source review binding stale')
    for n in NAMES:
        if digest(p/n)!=expected[n] or digest(source/n)!=expected[n]:
            raise ValueError('Approved AI image bytes changed')
        with Image.open(p/n) as im:
            im.load(); check_image_size(im.size)
            if im.mode!='RGB' or im.format!=('JPEG' if n==MAIN[0] else 'PNG'):
                raise ValueError('AI import format mismatch')
    status=read(p/'delivery-status.json')
    if status.get('galleryState')!='LEGACY_QUARANTINED' or status.get('currentQaPass') is not False:
        raise ValueError('Strict QA quarantine must be retained')
    print('USER_APPROVED_VL1276_ELEVEN_AI_IMPORT: approved bytes replaced; strict QA and Amazon readiness NOT certified')

def gate(root,base=None,head='HEAD'):
    root=Path(root)
    changed=[] if not base else subprocess.check_output(['git','diff','--name-only',base,head],cwd=root,text=True).splitlines()
    dirs=gallery_directories(root,changed,full=not base)
    validated=0; quarantined=0; partial=0; research=0; imports=0; ai_imports=0
    for p in dirs:
        if not p.is_dir(): continue
        if not any((p/n).exists() for n in NAMES):
            print(f'Research-only folder excluded from gallery validation: {p}'); research+=1; continue
        status=p/'delivery-status.json'
        if status.exists() and read(status).get('galleryState')=='LEGACY_QUARANTINED':
            relative=p.relative_to(root).as_posix()+'/'
            image_changes=[s for s in changed if s.startswith(relative) and Path(s).parent.as_posix()==relative.rstrip('/') and Path(s).suffix.lower() in ('.png','.jpg','.jpeg')]
            if image_changes:
                names=[Path(s).name for s in image_changes]
                if (p/'approved-slot-exception.json').exists() and set(names)=={MAIN[1]}:
                    validate_approved_import(root,p,names); imports+=1
                elif (p/'approved-ai-effect-import.json').exists() and set(names)==set(PT):
                    validate_ai_effect_import(root,p,names); ai_imports+=1
                elif p.name=='VL-1276' and (p/'approved-ai-gallery-import.json').exists() and set(names)==set(NAMES):
                    validate_vl1276_ai_gallery_import(root,p,names); ai_imports+=1
                else:
                    validate_partial(p,names); partial+=1
            quarantined+=1; continue
        validate(p); validated+=1
    print(f'Validated {validated} eligible galleries; {quarantined} quarantined folders excluded, not PASS')
    summary={'fullGalleriesValidated':validated,'quarantinedNotPassed':quarantined,'partialUpdatesValidated':partial,'approvedExactAssetImports':imports,'approvedAiEffectImportsNotQaPassed':ai_imports,'researchOnlyFolders':research}
    write(root/'gallery-ci-summary.json',summary)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f:
            f.write(f'### Gallery check scope\n\nFull galleries validated: {validated}. Quarantined, NOT PASS: {quarantined}. Scoped partial updates: {partial}. Exact user-approved imports: {imports}. AI-effect imports, NOT full QA: {ai_imports}. Research-only folders: {research}.\n\nCI success means checks executed successfully; it does not clear quarantine or certify Amazon readiness.\n')
    return summary

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('operation',choices=['normalize','remove-bg','overlay','badges','validate','finalize','gate','crop','contact','accept']); ap.add_argument('--input'); ap.add_argument('--output'); ap.add_argument('--size',type=int,default=None); ap.add_argument('--format',default='PNG'); ap.add_argument('--asset'); ap.add_argument('--directory'); ap.add_argument('--plan'); ap.add_argument('--brand'); ap.add_argument('--contact'); ap.add_argument('--slots',nargs='+'); ap.add_argument('--skip-normalization',action='store_true'); ap.add_argument('--allow-legacy',action='store_true'); ap.add_argument('--mask'); ap.add_argument('--style',default='Flat'); ap.add_argument('--padding',type=int,default=18); ap.add_argument('--x',type=int); ap.add_argument('--y',type=int); ap.add_argument('--width',type=int); ap.add_argument('--height',type=int); ap.add_argument('--tolerance',type=int,default=8); ap.add_argument('--full',type=int,default=42); ap.add_argument('--base'); ap.add_argument('--head',default='HEAD'); a=ap.parse_args()
    if a.operation=='normalize': normalize(a.input,a.output,a.size,a.format)
    elif a.operation=='remove-bg': remove_background(a.input,a.output,a.tolerance,a.full)
    elif a.operation=='overlay': overlay(a.input,a.asset,a.output,a.x,a.y,a.width,a.height,a.style,a.padding,a.mask)
    elif a.operation=='badges': badges(a.directory,a.asset,a.plan,a.output,a.brand,a.slots)
    elif a.operation=='validate': validate(a.directory,a.brand,a.allow_legacy)
    elif a.operation=='finalize': finalize(a.directory,a.asset,a.brand,a.contact,a.size,a.skip_normalization,a.slots)
    elif a.operation=='gate': gate(a.directory,a.base,a.head)
    elif a.operation=='crop': crop(a.input,a.output,a.x,a.y,a.width,a.height)
    elif a.operation=='contact': contact_sheet(a.directory,a.output)
    elif a.operation=='accept': accept(a.directory,a.brand,a.slots)
if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,OSError) as exc: sys.exit(str(exc))
