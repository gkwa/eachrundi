# eachrundi

## Summary

Learn how to use ansible galaxy to install ansible collections from a private gitlab repo.


## Motivation

### Learn about ansible collections


Ansible molecule [quickstart guide](https://ansible.readthedocs.io/projects/molecule/getting-started/) starts from the perspective that you should run molecule with an ansible collection.

I've never used ansible collections before, nor do I really know why molecule suggests them but I'm curious what benefit they provide over ansible roles--something I am familiar with.

Lots of fumbling later, I see how to get started.  Now I can start learning to use molecule and eventually iterate on `elasticsearch-certutil` which is my original motivation to use ansible.

### Learn about jinja2 template inheritance


Also I needed reason to learn jinja2 template inheritance better.  There are so many places its helpful.


### Learn about ansible execution environments

Now that I know to fetch collections from a private gitlab repo, I expect
this `execution-environment.yml` to work.

...havent yet tried it, thats next step.





```log
# file: execution-environment.yml
...
  galaxy:
    collections:
    - name: 'https://gitlab.com/streambox/faris.git#collections/ansible_collections/foo'
...
```

from https://ansible.readthedocs.io/en/latest/getting_started_ee/build_execution_environment/










```log
cat > execution-environment.yml<<EOF
version: 3

images:
  base_image:
    name: quay.io/fedora/fedora:latest

dependencies:
  ansible_core:
    package_pip: ansible-core
  ansible_runner:
    package_pip: ansible-runner
  system:
  - openssh-clients
  - sshpass
  galaxy:
    collections:
    - name: community.postgresql
EOF

```







## Purpose

Learn how to use ansible galaxy to install ansible collections from a private gitlab repo.


Create gitlab deploy token for your project (eg `streambox/faris`) on repository settings page manually
or using glab cli.



Manually, you'd go here: https://gitlab.com/streambox/faris/-/settings/repository

Suppose your deploy token was this:
```log
username:
gitlab+deploy-token-4103568

token:
gldt-yr9ZrxAKDFfai5EBKTnR
```



Then this works:
```log
# file: ~/.gitconfig:
[credential]
        helper = store --file /root/.my-credentials

# file: ~/.my-credentials:
https://gitlab+deploy-token-4103568:gldt-yr9ZrxAKDFfai5EBKTnR@gitlab.com

# file: ~/my_project/requirements.yml:
collections:
- name: 'https://gitlab.com/streambox/faris.git#collections/ansible_collections/foo'
  type: git
  version: master

# file: ~/my_project/run_test.sh:
timeout --verbose 10s ansible-galaxy collection install --requirements-file=requirements.yml

```

So, once those files are deployed, then you'd run

```bash
cd ~/my_project/
timeout --verbose 10s ansible-galaxy collection install --requirements-file=requirements.yml

```



## Usage

### Setup

`make test` does these steps:

- create gitlab deploy token for project `streambox/faris` using glab cli
- create docker container with ansible, ansible-galaxy and molecule installed
- put our new secret gitlab deploy token onto container
- run `ansible-galaxy` to install collection from private gitlab repo




```bash
make test
```

### Whats with this weird directory structure and url?


### Directory structure


> One of the recommended ways to create a collection is to place it under a collections/ansible_collections directory. If you don't put your collection into a directory named ansible_collections, molecule won't be able to find your role.

from  https://ansible.readthedocs.io/projects/molecule/getting-started/

### `requirements.yml` has weird url

```
collections:
- name: 'https://gitlab.com/streambox/faris.git#collections/ansible_collections/foo'
  type: git
  version: master

```

The format of the url is described in https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html#specifying-the-collection-location-within-the-git-repository

```bash
mkdir -p streambox/faris/collections/ansible_collections
cd streambox/faris

git init && git remote add origin git@gitlab.com:streambox/faris.git

rye init
rye add molecule
rye sync
. .venv/bin/activate
ansible --version
molecule --version
cd collections/ansible_collections
ansible-galaxy collection init foo.bar # create new collection bar in namespace foo
```

With that this url will render https://gitlab.com/streambox/faris.git#collections/ansible_collections/foo

### Inspection

```bash
make test
docker run --rm -ti emeraldchanter:latest bash
```

### Teardown



`make cleanup` does these steps:

- delete gitlab deploy token for project `streambox/faris`
- delete output directory


```bash
make clean
```



## Todo

- https://www.google.com/search?q=github+markdown+toc+generator&oq=github+markdown+toc&gs_lcrp=EgZjaHJvbWUqBwgBEAAYgAQyCQgAEEUYORiABDIHCAEQABiABDIICAIQABgWGB4yCAgDEAAYFhgeMggIBBAAGBYYHjIGCAUQRRhBMgYIBhBFGEEyBggHEEUYQdIBCDYwOTdqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8



## Miscellany

### Generate deploy keys (not deploy tokens)

```bash
eachrundi; bash output/generate_deploy_keys.sh
ls output/id_ed25519 output/id_ed25519.pub

eachrundi; bash output/cleanup_deploy_keys.sh
```
