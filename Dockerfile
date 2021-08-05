FROM python:3.9.6

WORKDIR /usr/src/app

# Copy all app code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Database configuration
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
