docker build -t bdbt-postgres:1.0 ./postgres
docker build -t bdbt-app-image:1.0 ./site
docker-compose up -d
docker ps