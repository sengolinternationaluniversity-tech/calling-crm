from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
marker='/* Clickable Admin top badge */'
if marker in text:
    raise SystemExit(0)
css='''\n\n/* Clickable Admin top badge */\nbody:not(.staff-role) #roleBadge{cursor:pointer;user-select:none;transition:background .15s ease,border-color .15s ease}\nbody:not(.staff-role) #roleBadge:hover{background:#dfeaff;border-color:#a9c5ea}\nbody:not(.staff-role) #roleBadge:focus-visible{outline:2px solid #2563eb;outline-offset:2px}\n'''
text=text.replace('</style>',css+'\n</style>',1)
needle="const topMasterBtn=$('#topMasterBtn');if(topMasterBtn)topMasterBtn.onclick=()=>{$$('.page').forEach(x=>x.classList.remove('active'));$('#masterPage').classList.add('active');$$('[data-page]').forEach(x=>x.classList.remove('active'));const context=$('#topContextTitle'),topTabs=$('#topInstituteTabs');if(context)context.classList.add('hidden');if(topTabs)topTabs.classList.add('hidden')};"
insert=needle+"\nconst topAdminBadge=$('#roleBadge');if(topAdminBadge){topAdminBadge.setAttribute('tabindex','0');topAdminBadge.setAttribute('role','button');topAdminBadge.onclick=()=>{if(!isAdmin())return;document.querySelector('[data-page=\\\"dashboard\\\"]')?.click()};topAdminBadge.onkeydown=e=>{if(!isAdmin())return;if(e.key==='Enter'||e.key===' '){e.preventDefault();document.querySelector('[data-page=\\\"dashboard\\\"]')?.click()}};}"
if needle not in text:
    raise SystemExit('top master handler not found')
text=text.replace(needle,insert,1)
p.write_text(text,encoding='utf-8')
