# AsyncWebApp-Backend

## COMMANDS

### Generate the key ssh on Linux Centos

```bash
ssh-keygen -t rsa -b 4096
```


### Pyenv on Linux Centos

Run

```bash
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

and then in the `.bashrc` file, configure...


```bash
export PATH="$HOME/.pyenv/bin:$PATH"
export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

```


### Quick Set Up

After clonning the repository it's enough to do

```bash
  pyenv local 3.9.6
  ```

  ```bash
  python -m venv .venv
  ```

  ```bash
  .venv\Scripts\activate
  ```

  ```bash
  python -m pip install pip-tools&pip install --upgrade pip-tools
  ```

  ```bash
  pip install --no-cache-dir -U pip setuptools wheel
  ```

  ```bash
  pip install -r pip/with-dep/requirements-dev.txt
  ```

  *** Extra for generate dependencies we can use...
  ```bash
  pip-compile --output-file=app/pip/with-dep/requirements-prod.txt app/pip/no-dep/requirements-prod.txt
  ```

  ```bash
  pip-compile --output-file=app/pip/with-dep/requirements-dev.txt app/pip/no-dep/requirements-dev.txt
  ```