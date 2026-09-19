from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')

start=text.find('function renderFeeBuilder(){')
end=text.find('\nwindow.addFeeDepartment=', start)
if start<0 or end<0:
    raise SystemExit('renderFeeBuilder block not found')

old_func=r'''function renderFeeBuilder(){const host=$('#feeBuilderHost'),allCols=S.feeColumns||[],cols=allCols.filter(x=>x.active),deps=(S.feeDepartments||[]).filter(x=>x.active);const manager=$('#feeColumnManager');if(manager&&isAdmin())manager.innerHTML=allCols.map(c=>`<span class="fee-column-chip ${c.active?'':'inactive'}"><b>${esc(c.label)}</b><small>${esc(c.column_key)}${c.formula?' = '+esc(c.formula):''}</small><button type="button" onclick="editFeeColumn('${attr(c.id)}')">Edit</button><button type="button" onclick="toggleFeeColumn('${attr(c.id)}',${!c.active})">${c.active?'Hide':'Show'}</button><button type="button" onclick="deleteFeeColumn('${attr(c.id)}')">×</button></span>`).join('')||'<span class="fee-builder-note">No columns</span>';host.innerHTML=deps.map(dep=>{const rows=(S.feeRows||[]).filter(x=>x.department_id===dep.id&&x.active);return `<section class="fee-department"><div class="fee-department-head"><h3>${esc(dep.name)}</h3>${isAdmin()?`<div class="fee-department-actions"><button class="btn primary" type="button" onclick="openFeeRowEditor('${attr(dep.id)}')">+ Course</button><button class="btn secondary" type="button" onclick="editFeeDepartment('${attr(dep.id)}')">Edit Department</button><button class="btn danger" type="button" onclick="deleteFeeDepartment('${attr(dep.id)}')">Delete</button></div>`:''}</div><div class="fee-data-wrap"><table class="fee-data-table"><thead><tr><th>S.No.</th>${cols.map(c=>`<th title="Key: ${attr(c.column_key)}${c.formula?' | Formula: '+attr(c.formula):''}">${esc(c.label)}</th>`).join('')}${isAdmin()?'<th>Action</th>':''}</tr></thead><tbody>${rows.map((row,i)=>{const data=feeResolvedRow(row,cols);return `<tr><td>${i+1}</td>${cols.map(c=>`<td class="${c.value_type==='currency'?'fee-currency':''}">${feeDisplayValue(c,data[c.column_key])}</td>`).join('')}${isAdmin()?`<td class="fee-row-actions"><button class="btn secondary" type="button" onclick="openFeeRowEditor('${attr(dep.id)}','${attr(row.id)}')">Edit</button><button class="btn danger" type="button" onclick="deleteFeeRow('${attr(row.id)}')">Delete</button></td>`:''}</tr>`}).join('')||`<tr><td colspan="${cols.length+1+(isAdmin()?1:0)}" class="empty">No courses added</td></tr>`}</tbody></table></div></section>`}).join('')||'<p class="empty">No active departments</p>'}'''
text=text[:start]+old_func+text[end:]

css_start=text.find('/* Fee faculty 3-column selector */')
if css_start>=0:
    css_end=text.find('</style>', css_start)
    if css_end<0:
        raise SystemExit('style end not found')
    text=text[:css_start]+text[css_end:]

settings_css=r'''

/* Fee Settings 3-column boxes */
#feeColumnManager.fee-column-manager{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:11px}
#feeColumnManager .fee-column-chip{width:100%;min-height:86px;display:grid;grid-template-columns:1fr auto auto auto;align-items:center;gap:6px;padding:10px 11px}
#feeColumnManager .fee-column-chip b,#feeColumnManager .fee-column-chip small{grid-column:1/-1;display:block;min-width:0;overflow-wrap:anywhere}
#feeColumnManager .fee-column-chip b{font-size:13px;color:#173f6c}
#feeColumnManager .fee-column-chip small{font-size:11px;color:#6b7f95}
#feeColumnManager>.fee-builder-note{grid-column:1/-1}
@media(max-width:980px){#feeColumnManager.fee-column-manager{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:680px){#feeColumnManager.fee-column-manager{grid-template-columns:1fr}}
'''
if '/* Fee Settings 3-column boxes */' not in text:
    text=text.replace('</style>', settings_css+'\n</style>',1)

p.write_text(text,encoding='utf-8')
