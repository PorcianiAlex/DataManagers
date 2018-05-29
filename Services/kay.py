# @author 'Luca Vavassori'

import kay_utilities

class KAY:

        '''
        This is the entry point of the KAY Fake News detection service.

        Methods:

        - handle:   it allows to analyse a request that comes from either the chatbot
                    or the web app. As parameters the function receive an url(s) and
                    the service from which the request has been generated {chatbot, webapp}

        '''

        def handle(self, request, source="chatbot"):

            urls = findurls(request)

            for url in urls:
                #TODO handle url
