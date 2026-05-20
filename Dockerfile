
FROM python:3.11-slim

#Create a folder called app in the cointainer 
WORKDIR /app

#Coppy necessary tools 
COPY requirements.txt .

#Dowload necessary tools 
RUN pip install --no-cache-dir -r requirements.txt

#Coppy all files to the cointainer 
COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "vietnam:app"]