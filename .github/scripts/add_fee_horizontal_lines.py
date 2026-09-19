from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
marker='/* Fee table horizontal lines */'
if marker in text:
    raise SystemExit('already applied')
css='''\n\n/* Fee table horizontal lines */\n.fee-data-table thead th{border-bottom:2px solid #9fb7d0!important}\n.fee-data-table tbody td{border-bottom:1px solid #b9cbe0!important}\n.fee-data-table tbody tr:hover td{background:#f8fbff}\n'''
text=text.replace('</style>',css+'\n</style>',1)
p.write_text(text,encoding='utf-8')
