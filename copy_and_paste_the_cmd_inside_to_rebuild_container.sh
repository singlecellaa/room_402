docker rm -f room_402-django
docker image rm room_402
docker build -t room_402 .
docker run -it --network=traefik --label "traefik.enable=true" --label "traefik.http.routers.room402.rule=Host(\`api.room402.temp.ziqiang.net.cn\`)" --label "traefik.http.routers.room402.entrypoints=websecure" --label "traefik.http.services.room402.loadbalancer.server.port=8086" --name room_402-django room_402