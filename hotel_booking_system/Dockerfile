# Use an official Ubuntu as a parent image
FROM ubuntu:20.04
# Set environment variables to avoid user interaction during package installation
ENV DEBIAN_FRONTEND=noninteractive
# Install dependencies, including netcat
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev libpq-dev netcat && \
    apt-get clean
# Set the working directory
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh
# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh
# Expose port 8000
EXPOSE 8000
# Use the entrypoint script to handle migrations and server startup
ENTRYPOINT ["/app/entrypoint.sh"]





