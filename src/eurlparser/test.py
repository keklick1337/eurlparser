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
