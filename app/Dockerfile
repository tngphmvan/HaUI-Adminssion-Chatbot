# Sử dụng Python làm base image
FROM python:3.11-slim

# set the working directory in the container
WORKDIR /app

# Copy file requirements.txt vào container
COPY requirements.txt .

# Install essential packages
RUN pip install --no-cache-dir -r requirements.txt

# copy all the files to the container
COPY . .

# expose the port 8000
EXPOSE 8000:8000

# command to run on container start
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "4" ]

