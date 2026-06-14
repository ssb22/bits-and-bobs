// save Tumblr private chat
// (c) Silas S. Brown 2025, License: Apache 2
// (I did say "public domain no warranty" but apparently
// some corporate offices don't trust that.  Apache 2 lets
// them know I don't have a silly patent up my sleeve that
// I'd try to enforce, so their policy might accept it more
// easily if you need to use this at work.)
// This script interacts with services owned by their
// respective operators; no affiliation is implied.

// Ensure you've scrolled back enough to populate whole history.
// Paste this line into DOM Inspector Console + copy the result.
// Tested in Firefox 139-140 on GNU/Linux

((e)=>{return e.nextSibling?e.nextSibling:e.firstChild.nextSibling})(document.getElementById('adBanner').nextSibling.nextSibling.firstChild.firstChild.firstChild.firstChild.nextSibling.firstChild.firstChild.nextSibling.firstChild).innerHTML.replace(/<[/]div><[/]div>/g,"</div></div>\n").replace(/<div class="_fx8y"><[/]div>/g,"").replace(/ style="padding-bottom: [^"]*"/g,"") /* tumblr-chat save */
