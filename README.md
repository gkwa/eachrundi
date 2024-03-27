# eachrundi

## Purpose

Learn how to use ansible galaxy to install ansible collection from a private gitlab repo

tl;dr

```log
# file: ~/.gitconfig:
[credential]
        helper = store --file /root/.my-credentials

# file: ~/.my-credentials:
https://gitlab+deploy-token-4103568:gldt-yr9ZrxAKDFfai5EBKTnR@gitlab.com

# file: ~/my_project/run_test.sh:
timeout --verbose 10s ansible-galaxy collection install --requirements-file=requirements.yml

# file: ~/my_project/requirements.yml:
collections:
- name: 'https://gitlab.com/streambox/faris.git#collections/ansible_collections/foo'
  type: git
  version: master
```

- use glab to create deploy token

## Usage

```bash
make
```

Cleanup:

```bash
make clean
```
