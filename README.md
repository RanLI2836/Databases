# Databases
Course Project


We implemented all the parts of our original proposal in part 1 successfully. There are 8 entities in our relational model including ScenicSpot, Itinerary, TourGroup, Tourist, Insurance, TourGuide, Hotel, and Vehicle, the relationships captured in our model are Visit, ComposedOf, Enroll, Stay, Transport, Guide, Contain. The users are able to interact with basic web form elements like text fields and dropdown menu, to administrate the database by adding, updating, and deleting information. 
In the home page, there is a dropdown menu for learning more information about hotels, scenic spots, tour guides and so on. Users can directly view all the information of these tables in our database. Moreover, users can input the scenic spots they want to visit and get the corresponding itineraries. If you search “island” in the text field, the key word “island” will be used in a query which will search for the names that include this key word in the ScenicSpot table and find the itineraries that include this scenic spot and other information about the itinerary like the hotel, guide, vehicle and group. The results can be viewed in itinerary page.

In tourist page, all the tourists’ name and gender are shown directly in a table. With the text fields in the left, you can add tourists to the database. The update and delete buttons in the rightmost column of the table allow user to update or delete the information of corresponding tourist. If you want to update the information of a tourist, click the “update” button and jump to edittourist page in which you can input the new information.

We designed a “advertising” bar in the tour guide page which shows some information of 4 popular tour guides. Using a query to find out the tour guides who have led the most tourists in the total tour groups they lead, we can print their ID, name, and the total tourists they have led. 
