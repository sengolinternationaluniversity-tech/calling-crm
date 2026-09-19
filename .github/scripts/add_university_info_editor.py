from pathlib import Path

p=Path('index.html')
text=p.read_text(encoding='utf-8')

old_markup='''  <section class="card university-detail-panel active" data-university-panel="info">
    <h2>Sengol International University</h2>
    <p class="university-detail-note">Admissions &amp; Outreach CRM</p>
  </section>'''
new_markup='''  <section class="card university-detail-panel active" data-university-panel="info">
    <div class="toolbar"><div><h2>University Info</h2><p class="university-detail-note">University ki saved information yahan table format mein dikhai degi.</p></div><div class="approval-toolbar-actions"><button id="addUniversityInfoColumn" class="btn secondary admin-only" type="button">+ Add Column</button><button id="addUniversityInfoRow" class="btn primary admin-only" type="button">+ Add Row</button><button id="refreshUniversityInfo" class="btn secondary" type="button">Refresh</button></div></div>
    <div id="universityInfoColumnManager" class="approval-column-manager admin-only"></div>
    <div class="table-wrap approval-table-wrap"><table class="approval-table"><thead id="universityInfoHead"><tr><th>S.No.</th><th>Title</th><th>Detail</th></tr></thead><tbody id="universityInfoBody"><tr><td colspan="3" class="empty">Loading university info...</td></tr></tbody></table></div>
  </section>'''
if old_markup not in text:
    raise SystemExit('university info markup target not found')
text=text.replace(old_markup,new_markup,1)

anchor='''$('#addApprovalColumn')?.addEventListener('click',addApprovalColumn);
$('#addApprovalRow')?.addEventListener('click',()=>openApprovalRowEditor());
$('#refreshApprovals')?.addEventListener('click',loadApprovals);
document.querySelector('[data-university-tab="approval"]')?.addEventListener('click',loadApprovals);'''
if anchor not in text:
    raise SystemExit('approval event anchor not found')

block=r'''

/* Editable University Info table (no uploads) */
async function loadUniversityInfo(){
 const body=$('#universityInfoBody'),head=$('#universityInfoHead');if(!body||!head)return;
 body.innerHTML='<tr><td colspan="3" class="empty">Loading university info...</td></tr>';
 const [c,r]=await Promise.all([
  db.from('crm_university_info_columns').select('*').eq('active',true).order('sort_order').order('created_at'),
  db.from('crm_university_info_rows').select('*').eq('active',true).order('sort_order').order('created_at')
 ]);
 const error=c.error||r.error;if(error){body.innerHTML='<tr><td colspan="3" class="empty">University info load nahi hui</td></tr>';toast(error.message);return}
 S.universityInfoColumns=c.data||[];S.universityInfoRows=r.data||[];renderUniversityInfo()
}
function renderUniversityInfo(){
 const head=$('#universityInfoHead'),body=$('#universityInfoBody'),cols=S.universityInfoColumns||[],rows=S.universityInfoRows||[];if(!head||!body)return;
 head.innerHTML=`<tr><th>S.No.</th>${cols.map(c=>`<th>${esc(c.label)}</th>`).join('')}${isAdmin()?'<th>Action</th>':''}</tr>`;
 const manager=$('#universityInfoColumnManager');
 if(manager&&isAdmin())manager.innerHTML=cols.map(c=>`<span class="approval-column-chip"><b>${esc(c.label)}</b><small>${esc(c.column_key)}</small><button type="button" onclick="editUniversityInfoColumn('${attr(c.id)}')">Edit</button><button type="button" onclick="deleteUniversityInfoColumn('${attr(c.id)}')">Delete</button></span>`).join('')||'<span class="fee-builder-note">No columns. + Add Column se naya column bana sakte hain.</span>';
 const span=1+cols.length+(isAdmin()?1:0);
 body.innerHTML=rows.map((row,i)=>`<tr><td>${i+1}</td>${cols.map(c=>`<td>${row.row_data?.[c.column_key]!==undefined&&row.row_data?.[c.column_key]!==''?esc(String(row.row_data[c.column_key])):'—'}</td>`).join('')}${isAdmin()?`<td><div class="approval-upload-actions"><button class="btn primary" type="button" onclick="openUniversityInfoRowEditor('${attr(row.id)}')">Edit</button><button class="btn danger" type="button" onclick="deleteUniversityInfoRow('${attr(row.id)}')">Delete</button></div></td>`:''}</tr>`).join('')||`<tr><td colspan="${span}" class="empty">No university info rows added</td></tr>`
}
window.addUniversityInfoColumn=async()=>{
 if(!isAdmin())return;const label=prompt('Column name');if(!label?.trim())return;
 const suggested=label.toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'').replace(/^[^a-z]+/,'')||'column';
 const key=prompt('Column Key',suggested);if(!key||!/^[a-z][a-z0-9_]*$/.test(key)){toast('Column key lowercase letters/numbers/underscore mein hona chahiye');return}
 const max=Math.max(0,...(S.universityInfoColumns||[]).map(x=>Number(x.sort_order)||0));
 const {error}=await db.from('crm_university_info_columns').insert({column_key:key,label:label.trim(),sort_order:max+10});
 if(error)toast(error.message);else{toast('Column added');loadUniversityInfo()}
};
window.editUniversityInfoColumn=async id=>{
 if(!isAdmin())return;const c=(S.universityInfoColumns||[]).find(x=>x.id===id);if(!c)return;
 const label=prompt('Column name',c.label);if(!label?.trim())return;const order=prompt('Sort order',String(c.sort_order??100));if(order===null)return;
 const {error}=await db.from('crm_university_info_columns').update({label:label.trim(),sort_order:Number(order)||100,updated_at:new Date().toISOString()}).eq('id',id);
 if(error)toast(error.message);else{toast('Column updated');loadUniversityInfo()}
};
window.deleteUniversityInfoColumn=async id=>{
 if(!isAdmin()||!confirm('Ye column delete karein?'))return;
 const {error}=await db.from('crm_university_info_columns').delete().eq('id',id);if(error)toast(error.message);else{toast('Column deleted');loadUniversityInfo()}
};
function ensureUniversityInfoRowModal(){
 let m=$('#universityInfoRowModal');if(m)return m;
 m=document.createElement('div');m.id='universityInfoRowModal';m.className='modal-bg';m.innerHTML='<form id="universityInfoRowForm" class="modal" style="width:min(820px,100%)"><div class="modal-head"><div><h2 id="universityInfoRowTitle">Add University Info Row</h2><p class="staff-form-note">University information fill karein. Is section mein upload/file option nahi hai.</p></div><button type="button" class="close" id="closeUniversityInfoRowModal">×</button></div><input type="hidden" name="row_id"><div id="universityInfoRowFields" class="approval-row-fields"></div><div class="modal-actions"><button type="button" class="btn secondary" id="cancelUniversityInfoRowModal">Cancel</button><button class="btn primary" type="submit">Save Row</button></div></form>';
 document.body.appendChild(m);const close=()=>m.classList.remove('open');$('#closeUniversityInfoRowModal').onclick=close;$('#cancelUniversityInfoRowModal').onclick=close;m.onclick=e=>{if(e.target===m)close()};$('#universityInfoRowForm').onsubmit=saveUniversityInfoRow;return m
}
window.openUniversityInfoRowEditor=(id='')=>{
 if(!isAdmin())return;const m=ensureUniversityInfoRowModal(),f=$('#universityInfoRowForm'),row=(S.universityInfoRows||[]).find(x=>x.id===id),cols=S.universityInfoColumns||[];
 f.elements.row_id.value=id;$('#universityInfoRowTitle').textContent=id?'Edit University Info Row':'Add University Info Row';
 $('#universityInfoRowFields').innerHTML=cols.map(c=>{const value=String(row?.row_data?.[c.column_key]??''),longField=/(detail|description|address|remarks|note|about)/i.test(c.column_key);return `<label class="field ${longField?'full':''}">${esc(c.label)}${longField?`<textarea name="col_${attr(c.column_key)}" style="width:100%;min-height:86px;padding:10px;border:1px solid #cbd9e8;border-radius:8px">${esc(value)}</textarea>`:`<input name="col_${attr(c.column_key)}" value="${attr(value)}">`}</label>`}).join('')||'<p class="empty full">Pehle + Add Column se kam se kam ek column banayein.</p>';
 m.classList.add('open')
};
async function saveUniversityInfoRow(e){
 e.preventDefault();if(!isAdmin())return;const f=e.target,id=f.elements.row_id.value,row=(S.universityInfoRows||[]).find(x=>x.id===id),data={...(row?.row_data||{})},cols=S.universityInfoColumns||[];
 if(!cols.length){toast('Pehle column add karein');return}
 cols.forEach(c=>{const el=f.elements[`col_${c.column_key}`];if(el)data[c.column_key]=el.value.trim()});
 const saveBtn=f.querySelector('button[type="submit"]');saveBtn.disabled=true;saveBtn.textContent='Saving...';
 try{
  let result;if(id)result=await db.from('crm_university_info_rows').update({row_data:data,updated_at:new Date().toISOString()}).eq('id',id);else{const max=Math.max(0,...(S.universityInfoRows||[]).map(x=>Number(x.sort_order)||0));result=await db.from('crm_university_info_rows').insert({row_data:data,sort_order:max+10})}
  if(result.error)throw result.error;$('#universityInfoRowModal').classList.remove('open');toast(id?'University info updated':'University info added');await loadUniversityInfo()
 }catch(err){toast(err.message||'Save failed')}finally{saveBtn.disabled=false;saveBtn.textContent='Save Row'}
}
window.deleteUniversityInfoRow=async id=>{
 if(!isAdmin()||!confirm('University info row delete karein?'))return;
 const {error}=await db.from('crm_university_info_rows').delete().eq('id',id);if(error)toast(error.message);else{toast('University info row deleted');loadUniversityInfo()}
};
$('#addUniversityInfoColumn')?.addEventListener('click',addUniversityInfoColumn);
$('#addUniversityInfoRow')?.addEventListener('click',()=>openUniversityInfoRowEditor());
$('#refreshUniversityInfo')?.addEventListener('click',loadUniversityInfo);
document.querySelector('[data-university-tab="info"]')?.addEventListener('click',loadUniversityInfo);
document.querySelector('[data-page="universitydetail"]')?.addEventListener('click',()=>setTimeout(()=>{if(document.querySelector('[data-university-tab="info"]')?.classList.contains('active'))loadUniversityInfo()},0));
'''

text=text.replace(anchor,anchor+block,1)
p.write_text(text,encoding='utf-8')
print('University Info editor added')
