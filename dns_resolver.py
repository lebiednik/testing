import dns.resolver

answer = dns.resolver.query('www.dnspython.org')
print answer.rrset
print 'The dnspython is', answer.rrset.ttl

answer = dns.resolver.query('www.google.com')
print answer.rrset
print 'The google is', answer.rrset.ttl

answer = dns.resolver.query('www.microsoft.com')
print answer.rrset
print 'The microsoft is', answer.rrset.ttl

answer = dns.resolver.query('cdn.castplatform.com')
print answer.rrset
print 'The cdn is', answer.rrset.ttl

answer = dns.resolver.query('www.server.com')
print answer.rrset
print 'The server is', answer.rrset.ttl
