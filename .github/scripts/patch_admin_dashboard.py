from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Admin management dashboard */'
if marker in text:
    raise SystemExit(0)

admin_html = r'''
<div id="adminDashboard">
  <div class="admin-dash-hero">
    <div><h1>Admin Dashboard</h1><p>Team calling, assignments, follow-ups aur performance ka live overview.</p></div>
    <div class="admin-dash-hero-actions"><button class="btn secondary" type="button" onclick="document.querySelector('[data-page=institutes]')?.click()">▦ Manage Institutes</button><button class="btn primary" type="button" onclick="document.querySelector('[data-page=reports]')?.click()">⌁ Open Reports</button></div>
  </div>
  <div class="admin-dash-cards">
    <article class="admin-dash-card"><span>Total Institutes</span><b id="adTotal">0</b><small>Master database</small></article>
    <article class="admin-dash-card"><span>Assigned</span><b id="adAssigned">0</b><small>With staff</small></article>
    <article class="admin-dash-card warning"><span>Unassigned</span><b id="adUnassigned">0</b><small>Needs allocation</small></article>
    <article class="admin-dash-card"><span>Active Staff</span><b id="adActiveStaff">0</b><small>Calling team</small></article>
    <article class="admin-dash-card"><span>Today Calls</span><b id="adTodayCalls">0</b><small>All staff</small></article>
    <article class="admin-dash-card"><span>Interested</span><b id="adInterested">0</b><small>This month</small></article>
    <article class="admin-dash-card"><span>Today Follow-ups</span><b id="adTodayFollowups">0</b><small>Team due today</small></article>
    <article class="admin-dash-card urgent"><span>Overdue</span><b id="adOverdue">0</b><small>Needs attention</small></article>
  </div>

  <div class="admin-dash-grid">
    <article class="card admin-dash-section">
      <div class="toolbar"><div><h2>Needs Attention</h2><p>Unassigned records, overdue follow-ups aur aaj ke due calls.</p></div><b id="adAttentionCount">0 due</b></div>
      <div id="adAttentionSummary" class="admin-attention-summary"></div>
      <div id="adAttentionList" class="admin-attention-list"><p class="empty">No urgent follow-ups</p></div>
    </article>
    <article class="card admin-dash-section">
      <div class="toolbar"><div><h2>Call Status Summary</h2><p>This month ke team call results.</p></div><b id="adStatusTotal">0 calls</b></div>
      <div id="adStatusSummary" class="admin-status-summary"><p class="empty">No calls this month</p></div>
    </article>
  </div>

  <article class="card admin-dash-section admin-team-card">
    <div class="toolbar"><div><h2>Team Performance</h2><p>Staff-wise assignment, calls, interested, done aur overdue.</p></div><button class="btn secondary" type="button" onclick="document.querySelector('[data-page=staff]')?.click()">Manage Staff</button></div>
    <div class="table-wrap"><table class="admin-team-table"><thead><tr><th>Staff</th><th>Assigned</th><th>Today Calls</th><th>Month Calls</th><th>Interested</th><th>Done</th><th>Overdue</th></tr></thead><tbody id="adTeamBody"><tr><td colspan="7" class="empty">Team data loading...</td></tr></tbody></table></div>
  </article>

  <div class="admin-dash-grid admin-dash-lower">
    <article class="card admin-dash-section">
      <div class="toolbar"><div><h2>Recent Team Activity</h2><p>Latest calls saved by staff.</p></div><button class="btn secondary" type="button" onclick="document.querySelector('[data-page=reports]')?.click()">View Report</button></div>
      <div class="table-wrap"><table class="admin-recent-table"><thead><tr><th>Staff</th><th>Institute</th><th>Call Time</th><th>Status</th><th>Remarks</th><th>Next Call</th></tr></thead><tbody id="adRecentBody"><tr><td colspan="6" class="empty">No recent calls</td></tr></tbody></table></div>
    </article>
    <article class="card admin-dash-section">
      <div class="toolbar"><div><h2>Performance Snapshot</h2><p>Today, week aur month ka combined team output.</p></div></div>
      <div id="adPerformance" class="admin-performance-snapshot"></div>
    </article>
  </div>
</div>
'''

html_anchor = '</div></section>\n\n<div id="staffDashboard">'
if html_anchor not in text:
    raise SystemExit('Dashboard HTML anchor not found')
text = text.replace(html_anchor, '</div>' + admin_html + '</section>\n\n<div id="staffDashboard">', 1)

css = r'''

/* Admin management dashboard */
body.staff-role #adminDashboard{display:none!important}
body:not(.staff-role) #dashboardPage>.heading,
body:not(.staff-role) #dashboardPage>.stats,
body:not(.staff-role) #dashboardPage>.dashboard-grid,
body:not(.staff-role) #dashboardPage>.lower-grid,
body:not(.staff-role) #dashboardPage>.quick-grid{display:none!important}
body:not(.staff-role) .content:has(#dashboardPage.active){padding-top:12px}
#adminDashboard{display:grid;gap:12px}
.admin-dash-hero{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:15px 18px;border:1px solid #d9b79f;border-radius:14px;background:linear-gradient(105deg,#fff6ef 0%,#f4dfd2 62%,#ead0bf 100%)}
.admin-dash-hero h1{margin:0;color:#5e2e18;font-size:24px}.admin-dash-hero p{margin:4px 0 0;color:#7b685c;font-size:13px}.admin-dash-hero-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.admin-dash-hero .primary{background:linear-gradient(90deg,#a74416,#713119)}
.admin-dash-cards{display:grid;grid-template-columns:repeat(8,minmax(118px,1fr));gap:9px}
.admin-dash-card{min-height:92px;padding:12px 13px;border:1px solid #dfc0ad;border-radius:12px;background:linear-gradient(145deg,#fff,#fff0e5);overflow:hidden}.admin-dash-card:nth-child(2){background:linear-gradient(145deg,#fff,#f7eadf)}.admin-dash-card:nth-child(4){background:linear-gradient(145deg,#fff,#f4e5db)}.admin-dash-card:nth-child(5){background:linear-gradient(145deg,#fff,#fff2e6)}.admin-dash-card:nth-child(6){background:linear-gradient(145deg,#fff,#fff0d9);border-color:#e5c58f}.admin-dash-card:nth-child(7){background:linear-gradient(145deg,#fff,#f6e4d8)}
.admin-dash-card.warning{background:linear-gradient(145deg,#fff,#fff5df);border-color:#e6c997}.admin-dash-card.warning b{color:#a65b08}.admin-dash-card.urgent{background:linear-gradient(145deg,#fff,#fde8e7);border-color:#e7b5af}.admin-dash-card.urgent b{color:#c42c29}
.admin-dash-card span{display:block;color:#6e574a;font-size:11px;font-weight:750}.admin-dash-card b{display:block;margin-top:4px;color:#8b3b18;font-size:25px;line-height:1}.admin-dash-card small{display:block;margin-top:6px;color:#8b776b;font-size:10px}
.admin-dash-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:12px}.admin-dash-lower{grid-template-columns:minmax(0,1.35fr) minmax(310px,.65fr)}
.admin-dash-section{margin:0;padding:14px;border-color:#ddc0ae}.admin-dash-section h2{margin:0;font-size:17px;color:#5b301d}.admin-dash-section .toolbar p{margin:3px 0 0;color:#846f62;font-size:11px}.admin-dash-section .toolbar>b{color:#8b3b18;font-size:12px}
.admin-attention-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:11px}.admin-attention-box{padding:9px 10px;border:1px solid #ead3c4;border-radius:10px;background:#fffaf6;cursor:pointer}.admin-attention-box b{display:block;color:#8b3b18;font-size:19px}.admin-attention-box span{font-size:10px;color:#79665b}.admin-attention-box.urgent{background:#fff2f1;border-color:#efc5c1}.admin-attention-box.urgent b{color:#bc302c}
.admin-attention-list{display:grid;gap:6px;margin-top:9px}.admin-attention-row{display:grid;grid-template-columns:minmax(0,1fr) 130px auto;gap:9px;align-items:center;padding:8px 10px;border:1px solid #ead3c4;border-radius:9px;background:#fffaf6}.admin-attention-row.overdue{background:#fff3f2;border-color:#efcbc7}.admin-attention-row b{display:block;font-size:12px}.admin-attention-row small{display:block;margin-top:2px;color:#806d61;font-size:10px}.admin-attention-staff{font-size:10px;color:#704229;font-weight:700}.admin-attention-tag{padding:4px 7px;border-radius:20px;background:#fff0df;color:#8a4d11;font-size:10px;font-weight:800;white-space:nowrap}.admin-attention-row.overdue .admin-attention-tag{background:#fde1df;color:#b72d29}
.admin-status-summary{display:grid;gap:8px;margin-top:11px}.admin-status-line{display:grid;grid-template-columns:minmax(110px,1fr) minmax(100px,1.4fr) 58px;align-items:center;gap:8px;font-size:12px}.admin-status-bar{height:8px;border-radius:20px;background:#f0e4dc;overflow:hidden}.admin-status-bar i{display:block;height:100%;border-radius:20px;background:linear-gradient(90deg,#ad4818,#6d321b)}.admin-status-line b{text-align:right;color:#6d3820;font-size:11px}
.admin-team-card{margin-top:0}.admin-team-table{min-width:850px}.admin-team-table th{font-size:11px}.admin-team-table td{padding:8px 9px;font-size:12px}.admin-team-table td:first-child{font-weight:750}.admin-team-table .overdue-count{color:#bd302c;font-weight:800}
.admin-recent-table{min-width:900px}.admin-recent-table th{font-size:11px}.admin-recent-table td{padding:8px 9px;font-size:12px;white-space:normal;vertical-align:top}.admin-recent-table td:nth-child(2){font-weight:700}.admin-recent-table td:nth-child(5){max-width:260px}
.admin-performance-snapshot{display:grid;gap:9px;margin-top:10px}.admin-performance-box{border:1px solid #e1c8b7;border-radius:11px;padding:10px 11px;background:#fffaf6}.admin-performance-box h3{margin:0 0 8px;color:#71371b;font-size:13px}.admin-performance-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}.admin-performance-metrics div{padding:7px 5px;border-radius:8px;background:#fff1e7;text-align:center}.admin-performance-metrics b{display:block;color:#913b17;font-size:17px}.admin-performance-metrics small{font-size:9px;color:#7f6c60}
@media(max-width:1250px){.admin-dash-cards{grid-template-columns:repeat(4,1fr)}}
@media(max-width:900px){.admin-dash-grid,.admin-dash-lower{grid-template-columns:1fr}.admin-dash-cards{grid-template-columns:repeat(2,1fr)}.admin-attention-summary{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.admin-dash-hero{align-items:flex-start;flex-direction:column}.admin-dash-hero-actions{justify-content:flex-start}.admin-dash-cards{grid-template-columns:1fr 1fr}.admin-attention-row{grid-template-columns:1fr auto}.admin-attention-staff{grid-column:1}.admin-performance-metrics{grid-template-columns:repeat(2,1fr)}}
'''
text = text.replace('\n</style>', css + '\n</style>', 1)

old_enter = 'if(!isAdmin())await loadStaffDashboard()}'
new_enter = 'if(!isAdmin())await loadStaffDashboard();else await loadAdminDashboard()}'
if old_enter not in text:
    raise SystemExit('Admin initial dashboard load anchor not found')
text = text.replace(old_enter, new_enter, 1)

old_nav = "if(p==='dashboard'){Promise.allSettled([loadStats(),loadDashboardAnalytics()]);if(!isAdmin())loadStaffDashboard()}"
new_nav = "if(p==='dashboard'){Promise.allSettled([loadStats(),loadDashboardAnalytics()]);if(!isAdmin())loadStaffDashboard();else loadAdminDashboard()}"
if old_nav not in text:
    raise SystemExit('Admin dashboard navigation anchor not found')
text = text.replace(old_nav, new_nav, 1)

js = r'''

function adminDashboardRanges(){
 const parts=Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Kolkata',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date()).filter(x=>x.type!=='literal').map(x=>[x.type,x.value]));
 const y=Number(parts.year),m=Number(parts.month),d=Number(parts.day),pad=n=>String(n).padStart(2,'0');
 const todayStart=new Date(`${y}-${pad(m)}-${pad(d)}T00:00:00+05:30`),todayEnd=new Date(todayStart.getTime()+86400000),civil=new Date(Date.UTC(y,m-1,d)),offset=(civil.getUTCDay()+6)%7,weekStart=new Date(todayStart.getTime()-offset*86400000),monthStart=new Date(`${y}-${pad(m)}-01T00:00:00+05:30`);
 return{todayStart:todayStart.toISOString(),todayEnd:todayEnd.toISOString(),weekStart:weekStart.toISOString(),monthStart:monthStart.toISOString(),rangeStart:new Date(Math.min(weekStart.getTime(),monthStart.getTime())).toISOString()}
}
async function fetchAdminDashboardLogs(start,end){
 let rows=[];
 for(let from=0;;from+=1000){
  const {data,error}=await db.from('crm_call_logs').select('id,institute_id,staff_id,status,remarks,next_call_at,created_at').gte('created_at',start).lt('created_at',end).order('created_at',{ascending:false}).range(from,from+999);
  if(error)throw error;rows.push(...(data||[]));if(!data||data.length<1000)break
 }
 return rows
}
function adminDashMetricBlock(title,rows){
 const unique=new Set(rows.map(x=>x.institute_id).filter(Boolean)).size,interested=rows.filter(x=>x.status==='Interested').length,done=rows.filter(x=>x.status==='Done').length;
 return `<div class="admin-performance-box"><h3>${esc(title)}</h3><div class="admin-performance-metrics"><div><b>${rows.length}</b><small>Calls</small></div><div><b>${unique}</b><small>Unique</small></div><div><b>${interested}</b><small>Interested</small></div><div><b>${done}</b><small>Done</small></div></div></div>`
}
function adminOpenInstituteMode(mode){
 document.querySelector('[data-page=institutes]')?.click();setTimeout(()=>document.querySelector(`[data-institute-tab="${mode}"]`)?.click(),60)
}
async function loadAdminDashboard(){
 if(!isAdmin()||!S.user)return;
 try{
  const r=adminDashboardRanges();
  const totalQ=db.from('crm_institutes').select('*',{count:'exact',head:true}).is('deleted_at',null),assignedQ=db.from('crm_institutes').select('*',{count:'exact',head:true}).is('deleted_at',null).not('assigned_to','is',null),unassignedQ=db.from('crm_institutes').select('*',{count:'exact',head:true}).is('deleted_at',null).is('assigned_to',null),notCalledQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).is('last_status',null),todayFollowQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).not('next_call_at','is',null).gte('next_call_at',r.todayStart).lt('next_call_at',r.todayEnd),overdueQ=db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).not('next_call_at','is',null).lt('next_call_at',r.todayStart),attentionQ=db.from('crm_institute_call_state').select('id,institute_name,assigned_to,assigned_name,assigned_username,last_status,next_call_at,mobile_no').not('next_call_at','is',null).lt('next_call_at',r.todayEnd).order('next_call_at',{ascending:true}).limit(8),recentQ=db.from('crm_call_logs').select('id,status,remarks,next_call_at,created_at,staff_id,crm_profiles(full_name,username),crm_institutes(institute_name,mobile_no)').order('created_at',{ascending:false}).limit(10);
  const [total,assigned,unassigned,notCalled,todayFollow,overdue,attention,recent,logs]=await Promise.all([totalQ,assignedQ,unassignedQ,notCalledQ,todayFollowQ,overdueQ,attentionQ,recentQ,fetchAdminDashboardLogs(r.rangeStart,r.todayEnd)]);
  const err=[total,assigned,unassigned,notCalled,todayFollow,overdue,attention,recent].find(x=>x?.error)?.error;if(err)throw err;
  const activeStaff=S.staff.filter(x=>x.role==='staff'&&x.active),month=logs.filter(x=>x.created_at>=r.monthStart),week=logs.filter(x=>x.created_at>=r.weekStart),today=logs.filter(x=>x.created_at>=r.todayStart),interested=month.filter(x=>x.status==='Interested').length;
  $('#adTotal').textContent=(total.count||0).toLocaleString();$('#adAssigned').textContent=(assigned.count||0).toLocaleString();$('#adUnassigned').textContent=(unassigned.count||0).toLocaleString();$('#adActiveStaff').textContent=activeStaff.length.toLocaleString();$('#adTodayCalls').textContent=today.length.toLocaleString();$('#adInterested').textContent=interested.toLocaleString();$('#adTodayFollowups').textContent=(todayFollow.count||0).toLocaleString();$('#adOverdue').textContent=(overdue.count||0).toLocaleString();
  $('#adAttentionSummary').innerHTML=`<div class="admin-attention-box warning" onclick="adminOpenInstituteMode('pending')"><b>${(unassigned.count||0).toLocaleString()}</b><span>Unassigned Institutes</span></div><div class="admin-attention-box"><b>${(notCalled.count||0).toLocaleString()}</b><span>Not Called</span></div><div class="admin-attention-box"><b>${(todayFollow.count||0).toLocaleString()}</b><span>Today Follow-ups</span></div><div class="admin-attention-box urgent"><b>${(overdue.count||0).toLocaleString()}</b><span>Overdue Follow-ups</span></div>`;
  const attentionRows=attention.data||[];$('#adAttentionCount').textContent=`${attentionRows.length.toLocaleString()} shown`;$('#adAttentionList').innerHTML=attentionRows.map(x=>{const over=String(x.next_call_at)<r.todayStart,staff=S.staff.find(s=>s.id===x.assigned_to),staffName=staff?.username||staff?.full_name||x.assigned_username||x.assigned_name||'Unassigned';return `<div class="admin-attention-row ${over?'overdue':''}"><div><b>${esc(x.institute_name||'—')}</b><small>${esc(x.last_status||'Follow-up')} · ${phones(x.mobile_no)[0]||'No mobile'}</small></div><span class="admin-attention-staff">${esc(staffName)}</span><span class="admin-attention-tag">${over?'Overdue':'Today'} · ${formatDate(x.next_call_at)}</span></div>`}).join('')||'<p class="empty">No overdue or today follow-ups</p>';
  const counts=statusCounts(month),monthTotal=month.length;$('#adStatusTotal').textContent=`${monthTotal.toLocaleString()} calls`;$('#adStatusSummary').innerHTML=Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(([s,n])=>`<div class="admin-status-line"><span>${esc(s)}</span><div class="admin-status-bar"><i style="width:${monthTotal?Math.max(4,Math.round(n*100/monthTotal)):0}%"></i></div><b>${n} · ${monthTotal?Math.round(n*100/monthTotal):0}%</b></div>`).join('')||'<p class="empty">No calls this month</p>';
  const staffCountRows=await Promise.all(activeStaff.map(async s=>{const [aq,oq]=await Promise.all([db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).eq('assigned_to',s.id),db.from('crm_institute_call_state').select('*',{count:'exact',head:true}).eq('assigned_to',s.id).not('next_call_at','is',null).lt('next_call_at',r.todayStart)]);if(aq.error)throw aq.error;if(oq.error)throw oq.error;const m=month.filter(x=>x.staff_id===s.id),t=today.filter(x=>x.staff_id===s.id);return{name:s.username||s.full_name||s.email||'Staff',assigned:aq.count||0,today:t.length,month:m.length,interested:m.filter(x=>x.status==='Interested').length,done:m.filter(x=>x.status==='Done').length,overdue:oq.count||0}}));
  staffCountRows.sort((a,b)=>b.month-a.month||b.today-a.today||a.name.localeCompare(b.name));$('#adTeamBody').innerHTML=staffCountRows.map(x=>`<tr><td>${esc(x.name)}</td><td>${x.assigned.toLocaleString()}</td><td>${x.today.toLocaleString()}</td><td>${x.month.toLocaleString()}</td><td>${x.interested.toLocaleString()}</td><td>${x.done.toLocaleString()}</td><td class="${x.overdue?'overdue-count':''}">${x.overdue.toLocaleString()}</td></tr>`).join('')||'<tr><td colspan="7" class="empty">No active staff</td></tr>';
  $('#adRecentBody').innerHTML=(recent.data||[]).map(x=>{const profile=x.crm_profiles||{},ins=x.crm_institutes||{},staffName=profile.username||profile.full_name||S.staff.find(s=>s.id===x.staff_id)?.username||'Staff';return `<tr><td>${esc(staffName)}</td><td>${esc(ins.institute_name||'—')}</td><td>${formatCallDateTime(x.created_at)}</td><td><span class="history-status-pill">${esc(x.status||'—')}</span></td><td>${esc(x.remarks||'No remarks')}</td><td>${x.next_call_at?formatDate(x.next_call_at):'—'}</td></tr>`}).join('')||'<tr><td colspan="6" class="empty">No recent calls</td></tr>';
  $('#adPerformance').innerHTML=adminDashMetricBlock('Today',today)+adminDashMetricBlock('This Week',week)+adminDashMetricBlock('This Month',month)
 }catch(e){console.error(e);toast('Admin dashboard load nahi hua: '+(e.message||e))}
}
'''
text = text.replace('\n</script></body></html>', js + '\n</script></body></html>', 1)
p.write_text(text, encoding='utf-8')
