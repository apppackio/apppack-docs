# AppPack Docs

To build locally, you'll need:

* Python 3.14
* [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

Run:

```shell
uv sync
make run
```

## Deployment

Deployment is handled by GitHub actions. Push to `deploy/prod` to trigger,

```
git push origin main:deploy/prod
```
