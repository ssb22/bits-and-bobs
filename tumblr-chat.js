// save Tumblr private chat - SSB 2025, public domain, no warranty

// Ensure you've scrolled back enough to populate whole history.
// Paste this line into DOM Inspector Console + copy the result.
// Tested in Firefox 139-140 on GNU/Linux

((e)=>{return e.nextSibling?e.nextSibling:e.firstChild.nextSibling})(document.getElementById('adBanner').nextSibling.nextSibling.firstChild.firstChild.firstChild.firstChild.nextSibling.firstChild.firstChild.nextSibling.firstChild).innerHTML.replace(/<[/]div><[/]div>/g,"</div></div>\n").replace(/<div class="_fx8y"><[/]div>/g,"") /* tumblr-chat save */
