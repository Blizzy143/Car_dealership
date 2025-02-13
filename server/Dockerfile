# Base Image
FROM python:3.12.0-slim-bookworm

# Environment Variables
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app

# Set Work Directory
WORKDIR $APP

# Copy Requirements File and Install Dependencies
COPY requirements.txt $APP
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the Project Files
COPY . $APP

# Expose Port
EXPOSE 8000

# Set Permissions and Entrypoint
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

# Start Gunicorn Server
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]