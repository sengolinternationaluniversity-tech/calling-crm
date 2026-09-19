from pathlib import Path

p=Path('index.html')
text=p.read_text(encoding='utf-8')

old_markup='''  <section class="card university-detail-panel" data-university-panel="fee">\n    <div class="toolbar"><div><h2>Fee Detail</h2><p class="university-detail-note">Admin ke saved departments, columns, calculations aur courses yahan live dikhte hain.</p></div><div class="fee-admin-actions"><button id="addFeeDepartment" class="btn primary admin-only" type="button">+ Department</button><button id="refreshFeeBuilder" class="btn secondary" type="button">Refresh</button></div></div>\n    <div id="feeBuilderHost"><p class="empty">Fee details loading...</p></div>\n  </section>'''
new_markup='''  <section class="card university-detail-panel" data-university-panel="fee">\n    <div class="toolbar"><div><h2>Fee Detail</h2><p class="university-detail-note">Admin ke saved departments, columns, calculations aur courses yahan live dikhte hain.</p></div><div class="fee-admin-actions"><button id="addFeeDepartment" class="btn primary admin-only" type="button">+ Department</button><button id="refreshFeeBuilder" class="btn secondary" type="button">Refresh</button></div></div>\n    <div class="fee-search-wrap"><input id="feeSearch" type="search" autocomplete="off" placeholder="Search course, specialization, eligibility, faculty..."></div>\n    <div id="feeBuilderHost"><p class="empty">Fee details loading...</p></div>\n  </section>'''
if old_markup not in text:
    raise SystemExit('fee detail markup target not found')
text=text.replace(old_markup,new_markup,1)

start=text.find('function renderFeeBuilder(){')
end=text.find('\nwindow.addFeeDepartment=', start)
if start<0 or end<0:
    raise SystemExit('renderFeeBuilder block not found')

new_func=r'''function renderFeeBuilder(){
 const host=$('#feeBuilderHost'),allCols=S.feeColumns||[],cols=allCols.filter(x=>x.active),deps=(S.feeDepartments||[]).filter(x=>x.active),query=String($('#feeSearch')?.value||'').trim().toLowerCase();
 const manager=$('#feeColumnManager');
 if(manager&&isAdmin())manager.innerHTML=allCols.map(c=>`<span class="fee-column-chip ${c.active?'':'inactive'}"><b>${esc(c.label)}</b><small>${esc(c.column_key)}${c.formula?' = '+esc(c.formula):''}</small><button type="button" onclick="editFeeColumn('${attr(c.id)}')">Edit</button><button type="button" onclick="toggleFeeColumn('${attr(c.id)}',${!c.active})">${c.active?'Hide':'Show'}</button><button type="button" onclick="deleteFeeColumn('${attr(c.id)}')">×</button></span>`).join('')||'<span class="fee-builder-note">No columns</span>';
 const sections=deps.map(dep=>{
   const departmentMatch=query&&String(dep.name||'').toLowerCase().includes(query);
   const rows=(S.feeRows||[]).filter(x=>x.department_id===dep.id&&x.active).filter(row=>{
     if(!query||departmentMatch)return true;
     const resolved=feeResolvedRow(row,cols),hay=[dep.name,...Object.values(row.row_data||{}),...cols.map(c=>c.label),...cols.map(c=>resolved[c.column_key])].map(v=>String(v??'')).join(' ').toLowerCase();
     return hay.includes(query)
   });
   if(query&&!departmentMatch&&!rows.length)return '';
   return `<section class="fee-department"><div class="fee-department-head"><h3>${esc(dep.name)}</h3>${isAdmin()?`<div class="fee-department-actions"><button class="btn primary" type="button" onclick="openFeeRowEditor('${attr(dep.id)}')">+ Course</button><button class="btn secondary" type="button" onclick="editFeeDepartment('${attr(dep.id)}')">Edit Department</button><button class="btn danger" type="button" onclick="deleteFeeDepartment('${attr(dep.id)}')">Delete</button></div>`:''}</div><div class="fee-data-wrap"><table class="fee-data-table"><thead><tr><th>S.No.</th>${cols.map(c=>`<th title="Key: ${attr(c.column_key)}${c.formula?' | Formula: '+attr(c.formula):''}">${esc(c.label)}</th>`).join('')}${isAdmin()?'<th>Action</th>':''}</tr></thead><tbody>${rows.map((row,i)=>{const data=feeResolvedRow(row,cols);return `<tr><td>${i+1}</td>${cols.map(c=>`<td class="${c.value_type==='currency'?'fee-currency':''}">${feeDisplayValue(c,data[c.column_key])}</td>`).join('')}${isAdmin()?`<td class="fee-row-actions"><button class="btn secondary" type="button" onclick="openFeeRowEditor('${attr(dep.id)}','${attr(row.id)}')">Edit</button><button class="btn danger" type="button" onclick="deleteFeeRow('${attr(row.id)}')">Delete</button></td>`:''}</tr>`}).join('')||`<tr><td colspan="${cols.length+1+(isAdmin()?1:0)}" class="empty">No courses added</td></tr>`}</tbody></table></div></section>`
 }).filter(Boolean);
 host.innerHTML=sections.join('')||(query?'<p class="empty">No matching fee records found</p>':'<p class="empty">No active departments</p>')
}
const feeSearchInput=$('#feeSearch');if(feeSearchInput)feeSearchInput.addEventListener('input',()=>renderFeeBuilder());'''
text=text[:start]+new_func+text[end:]

css='''\n\n/* Fee Detail search */\n.fee-search-wrap{margin:14px 0 4px}\n.fee-search-wrap input{width:min(680px,100%);padding:11px 14px;border:1px solid #c8d8e9;border-radius:9px;background:#fff;color:#17324d;outline:none}\n.fee-search-wrap input:focus{border-color:#7fa6d1;box-shadow:0 0 0 3px #dceafb}\n.fee-search-wrap input::placeholder{color:#7b8ea2}\n'''
if '/* Fee Detail search */' not in text:
    text=text.replace('</style>',css+'\n</style>',1)

p.write_text(text,encoding='utf-8')
