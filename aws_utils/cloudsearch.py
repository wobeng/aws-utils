class Cloudsearch:
    def __init__(self, domain_name, session):
        self.client = session.client('cloudsearch')
        response = self.client.describe_domains(DomainNames=[domain_name])
        self.info = response['DomainStatusList'][0]
        self.doc = session.client('cloudsearchdomain', endpoint_url='https://{}'.format(
            self.info['DomainStatusList']['DocService']['Endpoint']))
        self.search = session.client('cloudsearchdomain', endpoint_url='https://{}'.format(
            self.info['DomainStatusList']['SearchService']['Endpoint']))
