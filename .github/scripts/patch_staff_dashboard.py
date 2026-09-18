from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Staff calling dashboard */'
if marker in text:
    raise SystemExit(0)

institute_marker = '<section id="institutesPage" class="page">'
if institute_marker not in text:
    raise SystemExit('Institutes page marker not found')

staff_html = r'''
<div id="staffDashboard">
  <div class="staff-dash-hero">
    <div><h1>My Calling Dashboard</h1><p>Aaj ke priority calls, follow-ups aur performance ek jagah.</p></div>
    <button class="btn primary" type="button" onclick="document.querySelector('[data-page=calling]')?.click()">☎ Open Calling</button>
  </div>
  <div class="staff-dash-cards">
    <article class="staff-dash-card"><span>Assigned Institutes</span><b id="sdAssigned">0</b><small>Total assigned</small></article>
    <article class="staff-dash-card"><span>Not Called</span><b id="sdNotCalled">0</b><small>Calling pending</small></article>
    <article class="staff-dash-card"><span>Today Calls</span><b id="sdTodayCalls">0</b><small>Attempts today</small></article>
    <article class="staff-dash-card"><span>Interested</span><b id="sdInterested">0</b><small>This month</small></article>
    <article class="staff-dash-card"><span>Today Follow-ups</span><b id="sdTodayFollowups">0</b><small>Due today</small></article>
    <article class="staff-dash-card urgent"><span>Overdue</span><b id="sdOverdue">0</b><small>Needs action</small></article>
    <article class="staff-dash-card"><span>Done</span><b id="sdDone">0</b><small>This month</small></article>
    <article class="staff-dash-card"><span>Total Calls</span><b id="sdMonthCalls">0</b><small>This month</small></article>
  </div>
  <div class="staff-dash-grid">
    <article class="card staff-dash-section">
      <div class="toolbar"><div><h2>Needs Attention</h2><p>Overdue aur aaj ke follow-ups.</p></div><b id="sdAttentionCount">0 due</b></div>
      <div id="sdAttentionList" class="staff-attention-list"><p class="empty">No pending follow-up</p></div>
      <div id="sdNotCalledNote" class="staff-notcalled-note"></div>
    </article>
    <article class="card staff-dash-section">
      <div class="toolbar"><div><h2>Call Status Summary</h2><p>This month ke call results.</p></div><b id="sdStatusTotal">0 calls</b></div>
      <div id="sdStatusSummary" class="staff-status-summary"><p class="empty">No calls this month</p></div>
    </article>
  </div>
  <div class="staff-dash-grid staff-dash-lower">
    <article class="card staff-dash-section">
      <div class="toolbar"><div><h2>Recent Activity</h2><p>Aapki latest saved calls.</p></div><button class="btn secondary" type="button" onclick="document.querySelector('[data-page=calling]')?.click();setTimeout(()=>document.querySelector('[data-call-page-tab=history]')?.click(),80)">Call History</button></div>
      <div class="table-wrap"><table class="staff-dash-table"><thead><tr><th>Institute</th><th>Call Time</th><th>Status</th><th>Remarks</th><th>Next Call</th></tr></thead><tbody id="sdRecentBody"><tr><td colspan="5" class="empty">No recent calls</td></tr></tbody></table></div>
    </article>
    <article class="card staff-dash-section">
      <div class="toolbar"><div><h2>Performance Snapshot</h2><p>Calls, unique institutes aur outcomes.</p></div></div>
      <div id="sdPerformance" class="staff-performance-snapshot"></div>
    </article>
  </div>
</div>
'''
text = text.replace(institute_marker, staff_html + '\n' + institute_marker, 1)

css = r'''

/* Staff calling dashboard */
body:not(.staff-role) #staffDashboard{display:none!important}
body.staff-role #dashboardPage>.heading,
body.staff-role #dashboardPage>.stats,
body.staff-role #dashboardPage>.dashboard-grid,
body.staff-role #dashboardPage>.lower-grid,
body.staff-role #dashboardPage>.quick-grid{display:none!important}
body.staff-role .content:has(#dashboardPage.active){padding-top:12px}
#staffDashboard{display:grid;gap:12px}
.staff-dash-hero{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:15px 18px;border:1px solid #d9b79f;border-radius:14px;background:linear-gradient(105deg,#fff6ef 0%,#f4dfd2 62%,#ead0bf 100%)}
.staff-dash-hero h1{margin:0;color:#5e2e18;font-size:24px}.staff-dash-hero p{margin:4px 0 0;color:#7b685c;font-size:13px}.staff-dash-hero .btn{background:linear-gradient(90deg,#a74416,#713119);white-space:nowrap}
.staff-dash-cards{display:grid;grid-template-columns:repeat(8,minmax(118px,1fr));gap:9px}
.staff-dash-card{position:relative;min-height:92px;padding:12px 13px;border:1px solid #dfc0ad;border-radius:12px;background:linear-gradient(145deg,#fff,#fff0e5);overflow:hidden}
.staff-dash-card:nth-child(2){background:linear-gradient(145deg,#fff,#fff5df);border-color:#e5cca4}.staff-dash-card:nth-child(3){background:linear-gradient(145deg,#fff,#f9e8dc)}.staff-dash-card:nth-child(4){background:linear-gradient(145deg,#fff,#fff0d9);border-color:#e5c58f}.staff-dash-card:nth-child(5){background:linear-gradient(145deg,#fff,#f6e4d8)}.staff-dash-card:nth-child(7){background:linear-gradient(145deg,#fff,#f2e5db)}.staff-dash-card:nth-child(8){background:linear-gradient(145deg,#fff,#f8e8de)}
.staff-dash-card.urgent{background:linear-gradient(145deg,#fff,#fde8e7);border-color:#e7b5af}.staff-dash-card.urgent b{color:#c42c29}
.staff-dash-card span{display:block;color:#6e574a;font-size:11px;font-weight:750}.staff-dash-card b{display:block;margin-top:4px;color:#8b3b18;font-size:25px;line-height:1}.staff-dash-card small{display:block;margin-top:6px;color:#8b776b;font-size:10px}
.staff-dash-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:12px}.staff-dash-lower{grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr)}
.staff-dash-section{margin:0;padding:14px;border-color:#ddc0ae}.staff-dash-section h2{margin:0;font-size:17px;color:#5b301d}.staff-dash-section .toolbar p{margin:3px 0 0;color:#846f62;font-size:11px}.staff-dash-section .toolbar>b{color:#8b3b18;font-size:12px}
.staff-attention-list{display:grid;gap:7px;margin-top:11px}.staff-attention-row{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:10px;align-items:center;padding:9px 10px;border:1px solid #ead3c4;border-radius:10px;background:#fffaf6}.staff-attention-row.overdue{background:#fff3f2;border-color:#efcbc7}.staff-attention-row b{display:block;font-size:13px}.staff-attention-row small{display:block;margin-top:2px;color:#806d61;font-size:10px}.staff-attention-tag{padding:4px 7px;border-radius:20px;background:#fff0df;color:#8a4d11;font-size:10px;font-weight:800}.staff-attention-row.overdue .staff-attention-tag{background:#fde1df;color:#b72d29}.staff-attention-row .btn{padding:7px 10px;font-size:11px;background:#a74416;color:#fff}
.staff-notcalled-note{margin-top:9px;padding:9px 11px;border-radius:9px;background:#fff4e6;color:#704229;font-size:12px;font-weight:650}
.staff-status-summary{display:grid;gap:8px;margin-top:11px}.staff-status-line{display:grid;grid-template-columns:minmax(110px,1fr) minmax(100px,1.4fr) 52px;align-items:center;gap:8px;font-size:12px}.staff-status-bar{height:8px;border-radius:20px;background:#f0e4dc;overflow:hidden}.staff-status-bar i{display:block;height:100%;border-radius:20px;background:linear-gradient(90deg,#ad4818,#6d321b)}.staff-status-line b{text-align:right;color:#6d3820;font-size:11px}
.staff-dash-table{min-width:720px}.staff-dash-table th{font-size:11px}.staff-dash-table td{padding:8px 9px;font-size:12px;white-space:normal;vertical-align:top}.staff-dash-table td:nth-child(1){font-weight:700}.staff-dash-table td:nth-child(4){max-width:260px}
.staff-performance-snapshot{display:grid;gap:9px;margin-top:10px}.staff-performance-box{border:1px solid #e1c8b7;border-radius:11px;padding:10px 11px;background:#fffaf6}.staff-performance-box h3{margin:0 0 8px;color:#71371b;font-size:13px}.staff-performance-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}.staff-performance-metrics div{padding:7px 5px;border-radius:8px;background:#fff1e7;text-align:center}.staff-performance-metrics b{display:block;color:#913b17;font-size:17px}.staff-performance-metrics small{font-size:9px;color:#7f6c60}
@media(max-width:1250px){.staff-dash-cards{grid-template-columns:repeat(4,1fr)}}
@media(max-width:900px){.staff-dash-grid,.staff-dash-lower{grid-template-columns:1fr}.staff-dash-cards{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.staff-dash-hero{align-items:flex-start;flex-direction:column}.staff-dash-cards{grid-template-columns:1fr 1fr}.staff-attention-row{grid-template-columns:1fr auto}.staff-attention-row .btn{grid-column:1/-1}.staff-performance-metrics{grid-template-columns:repeat(2,1fr)}}
'''
text = text.replace('\n</style>', css + '\n</style>', 1)

old_enter = "await Promise.allSettled([loadStats(),loadDashboardAnalytics(),loadRows(),loadMasterStats()])}"
new_enter = "await Promise.allSettled([loadStats(),loadDashboardAnalytics(),loadRows(),loadMasterStats()]);if(!isAdmin())await loadStaffDashboard()}"
if old_enter not in text:
    raise SystemExit('enter dashboard load pattern not found')
text = text.replace(old_enter, new_enter, 1)

old_nav = "if(p==='dashboard')Promise.allSettled([loadStats(),loadDashboardAnalytics()])"
new_nav = "if(p==='dashboard'){Promise.allSettled([loadStats(),loadDashboardAnalytics()]);if(!isAdmin())loadStaffDashboard()}"
if old_nav not in text:
    raise SystemExit('dashboard nav pattern not found')
text = text.replace(old_nav, new_nav, 1)

js = r'''

function staffDashboardRanges(){
 const parts=Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Kolkata',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date()).filter(x=>x.type!=='literal').map(x=>[x.type,x.value]));
 const y=Number(parts.year),m=Number(parts.month),d=Number(parts.day),pad=n=>String(n).padStart(2,'0');
 const todayStart=new Date(`${y}-${pad(m)}-${pad(d)}T00:00:00+05:30`),todayEnd=new Date(todayStart.getTime()+86400000),civil=new Date(Date.UTC(y,m-1,d)),offset=(civil.getUTCDay()+6)%7,weekStart=new Date(todayStart.getTime()-offset*86400000),monthStart=new Date(`${y}-${pad(m)}-01T00:00:00+05:30`);
 return{todayStart:todayStart.toISOString(),todayEnd:todayEnd.toISOString(),weekStart:weekStart.toISOString(),monthStart:monthStart.toISOString(),rangeStart:new Date(Math.min(weekStart.getTime(),monthStart.getTime())).toISOString()}
}
async function fetchStaffDashboardLogs(start,end){
 let rows=[];
 for(let from=0;;from+=1000){
  const {data,error}=await db.from('crm_call_logs').select('id,institute_id,status,remarks,next_call_at,created_at').eq('staff_id',S.user.id).gte('created_at',start).lt('created_at',end).order('created_at',{ascending:false}).range(from,from+999);
  if(error)throw error;rows.push(...(data||[]));if(!data||data.length<1000)break
 }
 return rows
}
function staffDashMetricBlock(title,rows){
 const unique=new Set(rows.map(x=>x.institute_id).filter(Boolean)).size,interested=rows.filter(x=>x.status==='Interested').length,done=rows.filter(x=>x.status==='Done').length;
 return `<div class="staff-performance-box"><h3>${esc(title)}</h3><div class="staff-performance-metrics"><div><b>${rows.length}</b><small>Calls</small></div><div><b>${unique}</b><small>Unique</small></div><div><b>${interested}</b><small>Interested</small></div><div><b>${done}</b><small>Done</small></div></div></div>`
}
window.openStaffDashboardCall=async id=>{
 $$('.page').forEach(x=>x.classList.remove('active'));$('#callingPage').classList.add('active');$$('[data-page]').forEach(x=>x.classList.toggle('active',x.dataset.page==='calling'));const context=$('#topContextTitle'),topTabs=$('#topInstituteTabs');if(context)context.classList.add('hidden');if(topTabs)topTabs.classList.add('hidden');await openFollowupCall(id)
};
async function loadStaffDashboard(){
 if(isAdmin()||!S.user)return;
 try{
  const r=staffDashboardRanges();
  const assignedQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).eq('assigned_to',S.user.id),notCalledQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).eq('assigned_to',S.user.id).is('last_status',null),todayFollowQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).eq('assigned_to',S.user.id).not('next_call_at','is',null).gte('next_call_at',r.todayStart).lt('next_call_at',r.todayEnd),overdueQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).eq('assigned_to',S.user.id).not('next_call_at','is',null).lt('next_call_at',r.todayStart),attentionQ=db.from('crm_institute_call_state').select('id,institute_name,mobile_no,whatsapp_no,last_status,next_call_at').eq('assigned_to',S.user.id).not('next_call_at','is',null).lt('next_call_at',r.todayEnd).order('next_call_at',{ascending:true}).limit(10),recentQ=db.from('crm_call_logs').select('id,institute_id,status,remarks,next_call_at,created_at,crm_institutes(institute_name,mobile_no)').eq('staff_id',S.user.id).order('created_at',{ascending:false}).limit(8);
  const [assigned,notCalled,todayFollow,overdue,attention,recent,logs]=await Promise.all([assignedQ,notCalledQ,todayFollowQ,overdueQ,attentionQ,recentQ,fetchStaffDashboardLogs(r.rangeStart,r.todayEnd)]);
  const err=[assigned,notCalled,todayFollow,overdue,attention,recent].find(x=>x?.error)?.error;if(err)throw err;
  const month=logs.filter(x=>x.created_at>=r.monthStart),week=logs.filter(x=>x.created_at>=r.weekStart),today=logs.filter(x=>x.created_at>=r.todayStart),interested=month.filter(x=>x.status==='Interested').length,done=month.filter(x=>x.status==='Done').length;
  $('#sdAssigned').textContent=(assigned.count||0).toLocaleString();$('#sdNotCalled').textContent=(notCalled.count||0).toLocaleString();$('#sdTodayCalls').textContent=today.length.toLocaleString();$('#sdInterested').textContent=interested.toLocaleString();$('#sdTodayFollowups').textContent=(todayFollow.count||0).toLocaleString();$('#sdOverdue').textContent=(overdue.count||0).toLocaleString();$('#sdDone').textContent=done.toLocaleString();$('#sdMonthCalls').textContent=month.length.toLocaleString();
  const attentionRows=attention.data||[];$('#sdAttentionCount').textContent=`${attentionRows.length.toLocaleString()} shown`;
  $('#sdAttentionList').innerHTML=attentionRows.map(x=>{const over=String(x.next_call_at)<r.todayStart;return `<div class="staff-attention-row ${over?'overdue':''}"><div><b>${esc(x.institute_name||'—')}</b><small>${esc(x.last_status||'Follow-up')} · ${phones(x.mobile_no)[0]||'No mobile'}</small></div><span class="staff-attention-tag">${over?'Overdue':'Today'} · ${formatDate(x.next_call_at)}</span><button class="btn" type="button" onclick="openStaffDashboardCall('${attr(x.id)}')">☎ Call Now</button></div>`}).join('')||'<p class="empty">No overdue or today follow-ups</p>';
  $('#sdNotCalledNote').innerHTML=(notCalled.count||0)>0?`<b>${(notCalled.count||0).toLocaleString()} institutes</b> abhi call nahi hue hain. <button class="btn secondary" style="padding:5px 8px;margin-left:6px" type="button" onclick="document.querySelector('[data-page=calling]')?.click()">Start Calling</button>`:'All assigned institutes have a call status.';
  const counts=statusCounts(month),total=month.length;$('#sdStatusTotal').textContent=`${total.toLocaleString()} calls`;$('#sdStatusSummary').innerHTML=Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(([s,n])=>`<div class="staff-status-line"><span>${esc(s)}</span><div class="staff-status-bar"><i style="width:${total?Math.max(4,Math.round(n*100/total)):0}%"></i></div><b>${n} · ${total?Math.round(n*100/total):0}%</b></div>`).join('')||'<p class="empty">No calls this month</p>';
  $('#sdRecentBody').innerHTML=(recent.data||[]).map(x=>{const institute=x.crm_institutes||{};return `<tr><td>${esc(institute.institute_name||'—')}</td><td>${formatCallDateTime(x.created_at)}</td><td><span class="history-status-pill">${esc(x.status||'—')}</span></td><td>${esc(x.remarks||'No remarks')}</td><td>${x.next_call_at?formatDate(x.next_call_at):'—'}</td></tr>`}).join('')||'<tr><td colspan="5" class="empty">No recent calls</td></tr>';
  $('#sdPerformance').innerHTML=staffDashMetricBlock('Today',today)+staffDashMetricBlock('This Week',week)+staffDashMetricBlock('This Month',month)
 }catch(e){console.error(e);toast('Staff dashboard load nahi hua: '+(e.message||e))}
}
'''
text = text.replace('\n</script></body></html>', js + '\n</script></body></html>', 1)
p.write_text(text, encoding='utf-8')
