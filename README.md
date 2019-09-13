# Jungle Scout Tech Challenge

This is my submission for the Jungle Scout Tech Challenge.

To run this app:
1. In a separate terminal, run `docker-compose up` on `docker-compose.yml` to deploy a local mongoDB instance.
    * To query the database through shell, ssh into the docker image with `docker exec -it mongo-container bash`. Once inside, you can enter mongoDB shell with `mongo -u mongo_user -p mongo_pw`.
2. Run `pip3 install -r requirements.txt` to install needed python dependencies for this app.
3. In your main terminal, `cd` into the src directory and run `python3 app.py`. The app runs on `localhost:5000`.
4. To run unit tests, run `pytest` in the root directory.

In the app, you can either enter an ASIN in the text input and press "Search" or directly navigate to `/get/{ASIN}` to see the app in action.

# Tech Questions

### What were the biggest challenges you faced in writing the challenge?
Since the Amazon API is off-limits for this challenge, I went with the approach I had the most experience with -- web scraping.
The biggest challenge I faced logistically for this is that there is a lot of variance in how Amazon presents its data to users. Even throughout the time I spent developing, some pages would change over time, likely to due to A/B split testing. I went through a lot of pages to get a sense of the presentations possible and tried to make my xpath queries flexible to facilitate this. 

### Can you explain your thought process on how you solved the problem, and what iterations you went through to get to this solution?
Scrapy has an opinionated, but powerful pipeline-based workflow -- "spiders" are written as dispatchable processes that asychronously fetch data from websites, possibly scraping several webpages before terminating, and the results of these scrapes are then processed with some handler function. 

To get the parsing working correctly, I saved several amazon webpages locally and rapidly iterated through the test set with scrapy's shell to come up with xpath queries that would correctly grab the required information on as many different page variation as possible.

Once I got the parsing working on my test set, I built the flask app around the pipeline. The app only exposes a read function to users. The read function will either fetch the requested data from the mongodb database or trigger a scrapy job to fetch the necessary data and then persist the result.

I didn't have enough time to write unit tests for everything, but I added as many tests as I could to the core functionality of Scrapy's parsing pipeline. The key goal with this was that Amazon (or any website I would parse) is not static; for speed and reliability I wanted hardcoded mock html responses to test on. Additionally I wanted to do as little live testing as possible before I was confident in my scraping app, as Amazon is good at detecting suspicious repeated behaviour and is IP ban-happy.
Given some more time I would have liked to test:
* More edge cases for scrapy's xpath parsing ()
* Support more amazon page layouts
* Add repository testing with verified writes to a mock repository
* Add integration tests
* Stress / load testing

Additionally, given more time I would have added some admin capabilities such as removing products from the database or forcing a product to update its entry either on-demand or after its database entry was sufficiently old enough.

### If you had to scale this application to handle millions of people adding in ASIN's in a given day, what considerations would you make?
* This app currently loads ASIN entries on demand, for millions of users we should pre-load items depending on business needs. After identifying what our users direct the most traffic towards (long tail keywords, evergreen niches, current events-related fad products, etc) we can pre-fetch ASIN listings to reduce the level of on-demand fetching, ideally only needing it for rarely-searched and unpopular items.
* For millions of users, we should add distributed caching with something like Redis to serve frequently viewed items without needing database access.
* MongoDB was used in this app due to ease of setup, but for a larger audience Cassandra could be a better choice depending on what usage looks like. The schema-free, column-based architecture lends itself to the often sparse data we get from Amazon's products, with market-specific data points that don't exist on other products. Additionally since trends change quickly on Amazon, we may need rapid scaling up or down to deal with product relevancy -- Cassandra handles horizontal scaling and replication very well, not even requiring downtime to add/remove nodes.
* I would put more work into parallelizing the workflow in general. Luckily, scrapy is already set up for asynchronous handling of both dispatching and receiving scrape jobs, so most of the work would be on optimizing the flask app to scale horizontally in handling requests and kicking off jobs.

### Why did you choose the technologies you used?
* I chose Scrapy for the web scraping component. I have used this library before, and it is one of the most versatile and powerful scraping libraries available. This makes it easy to get support for the tool, as well as hire new developers to collaborate with it. This is a case of going with the right tool rather than the comfortable tool, as I typically operate with Java / Scala for my backend work. Scrapy is admittedly overkill for a problem like this, but in a real life app Scrapy is a good foundation for a scraping service for the reasons mentioned as well as its versatility in following links and supporting scrapes of dynamic / authentication-hidden pages. If this problem evolved to grab related products or to grab products per-category, scrapy would rise to meet that challenge well.
* I chose Python + Flask for integration with scrapy. Flask was chosen over Django as it is lighter weight and more geared towards an API-only microservice.
* I chose mongoDB because it is relatively simple to provision and works for this application, but as mentioned for a production app I might go for Cassandra instead depending on what usage looks like.
