from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* Staff University Detail new-tab behavior */'
if marker in text:
    raise SystemExit('already applied')

patch = r'''

/* Staff University Detail new-tab behavior */
(function(){
  const universityNav=document.querySelector('[data-page="universitydetail"]');
  if(!universityNav)return;
  const originalUniversityClick=universityNav.onclick;
  const isDedicatedUniversityTab=()=>new URLSearchParams(window.location.search).get('view')==='universitydetail';

  universityNav.onclick=function(e){
    if(S.profile && !isAdmin() && !isDedicatedUniversityTab()){
      if(e?.preventDefault)e.preventDefault();
      const url=new URL(window.location.href);
      url.searchParams.set('view','universitydetail');
      url.hash='';
      window.open(url.toString(),'_blank','noopener');
      return;
    }
    if(typeof originalUniversityClick==='function')return originalUniversityClick.call(this,e);
  };

  if(isDedicatedUniversityTab()){
    let attempts=0;
    const openUniversityPage=()=>{
      attempts++;
      if(S.profile && !isAdmin()){
        universityNav.click();
        return true;
      }
      return attempts>80;
    };
    if(!openUniversityPage()){
      const timer=setInterval(()=>{if(openUniversityPage())clearInterval(timer)},100);
    }
  }
})();
'''

needle = '\n</script></body></html>'
if needle not in text:
    raise SystemExit('script closing target not found')
text = text.replace(needle, patch + needle, 1)
p.write_text(text, encoding='utf-8')
