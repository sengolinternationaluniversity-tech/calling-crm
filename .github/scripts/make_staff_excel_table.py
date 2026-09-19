from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Admin staff Excel table */'
if marker in text:
    raise SystemExit(0)

old = '<section id="staffPage" class="page"><div class="heading"><div><h1>Staff</h1><p>Staff accounts Supabase Authentication se create hote hain.</p></div></div><div id="staffGrid" class="staff-grid"></div></section>'
new = '''<section id="staffPage" class="page"><div class="heading"><div><h1>Staff</h1><p>Staff accounts Supabase Authentication se create hote hain.</p></div></div><div id="staffGrid" class="staff-grid staff-grid-source" aria-hidden="true"></div><div class="table-wrap admin-staff-table-wrap"><table class="admin-staff-excel"><thead><tr><th>S.No.</th><th>Staff Name</th><th>User Name</th><th>Password</th><th>Action</th></tr></thead><tbody id="staffListBody"><tr><td colspan="5" class="empty">Loading staff...</td></tr></tbody></table></div></section>'''
if old not in text:
    raise SystemExit('staffPage source not found')
text = text.replace(old, new, 1)

css = r'''

/* Admin staff Excel table */
#staffPage .staff-grid-source{display:none!important}
#staffPage .admin-staff-table-wrap{margin-top:8px;border:1px solid #cbdbea;border-radius:10px;background:#fff;overflow:auto}
#staffPage .admin-staff-excel{width:100%;min-width:820px;border-collapse:collapse;table-layout:fixed;background:#fff}
#staffPage .admin-staff-excel th,
#staffPage .admin-staff-excel td{padding:12px 14px;border-right:1px solid #d6e2ef;border-bottom:1px solid #d6e2ef;text-align:left;vertical-align:middle}
#staffPage .admin-staff-excel th:last-child,
#staffPage .admin-staff-excel td:last-child{border-right:0}
#staffPage .admin-staff-excel tbody tr:last-child td{border-bottom:0}
#staffPage .admin-staff-excel th{background:#edf4ff;color:#2457a6;font-size:13px;font-weight:800}
#staffPage .admin-staff-excel td{color:#17324d;font-size:13px}
#staffPage .admin-staff-excel th:nth-child(1),#staffPage .admin-staff-excel td:nth-child(1){width:75px;text-align:center}
#staffPage .admin-staff-excel th:nth-child(2){width:25%}
#staffPage .admin-staff-excel th:nth-child(3){width:25%}
#staffPage .admin-staff-excel th:nth-child(4){width:150px}
#staffPage .admin-staff-excel th:nth-child(5){width:310px}
#staffPage .admin-staff-excel tbody tr:nth-child(even) td{background:#f9fbff}
#staffPage .admin-staff-excel tbody tr:hover td{background:#eef5ff}
#staffPage .staff-password-mask{display:inline-block;min-width:82px;letter-spacing:2px;color:#526b83;font-weight:700}
#staffPage .staff-name-cell b{display:block;color:#173f6c;font-size:14px}
#staffPage .staff-name-cell small{display:block;margin-top:3px;color:#7b8ea2;font-size:10px;text-transform:uppercase;font-weight:700}
#staffPage .staff-list-actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
#staffPage .staff-list-actions .btn{padding:6px 9px;border-radius:7px;font-size:11px;font-weight:700;white-space:nowrap}
#staffPage .staff-password-btn{background:#edf4ff;color:#2457a6;border:1px solid #cbdcf3}
#staffPage .staff-status-btn{background:#f3f7fc;color:#31516d;border:1px solid #d4e1ee}
#staffPage .staff-status-btn.activate{background:#edf9f2;color:#1f8b59;border-color:#cbe6d6}
@media(max-width:680px){#staffPage .admin-staff-table-wrap{border-radius:8px}}
'''
text = text.replace('</style>', css + '\n</style>', 1)

js = r'''

/* Admin staff Excel table */
function renderAdminStaffExcelTable(){
 const body=document.getElementById('staffListBody');if(!body)return;
 const rows=(S.staff||[]).filter(x=>String(x.role||'').toLowerCase()==='staff');
 body.innerHTML=rows.map((x,i)=>`<tr><td><b>${i+1}</b></td><td class="staff-name-cell"><b>${esc(x.full_name||x.username||'Unnamed')}</b><small>${x.active?'Active':'Inactive'}</small></td><td><b>${esc(x.username||'—')}</b></td><td><span class="staff-password-mask" title="Existing password Supabase se read nahi kiya ja sakta">••••••••</span></td><td><div class="staff-list-actions"><button class="btn primary" type="button" onclick="editStaff('${attr(x.id)}')">Edit</button><button class="btn staff-password-btn" type="button" onclick="openStaffPassword('${attr(x.id)}')">Change Password</button><button class="btn staff-status-btn ${x.active?'':'activate'}" type="button" onclick="toggleStaffStatus('${attr(x.id)}',${x.active?'false':'true'})">${x.active?'Deactivate':'Activate'}</button></div></td></tr>`).join('')||'<tr><td colspan="5" class="empty">No staff accounts</td></tr>'
}
window.openStaffPassword=id=>{window.editStaff(id);setTimeout(()=>{const form=document.getElementById('staffForm');if(!form)return;const input=form.elements.password,title=document.getElementById('staffModalTitle');if(title)title.textContent='Change Staff Password';if(input){input.value='';input.focus()}},0)};
const staffGridSource=document.getElementById('staffGrid');
if(staffGridSource)new MutationObserver(()=>renderAdminStaffExcelTable()).observe(staffGridSource,{childList:true,subtree:true,characterData:true});
document.querySelector('[data-page="staff"]')?.addEventListener('click',()=>setTimeout(renderAdminStaffExcelTable,0));
'''
pos = text.rfind('</script>')
if pos == -1:
    raise SystemExit('main script closing tag not found')
text = text[:pos] + js + '\n' + text[pos:]
p.write_text(text, encoding='utf-8')
