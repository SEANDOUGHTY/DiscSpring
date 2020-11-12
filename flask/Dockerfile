# Use the Python3.8.2 image
FROM tiangolo/uwsgi-nginx:python3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

RUN ls
# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]