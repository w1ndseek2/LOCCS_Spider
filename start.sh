pip3 install coloredlogs pyredis

sudo docker run --rm -d --name redis -v ./data:/data -p 6379:6379 redis --requirepass 'your_password'
