# Pymdown-Include

I tried hard to make the base name of the file to be included in the search
path, but I couldn't figure out how to do that. During the "preprocessor"
phase, I have no information about the file being processed. I just have the
content of the file as an array of lines.

## Some useful comands for developing

```
poetry install
poetry build
poetry run pytest
poetry run pytest --cov=pymdown_include
```