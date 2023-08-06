# HERE OAuth

`here_oauth` returns an oauth token for [HERE Technologies](https://platform.here.com) APIs.

## Requirements

A HERE [credential file](https://platform.here.com/management/projects).  

## Usage

```python
from here_oauth import here_oauth

token = here_oauth("credential_file")
print(token)
```

