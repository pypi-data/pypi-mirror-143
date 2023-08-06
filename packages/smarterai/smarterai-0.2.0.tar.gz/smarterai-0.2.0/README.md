[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.org/project/pip/)

# Smarter API for Python

This API allows communication between any python based Flex component on the [smarter.ai](https://www.smarter.ai/)
platform.

## User Installation

The latest released version are available at the Python Package Index (PyPI).

To install using pip:

```bash
pip install smarterai
```

## Usage

- For starters an account needs to be created at our platform. So visit our website and create an account
  at [smarter.ai](https://www.smarter.ai/).

- Then in order for the Flex's code to be accessible for the [smarter.ai](https://www.smarter.ai/) platform, follow
  these steps:
    1. Visit the [Studio](https://studio.smarter.ai/digital_twin)
    2. Create a [new Flex](https://studio.smarter.ai/digital_twin/newArtifact)
    3. Chose a code-based template of your choosing.
    4. Follow the wizard and make sure to choose ```Python 3.6``` as the programming Language.
    5. Go to Project -> Code and write/upload your code there.

- You can then start building your Flex's code by copy-pasting the code found in the examples below.

- The Flex's interface needs to consist of the following:
    1. Import ```smarterai```:
        ```python
            from smarterai import *
        ```
    2. A class called ```SmarterFlex```.
    2. ```SmarterFlex``` should inherit from ```SmarterPlugin```:
        ```python
            class SmarterComponent(SmarterPlugin):
        ```
    3. The class should have a method ```invoke``` with the following signature:
        ```python
            def invoke(self, port: str, message: SmarterMessage, smarter_sender: SmarterSender) -> Optional[SmarterMessage]:
        ```

### Example 1

This is the basic interface for a python based Flex.

```python
from smarterai import *


class SmarterComponent(SmarterPlugin):
    def invoke(self, port: str, message: SmarterMessage, smarter_sender: SmarterSender) -> Optional[SmarterMessage]:
        print("Received the message '{0}' on port '{1}'".format(message, port))
        return
```

### Example 2

If your Flex needs initializing/booting before it starts running. Then a method ```boot``` needs to be defined.

```python
from smarterai import *


class SmarterComponent(SmarterPlugin):
    def __init__(self):
        self.port_fn_mapper = {'boot': self.boot}

    def boot(self, message: SmarterMessage, smarter_sender: SmarterSender) -> Optional[SmarterMessage]:
        # Write code here
        return

    def invoke(self, port: str, message: SmarterMessage, smarter_sender: SmarterSender) -> Optional[SmarterMessage]:
        print("Received the message '{0}' on port '{1}'".format(message, port))
        self.port_fn_mapper[port](message, smarter_sender)
        return
```

## Credits

Authored by Nevine Soliman and Carlos Medina (smarter.ai - All rights reserved)