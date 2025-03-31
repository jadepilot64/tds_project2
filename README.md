IIT Madras Assignment Helper API
A FastAPI application that automatically answers questions from IIT Madras' Online Degree in Data Science course assignments.

Overview
This API processes questions from the Tools in Data Science course assignments, analyzes them, and returns correct answers. It can handle various question types including:

Extracting data from CSV files

Processing ZIP archives

Calculating statistics

Analyzing encoded files

Executing commands and formulas

Features
RESTful API for answering assignment questions

File upload and processing capabilities

Intelligent question analysis and pattern matching

Support for all five graded assignments from the course

Secure handling of queries via OpenAI integration

Installation
Clone this repository and install dependencies:

bash
git clone https://github.com/jadepilot64/tds_project2.git
cd tds_project2
pip install -r requirements.txt
Environment Setup
Create a .env file with the required environment variables:

text
AIPROXY_TOKEN=your_token_here
Usage
Run Locally
bash
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.

API Endpoint
Send POST requests to /api/ with:

question: The assignment question text (required)

file: Any file attachment (optional)

Example using curl:

bash
curl -X POST "http://localhost:8000/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@path/to/abcd.zip"
Response format:

json
{
  "answer": "1234567890"
}
Deployment
This application can be deployed to platforms like Vercel, Heroku, or any other service that supports Python applications.

License
This project is licensed under the MIT License - see the LICENSE file for details.