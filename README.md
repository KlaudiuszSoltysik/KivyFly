Video demonstration:


Script of the things I am talking about if you can't understand me:

OK, so I've made a project to track flights prices between major European cities.

Here is the application part of the project.

Firstly, there you enter the city you are departing from, and your destination city. The buttons here may help you.

Then, you have to add more details about your flight. Accommodation days are self-explaining.

Here I used an interesting algorithm. It checks the price of flights matching your preferences in the past 45 days using an API to download data. Let's say the cheapest flight was 100 euros. If you type here 10, it means we are looking for all flights that cost under 10% over the cheapest flight in history. In this case it will be 110 euros.

Next, you have to add your email address or phone number so a script part of the project that works in the cloud can send you a message.

If you try to add a flight with incorrect data app will tell you about it.

It searches for the cities you entered in the spreadsheet that I've made and uploaded to the cloud. The program will inform you in the case of failure, or when the cities you entered are the same.

Also you cant add flight with invalid data in the other text boxes. The app will hint you what you should fix. This should be over 1 day; discount over 0%, email address should contain @; length of the phone number should be 9.

You can show your entire saved wishlist or delete it with those buttons. It will also delete them from the cloud.

To make it everything possible, I used an API to download self-made airports data from Google spreadsheet.

User wishlist is uploaded or deleted from Google spreadsheet straight from the code using request library and API. Internet connection is obligatory.

All of this is necessary to run in the cloud the second part of this project.

To make this app even better, I could add a function to save files locally and update a cloud spreadsheet when running this program next time with an internet connection.

I could let user define who is going to flight (adult or kid).

Also, more code comments and visuals of this project may be improved.

And there is the script working in the cloud that searches for flights matching your wishlist in the next 3 months.

It is downloading data from the same spreadsheet that we uploaded before.

It will update you in case of finding matching flights automatically. For SMS messages I had to sign up to Twillio site.

There's a lot of API used in this project and plenty of Kivy library.
