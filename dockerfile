# Specify what version of python to use.
FROM python:3.11

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 7860 available to the world outside this container
# EXPOSE 7860

# Run gradio command to start the Gradio app
CMD ["python", "chat.py"]
