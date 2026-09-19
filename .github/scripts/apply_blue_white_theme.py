from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Blue White theme override */'
if marker in text:
    raise SystemExit(0)
css = r'''

/* Blue White theme override */
:root{
  --navy:#163a63;
  --blue:#2563eb;
  --green:#1f9d63;
  --red:#dc4c4c;
  --bg:#f5f9ff;
  --line:#d7e3f2;
  --ink:#17324d;
  --muted:#6b7f95;
}
body{background:#f5f9ff;color:#17324d}
.login{background:linear-gradient(135deg,#eaf3ff 0%,#cfe2ff 52%,#9fc5ff 100%)}
.login-card{background:#fff;border:1px solid #d5e3f3;box-shadow:0 22px 55px #3569a72b}
.login-card h1{color:#184f91}.login-card p{color:#6b7f95}.login-card .field input{background:#fff;border-color:#c9d9ea;color:#17324d}.login-card .primary{background:#2563eb;color:#fff}

.side{background:linear-gradient(180deg,#ffffff 0%,#eef5ff 100%);color:#234765;border:1px solid #cadcf0;box-shadow:0 8px 28px #2f65a51c}
.brand{color:#184f91;border-bottom-color:#dce8f6}.brand:before{background:#2563eb;color:#fff}.brand small{color:#71869d}
.nav button{color:#4f6780;background:transparent}.nav button.active,.nav button:hover{background:linear-gradient(90deg,#2f6feb,#1f5ed3);color:#fff;border-color:#2563eb}
.userbox{background:#f3f8ff;color:#234765;border-color:#d2e1f1}.userbox small{color:#70869d}.userbox .btn{background:#fff;border-color:#c9d9ea;color:#31516d}

.top{background:linear-gradient(90deg,#ffffff 0%,#f4f8ff 58%,#e7f1ff 100%);border-bottom:1px solid #d4e1ef;color:#234765;box-shadow:0 2px 12px #3569a712}
.top input{background:#fff;border:1px solid #c8d8e9;color:#17324d}.sidebar-toggle{background:#f4f8ff;color:#2563eb;border-color:#cadbec}
.role{background:#eaf2ff;color:#2457a6;border-color:#cbdcf3}.top-master-btn{background:#2563eb;border-color:#2563eb;color:#fff}.top-master-btn:hover{background:#1e55cf}
.top-context-title{background:#eaf2ff;color:#2457a6}.top-summary-toggle{background:#dce9fb;color:#2457a6}
.top-institute-tabs .institute-tabs{background:#edf4ff;border-color:#d3e1f2}.top-institute-tabs .institute-tab{color:#56708a}.top-institute-tabs .institute-tab.active{background:#2563eb;color:#fff}

.heading h1{color:#173f6c}.heading p{color:#6b7f95}
.card,.stat,.master-mini,.quick,.management-tools,.modal{background:#fff;border-color:#d6e2ef;box-shadow:none}
.primary{background:#2563eb;color:#fff}.secondary{background:#f3f7fc;color:#31516d;border:1px solid #d4e1ee}.danger{background:#fff0f0;color:#b23b3b}.red{background:#dc4c4c;color:#fff}.green{background:#1f9d63;color:#fff}
.filters input,.filters select,.field input,.field select,.office-add input,.call-toolbar select,textarea{background:#fff;border-color:#cbd9e8;color:#17324d}

.institute-tab.active,.call-page-tab.active{color:#2563eb;border-bottom-color:#2563eb}.follow-tabs button.active,.staff-report-quick .btn.active{background:#2563eb!important;color:#fff!important;border-color:#2563eb!important}
.master-banner,.assign-panel{background:#eef5ff;border-color:#cfe0f3}.master-mini{background:#fff}
.phone-chip{background:#edf5ff;color:#2457a6;border-color:#cfe0f3}.status-active{background:#edf9f2;color:#1f8b59}

.stat:nth-child(1){background:linear-gradient(135deg,#fff,#edf5ff)}
.stat:nth-child(2){background:linear-gradient(135deg,#fff,#f2f7ff)}
.stat:nth-child(3){background:linear-gradient(135deg,#fff,#eef6ff)}
.stat:nth-child(4){background:linear-gradient(135deg,#fff,#fff1f1)}
.stat:nth-child(1):before{background:#dbeaff;color:#2563eb}.stat:nth-child(2):before{background:#e4eefc;color:#3467b7}.stat:nth-child(3):before{background:#dfeeff;color:#2f6feb}.stat:nth-child(4):before{background:#fde1e1;color:#c94343}

.institute-data-table th,.report-history-table th,.call-history-table th,table th,.sr-table th{background:#edf4ff;color:#2457a6;border-color:#cbdbea}
.institute-data-table td,.call-history-table td,.report-history-table td,table td{border-color:#dfe8f2}
.institute-data-table tbody tr:nth-child(even) td{background:#f9fbff}.institute-data-table tbody tr:hover td{background:#eef5ff}
.table-wrap,.institute-grid-wrap{border-color:#ccdbe9}
.call-record,.report-history{border-color:#d4e0ed}.call-meta div{background:#f9fbff;border-color:#dbe5ef}.call-name-input{border-color:#cbd9e8}
.history-status-pill,.call-attempt,.followup-time{background:#eaf2ff;color:#2457a6}.history-status-pill.done{background:#edf9f2;color:#1f8b59}.history-status-pill.follow-up{background:#fff8dd;color:#866319}.followup-time.due{background:#fff0f0;color:#b93d3d}

/* Staff report blue-white */
body.staff-role #reportsPage>.report-filters{background:linear-gradient(135deg,#ffffff,#edf5ff);border-color:#d0dfee}
#staffReportDashboard .sr-card{background:linear-gradient(135deg,#fff,#f2f7ff)!important;border-color:#d4e1ef!important;box-shadow:0 4px 12px #3569a70d}
#staffReportDashboard .sr-card:nth-child(2n){background:linear-gradient(135deg,#fff,#eaf3ff)!important}
#staffReportDashboard .sr-card b{color:#2d63ad!important}
#staffReportDashboard .sr-card.alert{background:linear-gradient(135deg,#fff,#fff0f0)!important;border-color:#efc7c7!important}
#staffReportDashboard .sr-card.alert b{color:#bd3f3f!important}
#staffReportDashboard .sr-card.good{background:linear-gradient(135deg,#fff,#eef9f3)!important;border-color:#cbe6d6!important}
#staffReportDashboard .sr-card.good b{color:#1f8b59!important}
#staffReportDashboard .card:has(#srStatusBody),#staffReportDashboard .card:has(#srStageList),#staffReportDashboard .card:has(#srAttentionBody),#staffReportDashboard .card:has(#srInstituteBody){background:#fff!important;border-color:#d6e3f0!important}
.staff-report-section-title{color:#234f7b}.staff-report-section-title>span{background:#edf5ff!important;border-color:#d3e2f2!important}.sr-stage-fill{background:#2563eb}.sr-stage-track{background:#e5eef8}

/* Staff dashboard blue-white */
.staff-dash-hero{background:linear-gradient(105deg,#fff 0%,#edf5ff 65%,#dceaff 100%);border-color:#d2e1f0}.staff-dash-hero h1{color:#173f6c}.staff-dash-hero p{color:#6b7f95}.staff-dash-hero .btn{background:#2563eb}
.staff-dash-card{background:linear-gradient(145deg,#fff,#f2f7ff)!important;border-color:#d5e2ef!important}.staff-dash-card:nth-child(2n){background:linear-gradient(145deg,#fff,#eaf3ff)!important}
.staff-dash-card b{color:#2d63ad}.staff-dash-card span{color:#526b83}.staff-dash-card small{color:#7b8ea2}
.staff-dash-card.urgent{background:linear-gradient(145deg,#fff,#fff0f0)!important;border-color:#efc7c7!important}.staff-dash-card.urgent b{color:#bd3f3f}
.staff-dash-section{background:#fff;border-color:#d6e3f0}.staff-dash-section h2{color:#234f7b}.staff-attention-row{background:#f9fbff;border-color:#dbe6f1}.staff-attention-row.overdue{background:#fff4f4;border-color:#efcaca}.staff-attention-tag{background:#eaf2ff;color:#2457a6}.staff-notcalled-note{background:#edf5ff;color:#315a80}.staff-status-bar{background:#e5eef8}.staff-status-bar i{background:linear-gradient(90deg,#5f91f1,#2563eb)}
.staff-performance-box{background:#f9fbff;border-color:#d8e4ef}.staff-performance-metrics div{background:#edf5ff}.staff-performance-metrics b{color:#2d63ad}

/* Admin dashboard blue-white */
#adminDashboard{background:transparent}.admin-dash-hero{background:linear-gradient(105deg,#fff 0%,#edf5ff 65%,#dceaff 100%);border-color:#d2e1f0}.admin-dash-hero h1{color:#173f6c}.admin-dash-hero p{color:#6b7f95}.admin-dash-hero-actions .primary{background:#2563eb}
.admin-dash-card{background:linear-gradient(145deg,#fff,#f2f7ff)!important;border-color:#d5e2ef!important}.admin-dash-card:nth-child(2n){background:linear-gradient(145deg,#fff,#eaf3ff)!important}
.admin-dash-card b{color:#2d63ad}.admin-dash-card span{color:#526b83}.admin-dash-card small{color:#7b8ea2}
.admin-dash-card.warning{background:linear-gradient(145deg,#fff,#fff8e5)!important;border-color:#eadca9!important}.admin-dash-card.warning b{color:#8e6917}
.admin-dash-card.urgent{background:linear-gradient(145deg,#fff,#fff0f0)!important;border-color:#efc7c7!important}.admin-dash-card.urgent b{color:#bd3f3f}
.admin-dash-section{background:#fff;border-color:#d6e3f0}.admin-dash-section h2{color:#234f7b}.admin-attention-box{background:#f9fbff;border-color:#dbe6f1}.admin-attention-box b{color:#2d63ad}.admin-attention-box.urgent{background:#fff3f3;border-color:#efc8c8}.admin-attention-box.urgent b{color:#bd3f3f}
.admin-attention-row{background:#f9fbff;border-color:#dbe6f1}.admin-attention-row.overdue{background:#fff4f4;border-color:#efcaca}.admin-attention-tag{background:#eaf2ff;color:#2457a6}.admin-status-bar{background:#e5eef8}.admin-status-bar i{background:linear-gradient(90deg,#5f91f1,#2563eb)}
.admin-performance-box{background:#f9fbff;border-color:#d8e4ef}.admin-performance-metrics div{background:#edf5ff}.admin-performance-metrics b{color:#2d63ad}

/* Keep action states recognizable */
.wa-stack .green,.wa-icon{background:#1f9d63!important;color:#fff!important}.followup-time.due,.staff-attention-row.overdue .staff-attention-tag,.admin-attention-row.overdue .admin-attention-tag{color:#b93d3d}

@media(max-width:680px){.top{background:#f5f9ff}.side{background:#fff}}
'''
text = text.replace('</style>', css + '\n</style>', 1)
p.write_text(text, encoding='utf-8')
