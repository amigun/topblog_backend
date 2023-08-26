Когда запускаем впервые:
```bash
docker compose up
```

Когда делаем изменения в коде и хотим, чтобы они применились:
```bash
docker stop $(docker ps -qa)  # остановить все текущие контейнеры
docker rm $(docker ps -qa)  # удалить все текущие контейнеры
docker compose up --build --force-recreate  # перебилдить и запустить сервисы
```