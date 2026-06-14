// c.ai LLM history saver
// (c) Silas S. Brown 2024, License: Apache 2
// (I did say "public domain no warranty" but apparently
// some corporate offices don't trust that.  Apache 2 lets
// them know I don't have a silly patent up my sleeve that
// I'd try to enforce, so their policy might accept it more
// easily if you need to use this at work.)
// This script interacts with services owned by their
// respective operators; no affiliation is implied.

// Ensure you've scrolled back enough to populate whole history.
// By default 50 messages are shown when you load the character.
// As of 2025, the URL, which can be shared with other logged-in
// users, is the URL of the character, NOT of your specific chat
// which cannot be shared by URL.  However, if you yourself load
// a character, it will show your last 50 messages with them and
// can show more if you scroll back.

// If your chosen character is taken down, all conversation history
// is cleared and you'll no longer be able to access it, so frequent
// backups might be a good idea if you mentioned any idea you want
// to keep.  No timestamps are available.

// Paste this line into DOM Inspector Console + copy the result.

// To backup further conversation with the same character, you
// might not need to scroll all the way back to the beginning:
// simply search for the known last thing said in the new markup
// and if it's there you should then be able to copy starting
// from after this point.

// Tested in:
// Chrome 131 on GNU/Linux (replace "\n" with newline after copy-paste)
// Firefox 133-139 on GNU/Linux (right-click Copy Message: newlines intact)
// (in both cases ` needs to be removed before and after)
r=[];for(c=document.getElementById("chat-messages").firstChild;c;c=c.nextSibling) r.push('"""{'+c.getElementsByTagName("img")[0].alt+"} "+c.getElementsByClassName("prose")[0].innerHTML.replace(/<(p|ol|ul)[^>]*>/g,'<$1>').replace(/<p>([^<]*)<[/]p>$/,'$1').replace('"""',"'''").replace(/"$/,'"\n').replace(/[\\]/g,'&#92;')+'"""'); r.reverse(); r.join(',\n') /* character.ai save */
