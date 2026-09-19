from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Admin staff horizontal list */'
if marker in text:
    raise SystemExit(0)

css = r'''

/* Admin staff horizontal list */
#staffPage .staff-grid{
  display:grid;
  grid-template-columns:1fr;
  gap:9px;
  width:100%;
}
#staffPage .staff{
  margin:0;
  min-height:68px;
  padding:13px 18px;
  display:flex;
  align-items:center;
  gap:16px;
  border-radius:10px;
  background:#fff;
  border:1px solid #d6e3f0;
  box-shadow:none;
}
#staffPage .staff h3{
  margin:0;
  min-width:240px;
  flex:1 1 45%;
  color:#173f6c;
  font-size:16px;
}
#staffPage .staff p{
  margin:0;
  flex:0 0 110px;
  color:#6b7f95;
  font-size:12px;
}
#staffPage .staff b{
  margin-left:auto;
  color:#2457a6;
  font-size:13px;
}
#staffPage .staff:hover{
  background:#f7faff;
  border-color:#bfd3ea;
}
@media(max-width:680px){
  #staffPage .staff{flex-wrap:wrap;gap:7px 12px}
  #staffPage .staff h3{min-width:100%;flex-basis:100%}
  #staffPage .staff p{flex:1 1 auto}
  #staffPage .staff b{margin-left:0}
}
'''
text = text.replace('</style>', css + '\n</style>', 1)
p.write_text(text, encoding='utf-8')
