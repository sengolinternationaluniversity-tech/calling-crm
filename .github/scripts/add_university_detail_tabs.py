from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
marker='/* University detail tabs */'
if marker in text:
    raise SystemExit('already applied')
old='''<section id="universitydetailPage" class="page">\n  <div class="heading"><div><h1>University Detail</h1><p>Sengol International University information.</p></div></div>\n  <article class="card university-detail-page-card">\n    <h2 style="margin:0 0 6px">Sengol International University</h2>\n    <p style="margin:0;color:var(--muted)">Admissions &amp; Outreach CRM</p>\n  </article>\n</section>'''
new='''<section id="universitydetailPage" class="page">\n  <div class="heading"><div><h1>University Detail</h1><p>Sengol International University information.</p></div></div>\n  <div class="university-detail-tabs" role="tablist" aria-label="University detail sections">\n    <button type="button" class="university-detail-tab" data-university-tab="fee">Fee Detail</button>\n    <button type="button" class="university-detail-tab" data-university-tab="approval">Approval</button>\n    <button type="button" class="university-detail-tab active" data-university-tab="info">University Info</button>\n  </div>\n  <section class="card university-detail-panel" data-university-panel="fee">\n    <h2>Fee Detail</h2>\n    <p class="university-detail-note">Fee structure aur fee details yahan show hongi. Actual fee data add hone ke baad isi section mein rakha jayega.</p>\n  </section>\n  <section class="card university-detail-panel" data-university-panel="approval">\n    <h2>Approval</h2>\n    <p class="university-detail-note">University approvals aur recognition details yahan show hongi. Verified approval data add hone ke baad isi section mein rakha jayega.</p>\n  </section>\n  <section class="card university-detail-panel active" data-university-panel="info">\n    <h2>Sengol International University</h2>\n    <p class="university-detail-note">Admissions &amp; Outreach CRM</p>\n  </section>\n</section>'''
if old not in text:
    raise SystemExit('university detail section not found')
text=text.replace(old,new,1)
css='''\n\n/* University detail tabs */\n.university-detail-tabs{display:flex;gap:9px;flex-wrap:wrap;margin:0 0 14px;padding:8px;background:#f4f8ff;border:1px solid #d7e5f6;border-radius:12px;width:max-content;max-width:100%}\n.university-detail-tab{border:1px solid #c8d9ee;background:#fff;color:#31577f;padding:10px 17px;border-radius:9px;font-weight:800;cursor:pointer;transition:.15s ease}\n.university-detail-tab:hover{background:#edf5ff;border-color:#9fbfe3}\n.university-detail-tab.active{background:#2563eb;color:#fff;border-color:#2563eb;box-shadow:0 4px 12px #2563eb24}\n.university-detail-panel{display:none;margin-top:0;min-height:150px;padding:22px}\n.university-detail-panel.active{display:block}\n.university-detail-panel h2{margin:0 0 8px;color:#173f6c}\n.university-detail-note{margin:0;color:var(--muted);line-height:1.6}\n@media(max-width:680px){.university-detail-tabs{width:100%}.university-detail-tab{flex:1 1 100%;text-align:left}}\n'''
text=text.replace('</style>',css+'\n</style>',1)
js='''\n\n// University detail internal tabs\ndocument.querySelectorAll('[data-university-tab]').forEach(btn=>{\n  btn.addEventListener('click',()=>{\n    const mode=btn.dataset.universityTab;\n    document.querySelectorAll('[data-university-tab]').forEach(x=>x.classList.toggle('active',x===btn));\n    document.querySelectorAll('[data-university-panel]').forEach(x=>x.classList.toggle('active',x.dataset.universityPanel===mode));\n  });\n});\n'''
needle='/* Staff University Detail new-tab behavior */'
if needle not in text:
    raise SystemExit('staff university behavior marker not found')
text=text.replace(needle,js+'\n'+needle,1)
p.write_text(text,encoding='utf-8')
