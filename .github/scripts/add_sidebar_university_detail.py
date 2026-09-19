from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
marker='/* Sidebar university detail */'
if marker in text:
    raise SystemExit('already applied')
css='''\n\n/* Sidebar university detail */\n.sidebar-university{margin:-4px 8px 14px;padding:10px 11px;border:1px solid #d8e5f3;border-radius:10px;background:linear-gradient(135deg,#ffffff,#f1f7ff);display:flex;gap:9px;align-items:flex-start}\n.sidebar-university-icon{width:30px;height:30px;flex:0 0 30px;display:grid;place-items:center;border-radius:8px;background:#e8f1ff;color:#2563eb;font-size:15px}\n.sidebar-university b{display:block;color:#173f6c;font-size:11px;line-height:1.25}\n.sidebar-university small{display:block;margin-top:3px;color:#71869d;font-size:9px;line-height:1.25}\n@media(max-width:680px){.sidebar-university{margin:0 8px 12px}}\n'''
text=text.replace('</style>',css+'\n</style>',1)
old='<aside class="side"><div class="brand"><span>Calling CRM<small>Connect · Track · Grow</small></span></div>\n<nav class="nav">'
new='<aside class="side"><div class="brand"><span>Calling CRM<small>Connect · Track · Grow</small></span></div>\n<div class="sidebar-university"><span class="sidebar-university-icon">◆</span><div><b>Sengol International University</b><small>Admissions &amp; Outreach CRM</small></div></div>\n<nav class="nav">'
if old not in text:
    raise SystemExit('sidebar target not found')
text=text.replace(old,new,1)
p.write_text(text,encoding='utf-8')
