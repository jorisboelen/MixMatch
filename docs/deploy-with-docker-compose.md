# Deploy with Docker Compose

## System Requirements
* An x86_64 based Linux system
* At least 1GB of free memory

> For importing a large music library a recent multicore cpu is recommended

## Getting started
### Prerequisites
Make sure the following software is installed:

* Docker Engine : <https://docs.docker.com/engine/install>
* Docker Compose : <https://docs.docker.com/compose/install>

### Install MixMatch
Create a folder for the MixMatch application. The recommended path is ``/opt/mixmatch``:

```shell
mkdir /opt/mixmatch
```

In addition, create subfolders for storing music and image files:

```shell
mkdir /opt/mixmatch/image
mkdir /opt/mixmatch/music
mkdir /opt/mixmatch/postgresql
```

Download the following file and place it in the mixmatch folder:

* [docker-compose.yml](resources/docker-compose.yml)

```shell
mv docker-compose.yml /opt/mixmatch/
```

### Start MixMatch
Use [docker-compose](https://docs.docker.com/compose/) to launch the application:

```shell
cd /opt/mixmatch
docker compose up
```

By default, the webinterface is available on https://localhost:4433. Login with username: `mixmatch`
password: `mixmatch`.

### Configure MixMatch
Configuration settings can be set by creating a `.env` file in the application directory (`/opt/mixmatch`).

| Setting                | Default Value | Description                                                                                                             |
|------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------|
| MIXMATCH_PROXYPROTOCOL | `false`       | [PROXY protocol] enables NGINX to receive client connection information passed through proxy servers and load balancers |
| MIXMATCH_PUID          | `1000`        | The UserID, refer to `Storage Settings` for more details                                                                |
| MIXMATCH_PGID          | `1000`        | The GroupID, refer to `Storage Settings` for more details                                                               |
| POSTGRES_DB            | `mixmatch`    | The name of the postgresql database                                                                                     |
| POSTGRES_USER          | `mixmatch`    | The username for connecting to the postgresql database server                                                           |
| POSTGRES_PASSWORD      | `mixmatch`    | The password for connecting to the postgresql database server                                                           |
| RABBITMQ_DEFAULT_USER  | `mixmatch`    | The username for connecting to the rabbitmq broker                                                                      |
| RABBITMQ_DEFAULT_PASS  | `mixmatch`    | The password for connecting to the rabbitmq broker                                                                      |

#### Storage Settings
The path on the local filesystem where music is read from, and images and database files are stored, can be adjusted.

| Setting               | Default Value  | Description                                              |
|-----------------------|----------------|----------------------------------------------------------|
| MIXMATCH_VOLUME_IMAGE | `./image`      | The directory where image files are stored               |
| MIXMATCH_VOLUME_MUSIC | `./music`      | The directory where music files are imported from        |
| POSTGRES_VOLUME       | `./postgresql` | The directory where postgresql database files are stored |

Ensure any volume directories on the host are owned by the same user you specify in the `MIXMATCH_PUID` and `MIXMATCH_PGID` settings.
To find the correct value for user use the `id your_username` command as below:

```shell
id your_user
```

Example output:

```shell
uid=1000(your_user) gid=1000(your_user) groups=1000(your_user)
```

#### SSL Configuration
By default, a self-signed certificate is generated for `localhost`. To expose the service on a custom
domain name with a custom certificate adjust the settings as below.

| Setting                 | Value         | Description                                                                              |
|-------------------------|---------------|------------------------------------------------------------------------------------------|
| MIXMATCH_HOSTNAME       | `example.com` | Adjust to the hostname the service will be exposed on, ensure it matches the certificate |
| MIXMATCH_SSL_SELFSIGNED | `false`       | Disable generation of a self-signed certificate                                          |

In addition, bind a local directory to the path `./data/ssl` on the `mixmatch-web` container.

```yaml
services:
    web:
        container_name: mixmatch-web
        volumes:
            - /path/to/ssl/certificates:/data/ssl
```

Ensure the certificate files are named: `server.crt` and `server.key`.

[PROXY protocol]: https://docs.nginx.com/nginx/admin-guide/load-balancer/using-proxy-protocol/
