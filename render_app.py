# import os
# import subprocess
# import sys
# from threading import Thread

# # Get port from environment variable
# PORT = int(os.environ.get("PORT", 10000))

# def run_fastapi():
#     """Run the FastAPI backend server"""
#     subprocess.run([
#         sys.executable, 
#         "-m", 
#         "uvicorn", 
#         "app.main:app", 
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
#         "frontend/app.py",
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



# import os
# import subprocess
# import sys
# from threading import Thread

# # Import model_utils (works directly as it's in the same directory)
# from app.model_utils import load_all_models, preprocess_input

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
#     """Run the Streamlit frontend server"""
#     os.environ["STREAMLIT_SERVER_PORT"] = str(PORT + 1)
#     subprocess.run([
#         sys.executable,
#         "-m",
#         "streamlit",
#         "run",
#         "/frontend/app.py",  # Adjusted for new relative path
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
from app.model_utils import load_all_models, preprocess_input

# Get port from environment variable
PORT = int(os.environ.get("PORT", 10000))

def run_fastapi():
    """Run the FastAPI backend server"""
    subprocess.run([
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",  # FastAPI backend located in app.main
        "--host", "0.0.0.0",
        "--port", str(PORT)
    ])

def run_streamlit():
    """Run the Streamlit frontend"""
    os.environ["STREAMLIT_SERVER_PORT"] = str(PORT + 1)
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/app.py",  # Streamlit frontend located in frontend.app
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
