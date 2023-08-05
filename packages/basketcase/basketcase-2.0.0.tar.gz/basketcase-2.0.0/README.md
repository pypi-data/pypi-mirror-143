# BasketCase
Fetch resources from Instagram.

Downloads images and videos in their highest quality. You will need to authenticate in order to avoid rate limits and access controls.

Known limitations:
- Stories and highlights are not supported yet.
- Although two-factor authentication is supported, only the `totp` method has been tested.

## Installation and usage
1. Install it from [PyPI](https://pypi.org/project/basketcase/).

```sh
pip install basketcase
```

> This will put the executable `basketcase` on your PATH.

2. Create a text file (e.g. `basketcase.txt`) and populate it with resource URLs.

```
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
```

3. Pass the file as a positional argument. The `-l` flag means it will attempt to login first.

```sh
basketcase -l ./basketcase.txt
```

> Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase_{timestamp}/`).

## Development setup
1. `cd` to the project root and create a virtual environment in a directory named `venv`, which is conveniently ignored in version control.
2. Install the dependencies.

```sh
pip install -r requirements.txt
```

3. Install this package in editable mode.

```sh
pip install -e .
```

### Package build and upload
1. Update the requirements list.

```sh
pip freeze --exclude-editable > requirements.txt
```

2. Increment the version on `setup.cfg`.
3. Build and upload to PyPI.

```sh
python -m build
python -m twine upload dist/*
```

4. Commit and push the changes (and the new version tag) to the git repository.

