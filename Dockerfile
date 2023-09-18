# Use the official Python image as the base image
FROM python:3.9


# Set the working directory inside the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . /app

EXPOSE 8000

RUN pip install -r requirements.txt


# Define the command to start the application
ENTRYPOINT ["./entrypoint.sh"]
