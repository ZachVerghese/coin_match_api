FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# create root directory for our project in the container
RUN mkdir /src

# Set the working directory to /src
WORKDIR /src

# Copy the current directory contents into the container at /src
ADD ./coin_match /src/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt