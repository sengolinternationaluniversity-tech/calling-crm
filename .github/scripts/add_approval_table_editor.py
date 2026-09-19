from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')

old_markup='''  <section class="card university-detail-panel" data-university-panel="approval">\n    <div class="toolbar"><div><h2>Approval</h2><p class="university-detail-note">University approvals aur recognition documents.</p></div><button id="refreshApprovals" class="btn secondary" type="button">Refresh</button></div>\n    <form id="approvalUploadForm" class="approval-upload-form admin-only">\n      <input id="approvalName" type="text" maxlength="160" required placeholder="Name of Approval">\n      <input id="approvalFile" type="file" required accept=".pdf,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg,image/webp">\n      <button class="btn primary" type="submit">Upload Approval</button>\n    </form>\n    <div class="table-wrap approval-table-wrap"><table class="approval-table"><thead><tr><th>S.No.</th><th>Name of Approval</th><th>Upload</th></tr></thead><tbody id="approvalBody"><tr><td colspan="3" class="empty">Loading approvals...</td></tr></tbody></table></div>\n  </section>'''
new_markup='''  <section class="card university-detail-panel" data-university-panel="approval">\n    <div class="toolbar"><div><h2>Approval</h2><p class="university-detail-note">University approvals aur recognition documents.</p></div><div class="approval-toolbar-actions"><button id="addApprovalColumn" class="btn secondary admin-only" type="button">+ Add Column</button><button id="addApprovalRow" class="btn primary admin-only" type="button">+ Add Row</button><button id="refreshApprovals" class="btn secondary" type="button">Refresh</button></div></div>\n    <div id="approvalColumnManager" class="approval-column-manager admin-only"></div>\n    <div class="table-wrap approval-table-wrap"><table class="approval-table"><thead id="approvalHead"><tr><th>S.No.</th><th>Name of Approval</th><th>Upload</th></tr></thead><tbody id="approvalBody"><tr><td colspan="3" class="empty">Loading approvals...</td></tr></tbody></table></div>\n  </section>'''
if old_markup not in text:
    raise SystemExit('approval markup target not found')
text=text.replace(old_markup,new_markup,1)

old_css='''/* University approval uploads */\n.approval-upload-form{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:14px 0 4px;padding:10px;background:#f8fbff;border:1px solid #d6e4f4;border-radius:10px}\n.approval-upload-form input[type="text"]{flex:1 1 340px;min-width:220px;height:38px;padding:7px 10px;border:1px solid #c8d8e9;border-radius:8px;background:#fff;color:#17324d}\n.approval-upload-form input[type="file"]{flex:1 1 280px;min-width:230px;font-size:12px}\n.approval-table-wrap{border:1px solid #c4d3e2;border-radius:10px;overflow:auto}\n.approval-table{width:100%;border-collapse:collapse;table-layout:fixed;white-space:normal}\n.approval-table th,.approval-table td{border-right:1px solid #c4d3e2;border-bottom:1px solid #b9cbe0;padding:10px;vertical-align:middle}\n.approval-table th{background:#f5f9ff;color:#2457a6}\n.approval-table th:nth-child(1),.approval-table td:nth-child(1){width:80px;text-align:center}\n.approval-table th:nth-child(2),.approval-table td:nth-child(2){width:auto}\n.approval-table th:nth-child(3),.approval-table td:nth-child(3){width:330px}\n.approval-table th:last-child,.approval-table td:last-child{border-right:0}\n.approval-upload-actions{display:flex;gap:6px;align-items:center;flex-wrap:wrap}\n.approval-upload-actions .btn{padding:6px 9px;font-size:12px;text-decoration:none}\n@media(max-width:680px){.approval-upload-form{align-items:stretch}.approval-upload-form>*{width:100%!important}.approval-table{min-width:680px}}'''
new_css='''/* University approval table editor */\n.approval-toolbar-actions{display:flex;gap:7px;align-items:center;flex-wrap:wrap}\n.approval-column-manager{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0 4px;padding:10px;background:#f8fbff;border:1px solid #d6e4f4;border-radius:10px}\n.approval-column-chip{display:inline-flex;align-items:center;gap:6px;border:1px solid #d5e2ef;background:#fff;border-radius:8px;padding:6px 8px;font-size:12px;color:#31516d}\n.approval-column-chip b{color:#173f6c}.approval-column-chip small{color:#6b7f95}\n.approval-column-chip button{border:0;background:#edf4ff;color:#2457a6;border-radius:6px;padding:4px 7px;cursor:pointer}\n.approval-table-wrap{border:1px solid #c4d3e2;border-radius:10px;overflow:auto}\n.approval-table{width:100%;border-collapse:collapse;white-space:normal;min-width:760px}\n.approval-table th,.approval-table td{border-right:1px solid #c4d3e2;border-bottom:1px solid #b9cbe0;padding:10px;vertical-align:middle}\n.approval-table th{background:#f5f9ff;color:#2457a6;white-space:nowrap}\n.approval-table th:first-child,.approval-table td:first-child{width:72px;text-align:center}\n.approval-table th:last-child,.approval-table td:last-child{min-width:260px;border-right:0}\n.approval-upload-actions{display:flex;gap:6px;align-items:center;flex-wrap:wrap}\n.approval-upload-actions .btn{padding:6px 9px;font-size:12px;text-decoration:none}\n.approval-row-fields{display:grid;grid-template-columns:1fr 1fr;gap:11px}.approval-row-fields .full{grid-column:1/-1}\n.approval-row-fields .field{margin:0}.approval-row-fields input{width:100%}\n@media(max-width:680px){.approval-toolbar-actions{width:100%}.approval-toolbar-actions .btn{flex:1 1 auto}.approval-row-fields{grid-template-columns:1fr}.approval-row-fields .full{grid-column:auto}.approval-table{min-width:760px}}'''
if old_css not in text:
    raise SystemExit('approval css target not found')
text=text.replace(old_css,new_css,1)

start_anchor="const exportFeePdfBtn=$('#exportFeePdf');if(exportFeePdfBtn)exportFeePdfBtn.onclick=window.exportFeePdf;"
start_search=text.find(start_anchor)
start=text.find('/* University approval uploads */',start_search)
end=text.find('\n\nwindow.addFeeDepartment=',start)
if start<0 or end<0:
    raise SystemExit('approval js block not found')

new_js=r'''/* University approval table editor */
function approvalSafeName(name){return String(name||'file').toLowerCase().replace(/[^a-z0-9._-]+/g,'-').replace(/^-+|-+$/g,'').slice(-120)||'file'}
async function uploadApprovalFile(file){
 const path=`${new Date().getFullYear()}/${crypto.randomUUID()}-${approvalSafeName(file.name)}`;
 const {error}=await db.storage.from('university-approvals').upload(path,file,{cacheControl:'3600',upsert:false,contentType:file.type||undefined});
 if(error)throw error;return path
}
async function loadApprovals(){
 const body=$('#approvalBody'),head=$('#approvalHead');if(!body||!head)return;
 body.innerHTML='<tr><td colspan="3" class="empty">Loading approvals...</td></tr>';
 const [r,c]=await Promise.all([
  db.from('crm_university_approvals').select('*').eq('active',true).order('sort_order').order('created_at'),
  db.from('crm_university_approval_columns').select('*').eq('active',true).order('sort_order').order('created_at')
 ]);
 const error=r.error||c.error;if(error){body.innerHTML='<tr><td colspan="3" class="empty">Approvals load nahi hue</td></tr>';toast(error.message);return}
 S.approvals=r.data||[];S.approvalColumns=c.data||[];
 const signedPairs=await Promise.all(S.approvals.map(async x=>{
  if(!x.file_path)return[x.id,null];
  const {data:s,error:e}=await db.storage.from('university-approvals').createSignedUrl(x.file_path,3600);
  return[x.id,e?null:s?.signedUrl||null]
 }));
 S.approvalSigned=Object.fromEntries(signedPairs);
 renderApprovals()
}
function renderApprovals(){
 const head=$('#approvalHead'),body=$('#approvalBody'),cols=S.approvalColumns||[],rows=S.approvals||[];
 if(!head||!body)return;
 head.innerHTML=`<tr><th>S.No.</th><th>Name of Approval</th>${cols.map(c=>`<th>${esc(c.label)}</th>`).join('')}<th>Upload</th></tr>`;
 const manager=$('#approvalColumnManager');
 if(manager&&isAdmin())manager.innerHTML=cols.map(c=>`<span class="approval-column-chip"><b>${esc(c.label)}</b><small>${esc(c.column_key)}</small><button type="button" onclick="editApprovalColumn('${attr(c.id)}')">Edit</button><button type="button" onclick="deleteApprovalColumn('${attr(c.id)}')">Delete</button></span>`).join('')||'<span class="fee-builder-note">No custom columns. + Add Column se naya column bana sakte hain.</span>';
 const span=3+cols.length;
 if(!rows.length){body.innerHTML=`<tr><td colspan="${span}" class="empty">No approval rows added</td></tr>`;return}
 body.innerHTML=rows.map((x,i)=>`<tr><td>${i+1}</td><td><b>${esc(x.approval_name||'—')}</b></td>${cols.map(c=>`<td>${x.row_data?.[c.column_key]!==undefined&&x.row_data?.[c.column_key]!==''?esc(String(x.row_data[c.column_key])):'—'}</td>`).join('')}<td><div class="approval-upload-actions">${S.approvalSigned?.[x.id]?`<a class="btn secondary" href="${attr(S.approvalSigned[x.id])}" target="_blank" rel="noopener">View / Download</a>`:'<span class="fee-builder-note">No file</span>'}${isAdmin()?`<button class="btn secondary" type="button" onclick="replaceApprovalFile('${attr(x.id)}')">${x.file_path?'Replace':'Upload'}</button><button class="btn primary" type="button" onclick="openApprovalRowEditor('${attr(x.id)}')">Edit</button><button class="btn danger" type="button" onclick="deleteApproval('${attr(x.id)}')">Delete</button>`:''}</div>${x.file_name?`<div class="fee-builder-note">${esc(x.file_name)}</div>`:''}</td></tr>`).join('')
}
window.addApprovalColumn=async()=>{
 if(!isAdmin())return;const label=prompt('Column name');if(!label?.trim())return;
 const suggested=label.toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'').replace(/^[^a-z]+/,'')||'column';
 const key=prompt('Column Key',suggested);if(!key||!/^[a-z][a-z0-9_]*$/.test(key)){toast('Column key lowercase letters/numbers/underscore mein hona chahiye');return}
 const max=Math.max(0,...(S.approvalColumns||[]).map(x=>Number(x.sort_order)||0));
 const {error}=await db.from('crm_university_approval_columns').insert({column_key:key,label:label.trim(),sort_order:max+10});
 if(error)toast(error.message);else{toast('Column added');loadApprovals()}
};
window.editApprovalColumn=async id=>{
 if(!isAdmin())return;const c=(S.approvalColumns||[]).find(x=>x.id===id);if(!c)return;
 const label=prompt('Column name',c.label);if(!label?.trim())return;const order=prompt('Sort order',String(c.sort_order??100));if(order===null)return;
 const {error}=await db.from('crm_university_approval_columns').update({label:label.trim(),sort_order:Number(order)||100,updated_at:new Date().toISOString()}).eq('id',id);
 if(error)toast(error.message);else{toast('Column updated');loadApprovals()}
};
window.deleteApprovalColumn=async id=>{
 if(!isAdmin()||!confirm('Ye column delete karein? Existing row data JSON mein reh sakta hai, table se column hat jayega.'))return;
 const {error}=await db.from('crm_university_approval_columns').delete().eq('id',id);if(error)toast(error.message);else{toast('Column deleted');loadApprovals()}
};
function ensureApprovalRowModal(){
 let m=$('#approvalRowModal');if(m)return m;
 m=document.createElement('div');m.id='approvalRowModal';m.className='modal-bg';m.innerHTML='<form id="approvalRowForm" class="modal" style="width:min(820px,100%)"><div class="modal-head"><div><h2 id="approvalRowTitle">Add Approval Row</h2><p class="staff-form-note">Approval details fill karein. File optional hai; baad mein bhi upload/replace kar sakte hain.</p></div><button type="button" class="close" id="closeApprovalRowModal">×</button></div><input type="hidden" name="row_id"><div id="approvalRowFields" class="approval-row-fields"></div><div class="modal-actions"><button type="button" class="btn secondary" id="cancelApprovalRowModal">Cancel</button><button class="btn primary" type="submit">Save Row</button></div></form>';
 document.body.appendChild(m);const close=()=>m.classList.remove('open');$('#closeApprovalRowModal').onclick=close;$('#cancelApprovalRowModal').onclick=close;m.onclick=e=>{if(e.target===m)close()};$('#approvalRowForm').onsubmit=saveApprovalRow;return m
}
window.openApprovalRowEditor=(id='')=>{
 if(!isAdmin())return;const m=ensureApprovalRowModal(),f=$('#approvalRowForm'),row=(S.approvals||[]).find(x=>x.id===id),cols=S.approvalColumns||[];
 f.elements.row_id.value=id;$('#approvalRowTitle').textContent=id?'Edit Approval Row':'Add Approval Row';
 $('#approvalRowFields').innerHTML=`<label class="field full">Name of Approval<input name="approval_name" maxlength="160" required value="${attr(row?.approval_name||'')}"></label>${cols.map(c=>`<label class="field">${esc(c.label)}<input name="col_${attr(c.column_key)}" value="${attr(String(row?.row_data?.[c.column_key]??''))}"></label>`).join('')}<label class="field full">Upload File (optional)<input name="approval_file" type="file" accept=".pdf,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg,image/webp">${row?.file_name?`<small>Current: ${esc(row.file_name)}</small>`:''}</label>`;
 m.classList.add('open')
};
async function saveApprovalRow(e){
 e.preventDefault();if(!isAdmin())return;const f=e.target,id=f.elements.row_id.value,row=(S.approvals||[]).find(x=>x.id===id),name=f.elements.approval_name.value.trim();if(!name)return;
 const data={...(row?.row_data||{})};(S.approvalColumns||[]).forEach(c=>{const el=f.elements[`col_${c.column_key}`];if(el)data[c.column_key]=el.value.trim()});
 const file=f.elements.approval_file.files?.[0];let path='',payload={approval_name:name,row_data:data,updated_at:new Date().toISOString()};
 const saveBtn=f.querySelector('button[type="submit"]');saveBtn.disabled=true;saveBtn.textContent='Saving...';
 try{
  if(file){path=await uploadApprovalFile(file);payload={...payload,file_path:path,file_name:file.name,file_type:file.type||null}}
  let result;if(id)result=await db.from('crm_university_approvals').update(payload).eq('id',id);else{const max=Math.max(0,...(S.approvals||[]).map(x=>Number(x.sort_order)||0));result=await db.from('crm_university_approvals').insert({...payload,sort_order:max+10})}
  if(result.error)throw result.error;
  if(id&&file&&row?.file_path)await db.storage.from('university-approvals').remove([row.file_path]);
  $('#approvalRowModal').classList.remove('open');toast(id?'Approval row updated':'Approval row added');await loadApprovals()
 }catch(err){if(path)await db.storage.from('university-approvals').remove([path]);toast(err.message||'Save failed')}
 finally{saveBtn.disabled=false;saveBtn.textContent='Save Row'}
}
window.replaceApprovalFile=async id=>{
 if(!isAdmin())return;const row=(S.approvals||[]).find(x=>x.id===id);if(!row)return;
 const input=document.createElement('input');input.type='file';input.accept='.pdf,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg,image/webp';
 input.onchange=async()=>{const file=input.files?.[0];if(!file)return;let path='';try{path=await uploadApprovalFile(file);const {error}=await db.from('crm_university_approvals').update({file_path:path,file_name:file.name,file_type:file.type||null,updated_at:new Date().toISOString()}).eq('id',id);if(error)throw error;if(row.file_path)await db.storage.from('university-approvals').remove([row.file_path]);toast(row.file_path?'Approval file replaced':'Approval file uploaded');await loadApprovals()}catch(err){if(path)await db.storage.from('university-approvals').remove([path]);toast(err.message||'Upload failed')}};input.click()
};
window.deleteApproval=async id=>{
 if(!isAdmin()||!confirm('Approval row delete karein?'))return;const row=(S.approvals||[]).find(x=>x.id===id);if(!row)return;
 const {error}=await db.from('crm_university_approvals').delete().eq('id',id);if(error){toast(error.message);return}if(row.file_path)await db.storage.from('university-approvals').remove([row.file_path]);toast('Approval row deleted');loadApprovals()
};
$('#addApprovalColumn')?.addEventListener('click',addApprovalColumn);
$('#addApprovalRow')?.addEventListener('click',()=>openApprovalRowEditor());
$('#refreshApprovals')?.addEventListener('click',loadApprovals);
document.querySelector('[data-university-tab="approval"]')?.addEventListener('click',loadApprovals);'''

text=text[:start]+new_js+text[end:]
p.write_text(text,encoding='utf-8')
