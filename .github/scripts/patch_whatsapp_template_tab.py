from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'data-university-tab="messages"' in s:
    raise SystemExit('WhatsApp template tab already exists')

css = r'''

/* University WhatsApp message templates */
.message-template-help{margin:10px 0 2px;padding:10px 12px;background:#f7faff;border:1px solid #d8e5f2;border-radius:9px;color:#5f7890;font-size:12px;line-height:1.5}
.message-template-list{display:grid;gap:11px;margin-top:14px}
.message-template-card{border:1px solid #d6e3f0;border-radius:11px;background:#fff;overflow:hidden}
.message-template-card-head{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;background:#edf5ff;border-bottom:1px solid #d7e3f2}
.message-template-card-head h3{margin:0;color:#173f6c;font-size:14px}
.message-template-actions{display:flex;gap:6px;flex-wrap:wrap}
.message-template-actions .btn{padding:6px 9px;font-size:11px}
.message-template-message{margin:0;padding:13px 14px;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.55 Arial,sans-serif;color:#17324d;background:#fff}
.message-template-fields{display:grid;gap:10px}.message-template-fields .field{margin:0}.message-template-fields textarea{width:100%;min-height:260px;padding:11px;border:1px solid #cbd9e8;border-radius:9px;resize:vertical;color:#17324d;background:#fff}
@media(max-width:680px){.message-template-card-head{align-items:flex-start;flex-direction:column}.message-template-actions{width:100%}.message-template-actions .btn{flex:1 1 auto}}
'''
style_anchor = '</style>\n</head>'
if style_anchor not in s:
    raise SystemExit('style anchor not found')
s = s.replace(style_anchor, css + '\n</style>\n</head>', 1)

tab_anchor = '    <button type="button" class="university-detail-tab active" data-university-tab="info">University Info</button>'
if tab_anchor not in s:
    raise SystemExit('university info tab anchor not found')
s = s.replace(
    tab_anchor,
    tab_anchor + '\n    <button type="button" class="university-detail-tab admin-only" data-university-tab="messages">WhatsApp Template</button>',
    1,
)

panel_anchor = '  </section>\n</section>\n\n<section id="settingsPage"'
if panel_anchor not in s:
    raise SystemExit('university page closing anchor not found')
panel = r'''  </section>
  <section class="card university-detail-panel admin-only" data-university-panel="messages">
    <div class="toolbar"><div><h2>WhatsApp Templates</h2><p class="university-detail-note">Call ke baad bhejne wale reusable WhatsApp messages yahan Admin manage kar sakta hai.</p></div><div class="approval-toolbar-actions"><button id="addMessageTemplate" class="btn primary" type="button">+ Add Template</button><button id="refreshMessageTemplates" class="btn secondary" type="button">Refresh</button></div></div>
    <div class="message-template-help"><b>Available placeholders:</b> {{contact_name}}, {{institute_name}}, {{staff_name}}, {{staff_mobile}}. In placeholders ko baad mein Calling screen se actual details se replace kiya ja sakta hai.</div>
    <div id="messageTemplateList" class="message-template-list"><p class="empty">Templates loading...</p></div>
  </section>
</section>

<section id="settingsPage"'''
s = s.replace(panel_anchor, panel, 1)

js_anchor = 'window.addFeeDepartment=async()=>{'
if js_anchor not in s:
    raise SystemExit('JS anchor not found')
js = r'''
/* Admin WhatsApp message templates */
async function loadMessageTemplates(){
 if(!isAdmin())return;const box=$('#messageTemplateList');if(!box)return;box.innerHTML='<p class="empty">Templates loading...</p>';
 const {data,error}=await db.from('crm_university_message_templates').select('*').eq('active',true).order('sort_order').order('created_at');
 if(error){box.innerHTML='<p class="empty">Templates load nahi hue</p>';toast(error.message);return}S.messageTemplates=data||[];renderMessageTemplates()
}
function renderMessageTemplates(){
 const box=$('#messageTemplateList');if(!box||!isAdmin())return;const rows=S.messageTemplates||[];
 box.innerHTML=rows.map((x,i)=>`<article class="message-template-card"><div class="message-template-card-head"><h3>${i+1}. ${esc(x.name)}</h3><div class="message-template-actions"><button class="btn secondary" type="button" onclick="copyMessageTemplate('${attr(x.id)}')">Copy</button><button class="btn primary" type="button" onclick="openMessageTemplateEditor('${attr(x.id)}')">Edit</button><button class="btn danger" type="button" onclick="deleteMessageTemplate('${attr(x.id)}')">Delete</button></div></div><pre class="message-template-message">${esc(x.message||'')}</pre></article>`).join('')||'<p class="empty">No WhatsApp templates added</p>'
}
window.copyMessageTemplate=async id=>{
 const row=(S.messageTemplates||[]).find(x=>x.id===id);if(!row)return;
 try{await navigator.clipboard.writeText(row.message||'');toast('Template copied')}catch{const t=document.createElement('textarea');t.value=row.message||'';document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();toast('Template copied')}
};
function ensureMessageTemplateModal(){
 let m=$('#messageTemplateModal');if(m)return m;
 m=document.createElement('div');m.id='messageTemplateModal';m.className='modal-bg';m.innerHTML='<form id="messageTemplateForm" class="modal" style="width:min(850px,100%)"><div class="modal-head"><div><h2 id="messageTemplateTitle">Add WhatsApp Template</h2><p class="staff-form-note">Call ke baad bhejne ke liye message save karein.</p></div><button type="button" class="close" id="closeMessageTemplateModal">×</button></div><input type="hidden" name="template_id"><div class="message-template-fields"><label class="field">Template Name<input name="name" maxlength="120" required placeholder="e.g. After Call Follow-up"></label><label class="field">Message<textarea name="message" required placeholder="WhatsApp message likhein..."></textarea></label><label class="field">Sort Order<input name="sort_order" type="number" value="100"></label></div><div class="message-template-help"><b>Placeholders:</b> {{contact_name}}, {{institute_name}}, {{staff_name}}, {{staff_mobile}}</div><div class="modal-actions"><button type="button" class="btn secondary" id="cancelMessageTemplateModal">Cancel</button><button class="btn primary" type="submit">Save Template</button></div></form>';
 document.body.appendChild(m);const close=()=>m.classList.remove('open');$('#closeMessageTemplateModal').onclick=close;$('#cancelMessageTemplateModal').onclick=close;m.onclick=e=>{if(e.target===m)close()};$('#messageTemplateForm').onsubmit=saveMessageTemplate;return m
}
window.openMessageTemplateEditor=(id='')=>{
 if(!isAdmin())return;const m=ensureMessageTemplateModal(),f=$('#messageTemplateForm'),row=(S.messageTemplates||[]).find(x=>x.id===id);
 f.reset();f.elements.template_id.value=id;f.elements.name.value=row?.name||'';f.elements.message.value=row?.message||'';f.elements.sort_order.value=String(row?.sort_order??100);$('#messageTemplateTitle').textContent=id?'Edit WhatsApp Template':'Add WhatsApp Template';m.classList.add('open');setTimeout(()=>f.elements.name.focus(),0)
};
async function saveMessageTemplate(e){
 e.preventDefault();if(!isAdmin())return;const f=e.target,id=f.elements.template_id.value,payload={name:f.elements.name.value.trim(),message:f.elements.message.value.trim(),sort_order:Number(f.elements.sort_order.value)||100,updated_at:new Date().toISOString()};if(!payload.name||!payload.message)return;
 const btn=f.querySelector('button[type="submit"]');btn.disabled=true;btn.textContent='Saving...';try{const result=id?await db.from('crm_university_message_templates').update(payload).eq('id',id):await db.from('crm_university_message_templates').insert(payload);if(result.error)throw result.error;$('#messageTemplateModal').classList.remove('open');toast(id?'Template updated':'Template added');await loadMessageTemplates()}catch(err){toast(err.message||'Template save nahi hua')}finally{btn.disabled=false;btn.textContent='Save Template'}
}
window.deleteMessageTemplate=async id=>{
 if(!isAdmin()||!confirm('Ye WhatsApp template delete karein?'))return;const {error}=await db.from('crm_university_message_templates').delete().eq('id',id);if(error)toast(error.message);else{toast('Template deleted');loadMessageTemplates()}
};
$('#addMessageTemplate')?.addEventListener('click',()=>openMessageTemplateEditor());
$('#refreshMessageTemplates')?.addEventListener('click',loadMessageTemplates);
document.querySelector('[data-university-tab="messages"]')?.addEventListener('click',loadMessageTemplates);

'''
s = s.replace(js_anchor, js + js_anchor, 1)

p.write_text(s, encoding='utf-8')
print('Patched index.html with admin WhatsApp template tab')
