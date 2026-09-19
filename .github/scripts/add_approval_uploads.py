from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
old='''  <section class="card university-detail-panel" data-university-panel="approval">\n    <h2>Approval</h2>\n    <p class="university-detail-note">University approvals aur recognition details yahan show hongi. Verified approval data add hone ke baad isi section mein rakha jayega.</p>\n  </section>'''
new='''  <section class="card university-detail-panel" data-university-panel="approval">\n    <div class="toolbar"><div><h2>Approval</h2><p class="university-detail-note">University approvals aur recognition documents.</p></div><button id="refreshApprovals" class="btn secondary" type="button">Refresh</button></div>\n    <form id="approvalUploadForm" class="approval-upload-form admin-only">\n      <input id="approvalName" type="text" maxlength="160" required placeholder="Name of Approval">\n      <input id="approvalFile" type="file" required accept=".pdf,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg,image/webp">\n      <button class="btn primary" type="submit">Upload Approval</button>\n    </form>\n    <div class="table-wrap approval-table-wrap"><table class="approval-table"><thead><tr><th>S.No.</th><th>Name of Approval</th><th>Upload</th></tr></thead><tbody id="approvalBody"><tr><td colspan="3" class="empty">Loading approvals...</td></tr></tbody></table></div>\n  </section>'''
if old not in text: raise SystemExit('approval markup not found')
text=text.replace(old,new,1)

css=r'''

/* University approval uploads */
.approval-upload-form{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:14px 0 4px;padding:10px;background:#f8fbff;border:1px solid #d6e4f4;border-radius:10px}
.approval-upload-form input[type="text"]{flex:1 1 340px;min-width:220px;height:38px;padding:7px 10px;border:1px solid #c8d8e9;border-radius:8px;background:#fff;color:#17324d}
.approval-upload-form input[type="file"]{flex:1 1 280px;min-width:230px;font-size:12px}
.approval-table-wrap{border:1px solid #c4d3e2;border-radius:10px;overflow:auto}
.approval-table{width:100%;border-collapse:collapse;table-layout:fixed;white-space:normal}
.approval-table th,.approval-table td{border-right:1px solid #c4d3e2;border-bottom:1px solid #b9cbe0;padding:10px;vertical-align:middle}
.approval-table th{background:#f5f9ff;color:#2457a6}
.approval-table th:nth-child(1),.approval-table td:nth-child(1){width:80px;text-align:center}
.approval-table th:nth-child(2),.approval-table td:nth-child(2){width:auto}
.approval-table th:nth-child(3),.approval-table td:nth-child(3){width:330px}
.approval-table th:last-child,.approval-table td:last-child{border-right:0}
.approval-upload-actions{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.approval-upload-actions .btn{padding:6px 9px;font-size:12px;text-decoration:none}
@media(max-width:680px){.approval-upload-form{align-items:stretch}.approval-upload-form>*{width:100%!important}.approval-table{min-width:680px}}
'''
if '/* University approval uploads */' not in text:
    text=text.replace('</style>',css+'\n</style>',1)

anchor="const exportFeePdfBtn=$('#exportFeePdf');if(exportFeePdfBtn)exportFeePdfBtn.onclick=window.exportFeePdf;"
if anchor not in text: raise SystemExit('js anchor not found')
js=r'''

/* University approval uploads */
async function loadApprovals(){
 const body=$('#approvalBody');if(!body)return;
 body.innerHTML='<tr><td colspan="3" class="empty">Loading approvals...</td></tr>';
 const {data,error}=await db.from('crm_university_approvals').select('*').eq('active',true).order('sort_order').order('created_at');
 if(error){body.innerHTML='<tr><td colspan="3" class="empty">Approvals load nahi hue</td></tr>';toast(error.message);return}
 S.approvals=data||[];
 if(!S.approvals.length){body.innerHTML='<tr><td colspan="3" class="empty">No approvals uploaded</td></tr>';return}
 const signed=await Promise.all(S.approvals.map(async x=>{
  if(!x.file_path)return null;
  const {data:s,error:e}=await db.storage.from('university-approvals').createSignedUrl(x.file_path,3600);
  return e?null:s?.signedUrl||null
 }));
 body.innerHTML=S.approvals.map((x,i)=>`<tr><td>${i+1}</td><td><b>${esc(x.approval_name)}</b>${x.file_name?`<div class="fee-builder-note">${esc(x.file_name)}</div>`:''}</td><td><div class="approval-upload-actions">${signed[i]?`<a class="btn secondary" href="${attr(signed[i])}" target="_blank" rel="noopener">View / Download</a>`:'<span class="fee-builder-note">No file</span>'}${isAdmin()?`<button class="btn primary" type="button" onclick="replaceApprovalFile('${attr(x.id)}')">Replace</button><button class="btn danger" type="button" onclick="deleteApproval('${attr(x.id)}')">Delete</button>`:''}</div></td></tr>`).join('')
}
function approvalSafeName(name){return String(name||'file').toLowerCase().replace(/[^a-z0-9._-]+/g,'-').replace(/^-+|-+$/g,'').slice(-120)||'file'}
async function uploadApprovalFile(file){
 const path=`${new Date().getFullYear()}/${crypto.randomUUID()}-${approvalSafeName(file.name)}`;
 const {error}=await db.storage.from('university-approvals').upload(path,file,{cacheControl:'3600',upsert:false,contentType:file.type||undefined});
 if(error)throw error;return path
}
const approvalForm=$('#approvalUploadForm');if(approvalForm)approvalForm.onsubmit=async e=>{
 e.preventDefault();if(!isAdmin())return;
 const name=$('#approvalName').value.trim(),file=$('#approvalFile').files?.[0];if(!name||!file)return;
 const btn=approvalForm.querySelector('button[type="submit"]');btn.disabled=true;btn.textContent='Uploading...';
 let path='';
 try{
  path=await uploadApprovalFile(file);
  const max=Math.max(0,...(S.approvals||[]).map(x=>Number(x.sort_order)||0));
  const {error}=await db.from('crm_university_approvals').insert({approval_name:name,file_path:path,file_name:file.name,file_type:file.type||null,sort_order:max+10});
  if(error)throw error;
  approvalForm.reset();toast('Approval uploaded');await loadApprovals()
 }catch(err){if(path)await db.storage.from('university-approvals').remove([path]);toast(err.message||'Upload failed')}
 finally{btn.disabled=false;btn.textContent='Upload Approval'}
};
window.replaceApprovalFile=async id=>{
 if(!isAdmin())return;const row=(S.approvals||[]).find(x=>x.id===id);if(!row)return;
 const input=document.createElement('input');input.type='file';input.accept='.pdf,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg,image/webp';
 input.onchange=async()=>{const file=input.files?.[0];if(!file)return;let path='';try{path=await uploadApprovalFile(file);const {error}=await db.from('crm_university_approvals').update({file_path:path,file_name:file.name,file_type:file.type||null,updated_at:new Date().toISOString()}).eq('id',id);if(error)throw error;if(row.file_path)await db.storage.from('university-approvals').remove([row.file_path]);toast('Approval file replaced');await loadApprovals()}catch(err){if(path)await db.storage.from('university-approvals').remove([path]);toast(err.message||'Replace failed')}};input.click()
};
window.deleteApproval=async id=>{
 if(!isAdmin()||!confirm('Approval delete karein?'))return;const row=(S.approvals||[]).find(x=>x.id===id);if(!row)return;
 const {error}=await db.from('crm_university_approvals').delete().eq('id',id);if(error){toast(error.message);return}if(row.file_path)await db.storage.from('university-approvals').remove([row.file_path]);toast('Approval deleted');loadApprovals()
};
$('#refreshApprovals')?.addEventListener('click',loadApprovals);
document.querySelector('[data-university-tab="approval"]')?.addEventListener('click',loadApprovals);
'''
text=text.replace(anchor,anchor+js,1)
p.write_text(text,encoding='utf-8')
