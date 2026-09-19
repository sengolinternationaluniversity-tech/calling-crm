from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
start=text.find('function renderFeeBuilder(){')
end=text.find('\nwindow.addFeeDepartment=', start)
if start<0 or end<0:
    raise SystemExit('renderFeeBuilder block not found')
new_func=r'''function renderFeeBuilder(){
 const host=$('#feeBuilderHost'),allCols=S.feeColumns||[],cols=allCols.filter(x=>x.active),deps=(S.feeDepartments||[]).filter(x=>x.active);
 const manager=$('#feeColumnManager');
 if(manager&&isAdmin())manager.innerHTML=allCols.map(c=>`<span class="fee-column-chip ${c.active?'':'inactive'}"><b>${esc(c.label)}</b><small>${esc(c.column_key)}${c.formula?' = '+esc(c.formula):''}</small><button type="button" onclick="editFeeColumn('${attr(c.id)}')">Edit</button><button type="button" onclick="toggleFeeColumn('${attr(c.id)}',${!c.active})">${c.active?'Hide':'Show'}</button><button type="button" onclick="deleteFeeColumn('${attr(c.id)}')">×</button></span>`).join('')||'<span class="fee-builder-note">No columns</span>';
 if(!deps.length){host.innerHTML='<p class="empty">No active departments</p>';return}
 if(!deps.some(d=>d.id===S.feeSelectedDepartment))S.feeSelectedDepartment=deps[0].id;
 const selected=deps.find(d=>d.id===S.feeSelectedDepartment)||deps[0];
 host.innerHTML=`<div class="fee-faculty-grid">${deps.map(dep=>{const count=(S.feeRows||[]).filter(x=>x.department_id===dep.id&&x.active).length;return `<button type="button" class="fee-faculty-box ${dep.id===selected.id?'active':''}" onclick="selectFeeDepartment('${attr(dep.id)}')"><b>${esc(dep.name)}</b><small>${count} course${count===1?'':'s'}</small></button>`}).join('')}</div><div id="feeDepartmentDetail"></div>`;
 const rows=(S.feeRows||[]).filter(x=>x.department_id===selected.id&&x.active),detail=$('#feeDepartmentDetail');
 detail.innerHTML=`<section class="fee-department"><div class="fee-department-head"><h3>${esc(selected.name)}</h3>${isAdmin()?`<div class="fee-department-actions"><button class="btn primary" type="button" onclick="openFeeRowEditor('${attr(selected.id)}')">+ Course</button><button class="btn secondary" type="button" onclick="editFeeDepartment('${attr(selected.id)}')">Edit Department</button><button class="btn danger" type="button" onclick="deleteFeeDepartment('${attr(selected.id)}')">Delete</button></div>`:''}</div><div class="fee-data-wrap"><table class="fee-data-table"><thead><tr><th>S.No.</th>${cols.map(c=>`<th title="Key: ${attr(c.column_key)}${c.formula?' | Formula: '+attr(c.formula):''}">${esc(c.label)}</th>`).join('')}${isAdmin()?'<th>Action</th>':''}</tr></thead><tbody>${rows.map((row,i)=>{const data=feeResolvedRow(row,cols);return `<tr><td>${i+1}</td>${cols.map(c=>`<td class="${c.value_type==='currency'?'fee-currency':''}">${feeDisplayValue(c,data[c.column_key])}</td>`).join('')}${isAdmin()?`<td class="fee-row-actions"><button class="btn secondary" type="button" onclick="openFeeRowEditor('${attr(selected.id)}','${attr(row.id)}')">Edit</button><button class="btn danger" type="button" onclick="deleteFeeRow('${attr(row.id)}')">Delete</button></td>`:''}</tr>`}).join('')||`<tr><td colspan="${cols.length+1+(isAdmin()?1:0)}" class="empty">No courses added</td></tr>`}</tbody></table></div></section>`
}
window.selectFeeDepartment=id=>{S.feeSelectedDepartment=id;renderFeeBuilder()};'''
text=text[:start]+new_func+text[end:]
css=r'''

/* Fee faculty 3-column selector */
.fee-faculty-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:16px 0}
.fee-faculty-box{min-height:76px;padding:12px 14px;border:1px solid #c9d9e9;border-radius:10px;background:#f8fbff;color:#214d79;text-align:left;cursor:pointer;display:flex;flex-direction:column;justify-content:center;gap:5px;transition:.15s ease}
.fee-faculty-box b{font-size:13px;line-height:1.35}.fee-faculty-box small{font-size:11px;color:#6b7f95;font-weight:700}
.fee-faculty-box:hover{background:#eef5ff;border-color:#9fb9d5}.fee-faculty-box.active{background:#e1edfb;border-color:#6f91b3;box-shadow:inset 0 0 0 1px #6f91b3}.fee-faculty-box.active b{color:#163f69}
#feeDepartmentDetail .fee-department{margin-top:0}
@media(max-width:980px){.fee-faculty-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:680px){.fee-faculty-grid{grid-template-columns:1fr}.fee-faculty-box{min-height:62px}}
'''
if '/* Fee faculty 3-column selector */' not in text:
    text=text.replace('</style>',css+'\n</style>',1)
p.write_text(text,encoding='utf-8')
