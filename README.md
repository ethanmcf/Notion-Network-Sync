This is a monorepo, containerizes two apps with docker and runs them with different cronjobs
docker compose build linkedin-scraper
docker compose up linkedin-scraper

docker compose build notion-poller
docker compose up notion-poller
