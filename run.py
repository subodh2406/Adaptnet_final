# import os
# import subprocess
# import sys
# import time
# from threading import Thread
# from urllib.error import URLError

# import requests


# def check_server(url, max_retries=5):
#     """Check if a server is running and responding"""
#     for i in range(max_retries):
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 print(f"Server at {url} is running!")
#                 return True
#         except requests.exceptions.ConnectionError:
#             print(f"Waiting for server at {url} to start... (Attempt {i+1}/{max_retries})")
#             time.sleep(3)
#     return False

# def run_fastapi():
#     """Run the FastAPI backend server"""
#     try:
#         print("Starting FastAPI server...")
#         os.chdir(os.path.join(os.path.dirname(__file__), "app"))
#         subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error starting FastAPI server: {e}")
#         sys.exit(1)

# def run_streamlit():
#     """Run the Streamlit frontend server"""
#     try:
#         print("Starting Streamlit server...")
#         os.chdir(os.path.join(os.path.dirname(__file__), "frontend"))
#         subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error starting Streamlit server: {e}")
#         sys.exit(1)

# def main():
#     # Store the original working directory
#     original_dir = os.getcwd()
    
#     try:
#         # Start FastAPI server in a separate thread
#         fastapi_thread = Thread(target=run_fastapi)
#         fastapi_thread.start()
        
#         # Wait for FastAPI server to be ready
#         if not check_server("http://127.0.0.1:8000"):
#             print("Failed to start FastAPI server. Please check the server logs.")
#             sys.exit(1)
        
#         # Start Streamlit server
#         streamlit_thread = Thread(target=run_streamlit)
#         streamlit_thread.start()
        
#         # Keep the main thread alive
#         fastapi_thread.join()
#         streamlit_thread.join()
        
#     except KeyboardInterrupt:
#         print("\nShutting down servers...")
#         sys.exit(0)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         sys.exit(1)
#     finally:
#         # Restore the original working directory
#         os.chdir(original_dir)

# if __name__ == "__main__":
#     main()



import os
import subprocess
import sys
import time
from threading import Thread
import requests

# Get the port from the environment variable (Render provides it)
PORT = os.environ.get("PORT", 8000)  # Default to 8000 if PORT not set

def check_server(url, max_retries=5):
    """Check if a server is running and responding"""
    for i in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Server at {url} is running!")
                return True
        except requests.exceptions.ConnectionError:
            print(f"Waiting for server at {url} to start... (Attempt {i+1}/{max_retries})")
            time.sleep(3)
    return False

def run_fastapi():
    """Run the FastAPI backend server"""
    try:
        print(f"Starting FastAPI server on http://0.0.0.0:{PORT}...")
        os.chdir(os.path.join(os.path.dirname(__file__), "app"))
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(PORT), "--reload"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting FastAPI server: {e}")
        sys.exit(1)

def run_streamlit():
    """Run the Streamlit frontend server"""
    try:
        print("Starting Streamlit server...")
        os.chdir(os.path.join(os.path.dirname(__file__), "frontend"))
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit server: {e}")
        sys.exit(1)

def main():
    # Store the original working directory
    original_dir = os.getcwd()

    try:
        # Start FastAPI server in a separate thread
        fastapi_thread = Thread(target=run_fastapi)
        fastapi_thread.start()

        # Wait for FastAPI server to be ready
        if not check_server(f"http://127.0.0.1:{PORT}"):
            print(f"Failed to start FastAPI server on port {PORT}. Please check the server logs.")
            sys.exit(1)

        # Start Streamlit server
        streamlit_thread = Thread(target=run_streamlit)
        streamlit_thread.start()

        # Keep the main thread alive
        fastapi_thread.join()
        streamlit_thread.join()

    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # Restore the original working directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
