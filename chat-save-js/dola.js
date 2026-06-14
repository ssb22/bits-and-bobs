// Javascript to paste into browser developer console
// to help save a session of dola.com/chat
// (c) Silas S. Brown 2025-26, License: Apache 2
// (I did say "public domain no warranty" but apparently
// some corporate offices don't trust that.  Apache 2 lets
// them know I don't have a silly patent up my sleeve that
// I'd try to enforce, so their policy might accept it more
// easily if you need to use this at work.)
// This script interacts with services owned by their
// respective operators; no affiliation is implied.

// Scroll all the way back to the start first.
// Paste this line into DOM Inspector Console + copy the result.

((d)=>{var r=[],i,t;for(i=0;i<d.length;i++){t=d[i].getAttribute("data-testid");if(t=="send_message"||t=="receive_message"){r.push((t=="send_message"?"User: ":"Dola: ")+d[i].textContent.replace(/\n/g,'\n\n'))}}return r.join('\n\n')})(document.getElementsByTagName("div")) /* dola-save */
