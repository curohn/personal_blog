# Delivery App Simulation
The goal of this project is to demonstrate my skills in database design, while teaching myself to simulate data. For this project I'll design a database for my delivery app, create synthetic data with a python script, run analysis on top of it using streamlit, and answer hard questions about the business model.

I'd like to also relate it to the real world by researching actual delivery apps, their pricing models, and make an educated guess on the simulation parameters I'd need to compare them.


## Project Design:
### High Level Design
SQL
- Local instance of SQLite
- Will need data structure, and normlized database design
- Script to initialize dim tables, populate with data


Order Simulation Script
- Query dim tables, create synthetic data, populate fact tables
  - Introduce randomness and variablilty
  - order_id, customer_id, resturaunt_id, order_time, delivery_distance, cost, delivery_fee, tip, surge_mult, final_price, delivery_type, etc. 

Vizulization 
- Script to query fact tables
- Streamlit
- Distributions, charts

Analysis:
- Answer hard questions: expensive times, how much does express cost vs time to deliver, surge pricing effect on consumer, and business, impact of different values in simulated data
### Files within Project
- database.ipynb: Initializes, and populates data into dim tables


## Project Notes

### Locations, Distances, and Travel Time
We are going to be simulating orders in this project. We will have orders populate in random restaurants, from random customers, and assign a driver to those orders. But how do we deal with travel time calculations? Lets keep it simple, and assume our simulated world exists on a two dimentional grid system from 0,0 to 100,100. Each resturaunt, customer, and drivers home can be assigned a random coordinate for their location. 

Now what do we do about drivers? In the real world, a drivers location is always changing, they could be home, at a customers delivery address, at a resteruant, or at a location in between. For the first iteration of this project we are going to simplify that, and have our drivers always be at their home. This will allow us to keep track of our drivers and allocate orders based on available drivers who are closest to the next order. 

Distances will be calculated based on the absolute value differences in corrdinates. For the first iteration, we will assume drivers can only move on the x and y axis, and not diagonally. 
If a driver is located at 5,5 and a restaurant is located at 52,60 then the distance will be:
```
5 - 52 = |-47| = 47
5 - 60 = |-55| = 55
47 + 55 = **103**
```

If a driver is located at 72,12, and the destination is at 87,54 the distance will be:
```
72 - 87 = |-15| = 15
12 - 54 = |-42| = 42
15 + 42 = **57**
```
Travel time will be 1/2 of the distance in minutes, with a minumum of 1 minute. 

### Open Hours
For the first iteration of this project restaurant will always be open, and drivers will always be available. The number of orders will be dictated by customer demand

### Order Flow
An order will be generated from a customer. 
- Customers will have a random demand value (0.25-2x daily) assigned each day that will dictate how often they will order that day. 
The order will be assigned to a restaurant. 
- The nearest restaurant with that item will be selected
- The item will have an assigned prep time. 
A driver will be assigned to that order.
- Drivers will be assigned in sequential order
- Driver will then 'drive' to that restaurant, and pick up order
The driver will deliver that order.
- Driver will drive to customers location to deliver. 
The Driver will drive home


## Database Design
`dim_dates` is a helper table to handle dates, day/month/year calculations, as well as determining if dates are holidays or weekends. These fields will be used to add variance to our order simulation script

`dim_customers` Will contain all customers. Customers will be assigned a random address (0,0) - (100,100). They will also be assigned random phone numbers, emails, and names.

`dim_restaurants` Will contain all restaurants, their randomly assinged cordinate address,  Restaurants will be assumed to be able to cook multiple items in parallel, so we will just need the MAX(prep_time) for each order. 

`dim_menu` Will contain the specific items on the menu at each resturaunt (A-Z), each items cost, and a random "prep_time" value to simulate how long it would take to make that item.

`dim_drivers` Will contain drivers, their assigned coordinate address, and some generated names, emails, and phone numbers. 

`fact_orders` Will be our transaction table. It will be populated by the simulation script.



# Future Versions
Real world delivery apps, and how they compare to my simulated script
Improvements to bring my simulation closer to real world
- Driver schedule
- Driver transaction table
- Restaurant schedule
- Restaurant transaction table
- Order queue, resaurant queue, driver queue tables
- Logic to place orders not only at closest resauraunt but fastest accounting for queue and prep time
- Cluster addresses around city centers to better simulate real world
- Drivers can be home, a restauraunt, or a customers house
- Customers can order more then one item
