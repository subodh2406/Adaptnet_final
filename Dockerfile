# FROM python:3.9-slim

# WORKDIR /app

# # Copy requirements first to leverage Docker cache
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application
# COPY . .

# # Make port available to the world outside this container
# EXPOSE $PORT

# # Run the application
# CMD ["python", "render_app.py"]


# Use a Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# Expose the necessary port
EXPOSE 8000 8501

# Command to run FastAPI server and Streamlit server
CMD ["python", "render_app.py"]
