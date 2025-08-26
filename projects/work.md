I'm working on building out a data warehouse from scratch at a startup. It's been a fun project involving everything from setting up cloud infrastructure to working with the sales team to figure out what data they actually need. The main focus is getting Monthly Recurring Revenue (MRR) tracking sorted and making sure everyone has the data they need to make good decisions.
## Tech Stack & Tools

- Data Warehouse: Amazon Redshift
- Storage: Amazon S3
- Data Integration: Airbyte
- Data Transformation: dbt (data build tool)
- Visualization: Metabase (planned)
- Data Sources: HubSpot, billing system, customer success platform
- Project Management: Jira

# What I've Been Working On
## Getting Everything Set Up

- Worked with the ops team to get our Redshift warehouse and S3 storage up and running
- Got Airbyte working locally and connected it to our CRM system
- Set up a proper GitHub repo with a sensible structure for all our data models
- Created naming conventions so we don't end up with tables called "table_final_final_v2"

## Building Data Pipelines

- Built custom API scripts to pull revenue data from our billing system
- Migrated some old scripts to Airbyte to make everything more maintainable
- Set up automated data loads to S3 that actually run on schedule
- Got our CRM data flowing properly for sales pipeline analysis

## Data Modeling & Transformation

- Built dbt models to transform raw data into something actually useful
- Created revenue tables that actually reconcile with our billing system
- Built some recursive logic to track transaction histories properly
- Made tables for enhanced revenue reporting

## Analytics & Reporting

- Automated customer scoring reports so they don't have to be done manually
- Did a deep dive into churn analysis for leadership
- Built reporting for the sales team so they can actually see their pipeline
- Documented what all our metrics actually mean (surprisingly important!)

## Working with the Team

One of the fun parts has been figuring out what everyone actually needs:

- Regular check-ins with leadership to make sure I'm building the right stuff
- Worked with different department heads to understand their specific needs
- Spent a lot of time with the sales team to understand their workflow
- Dug into existing reports to see what was working and what wasn't

## What I'm Focused on Now

- Getting MRR tracking and forecasting dialed in
- Making sales pipeline reporting actually useful
- Customer lifecycle analysis and churn prediction
- Making sure our revenue numbers actually match between systems
- Diving deeper into CRM data relationships

## How It's Been Going

**May 2025**: Started the project, got infrastructure set up, talked to everyone
**June 2025**: Built data pipelines, created first dbt models, got initial reports working
**July 2025**: Advanced pipeline work, finished revenue tables, focused on sales team needs

# Wrap Up

It's been a great project that's let me work on everything from infrastructure to stakeholder management. Building a data warehouse from scratch at a startup is equal parts challenging and rewarding - you get to make all the architectural decisions, but you also have to make sure everything actually works for the business.
