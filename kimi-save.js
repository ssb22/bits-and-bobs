// Javascript to paste into browser developer console
// to help save a session of kimi.com/chat
// (scroll all the way back to the start before using this)
// Silas S. Brown 2025 - public domain - no warranty

// Note: Kimi now have their OWN function to copy a whole chat
// (Share icon / Copy text, works even if the session is too large for Copy link)
// - theirs uses Markdown rather than HTML, but
// (as of 2025-10) theirs does not add a blank line
// between user input and Kimi response (you can
// still search/replace "\nKimi: " -> "\n\nKimi: ")

((divs)=>{var r=[],i;for(i=0; i<divs.length; i++) { var cl=divs[i].classList,u=cl.contains("user-content"),m=cl.contains("markdown"); if(u||m)r.push((u?"User":"Kimi")+": "+divs[i].innerHTML.replace(/<\/div><div class="paragraph">/g,'<p>').replace(/<div class="paragraph">/g,'').replace(/<\/(div|li)>/g,'').replace(/l start="1">/g,"l>").replace(/ *<!--ClickLog Start-->.*?<!--ClickLog End-->/g,'').replace(/ class=""/g,'').replace(/<svg.*<\/svg>/g,'').replace(/ data-[^ ="]+="[^"]*"/g,'').replace(/<br>/g,'\n'))}return r.join('\n\n')})(document.getElementsByTagName("div")) /* kimi-save */
