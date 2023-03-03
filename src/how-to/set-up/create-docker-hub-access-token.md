# Creating a Docker Hub Access Token

During the initial AppPack set up, you'll be prompted for a Docker Hub username and access token. These are required to download the base images for the [Heroku buildpacks](https://hub.docker.com/u/heroku) used by AppPack while avoiding [Docker Hub's anonymous download rate limits](https://docs.docker.com/docker-hub/download-rate-limit/).

1. Create a free Personal account at [https://hub.docker.com/signup](https://hub.docker.com/signup)
2. Click "New Access Token" at [https://hub.docker.com/settings/security](https://hub.docker.com/settings/security)
3. In the pop-up, give your token a description ("apppack" is fine), select `Public Repo Read-only`, and click "Generate"
4. Copy the person access token (it should start with `dckr_pat_`)