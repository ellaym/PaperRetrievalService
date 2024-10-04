# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first (this ensures Docker cache works for dependencies)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5502

# Set environment variables (optional, if using them)
# ENV FLASK_ENV=production

# Run the Flask app
CMD ["python", "main.py"]
