# Zalo bot plus an internal web page as the entry point

Users reach agents through a Zalo bot, and use an internal web page for TP upload, review edits and Gantt export. Zalo has an official bot platform that works over long polling, so nothing is exposed to the internet, but it limits messages to 2000 characters and files to about 5 MB, which is why the web page exists. Personal WeChat was rejected because it has no official bot API and bridges risk account bans; WeCom is deferred until expansion to sites that use it.
