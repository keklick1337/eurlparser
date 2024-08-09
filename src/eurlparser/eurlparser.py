import re
from urllib.parse import parse_qs, quote
from typing import Optional, List, Dict

# Precompiled regular expressions
PROTOCOL_PATTERN = re.compile(r'^(?P<protocol>[a-zA-Z][a-zA-Z0-9+\-.]*)://')
IPV4_PATTERN = re.compile(
    r'^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
    r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
    r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
    r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$'
)
IPV6_PATTERN = re.compile(r'^\[([a-fA-F0-9:]+)\]$')
HOST_PORT_PATTERN = re.compile(r'^(?P<host>[^:/?#]+|\[[a-fA-F0-9:]+\])(?::(?P<port>\d+))?$')

class EnhancedURLParser:
    """
    A class to parse and analyze URLs into their components.

    Attributes:
        original_url (str): The original URL provided by the user.
        protocol (Optional[str]): The protocol/scheme of the URL (e.g., 'http', 'https').
        username (Optional[str]): The username in the URL, if present.
        password (Optional[str]): The password in the URL, if present.
        host (Optional[str]): The host (domain or IP address) of the URL.
        port (Optional[str]): The port of the URL, if present.
        path (Optional[str]): The path of the URL.
        path_array (Optional[List[str]]): The path split into components.
        query (Optional[Dict[str, List[str]]]): The query parameters of the URL.
        query_array (Optional[List[str]]): The query parameters split into key-value pairs.
        fragment (Optional[str]): The fragment of the URL, if present.
        tld (Optional[str]): The top-level domain (TLD) of the host, if applicable.
        main_domain (Optional[str]): The main domain of the host.
        subdomains (List[str]): The subdomains of the host.
        host_ipaddress (Optional[str]): The IP address of the host, if the host is an IP address.
        urlparams (Optional[List[str]]): URL parameters if present.
        full_domain (Optional[str]): The full domain of the host.
    """
    def __init__(self, url: str) -> None:
        self.original_url: str = url
        self.protocol: Optional[str] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.host: Optional[str] = None
        self.port: Optional[str] = None
        self.path: Optional[str] = None
        self.path_array: Optional[List[str]] = None
        self.query: Optional[Dict[str, List[str]]] = None
        self.query_array: Optional[List[str]] = None
        self.fragment: Optional[str] = None
        self.tld: Optional[str] = None
        self.main_domain: Optional[str] = None
        self.subdomains: List[str] = []
        self.host_ipaddress: Optional[str] = None
        self.urlparams: Optional[List[str]] = None
        self.full_domain: Optional[str] = None
        self.parse_url()

    def parse_url(self) -> None:
        """Parses the URL into its components."""
        url = self.original_url.strip()

        # Handle cases with one or two leading slashes
        if url.startswith("//"):
            url = url[2:]
        elif url.startswith("/"):
            url = url[1:]

        # Extract protocol
        protocol_match = PROTOCOL_PATTERN.match(url)
        if protocol_match:
            self.protocol = protocol_match.group('protocol')
            url = url[len(protocol_match.group(0)):]

        # Extract fragment (after #)
        if '#' in url:
            url, self.fragment = url.split('#', 1)

        # Extract query (after ?)
        if '?' in url:
            url, query_string = url.split('?', 1)
            self.query = parse_qs(query_string, keep_blank_values=True)  # FIX: Preserve empty query parameters
            self.query_array = query_string.split('&')

        # Extract host, port, and path
        url_splited = url.split('://', 1)[-1]
        if '/' in url:
            self.host, self.path = url_splited.split('@')[-1].split('/', 1)
            self.path = '/' + self.path
        else:
            self.host = url_splited.split('@')[-1] # FIX: Invalid protocol
            self.path = '/'  # FIX: Path should default to "/" if it's missing

        # Extract username and password
        if '@' in url_splited:
            # Ensure username:password is not part of the protocol by checking for '://'
            auth_part, remainder = url_splited.split('@', 1)
            if '://' not in auth_part:
                if ':' in auth_part:
                    self.username, self.password = auth_part.split(':', 1)
                else:
                    self.username = auth_part
                url = remainder
            else:
                # Invalid URL, clear username and password
                self.username = None
                self.password = None
        else:
            remainder = url

        # Extract port from the host
        host_port_match = HOST_PORT_PATTERN.match(self.host)
        if host_port_match:
            self.host = host_port_match.group('host')
            self.port = host_port_match.group('port')

        if self.host:
            # Check if host is an IPv6 address
            ipv6_match = IPV6_PATTERN.match(self.host)
            if ipv6_match:
                self.host = ipv6_match.group(1)

        # Split the path into parts
        if self.path:
            self.path_array = self.path.split('/')

        # Parse host into subdomains, main domain, and TLD
        if self.host and not self.is_ipv4(self.host) and not self.is_ipv6(self.host):
            domain_parts = self.host.split('.')
            if len(domain_parts) > 1:
                self.tld = domain_parts[-1]
                self.main_domain = domain_parts[-2]
                self.subdomains = domain_parts[:-2] if len(domain_parts) > 2 else []

    def is_ipv4(self, domain: str) -> bool:
        """Checks if the given domain is a valid IPv4 address."""
        return IPV4_PATTERN.match(domain) is not None

    def is_ipv6(self, domain: str) -> bool:
        """Checks if the given domain is a valid IPv6 address."""
        return IPV6_PATTERN.match(domain) is not None

    def get_fixed_url(self) -> str:
        """Constructs and returns the full URL from the parsed components."""
        url = ""
        if self.protocol:
            url += f"{self.protocol}://"
        if self.username:
            url += self.username
            if self.password:
                url += f":{self.password}"
            url += "@"
        if self.host:
            if self.is_ipv6(self.host):
                url += f"[{self.host}]"
            else:
                url += self.host
        if self.port:
            url += f":{self.port}"
        if self.path:
            url += self.path
        if self.query:
            url += '?' + '&'.join(f'{key}={quote(val)}' for key, value in self.query.items() for val in value)
        if self.fragment:
            url += f"#{self.fragment}"
        return url

    def get_url_structure(self) -> dict:
        """Returns a dictionary representation of the URL structure."""
        return {
            "protocol": self.protocol,
            "username": self.username,
            "password": self.password,
            "domain": {
                "host": self.host,
                "ip": self.host_ipaddress,
                "full_domain": self.full_domain,
                "tld": self.tld,
                "main_domain": self.main_domain,
                "subdomains": self.subdomains,
                "port": self.port,
                "urlparams": self.urlparams
            },
            "path": {
                "full": self.path,
                "array": self.path_array,
            },
            "query": {
                "full": self.query,
                "array": self.query_array
            },
            "fragment": self.fragment
        }
