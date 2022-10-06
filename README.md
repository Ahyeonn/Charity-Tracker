# Charity-Tracker
This is a charity tracker website where users can add donations to the three different charities that are listed and can also leave notes for each donation that the users have made. Whenever users leave notes or donations, the datas will save into the database so that users can keep track of their donation & note history. This website was made by Flask, MongoDB, PyMongo with the virtual environment for ACS 1710, ‘Web Architecture’.

# How to run with Docker
1. Open Terminal and run this command to build the image.
```
docker build . -t charitytracker
```
2. Run the container by running the command below.
```
docker run -p 5000:5000 charitytracker
```
3. Navigate to http://localhost:5000

# URL for my website
- Heroku: 
  https://charitytracker2.herokuapp.com/
- Caprover (Deployed with Docker):
  https://charity-app.dev.ahyeonjeon.tech/

# Status page for the Caprover website
- https://statuspage.freshping.io/63357-ACS32202022Status
