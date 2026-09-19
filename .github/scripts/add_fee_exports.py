from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')

old='''<div class="fee-admin-actions"><button id="addFeeDepartment" class="btn primary admin-only" type="button">+ Department</button><button id="refreshFeeBuilder" class="btn secondary" type="button">Refresh</button></div>'''
new='''<div class="fee-admin-actions"><button id="addFeeDepartment" class="btn primary admin-only" type="button">+ Department</button><button id="exportFeeExcel" class="btn green" type="button">Export Excel</button><button id="exportFeePdf" class="btn red" type="button">Export PDF</button><button id="refreshFeeBuilder" class="btn secondary" type="button">Refresh</button></div>'''
if old not in text:
    raise SystemExit('fee action toolbar target not found')
text=text.replace(old,new,1)

anchor="const feeSearchInput=$('#feeSearch');if(feeSearchInput)feeSearchInput.addEventListener('input',()=>renderFeeBuilder());"
if anchor not in text:
    raise SystemExit('fee search listener target not found')

js=r'''

function feeExportData(){
 const cols=(S.feeColumns||[]).filter(x=>x.active),deps=(S.feeDepartments||[]).filter(x=>x.active),query=String($('#feeSearch')?.value||'').trim().toLowerCase(),groups=[];
 deps.forEach(dep=>{
  const departmentMatch=query&&String(dep.name||'').toLowerCase().includes(query);
  const matched=(S.feeRows||[]).filter(x=>x.department_id===dep.id&&x.active).filter(row=>{
   if(!query||departmentMatch)return true;
   const resolved=feeResolvedRow(row,cols),hay=[dep.name,...Object.values(row.row_data||{}),...cols.map(c=>c.label),...cols.map(c=>resolved[c.column_key])].map(v=>String(v??'')).join(' ').toLowerCase();
   return hay.includes(query)
  });
  if(matched.length)groups.push({department:dep,rows:matched})
 });
 return{cols,groups,query}
}
window.exportFeeExcel=()=>{
 if(typeof XLSX==='undefined'){toast('Excel export library load nahi hui');return}
 const {cols,groups}=feeExportData(),rows=[];
 groups.forEach(g=>g.rows.forEach((row,i)=>{const data=feeResolvedRow(row,cols),out={'Faculty / Department':g.department.name,'S.No.':i+1};cols.forEach(c=>{const v=data[c.column_key];out[c.label]=(v===null||v===undefined)?'':v});rows.push(out)}));
 if(!rows.length){toast('Export ke liye fee records nahi mile');return}
 const ws=XLSX.utils.json_to_sheet(rows),headers=Object.keys(rows[0]);
 ws['!cols']=headers.map(h=>({wch:Math.min(55,Math.max(12,h.length+2,...rows.slice(0,80).map(r=>String(r[h]??'').length+2)))}));
 const wb=XLSX.utils.book_new();XLSX.utils.book_append_sheet(wb,ws,'Fee Detail');
 const d=new Date(),stamp=`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
 XLSX.writeFile(wb,`SIU-Fee-Detail-${stamp}.xlsx`)
};
window.exportFeePdf=()=>{
 const {cols,groups,query}=feeExportData();if(!groups.length){toast('Export ke liye fee records nahi mile');return}
 const win=window.open('','_blank');if(!win){toast('PDF ke liye popup allow karein');return}
 const sections=groups.map(g=>`<section><h2>${esc(g.department.name)}</h2><table><thead><tr><th>S.No.</th>${cols.map(c=>`<th>${esc(c.label)}</th>`).join('')}</tr></thead><tbody>${g.rows.map((row,i)=>{const data=feeResolvedRow(row,cols);return `<tr><td>${i+1}</td>${cols.map(c=>`<td>${feeDisplayValue(c,data[c.column_key])}</td>`).join('')}</tr>`}).join('')}</tbody></table></section>`).join('');
 const filter=query?`<p class="filter">Search filter: ${esc(query)}</p>`:'';
 win.document.open();win.document.write(`<!doctype html><html><head><meta charset="utf-8"><title>SIU Fee Detail</title><style>@page{size:A4 landscape;margin:9mm}*{box-sizing:border-box}body{font-family:Arial,sans-serif;color:#17324d;margin:0;font-size:9px}h1{font-size:18px;margin:0 0 3px;color:#173f6c}p.sub{margin:0 0 8px;color:#647b91}.filter{margin:0 0 10px;font-weight:700}section{margin:0 0 16px;page-break-inside:auto}h2{font-size:11px;margin:0;padding:7px 8px;background:#e9f2ff;border:1px solid #7f9fbe;border-bottom:0;color:#173f6c}table{width:100%;border-collapse:collapse;table-layout:auto}th,td{border:1px solid #aebfd1;padding:5px 6px;text-align:left;vertical-align:top;word-break:break-word}th{background:#f4f8ff;color:#2457a6;font-size:8.5px;white-space:nowrap}td{font-size:8px}tr{page-break-inside:avoid}.meta{display:flex;justify-content:space-between;gap:20px;margin-bottom:10px;color:#647b91}</style></head><body><h1>Sengol International University</h1><p class="sub">Fee Detail</p><div class="meta"><span>${filter}</span><span>Generated: ${new Date().toLocaleString('en-IN')}</span></div>${sections}</body></html>`);win.document.close();win.focus();setTimeout(()=>win.print(),350);win.onafterprint=()=>win.close()
};
const exportFeeExcelBtn=$('#exportFeeExcel');if(exportFeeExcelBtn)exportFeeExcelBtn.onclick=window.exportFeeExcel;
const exportFeePdfBtn=$('#exportFeePdf');if(exportFeePdfBtn)exportFeePdfBtn.onclick=window.exportFeePdf;
'''
text=text.replace(anchor,anchor+js,1)

css=r'''

/* Fee export buttons */
#universitydetailPage [data-university-panel="fee"] .fee-admin-actions{align-items:center}
#exportFeeExcel,#exportFeePdf{white-space:nowrap}
@media(max-width:680px){#universitydetailPage [data-university-panel="fee"] .fee-admin-actions{width:100%}#exportFeeExcel,#exportFeePdf{flex:1 1 auto}}
'''
if '/* Fee export buttons */' not in text:
    text=text.replace('</style>',css+'\n</style>',1)

p.write_text(text,encoding='utf-8')
