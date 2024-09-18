
source ecs.config

sudo systemctl start podman.socket
sudo setenforce 0

sudo chmod 755 /var/run/podman
sudo chown root:root /var/run/podman
sudo chmod 660 /var/run/podman/podman.sock

docker run --name ecs-agent \
  --detach \
  --env ECS_CLUSTER=$ECS_CLUSTER \
  --env ECS_BACKEND_HOST="" \
  --env ECS_CONFIG_FILE=/etc/ecs/ecs.config \
  --volume ./ecs.config:/etc/ecs/ecs.config \
  --volume /var/run/podman/podman.sock:/var/run/docker.sock \
  --volume ./data:/data \
  amazon/amazon-ecs-agent:latest
