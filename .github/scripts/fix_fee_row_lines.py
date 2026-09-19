from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
old='''/* Fee table horizontal lines */
.fee-department-head{border-bottom:2px solid #9fb7d0!important}
.fee-data-table thead th{border-bottom:2px solid #8ea8c2!important}
.fee-data-table tbody td{border-bottom:1px solid #9fb7d0!important}
.fee-data-table tbody tr:last-child td{border-bottom:1px solid #9fb7d0!important}
.fee-data-table tbody tr:hover td{background:#f8fbff}
'''
new='''/* Fee table horizontal lines */
.fee-department-head{border-bottom:3px solid #7898b8!important}
.fee-data-table{border-collapse:collapse!important}
.fee-data-table thead tr{border-bottom:3px solid #7898b8!important}
.fee-data-table thead th{border-bottom:0!important}
.fee-data-table tbody tr{border-bottom:2px solid #8fa9c3!important}
.fee-data-table tbody td{border-bottom:0!important}
.fee-data-table tbody tr:last-child{border-bottom:2px solid #7898b8!important}
.fee-data-table tbody tr:hover td{background:#f8fbff}
'''
if old not in text:
    raise SystemExit('target fee line block not found')
text=text.replace(old,new,1)
p.write_text(text,encoding='utf-8')
