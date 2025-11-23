// Claude LLM history saver - SSB 2025, public domain, no warranty

((d)=>{var r=[],i;for(i=0;i<d.length;i++)r.push(((d[i].getAttribute("class").search("claude-response")>-1)?"Claude: ":"User: ")+d[i].innerText);return r.join('\n\n')})(document.querySelectorAll('[data-testid="user-message"], div.font-claude-response')) /* claude-save */
