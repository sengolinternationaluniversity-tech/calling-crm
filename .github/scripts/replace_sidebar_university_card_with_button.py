from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')

# Remove the previously added sidebar university card styles.
old_css='''\n\n/* Sidebar university detail */\n.sidebar-university{margin:-4px 8px 14px;padding:10px 11px;border:1px solid #d8e5f3;border-radius:10px;background:linear-gradient(135deg,#ffffff,#f1f7ff);display:flex;gap:9px;align-items:flex-start}\n.sidebar-university-icon{width:30px;height:30px;flex:0 0 30px;display:grid;place-items:center;border-radius:8px;background:#e8f1ff;color:#2563eb;font-size:15px}\n.sidebar-university b{display:block;color:#173f6c;font-size:11px;line-height:1.25}\n.sidebar-university small{display:block;margin-top:3px;color:#71869d;font-size:9px;line-height:1.25}\n@media(max-width:680px){.sidebar-university{margin:0 8px 12px}}\n'''
text=text.replace(old_css,'\n')
old_html='<div class="sidebar-university"><span class="sidebar-university-icon">◆</span><div><b>Sengol International University</b><small>Admissions &amp; Outreach CRM</small></div></div>\n'
text=text.replace(old_html,'')

# Add a shared Admin + Staff sidebar button.
old_nav='<button data-page="callstatus" class="admin-only">Call Status</button><button data-page="settings">Settings</button>'
new_nav='<button data-page="callstatus" class="admin-only">Call Status</button><button data-page="universitydetail">University Detail</button><button data-page="settings">Settings</button>'
if 'data-page="universitydetail"' not in text:
    if old_nav not in text:
        raise SystemExit('nav target not found')
    text=text.replace(old_nav,new_nav,1)

# Add an icon matching the existing sidebar navigation language.
icon_target='.nav button[data-page="settings"]:before{content:"⚙"}'
icon_rule='.nav button[data-page="universitydetail"]:before{content:"▣"}'
if icon_rule not in text:
    if icon_target not in text:
        raise SystemExit('nav icon target not found')
    text=text.replace(icon_target,icon_rule+icon_target,1)

# Add a lightweight page; details can be expanded later without changing navigation.
page_marker='''\n<!-- University Detail page -->\n<section id="universitydetailPage" class="page">\n  <div class="heading"><div><h1>University Detail</h1><p>Sengol International University information.</p></div></div>\n  <article class="card university-detail-page-card">\n    <h2 style="margin:0 0 6px">Sengol International University</h2>\n    <p style="margin:0;color:var(--muted)">Admissions &amp; Outreach CRM</p>\n  </article>\n</section>\n'''
settings='<section id="settingsPage" class="page">'
if 'id="universitydetailPage"' not in text:
    if settings not in text:
        raise SystemExit('settings page target not found')
    text=text.replace(settings,page_marker+'\n'+settings,1)

p.write_text(text,encoding='utf-8')
