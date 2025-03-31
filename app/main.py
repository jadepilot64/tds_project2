# app/main.py
import os
import shutil
import tempfile
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.functions import (
    extract_zip_and_read_csv,
    process_encoded_files,
    calculate_statistics,
    make_api_request,
    execute_command,
    merge_csv_files,
    analyze_time_series,
    extract_zip_and_process_files,
    convert_keyvalue_to_json,
    calculate_prettier_sha256,
    sort_json_array,
    count_days_of_week,
    calculate_spreadsheet_formula
)

# Initialize FastAPI app
app = FastAPI(title="Assignment Answer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAI API configuration
OPENAI_API_CHAT = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
OPENAI_API_KEY = os.getenv("AIPROXY_TOKEN")

@app.post("/api/")
async def get_answer(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    # Create a temporary directory for files
    temp_dir = tempfile.mkdtemp()
    
    try:
        file_path = None
        if file:
            # Save the uploaded file
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
        
        # Process the question to extract relevant information
        question_lower = question.lower()
        
        # Try to match the question with appropriate function
        if "csv" in question_lower and "zip" in question_lower and "answer column" in question_lower:
            # Question about extracting value from a CSV in a zip file
            result = await extract_zip_and_read_csv(file_path, "answer")
            return {"answer": result}
            
        elif "encodings" in question_lower and ("sum" in question_lower or "total" in question_lower):
            # Question about processing files with different encodings
            symbols = []
            if "₹" in question_lower or "₹" in question:
                symbols.append("₹")
            if "$" in question_lower:
                symbols.append("$")
            if "€" in question_lower or "€" in question:
                symbols.append("€")
            if "£" in question_lower or "£" in question:
                symbols.append("£")
            if "¥" in question_lower or "¥" in question:
                symbols.append("¥")
                
            result = await process_encoded_files(file_path, symbols)
            return {"answer": result}
            
        elif "statistics" in question_lower or "calculate" in question_lower and "csv" in question_lower:
            # Question about calculating statistics
            operation = None
            if "sum" in question_lower:
                operation = "sum"
            elif "average" in question_lower:
                operation = "average"
            elif "median" in question_lower:
                operation = "median"
            elif "max" in question_lower:
                operation = "max"
            elif "min" in question_lower:
                operation = "min"
                
            column = None
            if "sales" in question_lower:
                column = "sales"
            elif "revenue" in question_lower:
                column = "revenue"
            elif "profit" in question_lower:
                column = "profit"
            elif "income" in question_lower:
                column = "income"
            
            result = await calculate_statistics(file_path, operation, column)
            return {"answer": result}
            
        elif "api request" in question_lower:
            # Question about making an API request
            url = None
            method = "GET"
            
            if "post" in question_lower:
                method = "POST"
                
            # Extract URL using regex or other methods
            # This is simplified and would need improvement
            words = question.split()
            for i, word in enumerate(words):
                if word.startswith("http"):
                    url = word
                    break
            
            result = await make_api_request(url, method)
            return {"answer": result}
            
        elif "command" in question_lower and "execute" in question_lower:
            # Find the command in the question (usually enclosed in quotes or backticks)
            import re
            command_match = re.search(r'[`\'"]([^`\'"]+)[`\'"]', question)
            if command_match:
                command = command_match.group(1)
                result = await execute_command(command)
                return {"answer": result}
                
        elif "prettier" in question_lower and "sha256" in question_lower:
            result = await calculate_prettier_sha256(file_path)
            return {"answer": result}
            
        # If no specific function matches, use a general approach
        import httpx
        
        # Prepare content for OpenAI
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Build context for the AI
        context = f"Question: {question}\n\n"
        
        if file_path:
            # Basic file info
            file_size = os.path.getsize(file_path)
            context += f"File provided: {file.filename} ({file_size} bytes)\n"
            
            # If it's a zip file, extract basic info
            if file.filename.endswith('.zip'):
                context += await extract_zip_and_process_files(file_path, "list")
        
        # Make the API request
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an assistant helping with IIT Madras' Data Science assignments. Provide only the exact answer that should be submitted, without explanations or reasoning."
                },
                {
                    "role": "user", 
                    "content": context
                }
            ],
            "temperature": 0.1,
            "max_tokens": 150
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENAI_API_CHAT, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    answer = result["choices"][0]["message"]["content"].strip()
                    return {"answer": answer}
                else:
                    raise HTTPException(status_code=500, detail="Unexpected API response format")
            else:
                raise HTTPException(status_code=response.status_code, detail=f"API request failed: {response.text}")
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}\n{error_details}")
    
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

# Root endpoint to check if API is running
@app.get("/")
async def root():
    return {"message": "IIT Madras Data Science TDS Assignment Helper API is running. Use /api/ endpoint for questions."}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
