import os,sys
from PIL import Image, ImageDraw
d=sys.argv[1]; fs=sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
cell=440; cols=6; rows=(len(fs)+cols-1)//cols
sh=Image.new('RGB',(cols*cell,rows*cell),'white'); dr=ImageDraw.Draw(sh)
for k,f in enumerate(fs):
    t=Image.open(os.path.join(d,f)); t.thumbnail((430,430)); x,y=(k%cols)*cell,(k//cols)*cell; sh.paste(t,(x+5,y+5)); dr.rectangle([x+5,y+5,x+60,y+30],fill='black'); dr.text((x+12,y+10),f,fill='yellow')
sh.save(sys.argv[2],quality=82)
