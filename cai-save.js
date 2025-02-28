// c.ai LLM history saver - SSB 2024, public domain, no warranty

// Ensure you've scrolled back enough to populate whole history.
// By default 50 messages are shown when you load the character.
// As of 2025, the URL, which can be shared with other logged-in
// users, is the URL of the character, NOT of your specific chat
// which cannot be shared by URL.  However, if you yourself load
// a character, it will show your last 50 messages with them and
// can show more if you scroll back.

// Paste this line into DOM Inspector Console + copy the result.

// To backup further conversation with the same character, you
// might not need to scroll all the way back to the beginning:
// simply search for the known last thing said in the new markup
// and if it's there you should then be able to copy starting
// from after this point.

// Tested in:
// Chrome 131 on GNU/Linux (replace "\n" with newline after copy-paste)
// Firefox 133-135 on GNU/Linux (right-click Copy Message: newlines intact)
// (in both cases ` needs to be removed before and after)
r=[];for(c=document.getElementById("chat-messages").firstChild;c;c=c.nextSibling) r.push('"""{'+c.getElementsByTagName("img")[0].alt+"} "+c.getElementsByClassName("prose")[0].innerHTML.replace(/<(p|ol|ul)[^>]*>/g,'<$1>').replace(/<p>([^<]*)<[/]p>$/,'$1').replace('"""',"'''").replace(/"$/,'"\n').replace(/[\\]/g,'&#92;')+'"""'); r.reverse(); r.join(',\n')
