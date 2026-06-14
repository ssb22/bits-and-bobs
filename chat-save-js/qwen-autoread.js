// chat.qwen.ai auto-play the TTS in browser
// (c) Silas S. Brown 2026, License: Apache 2
// (I did say "public domain no warranty" but apparently
// some corporate offices don't trust that.  Apache 2 lets
// them know I don't have a silly patent up my sleeve that
// I'd try to enforce, so their policy might accept it more
// easily if you need to use this at work.)
// This script interacts with services owned by their
// respective operators; no affiliation is implied.

// Paste this into the Console window
// Tested in Firefox 147-149 on Ubuntu GNU/Linux 24.04 & 26.04

function watchContainer(container) {
    const doneAttr = 'data-auto-tts-processed';
    if (container.hasAttribute(doneAttr)) return;
    let triesLeft=300; // half-seconds (could be high if "Thinking" and server loaded)
    const check=setInterval(()=>{
        if(container.children.length==6) {
            clearInterval(check);
            container.setAttribute(doneAttr, 't');
            container.lastElementChild.click();
            setTimeout(()=>{document.querySelector('.qwen-chat-package-comp-new-action-more-operation-text').click()},1000);
        } else if(!triesLeft--)clearInterval(check)
    }, 500)}

new MutationObserver((mutations) => {
    const ctrlIconsClass = 'qwen-chat-package-comp-new-action-control-icons';
    mutations.forEach((mutation)=>{
        mutation.addedNodes.forEach((node)=>{
            if (node.nodeType===1) {
                if(node.classList && node.classList.contains(ctrlIconsClass)) watchContainer(node);
                node.querySelectorAll(`.${ctrlIconsClass}`).forEach(watchContainer);
}})})}).observe(document.body,{childList:true,subtree:true});
