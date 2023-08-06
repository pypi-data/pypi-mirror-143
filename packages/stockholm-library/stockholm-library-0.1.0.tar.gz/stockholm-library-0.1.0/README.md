# Stockholm-Library

[![License][license_img]][license_target]
[![Latest PyPI version][pypi_version_img]][pypi_version_target]
[![PyPI status][pypi_status_img]][pypi_status_target]


[license_target]: https://raw.githubusercontent.com/vonNiklasson/stockholm-library/develop/LICENSE
[license_img]: https://img.shields.io/pypi/l/stockholm-library.svg

[pypi_version_target]: https://pypi.python.org/pypi/stockholm-library/
[pypi_version_img]: https://img.shields.io/pypi/v/stockholm-library.svg

[pypi_status_target]: https://pypi.python.org/pypi/stockholm-library/
[pypi_status_img]: https://img.shields.io/pypi/status/stockholm-library.svg

Unofficial SDK for interacting with [Stockholm Library](https://biblioteket.stockholm.se)

> Currently the project is in very early development and very little 
> functionality can be used. But if you are eager to get stuff going, 
> please consider helping out by [contributing](#contributing)!


## Usage

### Connecting

#### Connecting with credentials

The simplest way to connect with the client is through credentials.

```python
from stockholm_library import Client

client = Client()
success: bool = client.login(
    user="",
    pin="1234"
)
print(success)  # True
```

#### Fetching loaned books

```python
client.get_loans()
```


  
## Contributing

Contributions are always welcome!

To contribute, please take the following steps:

1. [Fork](https://github.com/vonNiklasson/stockholm-library/fork) the repo
2. Add your change
3. Make a pull request with a short description of the change you're proposing.


## Authors

- [@vonNiklasson](https://www.github.com/vonNiklasson)

  