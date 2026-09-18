from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
rule='body.staff-role #dashboardPage:not(.active)+#staffDashboard{display:none!important}'
if rule not in text:
    old='#staffDashboard{display:grid;gap:12px}'
    if old not in text:
        raise SystemExit('staff dashboard style marker not found')
    text=text.replace(old,old+'\n'+rule,1)
    p.write_text(text,encoding='utf-8')
