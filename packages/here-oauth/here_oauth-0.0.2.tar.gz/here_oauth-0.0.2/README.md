# HERE OAuth

`here_oauth` returns an oauth token for [HERE Technologies](https://platform.here.com) APIs.

## Requirements

A HERE [credential file](https://developer.here.com/tutorials/how-to-authenticate-with-here-oauth/#generating-here-oauth-credentials).  

## Install

```bash
$ pip install here_oauth
```

## Usage

```python
from here_oauth import here_oauth

token = here_oauth.get_token("credential_file")
print(token)
```

