from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'function openSendToCenter' in s:
    raise SystemExit('Send to Center flow already exists')

css = r'''

/* Send template + fee PDF to center */
.send-center-modal{width:min(1080px,100%)}
.send-center-grid{display:grid;grid-template-columns:minmax(300px,.85fr) minmax(360px,1.15fr);gap:18px;margin-top:14px}
.send-center-fields{display:grid;gap:10px}.send-center-fields .field{margin:0}.send-center-fields select,.send-center-fields input,.send-center-fields textarea{width:100%;padding:10px 11px;border:1px solid #cbd9e8;border-radius:8px;background:#fff;color:#17324d}.send-center-fields textarea{min-height:230px;resize:vertical;line-height:1.5}
.send-center-preview{border:1px solid #d5e2ef;border-radius:10px;background:#f8fbff;padding:13px;min-width:0}.send-center-preview h3{margin:0 0 4px;color:#173f6c;font-size:15px}.send-center-preview-note{margin:0 0 10px;color:#6b7f95;font-size:11px}.send-center-fee-table{width:100%;border-collapse:collapse;background:#fff;white-space:normal}.send-center-fee-table td{border:1px solid #d5e2ef;padding:8px 9px;font-size:12px;vertical-align:top}.send-center-fee-table td:first-child{width:38%;font-weight:800;color:#2457a6;background:#f5f9ff}.send-center-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;justify-content:flex-end}.send-center-actions .btn{min-height:38px}.send-center-help{margin-top:9px;padding:9px 11px;border:1px solid #d9e5f2;background:#f7faff;border-radius:8px;color:#60778f;font-size:11px;line-height:1.45}
@media(max-width:820px){.send-center-grid{grid-template-columns:1fr}.send-center-fields textarea{min-height:180px}.send-center-actions{justify-content:stretch}.send-center-actions .btn{flex:1 1 100%}}
'''
style_anchor = '</style>\n</head>'
if style_anchor not in s:
    raise SystemExit('style anchor not found')
s = s.replace(style_anchor, css + '\n</style>\n</head>', 1)

xlsx_anchor = '<script src="https://unpkg.com/xlsx@0.18.5/dist/xlsx.full.min.js"></script>'
if xlsx_anchor not in s:
    raise SystemExit('xlsx script anchor not found')
s = s.replace(xlsx_anchor, xlsx_anchor + '\n<script src="https://unpkg.com/jspdf@2.5.2/dist/jspdf.umd.min.js"></script>', 1)

old_placeholders = '{{contact_name}}, {{institute_name}}, {{staff_name}}, {{staff_mobile}}'
new_placeholders = '{{contact_name}}, {{institute_name}}, {{staff_name}}, {{staff_mobile}}, {{faculty}}, {{course_name}}, {{specialization}}, {{total_fee}}'
s = s.replace(old_placeholders, new_placeholders)

call_pattern = re.compile(r'function callQuickActions\(x\)\{.*?\}(?=function whatsappNumberBoxes)', re.S)
new_call = r'''function callQuickActions(x){const callNo=phones(x.mobile_no)[0]||'',waNums=phones(x.whatsapp_no);return `${callNo?`<a class="btn primary" href="tel:${attr(callNo)}">☎ Call</a>`:''}${waNums.map((num,i)=>`<a class="btn green" target="_blank" rel="noopener" href="https://wa.me/${num.replace(/^0/,'91')}" title="WhatsApp ${esc(num)}">WhatsApp${waNums.length>1?` ${i+1}`:''} · ${esc(num)}</a>`).join('')}<button class="btn secondary" type="button" onclick="openSendToCenter()">📄 Send to Center</button>`}'''
s, n = call_pattern.subn(new_call, s, count=1)
if n != 1:
    raise SystemExit(f'callQuickActions replacement count={n}')

js_anchor = "$('#recordForm').onsubmit=async e=>{"
if js_anchor not in s:
    raise SystemExit('record form JS anchor not found')

js = r'''

/* Calling: send saved template + selected fee structure */
function sendCenterWaNumber(value){let d=String(value||'').replace(/\D/g,'');if(d.length===10)d='91'+d;else if(d.length===11&&d.startsWith('0'))d='91'+d.slice(1);return d}
function sendCenterSelectedRow(){const id=$('#sendCenterCourse')?.value;return (S.sendFeeRows||[]).find(x=>String(x.id)===String(id))||null}
function sendCenterSelectedDepartment(){const id=$('#sendCenterDepartment')?.value;return (S.sendFeeDepartments||[]).find(x=>String(x.id)===String(id))||null}
function sendCenterPlainValue(col,val){if(val===null||val===undefined||val==='')return '—';if(col.value_type==='currency')return 'Rs. '+feeNumber(val).toLocaleString('en-IN',{maximumFractionDigits:2});if(col.value_type==='number')return feeNumber(val).toLocaleString('en-IN',{maximumFractionDigits:2});return String(val)}
function sendCenterCourseLabel(row){const d=row?.row_data||{},course=d.course_name||d.program||d.course||'Course',spec=d.specialization||'';return spec?`${course} — ${spec}`:course}
function sendCenterTemplateText(){
 const template=(S.sendTemplates||[]).find(x=>String(x.id)===String($('#sendCenterTemplate')?.value))||S.sendTemplates?.[0],inst=S.sendCenterInstitute||{},dep=sendCenterSelectedDepartment(),row=sendCenterSelectedRow(),allCols=S.sendFeeColumns||[],resolved=row?feeResolvedRow(row,allCols):{},staffMobile=String($('#sendCenterStaffMobile')?.value||'').trim(),course=resolved.course_name||resolved.program||resolved.course||row?.row_data?.course_name||'',spec=resolved.specialization||row?.row_data?.specialization||'';
 const map={contact_name:inst.owner_name||inst.institute_name||'Sir/Madam',institute_name:inst.institute_name||'',staff_name:S.profile?.full_name||S.profile?.username||'Sengol International University',staff_mobile:staffMobile,faculty:dep?.name||'',course_name:course,specialization:spec,total_fee:resolved.total!==undefined&&resolved.total!==''?'Rs. '+feeNumber(resolved.total).toLocaleString('en-IN',{maximumFractionDigits:2}):''};
 let text=String(template?.message||'Namaste {{contact_name}} Ji,\n\nSengol International University ka fee structure aapke saath share kar raha/rahi hoon.\n\nRegards,\n{{staff_name}}');
 Object.entries(map).forEach(([k,v])=>{text=text.replace(new RegExp('{{\\s*'+k+'\\s*}}','gi'),String(v??''))});
 return text.replace(/^Contact:\s*$/gmi,'').replace(/\n{3,}/g,'\n\n').trim()
}
function renderSendCenterMessage(){const ta=$('#sendCenterMessage');if(ta)ta.value=sendCenterTemplateText()}
function renderSendCenterPreview(){
 const box=$('#sendCenterFeePreview'),dep=sendCenterSelectedDepartment(),row=sendCenterSelectedRow(),allCols=S.sendFeeColumns||[],cols=allCols.filter(x=>x.active);if(!box)return;
 if(!row){box.innerHTML='<p class="empty">Faculty aur course select karein</p>';return}
 const data=feeResolvedRow(row,allCols);box.innerHTML=`<h3>${esc(dep?.name||'Fee Structure')}</h3><p class="send-center-preview-note">${esc(sendCenterCourseLabel(row))}</p><table class="send-center-fee-table"><tbody>${cols.map(c=>`<tr><td>${esc(c.label)}</td><td>${esc(sendCenterPlainValue(c,data[c.column_key]))}</td></tr>`).join('')}</tbody></table>`
}
function populateSendCenterCourses(){
 const select=$('#sendCenterCourse'),depId=$('#sendCenterDepartment')?.value;if(!select)return;const rows=(S.sendFeeRows||[]).filter(x=>String(x.department_id)===String(depId));select.innerHTML=rows.map(x=>`<option value="${attr(x.id)}">${esc(sendCenterCourseLabel(x))}</option>`).join('')||'<option value="">No course available</option>';renderSendCenterPreview();renderSendCenterMessage()
}
function ensureSendCenterModal(){
 let m=$('#sendCenterModal');if(m)return m;
 m=document.createElement('div');m.id='sendCenterModal';m.className='modal-bg';m.innerHTML=`<div class="modal send-center-modal" role="dialog" aria-modal="true" aria-labelledby="sendCenterTitle"><div class="modal-head"><div><h2 id="sendCenterTitle">Send to Center</h2><p class="staff-form-note">WhatsApp template aur selected course ka fee PDF ek hi flow se bhejein.</p></div><button type="button" class="close" id="closeSendCenterModal">×</button></div><div class="send-center-grid"><div class="send-center-fields"><label class="field">WhatsApp Number<select id="sendCenterWhatsapp"></select></label><label class="field">WhatsApp Template<select id="sendCenterTemplate"></select></label><label class="field">Faculty / Department<select id="sendCenterDepartment"></select></label><label class="field">Course<select id="sendCenterCourse"></select></label><label class="field">Your Contact No. (optional)<input id="sendCenterStaffMobile" inputmode="tel" placeholder="Template mein {{staff_mobile}} ke liye"></label><label class="field">Message (editable)<textarea id="sendCenterMessage"></textarea></label></div><div class="send-center-preview"><div id="sendCenterFeePreview"><p class="empty">Fee preview loading...</p></div><div class="send-center-help"><b>Phone:</b> “Share PDF + Message” supported mobile browsers par native share kholta hai, jahan WhatsApp choose karke PDF + message ek saath bhej sakte hain.<br><b>Desktop:</b> “Download Fee PDF” karein, phir “Open WhatsApp” se message kholkar PDF attach karein.</div></div></div><div class="send-center-actions"><button id="downloadSendCenterPdf" class="btn secondary" type="button">⬇ Download Fee PDF</button><button id="shareSendCenter" class="btn green" type="button">WhatsApp / Share PDF + Message</button><button id="openSendCenterWhatsapp" class="btn primary" type="button">Open WhatsApp Message</button></div></div>`;
 document.body.appendChild(m);const close=()=>m.classList.remove('open');$('#closeSendCenterModal').onclick=close;m.addEventListener('click',e=>{if(e.target===m)close()});$('#sendCenterTemplate').onchange=renderSendCenterMessage;$('#sendCenterDepartment').onchange=populateSendCenterCourses;$('#sendCenterCourse').onchange=()=>{renderSendCenterPreview();renderSendCenterMessage()};$('#sendCenterStaffMobile').oninput=()=>{try{localStorage.setItem('crm_staff_contact_'+(S.user?.id||''),$('#sendCenterStaffMobile').value)}catch{}renderSendCenterMessage()};$('#downloadSendCenterPdf').onclick=downloadSendCenterPdf;$('#shareSendCenter').onclick=shareSendCenter;$('#openSendCenterWhatsapp').onclick=openSendCenterWhatsapp;return m
}
async function loadSendCenterData(){
 const [t,d,c,r]=await Promise.all([db.from('crm_university_message_templates').select('*').eq('active',true).order('sort_order').order('created_at'),db.from('crm_university_fee_departments').select('*').eq('active',true).order('sort_order').order('name'),db.from('crm_university_fee_columns').select('*').order('sort_order').order('label'),db.from('crm_university_fee_rows').select('*').eq('active',true).order('sort_order')]);const error=t.error||d.error||c.error||r.error;if(error)throw error;S.sendTemplates=t.data||[];S.sendFeeDepartments=d.data||[];S.sendFeeColumns=c.data||[];S.sendFeeRows=r.data||[]
}
window.openSendToCenter=async()=>{
 const base=S.callRows?.[S.callIndex];if(!base){toast('Pehle calling record open karein');return}const f=$('#callDetailsForm'),inst={...base,owner_name:f?.elements?.owner_name?.value?.trim()||base.owner_name,whatsapp_no:f?.elements?.whatsapp_no?.value?.trim()||base.whatsapp_no,mobile_no:f?.elements?.mobile_no?.value?.trim()||base.mobile_no};const numbers=phones(inst.whatsapp_no).length?phones(inst.whatsapp_no):phones(inst.mobile_no);if(!numbers.length){toast('Center ka WhatsApp/Mobile number nahi hai');return}
 const m=ensureSendCenterModal();m.classList.add('open');$('#sendCenterFeePreview').innerHTML='<p class="empty">Template aur fee data loading...</p>';
 try{await loadSendCenterData();S.sendCenterInstitute=inst;$('#sendCenterWhatsapp').innerHTML=numbers.map(n=>`<option value="${attr(n)}">${esc(n)}</option>`).join('');$('#sendCenterTemplate').innerHTML=(S.sendTemplates||[]).map(x=>`<option value="${attr(x.id)}">${esc(x.name)}</option>`).join('')||'<option value="">Default Message</option>';$('#sendCenterDepartment').innerHTML=(S.sendFeeDepartments||[]).map(x=>`<option value="${attr(x.id)}">${esc(x.name)}</option>`).join('')||'<option value="">No faculty available</option>';let saved='';try{saved=localStorage.getItem('crm_staff_contact_'+(S.user?.id||''))||''}catch{}$('#sendCenterStaffMobile').value=saved;populateSendCenterCourses();renderSendCenterMessage()}catch(e){$('#sendCenterFeePreview').innerHTML='<p class="empty">Data load nahi hua</p>';toast(e.message||'Template/Fee data load nahi hua')}
};
function createSendCenterPdf(){
 const row=sendCenterSelectedRow(),dep=sendCenterSelectedDepartment();if(!row){toast('Course select karein');return null}const JsPDF=window.jspdf?.jsPDF;if(!JsPDF){toast('PDF library load nahi hui. Page refresh karein.');return null}const allCols=S.sendFeeColumns||[],cols=allCols.filter(x=>x.active),data=feeResolvedRow(row,allCols),course=String(data.course_name||row.row_data?.course_name||'Fee Structure'),safe=course.replace(/[^a-z0-9]+/gi,'-').replace(/^-+|-+$/g,'').slice(0,70)||'Fee-Structure',filename=`SIU-${safe}-Fee-Structure.pdf`,doc=new JsPDF({unit:'mm',format:'a4'});let y=18;
 doc.setFont('helvetica','bold');doc.setFontSize(16);doc.text('SENGOL INTERNATIONAL UNIVERSITY',105,y,{align:'center'});y+=8;doc.setFontSize(13);doc.text('FEE STRUCTURE',105,y,{align:'center'});y+=8;doc.setFontSize(10);doc.text(String(dep?.name||''),105,y,{align:'center',maxWidth:185});y+=7;doc.text(sendCenterCourseLabel(row),105,y,{align:'center',maxWidth:185});y+=10;doc.setDrawColor(180);doc.line(15,y,195,y);y+=7;
 cols.forEach(col=>{const label=String(col.label||col.column_key),value=sendCenterPlainValue(col,data[col.column_key]),lines=doc.splitTextToSize(value,115),height=Math.max(7,lines.length*5+2);if(y+height>278){doc.addPage();y=18}doc.setFont('helvetica','bold');doc.setFontSize(9);doc.text(label,17,y);doc.setFont('helvetica','normal');doc.text(lines,75,y);y+=height;doc.setDrawColor(225);doc.line(15,y-2,195,y-2)});if(y>265){doc.addPage();y=18}doc.setFontSize(8);doc.setTextColor(100);doc.text('Generated from Calling CRM · Sengol International University',105,287,{align:'center'});const blob=doc.output('blob'),file=new File([blob],filename,{type:'application/pdf'});return{doc,file,filename}
}
window.downloadSendCenterPdf=()=>{const pdf=createSendCenterPdf();if(!pdf)return;pdf.doc.save(pdf.filename);toast('Fee PDF downloaded')};
window.openSendCenterWhatsapp=()=>{const num=sendCenterWaNumber($('#sendCenterWhatsapp')?.value),message=$('#sendCenterMessage')?.value?.trim()||sendCenterTemplateText();if(!num){toast('WhatsApp number nahi mila');return}window.open(`https://wa.me/${num}?text=${encodeURIComponent(message)}`,'_blank','noopener')};
window.shareSendCenter=async()=>{
 const pdf=createSendCenterPdf();if(!pdf)return;const message=$('#sendCenterMessage')?.value?.trim()||sendCenterTemplateText();try{if(navigator.share&&navigator.canShare?.({files:[pdf.file]})){await navigator.share({title:'Sengol International University Fee Structure',text:message,files:[pdf.file]});return}}catch(e){if(e?.name==='AbortError')return}
 pdf.doc.save(pdf.filename);openSendCenterWhatsapp();toast('PDF download ho gaya. WhatsApp mein is PDF ko attach karke send karein.')
};
'''
s = s.replace(js_anchor, js + '\n' + js_anchor, 1)

p.write_text(s, encoding='utf-8')
print('Send to Center flow patched successfully')
