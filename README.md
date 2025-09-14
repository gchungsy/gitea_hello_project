
### Add Runner
```
docker run -d -e GITEA_INSTANCE_URL=http://192.168.1.21:3000/ -e GITEA_RUNNER_REGISTRATION_TOKEN=NaaKk9Jyi3AOo1ZUu7Ba6v5jqQCgbqhzRWB4cKvY -v /var/run/docker.sock:/var/run/docker.sock --name my_runner6 gitea/act_runner:nightly
```