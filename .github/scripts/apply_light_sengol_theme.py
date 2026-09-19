from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Light Sengol theme override */'
if marker in text:
    raise SystemExit(0)
css = r'''

/* Light Sengol theme override */
:root{
  --navy:#6f3b22;
  --blue:#c9682c;
  --green:#218c5a;
  --red:#d94a45;
  --bg:#fffaf5;
  --line:#ead8ca;
  --ink:#4a3021;
  --muted:#8a7467;
}
body{background:#fffaf5;color:#4a3021}
.login{background:linear-gradient(135deg,#fff1e6 0%,#f6c9a8 52%,#e9a06d 100%)}
.login-card{background:#fffdfb;border:1px solid #eed5c3;box-shadow:0 20px 50px #9f5d3230}
.login-card h1{color:#7b431f}.login-card p{color:#8a7467}
.login-card .field input{background:#fff;border-color:#e4c8b4;color:#4a3021}
.login-card .primary{background:#c9682c;color:#fff}

.side{background:linear-gradient(180deg,#fff8f1 0%,#f8eadf 100%);color:#5a3825;border:1px solid #e7cdbb;box-shadow:0 8px 26px #a56d4630}
.brand{color:#6f3b22;border-bottom-color:#ead5c5}.brand:before{background:#eaa36e;color:#fff}.brand small{color:#987d6b}
.nav button{color:#6f5546;background:transparent}.nav button.active,.nav button:hover{background:#eaa36e;color:#fff;border-color:#dd925c}
.userbox{background:#fff4ea;color:#5a3825;border-color:#e5c9b5}.userbox small{color:#8f7463}.userbox .btn{background:#fff;border-color:#dfc2ad;color:#6a4029}

.top{background:linear-gradient(90deg,#fff7f0 0%,#fbe7d8 58%,#f2c6a5 100%);border-bottom:1px solid #e7cdbb;color:#5a3825;box-shadow:0 2px 12px #a56d4618}
.top input{background:#fff;border:1px solid #e0c2ad;color:#4a3021}.sidebar-toggle{background:#fff;color:#9a562d;border-color:#e1c4b0}
.role{background:#fff1e6;color:#9b552a;border-color:#e6c4aa}.top-master-btn{background:#c9682c;border-color:#c9682c;color:#fff}.top-master-btn:hover{background:#b75b24}
.top-context-title{background:#fff0e4;color:#8a4824}.top-summary-toggle{background:#f5d7c1;color:#8d4b26}
.top-institute-tabs .institute-tabs{background:#f7ddcb;border-color:#e3bea2}.top-institute-tabs .institute-tab{color:#795744}.top-institute-tabs .institute-tab.active{background:#c9682c;color:#fff}

.heading h1{color:#633a24}.heading p{color:#8a7467}
.card,.stat,.master-mini,.quick,.management-tools,.modal{background:#fffdfb;border-color:#ead5c5;box-shadow:none}
.primary{background:#c9682c;color:#fff}.secondary{background:#fff4ea;color:#6b4732;border:1px solid #e5cbb8}.danger{background:#fdeceb;color:#b43b37}.red{background:#d94a45;color:#fff}
.green{background:#218c5a;color:#fff}
.filters input,.filters select,.field input,.field select,.office-add input,.call-toolbar select,textarea{background:#fff;border-color:#e0c7b5;color:#4a3021}

.institute-tab.active,.call-page-tab.active{color:#c9682c;border-bottom-color:#c9682c}.follow-tabs button.active,.staff-report-quick .btn.active{background:#c9682c!important;color:#fff!important;border-color:#c9682c!important}
.master-banner,.assign-panel{background:#fff3e9;border-color:#e7cdb9}.master-mini{background:#fffaf6}
.phone-chip{background:#fff1e7;color:#9b552a;border-color:#e7c8b1}.status-active{background:#eef8f2;color:#218c5a}

.stat:nth-child(1){background:linear-gradient(135deg,#fff,#fff0e6)}
.stat:nth-child(2){background:linear-gradient(135deg,#fff,#fcefe6)}
.stat:nth-child(3){background:linear-gradient(135deg,#fff,#fff6e4)}
.stat:nth-child(4){background:linear-gradient(135deg,#fff,#fff0ef)}
.stat:nth-child(1):before{background:#f8d7bf;color:#b75b24}.stat:nth-child(2):before{background:#f2d8c6;color:#9b552a}.stat:nth-child(3):before{background:#f7e4b8;color:#9a6a16}.stat:nth-child(4):before{background:#f7d4d1;color:#c33d38}

.institute-data-table th,.report-history-table th,.call-history-table th,table th,.sr-table th{background:#fff0e5;color:#9b552a;border-color:#dec7b7}
.institute-data-table td,.call-history-table td,.report-history-table td,table td{border-color:#eaded5}
.institute-data-table tbody tr:nth-child(even) td{background:#fffaf7}.institute-data-table tbody tr:hover td{background:#fff3e9}
.table-wrap,.institute-grid-wrap{border-color:#dec9ba}
.call-record,.report-history{border-color:#e1c9b8}.call-meta div{background:#fffaf6;border-color:#ead9cd}.call-name-input{border-color:#dfc5b2}
.history-status-pill,.call-attempt,.followup-time{background:#fff0e6;color:#9a4e26}.history-status-pill.done{background:#eef8f2;color:#218c5a}.history-status-pill.follow-up{background:#fff6dc;color:#8c6416}.followup-time.due{background:#fdebea;color:#bd3e39}

/* Staff report light cards */
body.staff-role #reportsPage>.report-filters{background:linear-gradient(135deg,#fffaf6,#fff0e5);border-color:#e4cbb8}
#staffReportDashboard .sr-card{background:linear-gradient(135deg,#fff,#fff6ef)!important;border-color:#ead1bd!important;box-shadow:0 4px 12px #b4774d12}
#staffReportDashboard .sr-card:nth-child(2n){background:linear-gradient(135deg,#fff,#fff2e8)!important}
#staffReportDashboard .sr-card b{color:#a85a2d!important}
#staffReportDashboard .sr-card.alert{background:linear-gradient(135deg,#fff,#fff0ef)!important;border-color:#efc4c0!important}
#staffReportDashboard .sr-card.alert b{color:#c13d38!important}
#staffReportDashboard .sr-card.good{background:linear-gradient(135deg,#fff,#eef8f2)!important;border-color:#cbe4d5!important}
#staffReportDashboard .sr-card.good b{color:#218c5a!important}
#staffReportDashboard .card:has(#srStatusBody),#staffReportDashboard .card:has(#srStageList),#staffReportDashboard .card:has(#srAttentionBody),#staffReportDashboard .card:has(#srInstituteBody){background:#fffdfb!important;border-color:#ead2c0!important}
.staff-report-section-title{color:#7a4a2e}.staff-report-section-title>span{background:#fff1e7!important;border-color:#e7cbb6!important}
.sr-stage-fill{background:#c9682c}.sr-stage-track{background:#f4e5da}

/* Staff dashboard light palette */
.staff-dash-hero{background:linear-gradient(105deg,#fffdfb 0%,#fff1e7 65%,#f7d7c1 100%);border-color:#e7cdb9}
.staff-dash-hero h1{color:#6f3b22}.staff-dash-hero p{color:#8a7467}.staff-dash-hero .btn{background:#c9682c}
.staff-dash-card{background:linear-gradient(145deg,#fff,#fff5ed)!important;border-color:#ead1bd!important}.staff-dash-card:nth-child(2n){background:linear-gradient(145deg,#fff,#fff1e7)!important}
.staff-dash-card b{color:#a85a2d}.staff-dash-card span{color:#715848}.staff-dash-card small{color:#927b6d}
.staff-dash-card.urgent{background:linear-gradient(145deg,#fff,#fff0ef)!important;border-color:#edc4c0!important}.staff-dash-card.urgent b{color:#c13d38}
.staff-dash-section{background:#fffdfb;border-color:#ead2c0}.staff-dash-section h2{color:#6b4028}.staff-attention-row{background:#fffaf6;border-color:#ecd8c9}.staff-attention-row.overdue{background:#fff3f2;border-color:#efcbc7}.staff-attention-tag{background:#fff0df;color:#8d5615}
.staff-notcalled-note{background:#fff3e7;color:#74482d}.staff-status-bar{background:#f2e3d8}.staff-status-bar i{background:linear-gradient(90deg,#e9a06d,#c9682c)}
.staff-performance-box{background:#fffaf6;border-color:#ead2c0}.staff-performance-metrics div{background:#fff2e8}.staff-performance-metrics b{color:#a85a2d}

/* Admin dashboard light palette */
#adminDashboard{background:transparent}
.admin-dash-hero{background:linear-gradient(105deg,#fffdfb 0%,#fff1e7 65%,#f7d7c1 100%);border-color:#e7cdb9}
.admin-dash-hero h1{color:#6f3b22}.admin-dash-hero p{color:#8a7467}.admin-dash-hero-actions .primary{background:#c9682c}
.admin-dash-card{background:linear-gradient(145deg,#fff,#fff5ed)!important;border-color:#ead1bd!important}.admin-dash-card:nth-child(2n){background:linear-gradient(145deg,#fff,#fff1e7)!important}
.admin-dash-card b{color:#a85a2d}.admin-dash-card span{color:#715848}.admin-dash-card small{color:#927b6d}
.admin-dash-card.warning{background:linear-gradient(145deg,#fff,#fff7e7)!important;border-color:#ecd7aa!important}.admin-dash-card.warning b{color:#9f6b16}
.admin-dash-card.urgent{background:linear-gradient(145deg,#fff,#fff0ef)!important;border-color:#edc4c0!important}.admin-dash-card.urgent b{color:#c13d38}
.admin-dash-section{background:#fffdfb;border-color:#ead2c0}.admin-dash-section h2{color:#6b4028}
.admin-attention-box{background:#fffaf6;border-color:#ecd8c9}.admin-attention-box b{color:#a85a2d}.admin-attention-box.urgent{background:#fff2f1;border-color:#efc5c1}.admin-attention-box.urgent b{color:#c13d38}
.admin-attention-row{background:#fffaf6;border-color:#ecd8c9}.admin-attention-row.overdue{background:#fff3f2;border-color:#efcbc7}.admin-attention-tag{background:#fff0df;color:#8d5615}
.admin-status-bar{background:#f2e3d8}.admin-status-bar i{background:linear-gradient(90deg,#e9a06d,#c9682c)}
.admin-performance-box{background:#fffaf6;border-color:#ead2c0}.admin-performance-metrics div{background:#fff2e8}.admin-performance-metrics b{color:#a85a2d}

/* Keep WhatsApp recognizable */
.wa-stack .green,.wa-icon{background:#218c5a!important;color:#fff!important}

@media(max-width:680px){.top{background:#fff1e7}.side{background:#fff8f1}}
'''
text = text.replace('</style>', css + '\n</style>', 1)
p.write_text(text, encoding='utf-8')
