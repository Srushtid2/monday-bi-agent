# Monday.com Business Intelligence AI Agent

This project implements an AI-powered Business Intelligence agent that answers founder-level questions using live data from monday.com boards.

## Features

- Conversational interface using Streamlit
- Live monday.com API integration
- Handles messy business data
- Provides insights on pipeline and operations
- Simple agent reasoning to route questions to the correct data source

## Architecture

User Question  
↓  
Streamlit Interface  
↓  
Agent Router (intent detection)  
↓  
Monday.com GraphQL API  
↓  
Business Insight Generation  

## Example Questions

- How is our pipeline?
- How many deals are currently active?
- What is the operations workload?

## Tech Stack

- Python
- Streamlit
- Monday.com API
- Requests library

## Running Locally

Install dependencies:
