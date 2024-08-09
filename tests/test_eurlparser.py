import unittest
from eurlparser.eurlparser import EnhancedURLParser

class TestEnhancedURLParser(unittest.TestCase):

    def test_ip_without_protocol(self):
        url = "//127.0.0.1"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "127.0.0.1")
        self.assertIsNone(parser.port)
        self.assertIsNone(parser.protocol)
        self.assertEqual(parser.path, "/")

    def test_ip_with_port_and_path(self):
        url = "//127.0.0.1:256/en-US/SomeFolder?arg1=%20%20test%20&arg2=%20test2%20#test=1234"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "127.0.0.1")
        self.assertEqual(parser.port, "256")
        self.assertEqual(parser.path, "/en-US/SomeFolder")
        self.assertEqual(parser.query, {"arg1": ["  test "], "arg2": [" test2 "]})
        self.assertEqual(parser.fragment, "test=1234")

    def test_url_with_invalid_protocol(self):
        url = "ht@tp://username:password@host/path"
        parser = EnhancedURLParser(url)
        self.assertIsNone(parser.protocol)
        self.assertEqual(parser.username, "username")
        self.assertEqual(parser.password, "password")
        self.assertEqual(parser.host, "host")
        self.assertEqual(parser.path, "/path")

    def test_url_with_no_host_or_protocol(self):
        url = "/just/a/path?query=param"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "just")
        self.assertIsNone(parser.protocol)
        self.assertEqual(parser.path, "/a/path")
        self.assertEqual(parser.query, {"query": ["param"]})

    def test_ip_with_port_without_protocol(self):
        url = "/127.0.0.1:1234/"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "127.0.0.1")
        self.assertEqual(parser.port, "1234")
        self.assertEqual(parser.path, "/")
        self.assertIsNone(parser.protocol)

    def test_ip_with_port_without_protocol_with_path(self):
        url = "/127.0.0.1:80/foo/bar?arg=123"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "127.0.0.1")
        self.assertEqual(parser.port, "80")
        self.assertEqual(parser.path, "/foo/bar")
        self.assertEqual(parser.path, "/foo/bar")
        self.assertEqual(parser.query, {"arg": ["123"]})
        self.assertIsNone(parser.tld)

    def test_ipv6_with_path(self):
        url = "/[fdb2:2c26:f4e4:1::1]/file.txt"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "fdb2:2c26:f4e4:1::1")
        self.assertEqual(parser.path, "/file.txt")
        self.assertIsNone(parser.port)
        self.assertIsNone(parser.protocol)

    def test_domain_with_port(self):
        url = "hostn123ame.test:2345"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "hostn123ame.test")
        self.assertEqual(parser.port, "2345")
        self.assertIsNone(parser.protocol)


    def test_ipv6_with_multiple_colons(self):
        url = "http://[2001:0db8:85a3:0000:0000:8a2e:0370:7334]/resource"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "http")
        self.assertEqual(parser.host, "2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        self.assertEqual(parser.path, "/resource")

    def test_url_with_fragment_only(self):
        url = "http://example.com#section2"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "http")
        self.assertEqual(parser.host, "example.com")
        self.assertEqual(parser.path, "/")
        self.assertEqual(parser.fragment, "section2")

    def test_url_with_path_and_no_host_or_protocol(self):
        url = "/path/with/slashes/and?query1=val1&query2=val2#fragment"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, 'path')
        self.assertIsNone(parser.protocol)
        self.assertEqual(parser.path, "/with/slashes/and")
        self.assertEqual(parser.query, {"query1": ["val1"], "query2": ["val2"]})
        self.assertEqual(parser.fragment, "fragment")

    def test_url_with_empty_query_parameter(self):
        url = "http://example.com/path?arg=&anotherarg=123"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "http")
        self.assertEqual(parser.host, "example.com")
        self.assertEqual(parser.path, "/path")
        self.assertEqual(parser.query, {"arg": [""], "anotherarg": ["123"]})

    def test_url_with_percent_encoded_characters(self):
        url = "http://example.com/%E2%9C%93?arg=%E2%9C%93&arg2[]=Hi1&arg2[]=Hi2"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "http")
        self.assertEqual(parser.host, "example.com")
        self.assertEqual(parser.path, "/%E2%9C%93")
        self.assertEqual(parser.query, {"arg": ["\u2713"], "arg2[]": ["Hi1", "Hi2"]})
        self.assertEqual(parser.get_fixed_url(), url)

    def test_domain_without_port(self):
        url = "hostn123ame.test"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.host, "hostn123ame.test")
        self.assertIsNone(parser.port)
        self.assertIsNone(parser.protocol)

    def test_protocol_with_auth(self):
        url = "t-e-s-t://username:pa$$w0rd@test.domain.name/"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "t-e-s-t")
        self.assertEqual(parser.username, "username")
        self.assertEqual(parser.password, "pa$$w0rd")
        self.assertEqual(parser.host, "test.domain.name")
        self.assertEqual(parser.path, "/")


    def test_url_with_special_characters_in_auth(self):
        url = "https://user%20name:pa$$w0rd%40%23%24%25@test.domain.name:8080/path/to/resource?arg1=value1&arg2=value2#section1"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "https")
        self.assertEqual(parser.username, "user%20name")
        self.assertEqual(parser.password, "pa$$w0rd%40%23%24%25")
        self.assertEqual(parser.host, "test.domain.name")
        self.assertEqual(parser.port, "8080")
        self.assertEqual(parser.path, "/path/to/resource")
        self.assertEqual(parser.query, {"arg1": ["value1"], "arg2": ["value2"]})
        self.assertEqual(parser.fragment, "section1")

    def test_url_with_array_query_parameters(self):
        url = "http://example.com/path?arg[]=value1&arg[]=value2&arg[]=value3"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "http")
        self.assertEqual(parser.host, "example.com")
        self.assertEqual(parser.path, "/path")
        self.assertEqual(parser.query, {"arg[]": ["value1", "value2", "value3"]})

    def test_ipv6_with_port(self):
        url = "http://[2001:db8::1]:8080/resource"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "http")
        self.assertEqual(parser.host, "2001:db8::1")
        self.assertEqual(parser.port, "8080")
        self.assertEqual(parser.path, "/resource")

    def test_ipv6_with_protocol(self):
        url = "https://[fdb2:2c26:f4e4:1::1]/file.txt"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "https")
        self.assertEqual(parser.host, "fdb2:2c26:f4e4:1::1")
        self.assertEqual(parser.path, "/file.txt")

    def test_protocol_with_base64_auth(self):
        url = "test://Base64-Text-Maybe==@test.domain.name/"
        parser = EnhancedURLParser(url)
        self.assertEqual(parser.protocol, "test")
        self.assertEqual(parser.username, "Base64-Text-Maybe==")
        self.assertEqual(parser.host, "test.domain.name")
        self.assertEqual(parser.path, "/")

if __name__ == '__main__':
    unittest.main()
