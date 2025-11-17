// Javascript to paste into browser developer console
// to help save a session of dola.com/chat
// Silas S. Brown 2025 - public domain - no warranty

// Scroll all the way back to the start first.
// Paste this line into DOM Inspector Console + copy the result.

((d)=>{var r=[],i,t;for(i=0;i<d.length;i++){t=d[i].getAttribute("data-testid");if(t=="send_message"||t=="receive_message"){r.push((t=="send_message"?"User: ":"Dola: ")+d[i].innerText)}}return r.join('\n\n')})(document.getElementsByTagName("div")) /* dola-save */
