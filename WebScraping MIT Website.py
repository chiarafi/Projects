#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Objective: 
    In order to understand the competetive information of MIT, we want to collect information about
    their Business Analytics Executive Programs. Therefore, we scrape relevant data from their website
    and collect the information in our dataframe called df.
"""

# Import required libaries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL of the course finder page
main_url = 'https://executive.mit.edu/course-finder?prefn1=courseTopics&prefv1=Business%20Analytics'

# Send a GET request to the main page
response = requests.get(main_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all course elements on the webpage and extract URLs
course_links = soup.find_all('a', class_='nameLink')
course_urls = ['https://executive.mit.edu' + link['href'] for link in course_links if 'href' in link.attrs]

# Initialize an empty list to store course data
courses = []

# Iterate over each course URL
for url in course_urls:
    
    # Send a get request
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract course name
    name_element = soup.find('h1', class_='product-name')
    name = name_element.text.strip() if name_element else 'Name Not Found'

    # Extract track information
    track_element = soup.find('p', class_='cert-track')
    track = track_element.text.strip() if track_element else 'Track Not Found'

    # Extract certificate credits
    credits = 'Credits Not Found'
    credits_heading = soup.find('p', string=lambda text: text and "Certificate Credits" in text)
    if credits_heading:
        credits_element = credits_heading.find_next_sibling('p', class_='mb-1 single-value')
        if credits_element:
            credits = credits_element.text.strip()

    # Extract price, duration, time commitment, and format
    price = 'Price Not Found'
    duration = 'Duration Not Found'
    time_commitment = 'Time Commitment Not Found'
    course_format = 'Format Not Found'
    price_input = soup.find('input', class_='hidden-table')
    if price_input and price_input.get('value'):
        try:
            price_data = json.loads(price_input['value'].replace('&quot;', '"'))
            if price_data:
                price = price_data[0].get('courseOfferingPrice', 'Price Not Found')
                duration = price_data[0].get('courseOfferingDuration', 'Duration Not Found')
                time_commitment = price_data[0].get('timeCommitment', 'Time Commitment Not Found')
                course_format = price_data[0].get('courseOfferingFormat', 'Format Not Found')
        except json.JSONDecodeError:
            price = 'Price Data Invalid'
            
   # Extract topics
    topics = []
    topics_heading = soup.find('p', string=lambda text: text and "Topics" in text)
    if topics_heading:
       topics_elements = topics_heading.find_all_next('p', class_='mb-1 single-value')
       topics = [topic.text.strip() for topic in topics_elements]
       
    topics = ["".join(filter(str.isalpha, s)) for s in topics]
    topics = list(filter(None, topics))
       


    # Append the course data to the list
    courses.append({
        'Name': name,
        'Track': track,
        'Credits': credits,
        'Price': price,
        'Duration': duration,
        'Time Commitment': time_commitment,
        'Format': course_format,
        'Topics': topics,
    })

# Create a DataFrame from the list
df = pd.DataFrame(courses)




# Next, we're adding the ratings for each course, using the main URL
# Send a GET request to the website
response = requests.get(main_url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize an empty list to store Rating data
starratings = []

# Find all course elements in the webpage
course_elements = soup.find_all('div', class_='pdp-link text-wrap')

# Iterate through all the courses
for course_element in course_elements:

    # This div should contain the star rating in the data-starrating attribute
    teaser_div = course_element.find('div', {'class': 'TTteaser'})
    if teaser_div:
        star_rating = teaser_div.get('data-starrating')
    else:
        # If the 'TTteaser' div is not found, check in nearby elements as a fallback mechanism
        teaser_div = course_element.find_previous('div', class_='TTteaser')
        star_rating = teaser_div.get('data-starrating', 'Not Available') if teaser_div else 'Not Available'
        
    # append the rating to the starrating-list
    starratings.append(star_rating)

# get the rating of the last course, as the loop didn't handle this one correctly
edit_course = course_elements[-1].find('a', class_='nameLink').text.strip()
teaser_div = course_element.find('div', {'class': 'TTteaser'})
if teaser_div:
    star_rating = teaser_div.get('data-starrating')
    starratings.append(star_rating)
else:
    # If the 'TTteaser' div is not found, check in nearby elements
    # This is a fallback mechanism and may need adjustment
    teaser_div = course_element.find_previous('div', class_='TTteaser')
    star_rating = teaser_div.get('data-starrating', 'Not Available') if teaser_div else 'Not Available'
    starratings.append(star_rating)

# drop the first element of the ratings, as, in our starrating-list, the rating at index 0 does not belong to any course; right now, the required list of ratings starts at index 1 and to fix this, we drop the first element
starratings.pop(0)

# add the rating to our dataframe
df['Star Rating'] = starratings


# Print the DataFrame
print(df)