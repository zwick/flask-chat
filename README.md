# Instructions

## Running as Python application
To install run this app directly, install the requirements via pip in requirements.txt. You should preferably do this 
using a Virtual Environment.

```
pip install -r requirements.txt
```

Then, run the app.

```
flask run -p 8000
```

View the app in your web browser at http://127.0.0.1:8000/. Open multiple tabs to simulate multiple clients connected 
to the chat.

## Running via Docker
To run this app via Docker, you need to have Docker installed on your machine. Then, run the app using the supplied
Docker Compose file. 

```
docker compose up
```

View the app in your web browser at the address listed. Open multiple tabs to simulate multiple clients connected 
to the chat.

