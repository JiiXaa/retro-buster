# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV DATABASE_URI=postgres://zlpxkbai:CLDWp-H_C8CKssEmZ0pPnj197EabSlUn@trumpet.db.elephantsql.com/zlpxkbai

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the command to start the Flask app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]