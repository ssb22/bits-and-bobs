// Javascript to paste into browser developer console
// to help save a session of chat.qwen.ai

// Silas S. Brown 2025-2026 - public domain - no warranty

// Ensure you've scrolled back enough to populate whole history.
// Paste this line into DOM Inspector Console + copy the result.
// Tested in Firefox 144-147 on GNU/Linux

((d)=>{var r=[],i;for(i=0;i<d.length;i++)r.push(((d[i].getAttribute("class").search("user-message")>-1)?"User: ":"Qwen: ")+d[i].innerText);return r.join('\n\n')})(document.querySelectorAll('.chat-user-message-wrapper, .response-message-content')) /* qwen-save */
