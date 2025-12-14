# Final Reflection

Repository Link: https://github.com/Sid1995-dev/OIM6301/tree/main/proj-python

## Section 1: Project Overview

**Which option did you choose for Part 1?**
- I chose to go with option A (Provided Dataset - E-commerce) as it was easier, readable and faster to get started with, especially as I've been new to programming.

**Which API(s) did you use in Part 2?**
- Used the REST Countries API (https://restcountries.com/) as it was easy to consume and did not require any authentication keys.

**Brief summary of what your project does:**
This project demonstrates Python programming skills through an e-commerce data analysis system. It includes the following:
- Local database setup
- Implementation of business queries using SQL and Python
- Report generation techniques (CSV and text summaries)
- Usage of public APIs to perform a simple task where a user can retrieve real-time information about any country they input, along with an example where we use a public API to retrive time-zones for the cities where customers are located in the e-commerce database.

## Section 2: Technical Challenges & Solutions

**What was the most challenging part technically and how did you solve it?**
- I think the hardest part was understanding the structure of raw data returned from SQL queries for processing and formatting via Python directly. Usage of SQL to implement the business queries was mostly straight forward as these are solved problems, however using Python to perform the same transformations was definitely challenging which is where AI helped a lot. With the use of `print()` statements to see the exact structure of raw outputs, AI to understand this data format and to make sense of what Python tools can be used to implement those SQL functions, I was able to solve it.
- While working with the countries API, I realized it was not returning the right country information in certain scenarios, for example inputting "India" returned "British Indian Ocean Territory". I looked up the API documentation at https://restcountries.com/ and realized that if I wanted to retrieve the exact match, I needed to add the `fullText=true` parameter to the endpoint. With this modification, I was able to retrieve exactly what I wanted! This was a lesson to review the basics of the API documentation before trying to call them directly.

## Section 3: AI Usage Documentation

### AI Usage 1
I took the help of AI to help with my database setup, mainly around the usage of foreign keys as I was not too comfortable with it yet. This felt like a straightforward task. I gave it context about my data and asked it to help me with my query. I validated it by having it explain the code and also by actually executing the code.

### AI Usage 2
AI was especially helpful in implementing the python versions of the SQL queries i.e. to use python instead of `GROUP BY` statements. This level of complexity in Python was definitely new to me, so I took some time to have AI explain it to me and to be able to test it. I did provide it intermediate outputs using `print()` statements as context to help me use the right Python tools (like loops, fetching specific information from strings and dictionaries) and to be able to complete code.

### AI Usage 3
AI helped with writing most of my `api_demo.py` and `api_integration.py` as I am fairly new to these. Especially around handling "JSON" responses and error handling. For `api_integration.py` I gave it a use-case and the API I'd like to use and business logic I'd like to implement and it was able to help output this error-free for me to test.

### AI Usage 4
I also used AI extensively for a lot of chores and cleanups around the project. This includes, cleaning-up some code, adding comments for all functions to make it more readable, creating the "Readme" file and some tasks like creating the ".gitignore" file which were all new to me. It was very exciting that AI was able to handle a lot of the non-critical tasks that could take a lot of time to do manually.

## Section 4: Learning Reflection

Through these exercises, I gained a deeper understanding of when and why Python can be used as a more powerful tool compared to running database queries alone. Python enables richer formatting, more complex workflows, and capabilities such as batch processing. The api_integration task, in particular, highlighted how combining public API integrations with database operations can create additional value.
Moving forward, I hope to become more proficient and fluent in Python, especially in using it for data visualization, including generating graphs and charts that I would generate for reports in my career. 