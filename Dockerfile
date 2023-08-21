# Use the official Python image as a base image
FROM python:3.10-bookworm

# Copy the current directory contents inside the container at /app/woorichApp
COPY . /app/woorichApp/

# Change directory to /app/woorichApp inside the container
WORKDIR /app/woorichApp

# Copy the requirements file outside the container into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for RDS connection
ENV RDS_HOST woorichdb.co53lyqqsjas.ap-northeast-2.rds.amazonaws.com
ENV RDS_PORT 3306
ENV RDS_DB_NAME woorichDB
ENV RDS_USERNAME woorich
ENV RDS_PASSWORD 12345678
ENV FLASK_APP woorichApp

# Run the Flask application
CMD ["flask", "run"]
