# Baremetal

## GCP

### Requirements

- gcloud CLI
- terraform

### gcloud CLI

Install gcloud CLI ([Instructions](https://cloud.google.com/sdk/docs/install)).

Once installed initialize it using

```bash
gcloud init
```

It will ask you to authenticate and select an `GCP` project.
(don't worry you can change between projects freely)

> You can query current selected project with

```bash
gcloud config get project
```

> and set the project with

```bash
gcloud config set <project-id>
```

Setup your application default credentials

```bash
gcloud auth application-default login
```

It will tell you where the credentials are stored, and the `GCP provider`
will inform `Terraform` about these credentials to authenticate to `GCP`.

### Deployment

> NOTE: enable `GCP Compute Engine`
> You might also need to enable billing...

```bash
gcloud services enable compute
```

Create an ssh key to connect to the servers

```bash
ssh-keygen -t ed25519 -C "email@example.com"
```

put it into `cloud-config.yml`

> NOTE: debian 12 seems to not being able to provision with `cloud-init`

You can create an entry into `~/.ssh/config` with

```ssh
Host <hostname>
  IdentityFile <path-to-private-ssh-key>
  HostName <public-ip>
  User <username>
```

## Terraform

> NOTE: When using Terraform make sure to have an unique terrafrom.tfstate
> SYNCED acrouss your team

Recreate a resource

```bash
terraform apply -replace="resource"
```
