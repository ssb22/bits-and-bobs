// chat.qwen.ai auto-play the TTS in browser
// Silas S. Brown 2026 - public domain - no warranty

// Paste this into the Console window
// Tested in Firefox 147 on Ubuntu GNU/Linux 24.04

function watchContainer(container) {
    const doneAttr = 'data-auto-tts-processed';
    if (container.hasAttribute(doneAttr)) return;
    let triesLeft=50;
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
