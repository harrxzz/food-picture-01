"""Golden ramen, painted with a tiny deterministic standard-library rasterizer."""
import math, os, struct, zlib
W = H = 720
pixels = bytearray(W * H * 3)
def ellipse(cx, cy, rx, ry, color, edge=0.10, light=0.10):
    for y in range(max(0,int(cy-ry-1)), min(H,int(cy+ry+2))):
        dy=(y+.5-cy)/ry
        for x in range(max(0,int(cx-rx-1)),min(W,int(cx+rx+2))):
            dx=(x+.5-cx)/rx
            d=dx*dx+dy*dy
            if d>=1: continue
            a=min(1,(1-d)/edge) if edge else 1
            shade=1+light*(-.55*dx-.8*dy)
            p=(y*W+x)*3
            for k in range(3): pixels[p+k]=int(pixels[p+k]*(1-a)+min(255,color[k]*shade)*a)
def line(x1,y1,x2,y2,width,color):
    n=max(1,int(math.hypot(x2-x1,y2-y1)/3))
    for i in range(n+1):
        t=i/n; ellipse(x1+(x2-x1)*t,y1+(y2-y1)*t,width,width,color,.22,.03)
def curved(points,width,color):
    for a,b in zip(points,points[1:]): line(*a,*b,width,color)
# Warm dark table, softly lit from the upper left.
for y in range(H):
    for x in range(W):
        glow=max(0,1-math.hypot((x-190)/650,(y-120)/750))
        grain=2*math.sin(y*.045)+math.sin(y*.18+x*.005)
        p=(y*W+x)*3
        pixels[p:p+3]=bytes(max(0,min(255,int(c+glow*g+grain))) for c,g in zip((23,27,28),(32,24,14)))
# Bowl shadow, ceramic, and amber broth.
ellipse(366,478,305,218,(11,13,14),.20,.0)
ellipse(360,402,300,276,(33,48,48),.07,.28)
ellipse(360,389,288,263,(92,119,111),.05,.25)
ellipse(360,385,270,245,(31,48,46),.035,.15)
ellipse(360,383,251,227,(191,104,46),.025,.25)
ellipse(360,376,237,214,(214,136,64),.025,.18)
# Noodles: looping, softly shadowed strands.
for j in range(19):
    pts=[]
    for i in range(64):
        t=i/63
        x=166+344*t
        y=397+j*5+16*math.sin(t*math.pi*3+j*.60)+6*math.sin(t*math.pi*7+j*.3)
        if ((x-360)/232)**2+((y-380)/209)**2 < .90: pts.append((x,y))
    if len(pts)>1:
        curved([(x,y+3) for x,y in pts],3.5,(151,80,37))
        curved(pts,2.6,(247,202,115))
# Chashu pork slices, with concentric fat and browned edges.
for x,y in ((254,323),(337,289)):
    ellipse(x+5,y+7,91,63,(117,54,36),.08,.16)
    ellipse(x,y,91,63,(179,102,72),.07,.24)
    ellipse(x-3,y-3,77,51,(224,170,124),.09,.20)
    ellipse(x-7,y-4,60,38,(193,120,87),.10,.20)
    ellipse(x-10,y-7,43,27,(229,174,128),.12,.18)
    curved([(x-58,y+12),(x-25,y+17),(x+10,y+12),(x+48,y-2)],2,(239,191,146))
# Soft-boiled egg halves.
for x,y in ((469,285),(527,351)):
    ellipse(x+5,y+7,65,78,(126,75,36),.1,.1)
    ellipse(x,y,65,78,(248,230,192),.08,.10)
    ellipse(x-2,y-3,49,61,(255,244,215),.10,.08)
    ellipse(x-2,y+1,33,42,(220,104,24),.10,.18)
    ellipse(x-4,y-4,28,36,(250,153,32),.12,.20)
    ellipse(x-13,y-18,10,6,(255,205,103),.3,.05)
# Nori and fine highlights complete the bowl.
for x,y,rx,ry in ((167,271,30,73),(196,239,28,66)):
    ellipse(x,y,rx,ry,(23,53,42),.06,.25)
    ellipse(x-5,y-5,rx*.65,ry*.8,(41,75,51),.08,.20)
# Chopped scallions, sesame and chili oil.
for i in range(38):
    x=250+(i*47%230); y=504+(i*29%70)
    if ((x-360)/240)**2+((y-380)/215)**2 < .93:
        ellipse(x,y,8,5,(31,104,55),.15,.12)
        ellipse(x-1,y-1,4,2,(130,193,91),.20,.1)
for i in range(58):
    x=153+(i*83%411); y=235+(i*61%284)
    if ((x-360)/238)**2+((y-380)/211)**2 < .90:
        ellipse(x,y,2.5,1.5,(251,218,159),.25,.0)
for x,y,r in ((183,395,7),(207,354,4),(552,449,6),(489,475,5),(418,216,4)):
    ellipse(x,y,r,r*.7,(163,54,22),.2,.2)
# Write a standards-compliant RGB PNG, with no external dependency.
raw=b''.join(b'\0'+pixels[y*W*3:(y+1)*W*3] for y in range(H))
def chunk(kind,data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
os.makedirs(out,exist_ok=True)
with open(os.path.join(out,'entry.png'),'wb') as f: f.write(png)
