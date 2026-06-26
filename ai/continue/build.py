from pbp import Page, part, wire, render, nid, esc, note

def title(pg,t,x=40,y=0,w=1300):
    pg.add(f'<mxCell id="{nid()}" value="{esc(t)}" style="text;html=1;fontSize=14;fontStyle=1;'
      f'align=left;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="40" as="geometry"/></mxCell>')
def tag(pg,label,x,y,kind,w=70,h=46):   # 'src'|'sink'|'pass'
    ins=["in"] if kind in("sink","pass") else []
    outs=["out"] if kind in("src","pass") else []
    return part(pg,label,ins,outs,x,y,w=w,h=h,fill="#f3eefc",stroke="#5b3aa0")

AN={"fill":"#fff2cc","stroke":"#b8860b","dashed":True}
A ={"fill":"#f0f0f0","stroke":"#666"}
GREY={"fill":"#f5f5f5","stroke":"#999","dashed":True}

# ============================ PAGE 1 ============================
p1=Page("1 - Clock + PSU","pong-sec1")
title(p1,"Atari PONG \u2014 Section 1: Master Clock + +5V Supply.  Gates=typed boxes; arrows point into inputs; "
         "inputs white / outputs blue; analog parts dashed.  +5/GND shown only here, where the supply lives.")
PY=560
j4=part(p1,"J-4",[],["o"],40,PY,70,46,**A); j5=part(p1,"J-5",[],["o"],40,PY+80,70,46,**A)
j7=part(p1,"J-7",[],["o"],40,PY+170,70,46,**A); j12=part(p1,"J-12",[],["o"],40,PY+230,70,46,**A)
d1=part(p1,"1N4001",["a"],["k"],200,PY,100,46,**AN); d2=part(p1,"1N4001",["a"],["k"],200,PY+80,100,46,**AN)
c80=part(p1,"8000uF",["+"],["g"],360,PY+150,100,46,**AN)
reg=part(p1,"LM309\n+5 REG",["IN"],["OUT","GND"],380,PY,130,96,fill="#e7f0e7",stroke="#3a6b3a")
c25=part(p1,"250uF",["+"],["g"],580,PY+150,100,46,**AN)
p5=tag(p1,"+5V",600,PY+10,"pass"); gnd=tag(p1,"GND",430,PY+320,"sink")
wire(p1,j4["o"],d1["a"]); wire(p1,j5["o"],d2["a"])
wire(p1,d1["k"],reg["IN"],"rect DC"); wire(p1,d2["k"],reg["IN"])
wire(p1,d1["k"],c80["+"]); wire(p1,c80["g"],gnd["in"])
wire(p1,reg["OUT"],p5["in"],"+5V"); wire(p1,reg["OUT"],c25["+"]); wire(p1,c25["g"],gnd["in"])
wire(p1,reg["GND"],gnd["in"]); wire(p1,j7["o"],gnd["in"]); wire(p1,j12["o"],gnd["in"])
OY=90
inv1=part(p1,"INV",["i"],["o"],330,OY,96,54); inv2=part(p1,"INV",["i"],["o"],520,OY,96,54)
r1=part(p1,"330\u03a9",["a"],["b"],330,OY-78,96,40,**AN); r2=part(p1,"330\u03a9",["a"],["b"],520,OY-78,96,40,**AN)
cc=part(p1,"0.1uF",["a"],["b"],452,OY+70,80,40,**AN)
xt=part(p1,"XTAL",["a"],["b"],330,OY+140,90,40,**AN); c1=part(p1,"100pF",["a"],["b"],452,OY+140,90,40,**AN)
nand=part(p1,"NAND",["i1","i2"],["o"],700,OY+30,110,66); clk1=tag(p1,"CLOCK",860,OY+50,"pass")
wire(p1,inv1["o"],cc["a"]); wire(p1,cc["b"],inv2["i"])
wire(p1,inv1["o"],r1["a"]); wire(p1,r1["b"],inv1["i"])
wire(p1,inv2["o"],r2["a"]); wire(p1,r2["b"],inv2["i"])
wire(p1,inv2["o"],c1["a"]); wire(p1,c1["b"],xt["a"]); wire(p1,xt["b"],inv1["i"],"feedback")
wire(p1,inv1["o"],nand["i1"],"osc"); wire(p1,inv1["o"],nand["i2"]); wire(p1,nand["o"],clk1["in"])
nxt=part(p1,"7493 (F8)\n\u00f716 counter\n[Section 2]",["14 CKA","2 R0(1)","3 R0(2)"],
         ["12 QA","9 QB","8 QC","11 QD"],1000,OY+10,170,150,**GREY)
wire(p1,clk1["out"],nxt["14 CKA"],"CLOCK")

# ============================ PAGE 2 ============================
p2=Page("2 - Horizontal Sync","pong-sec2")
title(p2,"Atari PONG \u2014 Section 2: Horizontal Counter Chain + H-Sync / H-Blank Decode.  "
         "CLOCK arrives from page 1; taps 1H..256H, H RESET, H SYNC, H BLANK go forward to later pages.")
# --- inputs from elsewhere ---
clk=tag(p2,"CLOCK\n(pg1)",40,90,"src",w=78); p5b=tag(p2,"+5V",40,210,"src",w=70)
# --- counter chain (top row) ---
f6=part(p2,"F6  74107\n\u00f72  (1H)",["1 J","4 K","12 CLK","13 CLR"],["3 Q","2 Q\u0305"],170,70,140,120)
c1a=part(p2,"7493  F8\n\u00f716 counter",["14 CKA","1 CKB","2 R0(1)","3 R0(2)"],
         ["12 QA","9 QB","8 QC","11 QD"],380,60,150,150)
c1b=part(p2,"7493  E8\n\u00f716 counter",["14 CKA","1 CKB","2 R0(1)","3 R0(2)"],
         ["12 QA","9 QB","8 QC","11 QD"],620,60,150,150)
ff256=part(p2,"256H FF  7474\n\u00f72",["3 CLK","2 D","1 CLR"],["5 Q","6 Q\u0305"],860,70,150,120)
# --- chain wiring ---
wire(p2,clk["out"],f6["12 CLK"],"CLOCK")
wire(p2,p5b["out"],f6["1 J"]); wire(p2,p5b["out"],f6["4 K"])
wire(p2,f6["3 Q"],c1a["14 CKA"],"1H")
wire(p2,c1a["12 QA"],c1a["1 CKB"])                       # internal ÷16 jumper
wire(p2,c1a["11 QD"],c1b["14 CKA"],"16H")
wire(p2,c1b["12 QA"],c1b["1 CKB"])                       # internal ÷16 jumper
wire(p2,c1b["8 QC"],ff256["3 CLK"],"128H")
wire(p2,ff256["6 Q\u0305"],ff256["2 D"])                 # toggle
# --- H-decode gates (middle band) ---
g5=part(p2,"7410  G5\nNAND",["3","4","5"],["6"],400,300,120,90)
lt=part(p2,"7400  H5\nNAND",["5","4"],["6"],600,300,120,70)
lb=part(p2,"7400  H5\nNAND",["9","10"],["8"],600,420,120,70)
hs=part(p2,"7400  H5\nNAND",["12","13"],["11"],800,360,120,70)
wire(p2,p5b["out"],g5["4"])                              # pin4 tied +5
# taps into G5 (64H, 16H) -- 64H from c1b QB, 16H from c1a QD
wire(p2,c1b["9 QB"],g5["3"],"64H")
wire(p2,c1a["11 QD"],g5["5"],"16H")
# blank latch (cross-coupled)
wire(p2,g5["6"],lt["5"])
wire(p2,lb["8"],lt["4"])
wire(p2,lt["6"],lb["9"])
# H SYNC = NAND(HBLANK, 32H);  32H from c1b QA
wire(p2,lb["8"],hs["12"],"HBLANK")
wire(p2,c1b["12 QA"],hs["13"],"32H")
# --- H RESET decode (right) ---
g30=part(p2,"7430  F7\n8-in NAND\n(line-end decode)",
         ["1","2","3","4","5","6","11","12"],["8"],1080,70,170,200,**GREY)
e7=part(p2,"E7  7474\nH-RESET FF",["11 CLK","12 D","13 CLR"],["9 Q"],1310,90,150,110)
# best-inference taps into the 8-input reset decode (VERIFY)
for src,pin,lbl in [(f6["3 Q"],"1","1H"),(c1a["12 QA"],"2","2H"),(c1a["9 QB"],"3","4H"),
                    (c1a["8 QC"],"4","8H"),(c1a["11 QD"],"5","16H"),(c1b["12 QA"],"6","32H"),
                    (c1b["9 QB"],"11","64H"),(ff256["5 Q"],"12","256H")]:
    wire(p2,src,g30[pin],lbl)
wire(p2,g30["8"],e7["12 D"])
wire(p2,clk["out"],e7["11 CLK"])
# --- H RESET distribution ---
hr=tag(p2,"H RESET",1310,260,"pass",w=86)
wire(p2,e7["9 Q"],hr["in"])
for dst in [c1a["2 R0(1)"],c1a["3 R0(2)"],c1b["2 R0(1)"],c1b["3 R0(2)"],ff256["1 CLR"],f6["13 CLR"],lb["10"]]:
    wire(p2,hr["out"],dst,"H RESET")
# --- outputs forward (sinks to later pages) ---
oH=part(p2,"H taps 1H..256H\n\u2192 pg3 H-position",["1H","2H","4H","8H","16H","32H","64H","128H","256H"],[],
        1500,300,180,200,**GREY)
for src,pin in [(f6["3 Q"],"1H"),(c1a["12 QA"],"2H"),(c1a["9 QB"],"4H"),(c1a["8 QC"],"8H"),
                (c1a["11 QD"],"16H"),(c1b["12 QA"],"32H"),(c1b["9 QB"],"64H"),(c1b["8 QC"],"128H"),
                (ff256["5 Q"],"256H")]:
    wire(p2,src,oH[pin],pin)
oblank=tag(p2,"H BLANK\n\u2192 pg3/8",1500,180,"sink",w=96,h=50); wire(p2,lb["8"],oblank["in"])
oblk2 =tag(p2,"H BLANKING\n\u2192 pg8",1500,110,"sink",w=96,h=50); wire(p2,lt["6"],oblk2["in"])
osync =tag(p2,"H SYNC\n\u2192 pg8 video",1500,40,"sink",w=96,h=50); wire(p2,hs["11"],osync["in"])

note(p2,"VERIFY against your copy (scan-limited reads):\n"
        "\u2022 7493 QA\u2013QD \u2194 tap mapping (1H..256H) and the QA\u2192CKB \u00f716 jumpers.\n"
        "\u2022 Exact 8 taps feeding 7430 F7 reset decode (shown = best inference).\n"
        "\u2022 F6 / E7 flip-flop pin roles (J/K/CLK/CLR vs D) and which latch output is H BLANK vs H BLANKING.\n"
        "\u2022 H SYNC gate inputs (HBLANK vs HBLANKING, + 32H).",
     1080,300,420,180)

render([p1,p2],"/mnt/user-data/outputs/pong_sections.drawio")
import re
x=open("/mnt/user-data/outputs/pong_sections.drawio").read()
edges=re.findall(r'<mxCell[^>]*edge="1"[^>]*>',x)
bad=[e for e in edges if e.count("source=")!=1 or e.count("target=")!=1]
print("pages: 2 | total edges:",len(edges),"| malformed:",len(bad))

# ============================ PAGE 3 ============================
p3=Page("3 - Horizontal Position","pong-sec3")
title(p3,"Atari PONG \u2014 Section 3: Horizontal Position (ball-H).  9316 loadable counters preset from the hit "
         "detector, carry-chained; loaded during H BLANK; FF G6 latches the result.  Denser sheet area \u2014 see VERIFY note.")
# inputs from elsewhere
clkH=tag(p3,"CLOCK\n(pg1/2)",40,90,"src",w=82)
hbk =tag(p3,"H BLANK\n(pg2)",40,180,"src",w=82)
pre =tag(p3,"ball-H preset\nA4/B4 + GND\n(verify bits)",40,300,"src",w=110,h=70)
p5c =tag(p3,"+5V",40,430,"src",w=70)
# attract / control gates  (E1 = one 7400; ATTRACT is a NAMED NET arriving from elsewhere)
attr=tag(p3,"ATTRACT\n(mode net,\ndriven in\nstart/score logic)",40,560,"src",w=120,h=86)
e1a=part(p3,"7400  E1\nNAND",["1","2"],["3"],250,560,140,80)
e1b=part(p3,"7400  E1\nNAND",["4","5"],["6"],250,690,140,80)
# counters
g7=part(p3,"9316  G7\nload counter",
        ["1 MR","2 CP","3 P0","4 P1","5 P2","6 P3","7 CEP","9 PE","10 CET"],
        ["14 Q0","13 Q1","12 Q2","11 Q3","15 TC"],300,80,170,300)
h7=part(p3,"9316  H7\nload counter",
        ["1 MR","2 CP","3 P0","4 P1","5 P2","6 P3","7 CEP","9 PE","10 CET"],
        ["14 Q0","13 Q1","12 Q2","11 Q3","15 TC"],620,80,170,300)
g6=part(p3,"74107  G6\nJK FF",["8 J","4 CLK","11 K","13 CLR"],["5 Q","6 Q\u0305"],940,120,150,150)
g5=part(p3,"7410  G5\nNAND",["9","10","11"],["8"],940,330,130,100)
# outputs forward
oBH=part(p3,"ball-H position\n\u2192 pg5/8 video",["BALL-H","H-COINC"],[],1280,150,170,110,**GREY)

# ---- wiring (confident structure; control lines = best read, see note) ----
# clock + load + clear
for c in (g7,h7):
    wire(p3,clkH["out"],c["2 CP"],"CLOCK")
wire(p3,hbk["out"],g7["9 PE"],"H BLANK (load)")
wire(p3,hbk["out"],h7["9 PE"],"H BLANK (load)")
# preset data inputs (verify bit mapping)
for c in (g7,h7):
    for pin in ("3 P0","4 P1","5 P2","6 P3"):
        wire(p3,pre["out"],c[pin])
# carry chain  G7.TC -> H7.CET ;  H7.TC -> FF clock
wire(p3,g7["15 TC"],h7["10 CET"],"carry")
wire(p3,h7["15 TC"],g6["4 CLK"],"H7 carry")
# enable (inferred tie-highs)
wire(p3,p5c["out"],g7["7 CEP"]); wire(p3,p5c["out"],g7["10 CET"])
wire(p3,p5c["out"],h7["7 CEP"])
# ATTRACT named net -> E1 pin 2 AND pin 4 (two separate wires; both are LOADS on the net)
wire(p3,attr["out"],e1a["2"],"ATTRACT")
wire(p3,attr["out"],e1b["4"],"ATTRACT")
wire(p3,p5c["out"],g6["8 J"]); wire(p3,p5c["out"],g6["11 K"])      # toggle
wire(p3,hbk["out"],g6["13 CLR"])
# FF + decode outputs
wire(p3,g6["5 Q"],oBH["BALL-H"],"BALL-H")
wire(p3,h7["15 TC"],g5["9"]); wire(p3,g6["5 Q"],g5["10"]); wire(p3,p5c["out"],g5["11"])
wire(p3,g5["8"],oBH["H-COINC"],"H coincidence")

note(p3,"NOTES / VERIFY (dense sheet area):\n"
        "\u2022 ATTRACT is a NAMED NET (driven elsewhere) \u2014 it feeds E1 pin 2 and pin 4 as two loads; corrected here.\n"
        "\u2022 NOT YET TRACED (treat as open, NOT N.C.): E1 pins 1, 3, 5, 6 and the 9316 MR(1) clear source.\n"
        "\u2022 9316 load vs enable: H BLANK shown into PE(9); could be CET(10).  CEP/CET tie-highs are inferred.\n"
        "\u2022 Preset data P0\u2013P3: A4/B4 (hit detector) vs grounded bits \u2014 exact bit map unread.\n"
        "\u2022 FF G6 pin roles and G5 decode output names (BALL-H / H-COINC are placeholders).",
     430,690,560,180)

render([p1,p2,p3],"/mnt/user-data/outputs/pong_sections.drawio")
import re
x=open("/mnt/user-data/outputs/pong_sections.drawio").read()
edges=re.findall(r'<mxCell[^>]*edge="1"[^>]*>',x)
bad=[e for e in edges if e.count("source=")!=1 or e.count("target=")!=1]
print("pages: 3 | total edges:",len(edges),"| malformed:",len(bad))

# ============================ PAGE 4 ============================
# (re-render including page 4)
p4=Page("4 - Vertical Sync","pong-sec4")
title(p4,"Atari PONG \u2014 Section 4: Vertical Counter Chain + V-Sync / V-Blank Decode (mirrors page 2).  "
         "H RESET (pg2) is the V clock \u2014 the V chain advances once per horizontal line.")
hrst=tag(p4,"H RESET (pg2)\n= V clock",40,80,"src",w=92,h=50)
p5e =tag(p4,"+5V",40,170,"src",w=70)
# vertical counter chain
v1=part(p4,"7493  E8\n\u00f716 counter",["14 CKA","1 CKB","2 R0(1)","3 R0(2)"],
        ["12 QA","9 QB","8 QC","11 QD"],200,60,150,150)
v2=part(p4,"7493  E9\n\u00f716 counter",["14 CKA","1 CKB","2 R0(1)","3 R0(2)"],
        ["12 QA","9 QB","8 QC","11 QD"],440,60,150,150)
d4=part(p4,"256V FF  74107  D4\n\u00f72",["8 J","9 CLK","11 K","13 CLR"],["5 Q","6 Q\u0305"],680,70,160,120)
# V RESET decode
g10=part(p4,"7410  D8\n3-in NAND\n(field-end decode)",["9","10","11"],["8"],920,60,160,120)
e7=part(p4,"7474  E7 (\u00bd)\nV-RESET FF",["2 D","3 CLK","1 CLR"],["5 Q","6 Q\u0305"],1140,70,150,110)
# V BLANK latch (7402 NOR pair) + V SYNC
n1=part(p4,"7402  F5\nNOR",["8","9"],["10"],460,320,120,70)
n2=part(p4,"7402  F5\nNOR",["11","12"],["13"],460,440,120,70)
hsv=part(p4,"7400  H5\nNAND",["4","5"],["3"],680,380,120,70)
# outputs forward
oV=part(p4,"V taps 1V..256V\n\u2192 pg5 V-position",["1V","2V","4V","8V","16V","32V","64V","128V","256V"],[],
        1360,300,180,200,**GREY)
osy=tag(p4,"V SYNC\n\u2192 pg8 video",1360,160,"sink",w=96,h=50)
obk=tag(p4,"V BLANK\n\u2192 pg5/8",1360,90,"sink",w=96,h=50)

# --- chain wiring ---
wire(p4,hrst["out"],v1["14 CKA"],"H RESET")
wire(p4,v1["12 QA"],v1["1 CKB"])
wire(p4,v1["11 QD"],v2["14 CKA"],"8V")
wire(p4,v2["12 QA"],v2["1 CKB"])
wire(p4,v2["11 QD"],d4["9 CLK"],"128V")
wire(p4,p5e["out"],d4["8 J"]); wire(p4,p5e["out"],d4["11 K"])      # toggle
# V RESET decode (best-inference taps)
for src,pin,lbl in [(v2["11 QD"],"9","128V"),(v2["8 QC"],"10","64V"),(d4["5 Q"],"11","256V")]:
    wire(p4,src,g10[pin],lbl)
wire(p4,g10["8"],e7["2 D"])
wire(p4,hrst["out"],e7["3 CLK"])
# V RESET distribution
vr=tag(p4,"V RESET",1140,250,"pass",w=86)
wire(p4,e7["5 Q"],vr["in"])
for dst in [v1["2 R0(1)"],v1["3 R0(2)"],v2["2 R0(1)"],v2["3 R0(2)"],d4["13 CLR"]]:
    wire(p4,vr["out"],dst,"V RESET")
# V BLANK NOR latch (cross-coupled) ; set/reset taps = best inference
wire(p4,n1["10"],n2["11"]); wire(p4,n2["13"],n1["9"])
wire(p4,v1["9 QB"],n2["12"],"16V")          # one decode input (verify)
wire(p4,vr["out"],n1["8"],"V RESET")        # latch reset (verify)
# V SYNC = NAND(V BLANK, 8V)
wire(p4,n1["10"],hsv["4"],"V BLANK")
wire(p4,v1["11 QD"],hsv["5"],"8V")
# outputs forward
for src,pin in [(v1["12 QA"],"1V"),(v1["9 QB"],"2V"),(v1["8 QC"],"4V"),(v1["11 QD"],"8V"),
                (v2["12 QA"],"16V"),(v2["9 QB"],"32V"),(v2["8 QC"],"64V"),(v2["11 QD"],"128V"),
                (d4["5 Q"],"256V")]:
    wire(p4,src,oV[pin],pin)
wire(p4,n1["10"],obk["in"]); wire(p4,hsv["3"],osy["in"])

note(p4,"VERIFY (scan-limited, mirrors pg2 uncertainties):\n"
        "\u2022 7493 QA\u2013QD \u2194 1V..256V tap mapping and \u00f716 jumpers; counter designators E8/E9 vs F8/F9.\n"
        "\u2022 Exact taps into 7410 D8 V-RESET decode and into the 7402 NOR V-BLANK latch (best inference).\n"
        "\u2022 D4 / E7 flip-flop pin roles; E7 is one 7474 shared between H RESET (pg2) and V RESET here.\n"
        "\u2022 V SYNC gate inputs (V BLANK + which V tap).",
     920,320,560,170)

render([p1,p2,p3,p4],"/mnt/user-data/outputs/pong_sections.drawio")

# ============================ PAGE 5 ============================
p5g=Page("5 - Vertical Position","pong-sec5")
title(p5g,"Atari PONG \u2014 Section 5: Vertical Position (ball-V).  9316 loadable counters preset 'from vert velocity', "
          "carry-chained; loaded during V BLANK; carry decoded to VVID (ball vertical video).  Mirrors page 3.")
vclk=tag(p5g,"H RESET\n(line rate)\n(verify)",40,90,"src",w=92,h=66)
vbk =tag(p5g,"V BLANK\n(pg4, load)",40,200,"src",w=92,h=50)
vel =tag(p5g,"ball-V preset\nVERT VELOCITY\nA\u1d65-D\u1d65 + GND\n(verify bits)",40,300,"src",w=120,h=80)
p5h =tag(p5g,"+5V",40,430,"src",w=70)
b3=part(p5g,"9316  B3\nload counter",
        ["1 MR","2 CP","3 P0","4 P1","5 P2","6 P3","7 CEP","9 PE","10 CET"],
        ["14 Q0","13 Q1","12 Q2","11 Q3","15 TC"],300,80,170,300)
a3=part(p5g,"9316  A3\nload counter",
        ["1 MR","2 CP","3 P0","4 P1","5 P2","6 P3","7 CEP","9 PE","10 CET"],
        ["14 Q0","13 Q1","12 Q2","11 Q3","15 TC"],620,80,170,300)
b0=part(p5g,"7400  B0\nNAND",["4","5"],["6"],940,120,130,80)
vd=part(p5g,"7402  D2\nNOR",["11","12"],["13"],940,280,130,80)
oVV=part(p5g,"VVID (ball-V video)\n\u2192 pg8 video",["VVID","V-COINC"],[],1260,150,180,110,**GREY)

# clock + load
for c in (b3,a3): wire(p5g,vclk["out"],c["2 CP"],"clk")
wire(p5g,vbk["out"],b3["9 PE"],"V BLANK (load)")
wire(p5g,vbk["out"],a3["9 PE"],"V BLANK (load)")
# preset data (verify bit mapping)
for c in (b3,a3):
    for pin in ("3 P0","4 P1","5 P2","6 P3"): wire(p5g,vel["out"],c[pin])
# carry chain
wire(p5g,b3["15 TC"],a3["10 CET"],"carry")
wire(p5g,a3["15 TC"],b0["4"],"A3 carry")
# enables (inferred tie-highs)
wire(p5g,p5h["out"],b3["7 CEP"]); wire(p5g,p5h["out"],b3["10 CET"])
wire(p5g,p5h["out"],a3["7 CEP"])
# decode -> VVID
wire(p5g,b0["6"],vd["11"]); wire(p5g,a3["15 TC"],vd["12"])
wire(p5g,b0["6"],oVV["V-COINC"],"V coincidence")
wire(p5g,vd["13"],oVV["VVID"],"VVID")

note(p5g,"NOTES / VERIFY (mirrors pg3 uncertainties):\n"
         "\u2022 Clock/load source for ball-V counters: shown H RESET (line rate) + V BLANK load \u2014 verify.\n"
         "\u2022 Preset P0\u2013P3: which bits from VERT VELOCITY (A\u1d65-D\u1d65) vs grounded \u2014 exact bit map unread.\n"
         "\u2022 9316 load(PE) vs enable(CET) pin and CEP/CET tie-highs are inferred.\n"
         "\u2022 B0 / D2 gate roles and the VVID / V-COINC output net names (placeholders).\n"
         "\u2022 NOT TRACED (open, not N.C.): 9316 MR(1) clear source; B0 pin 5, D2 / decode other inputs.",
     300,460,560,180)

render([p1,p2,p3,p4,p5g],"/mnt/user-data/outputs/pong_sections.drawio")
