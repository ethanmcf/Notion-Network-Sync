docker build -t linkedin-notion-sync .
docker run --env-file .env linkedin-notion-sync
