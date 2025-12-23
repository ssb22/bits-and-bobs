
from https://ssb22.user.srcf.net/law/borrowers.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/law/borrowers.html) just in case)

# The Telegram Borrowers

电报地板下的小矮人

**WARNING:** What I did involves chatting with a criminal organisation. **Do not try this at home.** I helped fix a security flaw in the Linux kernel and I know some of the best security engineers in the world. If you’re not at that level, *do not attempt*.

**警告:** 这个小调查包括与犯罪组织人员聊天。 **劝大家别自己这样做。** 我以前帮了Linux核心开发者找和修个安全漏洞，也认识世界最高保安工程师的一些。如果你没有那样水平， **并不尝试我所做的。**

In August 2023 two of my Chinese friends whom I’d introduced to Telegram Messenger had their accounts temporarily compromised by an organised social-engineering attack. I don’t know if this crime gang has a name, so with a nod to Mary Norton I’m calling them The Telegram Borrowers.

2023年8月，我所推荐他们Telegram软件的两位中国朋友被社会工程团队欺骗而帐户被暂时被泄漏。我不知道这个犯罪集团有没有名字，所以根据玛丽·诺顿的儿童小说，我称他们为《电报地板下的小矮人》。

The gang’s “phishing” entry point is a third-party Telegram “bot” which pretends to be an official function of Telegram. If someone doesn’t know what Telegram “bots” are, it does indeed look official, and Telegram would do well to make it more obvious to non-technical users that they are interacting with a third party.

团队的钓鱼式攻击使用Telegram的第三方机器帐户，那个帐户装为官方功能。人要是不知道“bot”是指什么，他们很可能以为这真的是官方的，所以我希望Telegram未来能更清楚向人指出他们正在跟个第三方帐户谈话。

The scamming bot pretends to be an equivalent of Chinese WeChat’s “vouch for a friend” function. A message from your friend’s account tells you they are in some kind of trouble (which is true: their account has been compromised), and that you can vouch for them using the “official bot” (which is false). Crucially, the message will seem genuine, because it has been written by a human professional scammer who has full access to your friend’s Telegram chat history and can see how they normally write to you. If you open their link, the bot will take you through the steps required to give them access to your own Telegram account as well, under the pretense of vouching for your friend.

骗局机器帐户假装做微信‘保证朋友’功能的Telegram相等。来自你朋友帐户的信声称朋友有某些问题（其实他们真的有问题: 他们的帐户被泄漏了），而您可以使用“官方功能”（假）解救你的朋友。关键的问题是这个信看起来是真的，因为不是“人工智能”写的，是来自真正的职业骗徒而那个网诈会看你朋友的所有Telegram聊天记录，所以会框出那位朋友与你往往怎样谈话。如果你真的打开那位骗局所发给你的连接，他们的机器帐户会以帮助朋友为虚假而逐渐地指导你如何容许团队也进去你自己的Telegram帐户。

Part of the gang’s operational security appears to call for the chat that contains the bot link to be remotely deleted if the mark does not comply, or immediately after they do comply. This makes it harder to report the bot to Telegram. The gang will of course be able to set up a new bot, but that does inconvenience them, so they try to avoid letting you keep the bot address long enough to report it.

此帮派的行动安全看来包括这个规则: 如果受害者不马上打开连接，或者打开后，就删除双方的聊天，以免受害者报告此连接。犯罪组织当然能创造新的连接，但看来这有点不方便所以他们试试避免经常得这样做。

But that didn’t stop me from opening a new chat to my would-be scammer and chit-chatting about how their business is going. I showed off my credentials a bit so they knew why I wouldn’t be scammed, but I can still be a ‘nice guy’ and who doesn’t sometimes need to take time out for a chat?

但那不阻止我打开另一个对话框而与骗徒聊一聊生意怎么样。我一点夸耀自己的资格让他们知道我为什么不容易受骗，但仍然能做个轻松聊天，谁没有偶尔需要休息聊天?

This operative claimed they had compromised 73,000 accounts and were currently doing 50 a day (which would mean they’ve been going for 4 years). The intention was not to make long-term use of the compromised accounts themselves, but to scan their chat history for financial information, which they said had so far enabled them to raid bank accounts to the tune of 1.97 million dollars and they were aiming for 3 million.

本技工声称已经泄漏了7万3千帐户而目前做一天50个（如果是真的，他们看来已经4年运转）。目的不是长期使用Telegram帐户的本身，而是扫描聊天记录找到银行细节，他们说这样已经拿走197万美金而希望能拿到300万。

![chats.jpg](https://ssb22.user.srcf.net/law/chats.jpg)

They were using a VPN with an exit node in AsiaNet HK’s infrastructure, and the “Nicegram” fork of the Telegram client, version 1.3.2 (the June release), on a slightly nicer iPhone than my friend’s. They were using the Nicegram fork because it lets you log into an unlimited number of Telegram accounts at the same time.

他们使用香港AsiaNet服务器的VPN而Telegram的Nicegram复刻（不是最新的版本），在个比我朋友贵的iPhone。那个Nicegram复刻容许他们同时登入无限的Telegram帐户。

![nicegram.jpg](https://ssb22.user.srcf.net/law/nicegram.jpg)

One of my friends kept trying to get back into his account, so they put a 2-factor authentication on it with their own GMail account as the recovery backup. He later got his account deleted, but only after the Borrowers had already finished with it anyway: both accounts were logged out 5 days after they’d been entered.

一个朋友不断尝试再次登入他的帐户所以他们加个双因子认证密码而用自己的gmail做恢复电邮地址。他之后删除他的Telegram帐户，但那时候《地板下小矮人》已经结束了: 我两朋友的帐户都5天后被登出了。

I don’t know how the Borrowers were affected by the late-September 2023 update which introduced more prominent warnings with delays and cancellation options when an account is logged into from elsewhere. In November 2025 I saw a less-sophisticated attempt to have Chinese users interact with a “Telegram Tips” bot which had clear “third party” labelling above its claim to be official (it may still have drawn in some who had the interface language set incorrectly).

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
iPhone is a trademark of Apple in some countries.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Telegram is a trademark of Telegram Messenger LLP.
WeChat is a trademark of Tencent Holdings Limited.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
