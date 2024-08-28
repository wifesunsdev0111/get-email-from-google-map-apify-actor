import re

def extract_emails(string):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(pattern, string)
    return emails

def convert_to_email_format(email):
    suffixes = [
        '.com', '.org', '.net', '.edu', '.gov', '.mil', '.int', '.info', '.biz',
        '.name', '.us', '.uk', '.ca', '.au', '.de', '.fr', '.jp', '.cn', '.br',
        '.in', '.gov', '.edu', '.mil', '.int', '.aero', '.museum', '.coop',
        '.jobs', 'travel', '.tech', '.app', '.blog', '.shop', '.music',
        '.photography', '.academy', '.club', '.store', '.design', '.orgYour'
    ]

    for suffix in suffixes:
        if email.endswith(suffix):
            return email

        suffix_with_dot = '.' + suffix
        if suffix_with_dot in email:
            prefix = email.rsplit(suffix_with_dot, 1)[0]
            return prefix + suffix

    return None

# emails = ['?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fwater-contact', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fcity-council-contacts', 'waterconservation@FortWorthTexas.gov', 'District2@fortworthtexas.gov', 'District3@fortworthtexas.gov', 'District4@fortworthtexas.gov', 'District5@fortworthtexas.gov', 'District6@fortworthtexas.gov', 'District7@fortworthtexas.gov', 'District8@fortworthtexas.gov', 'District9@fortworthtexas.gov', 'District10@fortworthtexas.gov', 'District11@fortworthtexas.gov', 'beth.ellis@fortworthtexas.gov', '%20District2@fortworthtexas.gov', 'Maira.Gallegos@fortworthtexas.gov', 'Katie.Wharry@fortworthtexas.gov', 'Danel.Mason@fortworthtexas.gov', 'Booker.Thomas@fortworthtexas.gov', '%20district5@fortworthtexas.gov', 'sandi.breaux@fortworthtexas.gov', 'Joshua.Rivers@fortworthtexas.gov', 'kendyll.locke@fortworthtexas.gov', 'davia.johnson@fortworthtexas.gov', 'sami.roop@fortworthtexas.gov', 'sally.matzen@fortworthtexas.gov', 'Anthony.Rojas@fortworthtexas.gov', 'Disrict10@fortworthtexas.gov', 'Tara.Holt@fortworthtexas.gov', 'Jimika.Allison@fortworthtexas.gov', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fgovernment%2felected-officials%2fcontact', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fcode-compliance-contact', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fgovernment%2fmayor%2fcontact', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fdevelopment-services-contact', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fcity-management-contacts', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fmunicipal-contact', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fhuman-resources-contacts', '?Body=https%3a%2f%2fwww.fortworthtexas.gov%2fa-z-index%2fdiversity-inclusion-contacts']

def clear_emails(emails):
    cleared_emails = []

    for email in emails:
        formatted_email = convert_to_email_format(email)
        if formatted_email:
            cleared_emails.append(formatted_email)
            # print(formatted_email)
    return cleared_emails

# print(clear_emails(['info@specialistfence.orgYour']))
