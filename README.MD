# vpn sniffer

a simple PPTP vpn sniffer runs on Linux (Ubuntu 14.04 LTS tested). my graduation project.

features:
1. sniff packets from fixed network interface
2. show real-time traffic in a diagram (not very accurate)
3. log user's login and logout
4. log http traffic and ftp traffic (simply)
5. simple log manager (select and delete)

In addition, this project includes some crypto functions that I wrote when I did research on PPTP protocol.
If someone is in trouble with MSCHAPV2 key generating or challenge value generating, this is the example you are looking for.

dependencies:
1. linux
2. pyqt5
3. pyqtgraph
4. pyshark
5. psutil

# How dose it work

From local network interface, the program searches PPTP packets to find out a user's login/logout action.

When a user logins, program start a new thread, in this thread, a new capture to the user's virtual interface(ppp0, ppp1 etc.)
started and each packet will be analysis to find http requests and ftp commands, which will produce some logs.

For all QTableViews, I write model classes which subclassing QAbstractItemModel.