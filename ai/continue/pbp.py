# PBP-style draw.io builder with obstacle-avoiding wire routing.
# Conventions: rounded boxes+pins; pins longer, overlapping parent; inputs white / outputs #1BA1E2;
# every wire is one discrete edge (one source, one target); arrows point into inputs; rounded edges
# routed around part bodies via A* through open channels.
import html, itertools, heapq
_violations=[]
_cid = itertools.count(2)
def nid(): return next(_cid)
def esc(s): return html.escape(str(s), quote=True)

IN_FILL="#ffffff"; OUT_FILL="#1BA1E2"
PIN_L=40; PIN_H=18; OVERLAP=16
GRID=10; MARGIN=14          # routing grid + clearance around parts
LEAD=6                      # gap from part box to first/last waypoint

class Page:
    def __init__(self, name, pid):
        self.name=name; self.pid=pid; self.cells=[]
        self.wires=[]               # (src_pin, dst_pin, label)
        self.boxes=[]               # part bounding boxes (x0,y0,x1,y1) incl pins
        self.pin=  {}               # pin_id -> dict(cx,cy,side,box_idx)
    def add(self,c): self.cells.append(c)

def part(page, label, ins, outs, x, y, w=120, h=None,
         fill="#eef3fb", stroke="#2b4b6f", dashed=False, font=12):
    x=round(x/10)*10; y=round(y/10)*10            # snap to grid for clean routing
    n=max(len(ins),len(outs),1)
    if h is None: h=max(54, 30*n+16)
    bid=nid(); ports={}
    ds=";dashed=1" if dashed else ""
    page.add(f'<mxCell id="{bid}" value="{esc(label)}" style="rounded=1;arcSize=12;whiteSpace=wrap;'
      f'html=1;fontStyle=1;fontSize={font};fillColor={fill};strokeColor={stroke}{ds};verticalAlign=middle;" '
      f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    box_idx=len(page.boxes)
    page.boxes.append((x-(PIN_L-OVERLAP), y, x+w+(PIN_L-OVERLAP), y+h))   # incl pin reach L/R
    def place(names, side):
        k=len(names)
        for i,nm in enumerate(names):
            yy=(h*(i+1)/(k+1))-PIN_H/2
            if side=='L':
                xx=-(PIN_L-OVERLAP); fillc=IN_FILL; al="align=left;spacingLeft=2;"
                cx=x+xx+PIN_L/2; 
            else:
                xx=w-OVERLAP; fillc=OUT_FILL; al="align=right;spacingRight=2;"
                cx=x+xx+PIN_L/2
            cy=y+yy+PIN_H/2
            pid=nid()
            page.add(f'<mxCell id="{pid}" value="{esc(nm)}" style="rounded=1;arcSize=40;whiteSpace=wrap;'
              f'html=1;fontSize=9;fillColor={fillc};strokeColor={stroke};{al}verticalAlign=middle;" '
              f'vertex="1" parent="{bid}"><mxGeometry x="{xx}" y="{yy}" width="{PIN_L}" height="{PIN_H}" '
              f'as="geometry"/></mxCell>')
            page.pin[pid]=dict(cx=cx,cy=cy,side=side,box=box_idx)
            ports[nm]=pid; ports[(side,i)]=pid
    place(ins,'L'); place(outs,'R')
    ports['_body']=bid
    return ports

def wire(page, src_out, dst_in, label=""):
    page.wires.append((src_out, dst_in, label))

def note(page, text, x, y, w=300, h=90):
    page.add(f'<mxCell id="{nid()}" value="{esc(text)}" style="rounded=1;whiteSpace=wrap;html=1;'
      f'fontSize=10;align=left;verticalAlign=top;fillColor=#fff8e1;strokeColor=#e0a800;dashed=1;'
      f'spacingLeft=6;spacingTop=4;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" '
      f'height="{h}" as="geometry"/></mxCell>')
    page.boxes.append((x,y,x+w,y+h))   # treat notes as obstacles too

# ---------------- A* router ----------------
def _route(start, goal, blocks, bounds):
    x0,y0,x1,y1=bounds; G=GRID
    W=int((x1-x0)/G)+1; H=int((y1-y0)/G)+1
    blk=bytearray(W*H)
    def idx(gx,gy): return gx*H+gy
    for (bx0,by0,bx1,by1) in blocks:
        gx0=max(0,int((bx0-x0)//G)); gx1=min(W-1,int((bx1-x0)//G)+1)
        gy0=max(0,int((by0-y0)//G)); gy1=min(H-1,int((by1-y0)//G)+1)
        for gx in range(gx0,gx1+1):
            base=gx*H
            for gy in range(gy0,gy1+1): blk[base+gy]=1
    def g_of(p):
        return (min(W-1,max(0,round((p[0]-x0)/G))), min(H-1,max(0,round((p[1]-y0)/G))))
    s=g_of(start); t=g_of(goal)
    blk[idx(*s)]=0; blk[idx(*t)]=0
    DIRS=[(1,0),(-1,0),(0,1),(0,-1)]
    TURN=3
    openh=[(0,s[0],s[1],-1)]; came={}; gsc={(s[0],s[1],-1):0}
    found=None
    while openh:
        f,gx,gy,d=heapq.heappop(openh)
        if (gx,gy)==t: found=(gx,gy,d); break
        cg=gsc.get((gx,gy,d),1e9)
        for di,(dx,dy) in enumerate(DIRS):
            nx,ny=gx+dx,gy+dy
            if nx<0 or ny<0 or nx>=W or ny>=H or blk[idx(nx,ny)]: continue
            ng=cg+1+(TURN if d!=-1 and di!=d else 0)
            key=(nx,ny,di)
            if ng<gsc.get(key,1e9):
                gsc[key]=ng; came[key]=(gx,gy,d)
                h=abs(nx-t[0])+abs(ny-t[1])
                heapq.heappush(openh,(ng+h,nx,ny,di))
    if not found:  # fallback: straight L
        return [start,(goal[0],start[1]),goal]
    path=[]; cur=found
    while cur in came:
        path.append((x0+cur[0]*G,y0+cur[1]*G)); cur=came[cur]
    path.append((x0+s[0]*G,y0+s[1]*G)); path.reverse()
    pts=[start]+path+[goal]
    # collapse collinear
    out=[pts[0]]
    for p in pts[1:]:
        if len(out)>=2:
            a,b=out[-2],out[-1]
            if (a[0]==b[0]==p[0]) or (a[1]==b[1]==p[1]): out[-1]=p; continue
        out.append(p)
    return out

def _emit_wires(page, bounds):
    for s,d,label in page.wires:
        ps=page.pin[s]; pd=page.pin[d]
        sbox=page.boxes[ps['box']]; dbox=page.boxes[pd['box']]
        start=(sbox[2]+LEAD, ps['cy']) if ps['side']=='R' else (sbox[0]-LEAD, ps['cy'])
        goal =(dbox[0]-LEAD, pd['cy']) if pd['side']=='L' else (dbox[2]+LEAD, pd['cy'])
        blocks=[b for i,b in enumerate(page.boxes) if i not in (ps['box'],pd['box'])]
        pts=_route(start,goal,blocks,bounds)
        for (ax,ay),(bx,by) in zip(pts,pts[1:]):
            for (rx0,ry0,rx1,ry1) in blocks:
                if min(ax,bx)<rx1 and max(ax,bx)>rx0 and min(ay,by)<ry1 and max(ay,by)>ry0:
                    _violations.append((label,(ax,ay),(bx,by))); break
        mids=pts[1:-1] if len(pts)>2 else []
        arr="".join(f'<mxPoint x="{round(px)}" y="{round(py)}"/>' for px,py in mids)
        ex="1" if ps['side']=='R' else "0"; en="0" if pd['side']=='L' else "1"
        style=(f"edgeStyle=none;rounded=1;html=1;startArrow=none;endArrow=block;endFill=1;"
               f"strokeColor=#333333;fontSize=9;exitX={ex};exitY=0.5;exitDx=0;exitDy=0;"
               f"entryX={en};entryY=0.5;entryDx=0;entryDy=0;jettySize=auto;")
        page.add(f'<mxCell id="{nid()}" value="{esc(label)}" style="{style}" edge="1" parent="1" '
          f'source="{s}" target="{d}"><mxGeometry relative="1" as="geometry">'
          f'<Array as="points">{arr}</Array></mxGeometry></mxCell>')

def render(pages, path):
    diags=[]
    for pg in pages:
        xs=[b[0] for b in pg.boxes]+[b[2] for b in pg.boxes]
        ys=[b[1] for b in pg.boxes]+[b[3] for b in pg.boxes]
        bounds=(min(xs)-80,min(ys)-80,max(xs)+80,max(ys)+80)
        _emit_wires(pg,bounds)
        body="\n".join(pg.cells)
        diags.append(f'''  <diagram name="{esc(pg.name)}" id="{pg.pid}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1700" pageHeight="1100" math="0" shadow="0">
      <root><mxCell id="0"/><mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>''')
    open(path,"w").write('<mxfile host="app.diagrams.net" type="device">\n'+"\n".join(diags)+'\n</mxfile>\n')
    return pages
