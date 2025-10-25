// Javascript to paste into browser developer console
// to help save a session of chat.qwen.ai
// Silas S. Brown 2025 - public domain - no warranty

((d)=>{var r=[],i;for(i=0;i<d.length;i++)r.push(((d[i].getAttribute("class").search("user-message")>-1)?"User: ":"Qwen: ")+d[i].innerText);return r.join('\n\n')})(document.querySelectorAll('.user-message-text-content, .response-message-body')) /* qwen-save */
