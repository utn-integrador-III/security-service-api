def is_valid_email_domain(email):
    allowed_domains = ["@utn.ac.cr", "@est.utn.ac.cr", "@adm.utn.ac.cr", '@gmail.com']
    return any(email.endswith(domain) for domain in allowed_domains)