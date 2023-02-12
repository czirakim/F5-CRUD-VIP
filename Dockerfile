# Use an official ubuntu image as the base image
FROM ubuntu:latest

# specify shell
#SHELL ["/bin/bash", "-c"]

# This line adds the Jenkins user to the /etc/sudoers file, allowing it to run sudo commands without a password prompt
#RUN echo "jenkins ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers



# Install dependencies
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get install -y python3.10 python3-pip


# Install Jenkins
#RUN wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | gpg --dearmor -o /usr/share/keyrings/jenkins.gpg && \
#    sh -c 'echo deb [signed-by=/usr/share/keyrings/jenkins.gpg] http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list' && \
#    apt update && \
#    apt-get install -y jenkins 


# start jenkins
#RUN service jenkins start  

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the image
COPY requirements.txt /app/

# Install the packages listed in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the files to the image
#COPY . /app/

# Expose Jenkins on port 8080
#EXPOSE 8080

# specify shell
SHELL ["/bin/bash", "-c"]

# Run a bash shell when the container is started
CMD ["/bin/bash"]