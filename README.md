🧠 IIT Madras TDS Assignment Helper

FastAPI application that automatically answers questions from IIT Madras' Online Degree in Data Science, Tools in Data Science course assignments, saving you time and effort.

<p align="center"> <img src="https://user-images.githubusercontent.com/74038190/212257468-1e9a91c1-b626-4baa-b15d-5c385dfa7ed2.gif" width="500"> </p>

🚀 Features

✅ Intelligent Question Analysis: Automatically identifies question patterns and selects appropriate processing methods

📊 Data Extraction: Extracts valuable information from CSV files and ZIP archives

📈 Statistical Processing: Performs calculations on datasets with precision

🔍 File Analysis: Processes encoded files and extracts relevant data

⚙️ Command Simulation: Handles command execution and formula processing

🔒 Secure Integration: Connects with AI services for enhanced processing capabilities

📋 Overview

This API seamlessly processes questions from the Tools in Data Science course assignments and returns accurate answers. It can handle various question types including:

📁 Extracting data from CSV files

🗜️ Processing ZIP archives

📊 Calculating statistics

🔤 Analyzing encoded files

💻 Executing commands and formulas

🛠️ Installation
Clone this repository and install dependencies:


`git clone https://github.com/jadepilot64/tds_project2.git
cd tds_project2
pip install -r requirements.txt`

⚙️ Environment Setup
Create a .env file with the required environment variables:


`AIPROXY_TOKEN=your_token_here`

📝 Usage
Run Locally


`uvicorn app.main:app --reload`

The API will be available at http://localhost:8000.

API Endpoint
Send POST requests to /api/ with:

question: The assignment question text (required)

file: Any file attachment (optional)

Example Request

`curl -X POST "http://localhost:8000/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@path/to/abcd.zip"`
  
Response Format
json
{
  "answer": "1234567890"
}

🚀 Deployment
This application can be deployed to platforms like:

Vercel

Heroku

Railway

Any other service that supports Python applications

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

<p align="center"> <sub>Made with ❤️</sub> </p>