from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
marker='''/* Staff University Detail tabs match Calling tab height */\nbody.staff-role #universitydetailPage .university-detail-tabs{\n  margin:0 0 8px;\n  padding:2px 4px;\n  gap:5px;\n  min-height:30px;\n  align-items:center;\n  border-radius:8px;\n}\nbody.staff-role #universitydetailPage .university-detail-tab{\n  padding:4px 12px;\n  min-height:26px;\n  font-size:13px;\n  line-height:1.1;\n  border-radius:7px;\n}\n'''
if '/* Staff University Detail tabs match Calling tab height */' not in text:
    text=text.replace('</style>', '\n\n'+marker+'\n</style>', 1)
p.write_text(text,encoding='utf-8')
