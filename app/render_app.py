# import os
# import subprocess
# import sys
# from threading import Thread

# # Import model_utils (works directly as it's in the same directory)
# from model_utils import load_all_models, preprocess_input

# # Get port from environment variable
# PORT = int(os.environ.get("PORT", 10000))

# def run_fastapi():
#     """Run the FastAPI backend server"""
#     subprocess.run([
#         sys.executable, 
#         "-m", 
#         "uvicorn", 
#         "main:app", 
#         "--host", 
#         "0.0.0.0",
#         "--port", 
#         str(PORT)
#     ])

# def run_streamlit():
#     """Run the Streamlit frontend"""
#     os.environ["STREAMLIT_SERVER_PORT"] = str(PORT + 1)
#     subprocess.run([
#         sys.executable,
#         "-m",
#         "streamlit",
#         "run",
#         "../frontend/app.py",  # Adjusted for new relative path
#         "--server.address",
#         "0.0.0.0",
#         "--server.port",
#         str(PORT + 1)
#     ])

# if __name__ == "__main__":
#     # Start both servers in separate threads
#     fastapi_thread = Thread(target=run_fastapi)
#     streamlit_thread = Thread(target=run_streamlit)
    
#     fastapi_thread.start()
#     streamlit_thread.start()
    
#     # Wait for both threads
#     fastapi_thread.join()
#     streamlit_thread.join()




import os
import subprocess
import sys
from threading import Thread

# Import model_utils (works directly as it's in the same directory)
# from model_utils import load_all_models, preprocess_input
from app.model_utils import load_all_models, preprocess_input

# Get port from environment variable (Render typically assigns dynamic ports)
PORT = int(os.environ.get("PORT", 10000))

def run_fastapi():
    """Run the FastAPI backend server"""
    subprocess.run([
        sys.executable, 
        "-m", 
        "uvicorn", 
        "main:app", 
        "--host", 
        "0.0.0.0",  # Allow access from any network
        "--port", 
        str(PORT)
    ])

def run_streamlit():
    """Run the Streamlit frontend"""
    os.environ["STREAMLIT_SERVER_PORT"] = str(PORT + 1)  # Assign Streamlit to a different port
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "../frontend/app.py",  # Adjusted for new relative path (Ensure this path is correct)
        "--server.address",
        "0.0.0.0",  # Allow access from any network
        "--server.port",
        str(PORT + 1)  # Streamlit will run on the next port after FastAPI
    ])

if __name__ == "__main__":
    # Start both servers in separate threads for concurrency
    fastapi_thread = Thread(target=run_fastapi)
    streamlit_thread = Thread(target=run_streamlit)
    
    fastapi_thread.start()
    streamlit_thread.start()
    
    # Wait for both threads to complete (this keeps the main thread alive)
    fastapi_thread.join()
    streamlit_thread.join()
