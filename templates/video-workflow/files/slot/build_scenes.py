"""TEMPLATE: the SC list below is the Infosys video example. For a new video replace the SC entries with that video's screens (times from timing_en.json).
Builds index.html (HyperFrames composition) + scene_times.json for the approved Infosys scenes.
All screen times come from the English-mode Whisper pass (edit/transcripts/timing_en.json), so each reveal lands on the spoken word.
Re-run after changing a time:   python3 build_scenes.py
T   = second in the source video where the scene starts, dur = length, rel = reveal time inside the scene (seconds after T).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = {"accent": "#D7263D", "accent_light": "#ff6b7d", "accent_light2": "#ff8a98", "ink": "#14171c", "ground": "#f2f2ef",
         "sans": "Inter Tight", "serif": "Instrument Serif", "sans_file": "InterTight.ttf",
         "serif_italic_file": "InstrumentSerif-Italic.ttf", "serif_regular_file": "InstrumentSerif-Regular.ttf"}
if os.path.exists(os.path.join(HERE, "theme.json")):
    THEME.update(json.load(open(os.path.join(HERE, "theme.json"))))  # the THEME changes per video; everything else stays

ell = '<svg viewBox="0 0 330 120" preserveAspectRatio="none"><path class="draw" d="M20 70 C14 26 110 8 190 14 C290 22 318 70 250 100 C180 124 40 114 22 78" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg>'
TICK = '<u class="tk"><svg viewBox="0 0 24 24"><path class="tkp" d="M6 12.5l4 4 8-9" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></u>'
PTICK = '<svg viewBox="0 0 24 24"><path d="M6 12.5l4 4 8-9" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def bar(on, k=4):
    """Progress bar: shows only the sections that have started (k of them). Earlier ones are 'done' (red), the current one is 'on' (red + bold).
    on='all' = training finished, every section done. k=0 = no bar (before any section starts)."""
    if k == 0:
        return ''
    n = ["Induction", "Generic", "Stream", "Behavioural"][:k]
    def cls(i):
        if on == "all" or (isinstance(on, int) and i < on):
            return "done"
        return "on" if i == on else ""
    return '<div class="bar">' + ''.join(f'<span class="{cls(i)}">{x}</span>' for i, x in enumerate(n)) + '</div>'


def rows(items):
    return '<div class="list">' + ''.join(f'<div class="row"><u>{i+1}</u>{n}<em>{d}</em></div>' for i, (n, d) in enumerate(items)) + '</div>'


def tickrows(items):
    return '<div class="list">' + ''.join(f'<div class="row tkr">{TICK}{n}</div>' for n in items) + '</div>'


def chips(items):
    return '<div class="chips">' + ''.join(f'<div class="chip2">{n}</div>' for n in items) + '</div>'


def bigtick(label):
    return ('<div class="bigtick"><svg viewBox="0 0 100 100"><circle class="bc" cx="50" cy="50" r="46" fill="none" stroke="#D7263D" stroke-width="6"/>'
            '<path class="bp" d="M28 52 L44 67 L73 35" fill="none" stroke="#D7263D" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'<div class="bl">{label}</div></div>')


def months(title, seg2, cap=""):
    return (bar('all') + f'<div class="t">{title}</div><div class="mbar"><div class="seg seg1">3&nbsp;<i>LPA</i></div><div class="seg seg2">{seg2}</div></div>'
            '<div class="mlab ml1">first 6 months</div><div class="mlab ml2">next 12 months</div>' + cap)


# id, T, dur, class, html, js (uses helpers; times are seconds after T), pops (relative), dings (relative)
SC = [
    ("db", 2.0, 18.3, 'light', bar(0, 0) + '<div class="t">Student <i>doubts</i></div>' + chips(["How long?", "What process?", "How many steps?", "Full-time conditions?", "3.6 LPA or 3 LPA?"]) + '<div class="msg m1">Answers <i>in this video</i></div>',
     "inUp('db','.t',.3,30,.5);chipsAt('db',[.4,2.3,3.7,7.7,9.4]);tl.to(Q('db','.chips')[0],{opacity:0,duration:.35},OFF.db[0]+14.6);inUp('db','.m1',15.0,30,.6);", [.4, 2.3, 3.7, 7.7, 9.4], [15.0]),
    ("s2", 28.0, 4.4, 'light', bar(0, 0) + f'<div class="lab">total training</div><div class="num"><span class="circ">92 <i>days</i>{ell}</span></div><div class="sub2">4 parts</div>',
     "inUp('s2','.lab',.2,20,.4);pop('s2','.num',1.0);draw('s2',1.3);inUp('s2','.sub2',3.4,20,.5);", [1.0], []),
    ("s3", 32.5, 13, 'light', bar(0, 0) + '<div class="t">4 <i>parts</i></div>' + rows([("Induction", "5 days"), ("Generic", "36 days"), ("Stream", "45 days"), ("Behavioural", "6 days")]),
     "inUp('s3','.t',.2,30,.5);rowsAt('s3',[.4,2.5,6.0,8.6]);", [.4, 2.5, 6.0, 8.6], []),
    ("s4", 58.2, 6.8, 'light', bar(0, 1) + f'<div class="lab">day 5 · pre-test</div><div class="num"><span class="circ">65<span class="pc">%</span>{ell}</span></div><div class="sub2">to pick your <i>stream</i></div>',
     "inUp('s4','.lab',.3,20,.4);pop('s4','.num',1.7);draw('s4',2.3);inUp('s4','.sub2',5.6,20,.5);", [1.7], []),
    ("s4b", 68.6, 7.0, 'light', bar(0, 1) + '<div class="t">Pre-test <i>syllabus</i></div>' + rows([("Aptitude", ""), ("Verbal Ability", ""), ("Java", ""), ("DBMS", "")]),
     "inUp('s4b','.t',.2,30,.5);rowsAt('s4b',[2.4,3.1,4.6,5.1]);", [2.4, 3.1, 4.6, 5.1], []),
    ("sa1", 84.9, 7.5, 'light', bar(0, 1) + '<div class="t">1st <i>attempt</i></div>' + chips(["Java + Oracle", "Java + React", "Performance Testing"]),
     "inUp('sa1','.t',.2,30,.5);chipsAt('sa1',[1.6,3.0,4.4]);", [1.6, 3.0, 4.4], []),
    ("sa2", 94.2, 4.8, 'light', bar(0, 1) + '<div class="t">2nd <i>attempt</i></div>' + chips(["Software Development Engineering Testing"]),
     "inUp('sa2','.t',.3,30,.5);chipsAt('sa2',[1.7]);", [1.7], []),
    ("sa3", 99.4, 6.8, 'light', bar(0, 1) + '<div class="t">3rd <i>attempt</i></div>' + chips(["AIS", "Windows AS", "Networking"]),
     "inUp('sa3','.t',.3,30,.5);chipsAt('sa3',[2.1,2.8,3.4]);", [2.1, 2.8, 3.4], []),
    ("gt", 110.9, 13.1, 'light', bar(1, 2) + '<div class="t">Generic <i>test</i></div>' + tickrows(["Java", "HSQL"]) + '<div class="sub2 att">3 attempts</div>' + bigtick('Test <i>cleared</i>'),
     "inUp('gt','.t',.2,30,.5);tickRowsAt('gt',[1.2,1.7]);inUp('gt','.sub2',6.7,20,.5);bigTickAt('gt',11.7);", [1.2, 1.7, 6.7], [12.1]),
    ("s5", 124.2, 5.5, 'light', bar(2, 3) + '<div class="t">The <i>journey</i></div><div class="line"><b></b></div>' + ''.join(
        f'<div class="stop" style="left:{x}cqw"></div><div class="lbl" style="left:{x}cqw">{n}<br><i>{d}</i></div>'
        for x, n, d in [(20, "Induction", "5 days"), (50, "Generic", "36 days"), (80, "Stream", "45 days")]),
     "inUp('s5','.t',.2,30,.5);grow('s5','.line',.5,2.6);Q('s5','.stop').forEach((el,i)=>tl.fromTo(el,{opacity:0,scale:.5},{opacity:1,scale:1,duration:.35,ease:'back.out(1.6)'},OFF.s5[0]+.6+i*.55));inUp('s5','.lbl',.8,20,.4,.55);", [], []),
    ("ss", 129.9, 11.0, 'light', bar(2, 3) + '<div class="t">Stream <i>training</i></div><div class="badge">45 days</div>' + chips(["Advanced Java", "Performance Testing", "JMeter", "Front End Performance Testing", "Capstone project"]),
     "inUp('ss','.t',.15,30,.5);pop('ss','.badge',.35,.4);chipsAt('ss',[2.7,3.5,4.7,5.5,8.0]);", [.35, 2.7, 3.5, 4.7, 5.5, 8.0], []),
    ("st", 141.9, 13.0, 'light', bar(2, 3) + '<div class="t">3 <i>assessments</i></div>' + tickrows(["Written", "Written", "Project"]) + bigtick('All <i>cleared</i>'),
     "inUp('st','.t',.3,30,.5);tickRowsAt('st',[3.8,7.0,9.5]);bigTickAt('st',11.3);", [3.8, 7.0, 9.5], [11.75]),
    ("s6", 160.4, 6.4, 'light', bar(3, 4) + '<div class="lab">behavioural test</div><div class="pill2">2 attempts</div><div class="two"><div class="n1">65 <i>questions</i></div></div><div class="sub2">60 minutes</div>',
     "inUp('s6','.lab',.2,20,.4);pop('s6','.pill2',1.1,.4);inUp('s6','.n1',3.7,50,.6);inUp('s6','.sub2',5.6,20,.5);", [1.1, 3.7, 5.6], []),
    ("bp", 166.9, 11.5, 'light', bar(3, 4) + '<div class="t">Pass each <i>level</i></div><div class="line"><b></b></div>' + ''.join(
        f'<div class="stop" style="left:{x}cqw"></div><div class="pass" style="left:{x}cqw">{PTICK}</div><div class="lbl" style="left:{x}cqw">{n}</div>'
        for x, n in [(14, "Induction"), (38, "Generic"), (62, "Stream"), (86, "Behavioural")]) + '<div class="avg">All levels done <i>→ average %</i></div>',
     "inUp('bp','.t',.2,30,.5);progressAt('bp',[1.4,2.9,4.5,6.7]);inUp('bp','.avg',8.8,30,.6);", [1.4, 2.9, 4.5, 6.7], [8.8]),
    ("s7", 187.7, 3.4, 'light', bar('all') + '<div class="lab">first 6 months</div><div class="two"><div class="n1">3 <i>LPA</i></div></div><div class="sub2">fixed package</div>',
     "inUp('s7','.lab',.2,20,.4);pop('s7','.n1',1.8);inUp('s7','.sub2',2.4,20,.5);", [1.8], [1.8]),
    ("s8", 193.9, 13.2, 'light', bar('all') + '<div class="t">Your <i>average</i></div>' + rows([("65–69%", "incentive"), ("70–79%", "incentive"), ("80%+", "3.6 LPA")]),
     "inUp('s8','.t',.2,30,.5);rowsAt('s8',[1.2,5.9,9.9]);", [1.2, 5.9, 9.9], []),
    ("s9", 207.2, 3.7, 'light', bar('all') + '<div class="lab">full time</div><div class="two"><div class="n1 red">3.6 <i>LPA</i></div></div><div class="sub2">80% average or more</div>',
     "inUp('s9','.lab',1.5,20,.4);pop('s9','.n1',.4);inUp('s9','.sub2',2.2,20,.5);", [.4], [.4]),
    ("mo1", 211.0, 3.9, 'light', months('Your <i>package</i>', '3.6&nbsp;<i>LPA</i>'),
     "inUp('mo1','.t',.2,30,.5);grow('mo1','.seg1',.15,.6);grow('mo1','.seg2',1.5,.8);inUp('mo1','.ml1',.5,20,.4);inUp('mo1','.ml2',1.6,20,.4);", [1.5], []),
    ("hd", 220.4, 18.4, 'light', bar('all') + '<div class="t">Training <i>difficulty</i></div><div class="list"><div class="row"><u>1</u>Cognizant<em></em></div><div class="row"><u>2</u>Accenture<em></em></div><div class="row hot"><u>3</u>Infosys<em>hardest</em></div></div><div class="msg m1">Don\'t <i>cool down</i></div><div class="msg m2">Stay <i>focused</i></div>',
     "inUp('hd','.t',.2,30,.5);rowsAt('hd',[1.8,2.5,6.4]);inUp('hd','.m1',11.2,30,.5);tl.to(Q('hd','.m1')[0],{opacity:0,duration:.3},OFF.hd[0]+15.0);inUp('hd','.m2',15.4,30,.5);", [1.8, 2.5, 6.4], []),
    ("s10", 244.8, 4.0, 'broll', '<div class="scrim"></div><div class="w">No <i>re-attempts</i></div><div class="chip">for 3.6 LPA</div><div class="line"></div>',
     "inUp('s10','.w',.75,50,.7);inUp('s10','.chip',2.5,20,.5);grow('s10','.line',2.6,.8);", [2.5], []),
    ("mo2", 262.6, 5.4, 'light', months('What <i>decides</i> it', '?', '<div class="cap2">decided by <i>your assessments</i></div>'),
     "inUp('mo2','.t',.2,30,.5);grow('mo2','.seg1',.4,.6);grow('mo2','.seg2',1.9,.8);inUp('mo2','.ml1',.6,20,.4);inUp('mo2','.ml2',2.0,20,.4);inUp('mo2','.cap2',4.3,30,.5);", [1.9, 4.3], []),
]

off = 0.0
body = ""
OFF = {}
TIMES = {}
anim = ""
for sid, T, dur, cls, h, js, pops, dings in SC:
    OFF[sid] = [round(off, 3), dur]
    TIMES[sid] = {"T": T, "dur": dur, "pops": pops, "dings": dings}
    if sid == "s10":
        body += f'<video id="nb" muted playsinline class="clip" data-start="{round(off, 3)}" data-duration="{dur}" data-track-index="0" src="assets/focus.mp4" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover"></video>\n'
    body += f'<div id="{sid}" class="clip scene {cls}" data-start="{round(off, 3)}" data-duration="{dur}" data-track-index="0">{h}</div>\n'
    anim += f"// {sid}  (source {T}s)\n{js}\n"
    off += dur
total = round(off, 3)

SCENES_HTML = os.path.join(HERE, "base_styles.html")  # base look of the approved scenes (kept in the project)
css = open(SCENES_HTML).read()
css = css[css.index("<style>") + 7:css.index("</style>")]
css = css.replace(".s{display:none;", ".scene{").replace(".s:target{display:block}.s>*{position:absolute}", ".scene>*{position:absolute}").replace(".s i{", ".scene i{")
css = css.replace(".broll{background:#000 url(data:image/jpeg;base64,__B2__) center/cover}", ".broll{background:#000}.broll video{left:0;top:0;width:100%;height:100%;object-fit:cover}")
EXTRA = """
.chips{left:8cqw;top:26cqw;display:flex;flex-wrap:wrap;gap:1.8cqw;width:80cqw}.chip2{background:#fff;border-radius:99cqw;padding:1.4cqw 3.4cqw;font-weight:700;font-size:4.4cqw;box-shadow:0 .5cqw 1.6cqw rgba(0,0,0,.08)}
.row u svg{width:72%;height:72%}.row.tkr{width:50cqw}.sub2.att{top:42cqw}
.badge{left:62cqw;top:13cqw;background:#D7263D;color:#fff;font-weight:800;font-size:4cqw;padding:.8cqw 2.6cqw;border-radius:99cqw}
.bigtick{left:64cqw;top:16.5cqw;width:26cqw;text-align:center}.bigtick svg{position:relative;width:26cqw;height:26cqw;display:block}
.bigtick .bl{position:relative;font-weight:800;font-size:4.4cqw;margin-top:1.4cqw}.bigtick .bl i{font-size:5.2cqw}
#ss .badge{left:8cqw;top:21.6cqw}#ss .chips{top:31cqw;width:86cqw}#ss .chip2{font-size:3.8cqw;padding:1.2cqw 3cqw}
.pass{top:30.4cqw;width:4.2cqw;height:4.2cqw;border-radius:50%;background:#D7263D;transform:translateX(-50%);display:flex;align-items:center;justify-content:center}.pass svg{width:70%;height:70%}
.avg{left:8cqw;top:46cqw;font-weight:800;font-size:4.4cqw}.avg i{font-size:5cqw}#bp .lbl{top:38cqw}
.row.hot{background:#D7263D;color:#fff}.row.hot em{color:#fff}.row.hot u{background:#fff;color:#D7263D}
.msg{left:8cqw;top:47cqw;font-weight:800;font-size:5cqw}.msg i{font-size:5.8cqw}
.pill2{left:8cqw;top:15.6cqw;background:#D7263D;color:#fff;font-weight:800;font-size:3.6cqw;padding:.8cqw 2.4cqw;border-radius:99cqw}
.mbar{left:8cqw;top:24cqw;width:84cqw;height:13cqw;display:flex;gap:1cqw}
.seg{height:100%;border-radius:1.8cqw;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:5cqw;color:#fff;overflow:hidden;white-space:nowrap}
.seg1{width:27.7cqw;background:#14171c}.seg2{width:55.3cqw;background:#D7263D}.seg i{color:#fff;font-size:5.8cqw}
.mlab{top:39cqw;font-weight:700;font-size:3.4cqw;color:#5d6572}.ml1{left:8cqw}.ml2{left:36.7cqw}
.cap2{left:8cqw;top:46cqw;font-weight:800;font-size:4.4cqw}.cap2 i{font-size:5cqw}
.bar span{flex:0 0 calc(25% - .6cqw)}.bar span.done{border-top-color:var(--c);color:#5d6572}.bar span.on{font-weight:800}
#db .chips{top:26cqw;width:86cqw}#db .chip2{font-size:3.8cqw;padding:1.2cqw 3cqw}#db .msg{top:30cqw;font-size:7.4cqw}#db .msg i{font-size:8.6cqw}
#s10 .w{right:auto;left:6cqw;text-align:left}#s10 .chip{right:auto;left:6cqw}#s10 .line{right:auto;left:6cqw}#s10 .scrim{background:linear-gradient(90deg,rgba(0,0,0,.62),rgba(0,0,0,0) 62%)}
"""
css += EXTRA

fonts = (f"@font-face{{font-family:'{THEME['sans']}';src:url(assets/fonts/{THEME['sans_file']});font-weight:100 900}}\n"
         f"@font-face{{font-family:'{THEME['serif']}';src:url(assets/fonts/{THEME['serif_regular_file']});font-style:normal}}\n"
         f"@font-face{{font-family:'{THEME['serif']}';src:url(assets/fonts/{THEME['serif_italic_file']});font-style:italic}}\n")

JS_HELPERS = """
const OFF=__OFF__;
window.__timelines=window.__timelines||{};
const tl=gsap.timeline({paused:true});
const Q=(s,sel)=>document.querySelectorAll('#'+s+' '+sel);
function inUp(s,sel,rel,dy,d,stag){dy=dy||40;d=d||.5;stag=stag||0;Q(s,sel).forEach((el,i)=>tl.fromTo(el,{opacity:0,y:dy},{opacity:1,y:0,duration:d,ease:"power3.out"},OFF[s][0]+rel+i*stag));}
function pop(s,sel,rel,d){d=d||.45;Q(s,sel).forEach(el=>tl.fromTo(el,{opacity:0,scale:.6},{opacity:1,scale:1,duration:d,ease:"back.out(1.6)"},OFF[s][0]+rel));}
function draw(s,rel,d){d=d||.8;Q(s,'svg path.draw').forEach(p=>{const L=p.getTotalLength();p.style.strokeDasharray=L;tl.fromTo(p,{strokeDashoffset:L},{strokeDashoffset:0,duration:d,ease:"power2.inOut"},OFF[s][0]+rel);});}
function grow(s,sel,rel,d){Q(s,sel).forEach(el=>{const w=getComputedStyle(el).width;tl.fromTo(el,{width:0},{width:w,duration:d,ease:"power2.out"},OFF[s][0]+rel);});}
function rowsAt(s,times){const r=Q(s,'.row');times.forEach((t,i)=>{if(r[i])tl.fromTo(r[i],{opacity:0,y:50},{opacity:1,y:0,duration:.5,ease:"power3.out"},OFF[s][0]+t);});}
function chipsAt(s,times){const r=Q(s,'.chip2');times.forEach((t,i)=>{if(r[i])tl.fromTo(r[i],{opacity:0,y:40,scale:.9},{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(1.4)"},OFF[s][0]+t);});}
function tickRowsAt(s,times){const r=Q(s,'.row');times.forEach((t,i)=>{if(!r[i])return;tl.fromTo(r[i],{opacity:0,y:50},{opacity:1,y:0,duration:.5,ease:"power3.out"},OFF[s][0]+t);const p=r[i].querySelector('.tkp');const L=p.getTotalLength();p.style.strokeDasharray=L;tl.fromTo(p,{strokeDashoffset:L},{strokeDashoffset:0,duration:.35,ease:"power2.out"},OFF[s][0]+t+.4);});}
function bigTickAt(s,t){const c=Q(s,'.bigtick .bc')[0],p=Q(s,'.bigtick .bp')[0],b=Q(s,'.bigtick')[0],l=Q(s,'.bigtick .bl')[0];const Lc=c.getTotalLength(),Lp=p.getTotalLength();c.style.strokeDasharray=Lc;p.style.strokeDasharray=Lp;tl.fromTo(b,{opacity:0,scale:.85},{opacity:1,scale:1,duration:.3,ease:"back.out(1.6)"},OFF[s][0]+t);tl.fromTo(c,{strokeDashoffset:Lc},{strokeDashoffset:0,duration:.55,ease:"power2.inOut"},OFF[s][0]+t);tl.fromTo(p,{strokeDashoffset:Lp},{strokeDashoffset:0,duration:.4,ease:"power2.out"},OFF[s][0]+t+.45);tl.fromTo(l,{opacity:0,y:20},{opacity:1,y:0,duration:.4},OFF[s][0]+t+.8);}
function progressAt(s,pass){const st=OFF[s][0],ln=Q(s,'.line b')[0],W=parseFloat(getComputedStyle(Q(s,'.line')[0]).width);tl.set(ln,{width:0},0);pass.forEach((t,i)=>{if(i>0)tl.to(ln,{width:W*i/3,duration:.6,ease:"power2.inOut"},st+t-.6);tl.fromTo(Q(s,'.pass')[i],{opacity:0,scale:.4},{opacity:1,scale:1,duration:.35,ease:"back.out(1.8)"},st+t);tl.fromTo(Q(s,'.lbl')[i],{opacity:0,y:20},{opacity:1,y:0,duration:.4},st+t-.3);tl.fromTo(Q(s,'.stop')[i],{opacity:0},{opacity:1,duration:.3},st+t-.3);});}
Object.keys(OFF).forEach(s=>Q(s,'.bar').forEach(b=>tl.fromTo(b,{opacity:0},{opacity:1,duration:.4},OFF[s][0])));
['s4','gt','s5','s6'].forEach(s=>{if(!OFF[s])return;Q(s,'.bar span.on').forEach(sp=>tl.fromTo(sp,{borderTopColor:'#cfcfca'},{borderTopColor:'#D7263D',duration:.5,ease:"power2.out"},OFF[s][0]+.25));});
['s7','s8','s9','mo1','mo2','hd'].forEach(s=>{if(!OFF[s])return;Q(s,'.bar span').forEach((sp,i)=>tl.fromTo(sp,{borderTopColor:'#cfcfca',color:'#7a808a'},{borderTopColor:'#D7263D',color:'#14171c',duration:.35,ease:"power2.out"},OFF[s][0]+.25+i*.28));});
""".replace("__OFF__", json.dumps(OFF))

html = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{fonts}
:root{{--c:#D7263D}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:#000}}
#root{{width:1920px;height:1080px;position:relative}}
{css}
.scene{{position:absolute;inset:0;width:1920px;height:1080px}}
#s10{{background:transparent}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{body}
</div>
<script>{JS_HELPERS}
{anim}
window.__timelines["main"]=tl;tl.seek(0);</script>
</body></html>"""
for old, new in [("#D7263D", THEME["accent"]), ("#ff6b7d", THEME["accent_light"]), ("#ff8a98", THEME["accent_light2"]),
                 ("#14171c", THEME["ink"]), ("#f2f2ef", THEME["ground"]), ("'Inter Tight'", "'" + THEME["sans"] + "'"), ("'Instrument Serif'", "'" + THEME["serif"] + "'")]:
    html = html.replace(old, new)
open(os.path.join(HERE, "index.html"), "w").write(html)
json.dump(OFF, open(os.path.join(HERE, "offsets.json"), "w"))
json.dump(TIMES, open(os.path.join(HERE, "scene_times.json"), "w"), indent=1)
print("total", total, "scenes", len(SC))
