# Chat App
Simple chat app

## To Run This Project Locally
```bash
git clone https://github.com/MKisil/chat_app.git
```
```bash
cd chat_app
```
```bash
docker compose run --rm chat-app sh -c "python manage.py makemigrations chat"
```
```bash
docker compose run --rm chat-app sh -c "python manage.py migrate"
```
```bash
docker compose up
```
After setup, visit [127.0.0.1](http://127.0.0.1) in your browser.
