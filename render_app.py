import os
import subprocess
import sys
from threading import Thread

# Get port from environment variable
PORT = int(os.environ.get("PORT", 10000))

def run_fastapi():
    """Run the FastAPI backend server"""
    subprocess.run([
        sys.executable, 
        "-m", 
        "uvicorn", 
        "app.main:app", 
        "--host", 
        "0.0.0.0",
        "--port", 
        str(PORT)
    ])

def run_streamlit():
    """Run the Streamlit frontend"""
    os.environ["STREAMLIT_SERVER_PORT"] = str(PORT + 1)
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/app.py",
        "--server.address",
        "0.0.0.0",
        "--server.port",
        str(PORT + 1)
    ])

if __name__ == "__main__":
    # Start both servers in separate threads
    fastapi_thread = Thread(target=run_fastapi)
    streamlit_thread = Thread(target=run_streamlit)
    
    fastapi_thread.start()
    streamlit_thread.start()
    
    # Wait for both threads
    fastapi_thread.join()
    streamlit_thread.join()