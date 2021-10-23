# AppPack Docs

To build locally, you'll need:

* Python 3.9
* [PDM](https://pdm.fming.dev/#installation)

Run:

```shell
pdm sync
pdm run mkdocs serve
```

## Deployment

Deployment is handled by GitHub actions. Push to `deploy/prod` to trigger,

```
git push origin main:deploy/prod
```
