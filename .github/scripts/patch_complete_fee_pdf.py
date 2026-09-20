from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Load AutoTable after jsPDF so the complete fee structure can span pages cleanly.
needle = '<script src="https://unpkg.com/jspdf@2.5.2/dist/jspdf.umd.min.js"></script>'
autotable = '<script src="https://unpkg.com/jspdf-autotable@3.8.4/dist/jspdf.plugin.autotable.min.js"></script>'
assert needle in s, 'jsPDF script tag not found'
if autotable not in s:
    s = s.replace(needle, needle + '\n' + autotable, 1)

# Make the modal explicit: course selection personalizes the message, while PDF is complete.
s = s.replace(
    'WhatsApp template aur selected course ka fee PDF ek hi flow se bhejein.',
    'WhatsApp template ke saath complete university fee PDF bhejein. Faculty/Course selection sirf message personalization ke liye hai.'
)
s = s.replace(
    '<b>Phone:</b> “Share PDF + Message” supported mobile browsers par native share kholta hai, jahan WhatsApp choose karke PDF + message ek saath bhej sakte hain.<br><b>Desktop:</b> “Download Fee PDF” karein, phir “Open WhatsApp” se message kholkar PDF attach karein.',
    '<b>Complete PDF:</b> sabhi active Faculty/Departments, Courses aur fee columns ek hi multi-page PDF mein aayenge.<br><b>Phone:</b> “Share Complete PDF + Message” supported mobile browsers par native share kholta hai, jahan WhatsApp choose karke complete PDF + message bhej sakte hain.<br><b>Desktop:</b> “Download Complete Fee PDF” karein, phir “Open WhatsApp” se message kholkar PDF attach karein.'
)
s = s.replace('⬇ Download Fee PDF', '⬇ Download Complete Fee PDF')
s = s.replace('WhatsApp / Share PDF + Message', 'WhatsApp / Share Complete PDF + Message')

new_func = r'''function createSendCenterPdf(){
 const JsPDF=window.jspdf?.jsPDF;if(!JsPDF){toast('PDF library load nahi hui. Page refresh karein.');return null}
 const allCols=S.sendFeeColumns||[],cols=allCols.filter(x=>x.active),deps=(S.sendFeeDepartments||[]).filter(x=>x.active),rows=(S.sendFeeRows||[]).filter(x=>x.active);
 if(!cols.length||!deps.length||!rows.length){toast('Complete fee data nahi mila');return null}
 const doc=new JsPDF({orientation:'landscape',unit:'mm',format:'a4'}),filename='SIU-Complete-Fee-Structure.pdf',pageWidth=doc.internal.pageSize.getWidth(),pageHeight=doc.internal.pageSize.getHeight(),margin=9;
 if(typeof doc.autoTable!=='function'){toast('Complete PDF table library load nahi hui. Page refresh karein.');return null}
 let rendered=0;
 deps.forEach(dep=>{
  const depRows=rows.filter(row=>String(row.department_id)===String(dep.id));if(!depRows.length)return;
  if(rendered)doc.addPage();rendered++;
  const drawHeader=()=>{doc.setTextColor(23,50,77);doc.setFont('helvetica','bold');doc.setFontSize(13);doc.text('SENGOL INTERNATIONAL UNIVERSITY',pageWidth/2,9,{align:'center'});doc.setFontSize(9);doc.text('COMPLETE FEE STRUCTURE',pageWidth/2,14,{align:'center'});doc.setFontSize(8.5);doc.text(String(dep.name||'Faculty / Department'),margin,21,{maxWidth:pageWidth-margin*2});doc.setDrawColor(160,183,208);doc.line(margin,24,pageWidth-margin,24)};
  const head=[['S.No.',...cols.map(c=>String(c.label||c.column_key))]];
  const body=depRows.map((row,i)=>{const data=feeResolvedRow(row,allCols);return [String(i+1),...cols.map(c=>sendCenterPlainValue(c,data[c.column_key]))]});
  doc.autoTable({
   head,body,startY:27,margin:{left:margin,right:margin,top:27,bottom:12},theme:'grid',
   styles:{font:'helvetica',fontSize:6.2,cellPadding:1.35,valign:'top',overflow:'linebreak',textColor:[23,50,77],lineColor:[196,211,226],lineWidth:.15},
   headStyles:{fillColor:[237,244,255],textColor:[36,87,166],fontStyle:'bold',fontSize:6.3,lineColor:[159,183,208],lineWidth:.2},
   columnStyles:{0:{cellWidth:10,halign:'center'}},
   showHead:'everyPage',
   willDrawPage:()=>drawHeader(),
   didDrawPage:data=>{doc.setFont('helvetica','normal');doc.setFontSize(6.5);doc.setTextColor(105,127,149);doc.text(`Page ${doc.internal.getNumberOfPages()}`,pageWidth-margin,pageHeight-5,{align:'right'});doc.text('Generated from Calling CRM',margin,pageHeight-5)}
  });
 });
 if(!rendered){toast('Complete fee data nahi mila');return null}
 const blob=doc.output('blob'),file=new File([blob],filename,{type:'application/pdf'});return{doc,file,filename}
}'''

pattern = r"function createSendCenterPdf\(\)\{.*?\n\}\nwindow\.downloadSendCenterPdf="
match = re.search(pattern, s, flags=re.S)
assert match, 'createSendCenterPdf block not found'
s = s[:match.start()] + new_func + '\nwindow.downloadSendCenterPdf=' + s[match.end():]

# Update status/toast wording to match complete PDF behavior.
s = s.replace("toast('Fee PDF downloaded')", "toast('Complete fee PDF downloaded')")
s = s.replace("toast('PDF download ho gaya. WhatsApp mein is PDF ko attach karke send karein.')", "toast('Complete fee PDF download ho gaya. WhatsApp mein is PDF ko attach karke send karein.')")

p.write_text(s, encoding='utf-8')
