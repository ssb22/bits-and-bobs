// c.ai LLM history saver - SSB 2024
// Ensure you've scrolled back enough to populate whole history.
// Paste this line into DOM Inspector Console and copy the result.
// Tested in Chrome 131 on GNU/Linux.
r=[];for(c=document.getElementById("chat-messages").firstChild;c;c=c.nextSibling) r.push('"""{'+c.getElementsByTagName("img")[0].alt+"} "+c.getElementsByClassName("prose")[0].innerHTML.replace(/<(p|ol|ul)[^>]*>/g,'<$1>').replace(/<p>([^<]*)<[/]p>$/,'$1').replace('"""',"'''").replace(/"$/,'"\n').replace(/[\\]/g,'&#92;')+'"""'); r.reverse(); r.join(',\n')
