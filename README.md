# Enhanced URL Parser

A powerful URL parser with detailed analysis.

## Features

- Parse URLs into components like protocol, host, path, query, and fragment.
- Supports both IPv4 and IPv6 addresses.
- Handles URLs with or without protocols.
- Reconstruct the URL from parsed components.

## Installation

```bash
pip install eurlparser
```

## Usage
Here's how to use the `EnhancedURLParser` class to parse and analyze URLs.

## Basic Example
```python
from eurlparser import EnhancedURLParser

# Example URL
url = "https://user:password@www.example.com:8080/path/to/resource?query=python&foo=bar#section"

# Initialize the parser
parser = EnhancedURLParser(url)

# Access different components
print("Protocol:", parser.protocol)            # Output: https
print("Username:", parser.username)            # Output: user
print("Password:", parser.password)            # Output: password
print("Host:", parser.host)                    # Output: www.example.com
print("Port:", parser.port)                    # Output: 8080
print("Path:", parser.path)                    # Output: /path/to/resource
print("Query:", parser.query)                  # Output: {'query': ['python'], 'foo': ['bar']}
print("Fragment:", parser.fragment)            # Output: section

# Reconstruct the URL
reconstructed_url = parser.get_fixed_url()
print("Reconstructed URL:", reconstructed_url)
# Output: https://user:password@www.example.com:8080/path/to/resource?query=python&foo=bar#section

# Get a structured dictionary of the URL components
url_structure = parser.get_url_structure()
print("URL Structure:", url_structure)
```

## Handling URLs Without Protocol
```python
from eurlparser import EnhancedURLParser

# Example URL without protocol
url = "/www.example.com/path/to/resource?query=python"

# Initialize the parser
parser = EnhancedURLParser(url)

# Access components
print("Host:", parser.host)                    # Output: www.example.com
print("Path:", parser.path)                    # Output: /path/to/resource
print("Query:", parser.query)                  # Output: {'query': ['python']}

# Reconstruct the URL (defaults to path '/')
reconstructed_url = parser.get_fixed_url()
print("Reconstructed URL:", reconstructed_url)
# Output: www.example.com/path/to/resource?query=python
```

## Parsing and Handling IPv6 Addresses
``python
from eurlparser import EnhancedURLParser

# Example URL with IPv6 address
url = "http://[2001:db8::1]:8080/path?query=value"

# Initialize the parser
parser = EnhancedURLParser(url)

# Access components
print("Protocol:", parser.protocol)            # Output: http
print("Host:", parser.host)                    # Output: 2001:db8::1
print("Port:", parser.port)                    # Output: 8080
print("Path:", parser.path)                    # Output: /path
print("Query:", parser.query)                  # Output: {'query': ['value']}

# Reconstruct the URL
reconstructed_url = parser.get_fixed_url()
print("Reconstructed URL:", reconstructed_url)
# Output: http://[2001:db8::1]:8080/path?query=value
```

# Handling Invalid or Unusual URLs
```python
from eurlparser import EnhancedURLParser

# Example of an invalid protocol in the URL
url = "ht@tp://example.com/path"

# Initialize the parser
parser = EnhancedURLParser(url)

# Access components
print("Host:", parser.host)                    # Output: example.com
print("Path:", parser.path)                    # Output: /path
print("Protocol:", parser.protocol)            # Output: None (invalid protocol)

# Even with unusual inputs, the URL can be reconstructed correctly:
reconstructed_url = parser.get_fixed_url()
print("Reconstructed URL:", reconstructed_url)
# Output: example.com/path
```

## Contribution
Feel free to contribute to the project by forking the repository and creating pull requests. If you encounter any issues or have suggestions, please open an issue on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
