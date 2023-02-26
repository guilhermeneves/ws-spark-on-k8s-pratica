### Usando Bind mount
    docker run -it --rm -d --name web -p 8080:80 -v ./labs/0_docker:/usr/share/nginx/html nginx

### Usando Volumes
    docker volume ls
    docker volume create spok-workshop
    docker run -it --rm -d --name web -p 8080:80 -v site-content:/usr/share/nginx/html nginx
    docker inspect volume spok-workshop