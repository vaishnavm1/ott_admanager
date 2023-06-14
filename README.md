# ott_admanager
# OTT(On This Time) Advertisement Management System developed in Django framework
The project consists of client management web application for a digital newspaper, where there are multiple users with specific roles like <br />
Admin,Accountant,Marketer, Publisher
# Sequence of actions by every user
Admin has priviliges to add any other user except admin <br />
Accountant can add marketer user and can view all the marketers and clients <br />
Marketer can add client(s), marketer then adds advertisement of that client and specified time slot(if it's not already booked), then advertisement is approved by 
accountant, marketer can also request for discount or GST amount waived off, these requests are handled by admin user only, a release order is generated of every advertisement
it contains all the information about advertisement and agreed amount, marketer has to print the release order and takes client's signature and upload it's photograph to the application
it is approved by accountant, once accountant approves the advertisement it is show to publisher on advertisement's specifed date and publisher clicks 'Published' button only when
it is actually published on digital magazine <br />
All the order are shown to admin according to marketer and/or client, admin can download the order history in pdf format report also <br />
