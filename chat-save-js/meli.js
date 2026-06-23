// Javascript to paste into browser developer console (F12)
// to help save a session of app.meli.im
// (c) Silas S. Brown 2026, License: Apache 2
// (I did say "public domain no warranty" on these scripts
// but apparently some corporate offices don't trust that.
// Apache 2 lets them know I don't have a silly patent up my
// sleeve that I'd try to enforce, so their policy might
// accept it more easily if you need to use this at work.)
// This script interacts with services owned by their
// respective operators; no affiliation is implied.

// Note: will NOT save the whole conversation for large ones.
// If you scroll back, it will likely save where you are + the end.
// You might therefore need to assemble it from several pieces.

(function() { let spans=document.getElementsByTagName("span"),lines=[],P=((s,n)=>{for(let j=0;j<n&&s;j++)s=s.parentNode;return s}),i=0; while(i<spans.length){let text=spans[i].textContent.trim(),p=P(spans[i],9),t=P(spans[i],4)?.nextSibling?.firstChild?.textContent?.trim(),j=i;while(1){let oi=i;if(spans[i].firstChild?.nodeName=="SPAN")i++;while(spans[j].nextSibling?.nodeName=="SPAN"){text+=" "+spans[j=++i].textContent.trim();if(spans[i].firstChild?.nodeName=="SPAN")i++}while(P(spans[j],2).nextSibling?.firstChild?.firstChild?.nodeName=="SPAN" || P(spans[j],2).nextSibling?.firstChild?.firstChild?.nextSibling?.firstChild?.firstChild?.nodeName=="SPAN" || P(spans[j],3).nextSibling?.firstChild?.nextSibling?.firstChild?.firstChild?.nodeName=="SPAN" || P(spans[j],4).nextSibling?.firstChild?.firstChild?.nodeName=="SPAN" || spans[j].parentNode.nextSibling?.nextSibling?.firstChild?.firstChild?.nodeName=="SPAN" || P(spans[j],2).nextSibling && !P(spans[j],2).nextSibling.hasChildNodes() && P(spans[j],2).nextSibling.nextSibling?.firstChild?.firstChild?.nodeName=="SPAN") {text+="\n"+spans[j=++i].textContent.trim();if(spans[i].firstChild?.nodeName=="SPAN")i++}if(oi==i)break}if(text&&p?.style) lines.push(`${p.style["align-items"]=="flex-end"?"User":"Meli"} (${t}): ${text}`);i++}lines.reverse(); return lines.join("\n\n")})(); /* app.meli.im save */
