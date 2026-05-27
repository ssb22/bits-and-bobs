// Javascript to paste into browser developer console
// to help save a session of chat.qwen.ai

// Silas S. Brown 2025-2026 - public domain - no warranty

// Ensure you've scrolled back enough to populate whole history.
// Paste this line into DOM Inspector Console + copy the result.
// Tested in Firefox 144-151 on GNU/Linux

((d)=>{function M(e){if(!e)return '';if(e.nodeType==3)return e.textContent.replace(/\n+/g,' ');if(e.nodeType!=1)return '';var t=e.tagName,c=e.getAttribute('class')||'',i=Array.from(e.childNodes).map(M).join('');if(c.includes('line-numbers'))return '';if(c.includes('view-line')||c.includes('qwen-markdown-code-header'))return i+'\n';if(c.includes('qwen-markdown-paragraph')||t=='P')return '\n'+i.trim()+'\n\n';if(c.includes('qwen-markdown-space'))return '\n\n';if(t.match(/H[1-6]/)||c.includes('qwen-markdown-heading')){lvl=parseInt((t.match(/H([1-6])/)||"H3")[1]);return '\n'+'#'.repeat(lvl)+' '+i.trim()+'\n\n'}if(t=='UL'||t=='OL'||c.includes('qwen-markdown-list'))return '\n'+i+'\n';if(t=='LI'){p=e.parentElement;return((p.tagName=='OL')?Array.from(p.children).filter(c=>c.tagName=='LI').indexOf(e)+parseInt(p.getAttribute('start')||1)+'. ':'- ')+i.trim()+'\n'}if(t=='BLOCKQUOTE')return '\n> '+i.trim()+'\n\n';if(t=='PRE')return '```'+i+'```\n\n';if(c.includes('qwen-markdown-strong')||t=='STRONG'||t=='B')return '**'+i.trim()+'**';if(t=='EM'||t=='I')return '*'+i.trim()+'*';if(t=='CODE')return '`'+i+'`';if(t=='BR')return '\n';if(t=='A')return '['+i.trim()+']('+(e.getAttribute('href')||'')+')';return i}r=[];for(i=0; i < d.length;i++)r.push(((d[i].getAttribute("class")||"").includes("user-message")?"User: ":"Qwen: ")+M(d[i]).replace(/\n{3,}/g,'\n\n').trim());return r.join('\n\n')})(document.querySelectorAll('.chat-user-message-wrapper, .response-message-content')) /* qwen-save */
