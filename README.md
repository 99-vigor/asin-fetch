# Jungle Scout Tech Challenge

This is my submission for the Jungle Scout Tech Challenge.

To run this app:
1. In a separate terminal, run `docker-compose up` on `docker-compose.yml` to deploy a local mongoDB instance.
    * To query the database through shell, ssh into the docker image with `docker exec -it mongo-container bash`. Once inside, you can enter mongoDB shell with `mongo -u mongo_user -p mongo_pw`.
2. Run `pip3 install -r requirements.txt` to install needed python dependencies for this app.
3. In your main terminal, `cd` into the src directory and run `python3 app.py`. The app runs on `localhost:5000`.
4. To run unit tests, run `pytest` in the root directory.

In the app, you can either enter an ASIN in the text input and press "Search" or directly navigate to `/get/{ASIN}` to see the app in action.

### Technology Choices
The crux of this app is scrapy for scraping data from Amazon's frontend. I have used this library before, and it is one of the most versatile and powerful scraping libraries available. This makes it easy to get support for the tool, as well as hire new developers to collaborate with it. This is a case of going with the right tool rather than the comfortable tool, as I typically operate with Java / Scala for my backend work. Scrapy is admittedly overkill for a problem like this, but in a real life app Scrapy is a good foundation for a scraping service for the reasons mentioned as well as its versatility in following links and supporting scrapes of dynamic / authentication-hidden pages.

To facilitate data getting to the frontend, the scrapy workflow was wrapped with flask as a microservice. In an ideal production environment, this scraping service would be a standalone API that serves data to many other services. To this end we do not need Django, as it is much heavier and opinionated for an app that should be API-only.

### Application Architecture
This app was designed to be full stack, with Flask + Scrapy + MongoDB on the backend serving requests via HTTP responses and a React frontend receiving those responses and displaying data.

### Application Architecture

### Code Organization

### Code Itself

### Tests/Test Considerations

### Ops Considerations

# Tech Questions

### What were the biggest challenges you faced in writing the challenge?

### Can you explain your thought process on how you solved the problem, and what iterations you went through to get to this solution?

### If you had to scale this application to handle millions of people adding in ASIN's in a given day, what considerations would you make?

### Why did you choose the technologies you used?






