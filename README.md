## Development

### Using a virtual environment

Create a virtual environment

```bash
python3 -m venv venv
```

Activate the virtual environment

```bash
source venv/bin/activate
```

Deactivate the virtual environment

```bash
deactivate
```

### Adding a dependency

From an activated virtual environment

```bash
pip install <the-dep>
```

### Saving and installing dependencies

Use

```bash
pip freeze > requirements.txt
```

to save project dependencies to a file and

```bash
pip install -r requirements.txt 
```

to install them.