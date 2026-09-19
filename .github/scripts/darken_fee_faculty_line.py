from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
old='.fee-department-head{border-bottom:2px solid #9fb7d0!important}'
new='.fee-department-head{border-bottom:2px solid #6f91b3!important}'
if old not in text:
    raise SystemExit('faculty separator target not found')
text=text.replace(old,new,1)
p.write_text(text,encoding='utf-8')
