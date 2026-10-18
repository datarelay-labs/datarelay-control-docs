#!/usr/bin/env python3
"""Pixel-accurate callouts over existing, historical Control UI test screenshots.

Requires Pillow. Real controls remain unchanged; only crops and overlays.
"""
from pathlib import Path
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "images/screenshots/verified"
TARGET = ROOT / "images/screenshots/annotated"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

@dataclass(frozen=True)
class Shot:
    key: str
    src: str
    crop: tuple[int,int,int,int]
    marks: tuple[tuple[tuple[int,int,int,int],str],...]

SHOTS = [
    Shot("select-connector","01-connect-tabs.png",(244,477,1258,1103),(
        ((260,809,1239,855),"Choose Saved Connector"),
        ((815,1050,1085,1095),"Continue to Sample"))),
    Shot("run-test","02-sample-tabs-run-test.png",(244,489,1258,925),(
        ((260,625,366,660),"Run Test"),
        ((506,752,994,816),"Review HTTP status and records"),
        ((1026,688,1230,724),"Open Record Selection"))),
    Shot("record-selection","03-record-selection-tree.png",(244,905,1258,1417),(
        ((459,941,718,973),"Review suggested record path"),
        ((254,1024,739,1112),"Expand JSON Tree and inspect fields"),
        ((757,1141,1239,1257),"Select a checkpoint field"))),
    Shot("field-mapping","transform-step-screenshot.png",(257,396,1415,1012),(
        ((260,519,667,566),"Inspect incoming sample"),
        ((673,520,1024,566),"Map source fields"),
        ((1035,520,1400,566),"Verify final event preview"))),
    Shot("add-static-field","transform-add-field.png",(672,415,1409,754),(
        ((1275,424,1399,465),"Click Add field"),
        ((1166,465,1401,518),"Choose Static Value"),
        ((1034,539,1161,700),"Close menu, then inspect preview"))),
    Shot("deploy-readiness","08-deploy-blocked-after-api-failure.png",(244,505,1259,1213),(
        ((258,523,1247,600),"Read blocking readiness status"),
        ((262,729,806,853),"Open Edit for missing data/records"),
        ((1060,1167,1257,1205),"Deploy remains unavailable"))),
    Shot("stream-actions","09-stream-created.png",(244,405,1258,861),(
        ((266,471,822,522),"Read Stream creation status"),
        ((291,573,420,609),"Start Stream only when ready"),
        ((291,616,384,655),"Open Logs and verify runtime"))),
    Shot("dashboard-triage","dashboard-overview.png",(241,93,1419,977),(
        ((1122,97,1266,137),"Choose time range"),
        ((244,163,1416,231),"Check overall health"),
        ((1035,736,1414,846),"Use View all for alert detail"))),
    Shot("source-api-error","06-api-failure-blocks-transform.png",(244,548,1258,902),(
        ((260,677,1237,795),"Read HTTP 503 error details"),
        ((364,626,423,663),"Retry after fixing source"),
        ((929,850,1081,885),"Do not advance while blocked"))),
    Shot("saved-draft","02-draft-banner.png",(243,401,1258,461),(
        ((1018,413,1138,452),"Resume saved draft"),
        ((1144,413,1244,452),"Or start fresh"))),
]

def font(size): return ImageFont.truetype(FONT, size=size)

def annotate(shot):
    src=SOURCE/shot.src
    assert src.is_file(),src
    original=Image.open(src).convert("RGB")
    l,t,r,b=shot.crop
    assert 0<=l<r<=original.width and 0<=t<b<=original.height
    crop=original.crop(shot.crop)
    w,h=crop.size
    top=55
    bottom=30+len(shot.marks)*38
    canvas=Image.new("RGB",(w,top+h+bottom),(12,24,38))
    canvas.paste(crop,(0,top))
    d=ImageDraw.Draw(canvas)
    d.text((16,15),"DATARELAY CONTROL",font=font(24),fill=(250,251,253))
    tag="HISTORICAL UI TEST / ANNOTATED"
    tagw=d.textbbox((0,0),tag,font=font(15))[2]
    d.text((w-tagw-17,21),tag,font=font(15),fill=(255,199,91))
    for n,(box,label) in enumerate(shot.marks,1):
        x1,y1,x2,y2=box
        assert l<=x1<x2<=r and t<=y1<y2<=b,(shot.key,box)
        d.rounded_rectangle((x1-l,y1-t+top,x2-l,y2-t+top),radius=9,outline=(255,184,66),width=5)
        cx=max(23,min(w-23,x1-l+17))
        cy=max(top+23,y1-t+top-12)
        d.ellipse((cx-21,cy-21,cx+21,cy+21),fill=(255,195,88),outline=(7,22,35),width=3)
        bb=d.textbbox((0,0),str(n),font=font(24))
        d.text((cx-(bb[2]-bb[0])/2,cy-(bb[3]-bb[1])/2-bb[1]),str(n),font=font(24),fill=(7,22,35))
        d.text((18,top+h+12+(n-1)*38),f"{n}. {label}",font=font(23),fill=(255,242,218))
    TARGET.mkdir(parents=True,exist_ok=True)
    out=TARGET/(shot.key+".webp")
    canvas.save(out,"WEBP",quality=93,method=6)
    assert out.is_file() and out.stat().st_size>5000
    print(out.relative_to(ROOT),out.stat().st_size)

if __name__=="__main__":
    for shot in SHOTS:annotate(shot)
