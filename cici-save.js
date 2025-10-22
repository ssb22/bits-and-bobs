// Javascript to paste into browser developer console
// to help save a session of cici.com/chat
// (scroll all the way back to the start before using this)
// Silas S. Brown 2025 - public domain - no warranty

((d)=>{var r=[],i,t;for(i=0;i<d.length;i++){t=d[i].getAttribute("data-testid");if(t=="send_message"||t=="receive_message"){r.push((t=="send_message"?"User: ":"Cici: ")+d[i].innerText)}}return r.join('\n\n')})(document.getElementsByTagName("div")) /* cici-save */
