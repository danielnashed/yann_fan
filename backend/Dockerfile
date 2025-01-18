# Use the official AWS Lambda Python 3.11 runtime image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory inside the container
WORKDIR /var/task

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the source code into the container
COPY . .

# Set the default command to the Lambda handler function
CMD ["lambda_function.handler"]