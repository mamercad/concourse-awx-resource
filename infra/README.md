# Infra stuff (for local dev)

The [Makefile](Makefile) might help, there's also [.envrc.example](.envrc) (below) if you use [direnv](https://github.com/direnv/direnv) or something similar.

```bash
❯ make help
help:  Shows this help
status:  Shows Concourse status
up:  Spins up Concourse in Docker compose
login:  Set the fly Concourse target
forget:  Delete the fly Concourse target
down:  Spins down Concourse
nuke:  Nukes Concourse from Docker compose
crypto:  Generates Docker registry crypto
```

```bash
❯ cat .envrc.example
export CONCOURSE_TARGET="tutorial"
export CONCOURSE_EXTERNAL_URL="http://localhost:8080"
export CONCOURSE_ADD_LOCAL_USER="<user>:<password>"
export CONCOURSE_MAIN_TEAM_LOCAL_USER="<user>"
export CONCOURSE_MAIN_TEAM_LOCAL_PASS="<password>"
export CONCOURSE_CLIENT_SECRET="<supersecret>"
export CONCOURSE_TSA_CLIENT_SECRET="<supersecret>"
export REGISTRY_CRT="registry.crt"
export REGISTRY_KEY="registry.key"
export REGISTRY_COUNTRY="US"
export REGISTRY_STATE="MI"
export REGISTRY_LOCALITY="Detroit"
export REGISTRY_ORGANIZATION="ACME"
export REGISTRY_CANONICAL_NAME="registry"
```
