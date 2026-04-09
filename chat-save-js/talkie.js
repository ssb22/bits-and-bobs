// Javascript to paste into browser developer console
// to help save a session of talkie-ai.com (Minimax)

// Silas S. Brown 2026 - public domain - no warranty

// Ensure you've scrolled back enough to populate history
// (you may not get all of it; ~650 messages max = ~325 responses)
// Paste this line into DOM Inspector Console + copy the result.
// Tested in Firefox 149 on GNU/Linux

(function() { msg=document.getElementsByClassName("__pc-message__");L=[]; ai="AI";a=msg[0].querySelector('img[alt*="chat with ai character"]');if(a){a=a.alt.match(/chat with ai character:\s*(.+)/i);if(a)ai=a[1].trim()} for(i=msg.length-1;i >= 0;i--) {c=msg[i].querySelector('[class*="Message_message__"]');e=msg[i].querySelector('[class*="Message_text___"]');if(c&&e){t=document.createElement('div');t.innerHTML=e.innerHTML.replace(/<span[^>]*Message_em__[^>]*>([^<]*)<\/span>/g,'*$1*');t=(t.textContent||t.innerText||'').replace(/\s+/g,' ').trim();if(t)L.push((c.className.includes('user')?'User':ai)+": "+t)}} return L.join('\n\n')})(); /* talkie.ai-save */
