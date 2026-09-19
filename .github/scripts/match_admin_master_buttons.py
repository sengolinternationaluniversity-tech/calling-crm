from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Match Admin and Master top buttons */'
if marker in text:
    raise SystemExit(0)
css = r'''

/* Match Admin and Master top buttons */
body:not(.staff-role) .top .role,
body:not(.staff-role) .top .top-master-btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-height:30px;
  padding:5px 10px;
  border:1px solid #cbdcf3;
  border-radius:20px;
  background:#eaf2ff;
  color:#2457a6;
  font-size:12px;
  font-weight:700;
  line-height:1;
  box-shadow:none;
}
body:not(.staff-role) .top .top-master-btn{
  margin-left:7px;
  cursor:pointer;
}
body:not(.staff-role) .top .top-master-btn:hover{
  background:#dfeaff;
  color:#1f4f97;
  border-color:#b8cfea;
}
'''
text = text.replace('</style>', css + '\n</style>', 1)
p.write_text(text, encoding='utf-8')
