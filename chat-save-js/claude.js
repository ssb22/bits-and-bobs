// Claude LLM history saver
// (c) Silas S. Brown 2025-26, License: Apache 2
// (I did say "public domain no warranty" but apparently
// some corporate offices don't trust that.  Apache 2 lets
// them know I don't have a silly patent up my sleeve that
// I'd try to enforce, so their policy might accept it more
// easily if you need to use this at work.)
// This script interacts with services owned by their
// respective operators; no affiliation is implied.

((d)=>{var r=[],i;for(i=0;i<d.length;i++)r.push(((d[i].getAttribute("class").search("claude-response")>-1)?"Claude: ":"User: ")+d[i].textContent.replace(/\n/g,'\n\n'));return r.join('\n\n')})(document.querySelectorAll('[data-testid="user-message"], div.font-claude-response')) /* claude-save */
