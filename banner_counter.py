import cssselect
import requests
import os
import time
import lxml.html

class AdCounter(object):
    """
    This class applies elemhide rules from AdBlock Plus to an lxml document or element object.
    One or more AdBlock Plus filter subscription files must be provided.

    Example usage:

#    >>> import lxml.html
#    >>> remover = AdCounter('adList/easylist.txt')
#    >>> doc = lxml.html.document_fromstring("<html>...</html>")
#    >>> remover.count_ads(doc)
    """

    def __init__(self, *rules_files):
        """
        :param rules_files: path to rules files
        """
        if not rules_files:
            rule_urls = [#'https://filters.adtidy.org/extension/chromium/filters/2.txt',
                         'https://easylist.to/easylist/easylist.txt'
                         ]

            rules_files = [url.rpartition('/')[-1] for url in rule_urls]

            if not os.path.isdir("adList"):
                os.mkdir("adList")

            # download files containing rules
            for rule_url, rule_file in zip(rule_urls, rules_files):
                r = requests.get(rule_url)
                with open("adList/" + rule_file, 'w', encoding='utf-8') as f:
                    f.write(r.text)

        translator = cssselect.HTMLTranslator()
        self.rules = []

        for rules_file in rules_files:
            with open(rules_file, 'r', encoding="utf-8") as f:
                for line in f:
                    # elemhide rules are prefixed by ## in the adblock filter syntax
                    if line[:2] == '##':
                        try:
                            self.rules.append(translator.css_to_xpath(line[2:]))
                        except cssselect.SelectorError:
                            # just skip bad selectors
                            pass

        # create one large query by joining them the xpath | (or) operator
        self.xpath_query = '|'.join(self.rules)

    def count_ads(self, url):
        """
        Convert webpage content to lxml document.
        Counts ads from an lxml document or element object.
        """

        html = requests.get(url).text
        doc = lxml.html.document_fromstring(html)
        print(len(self.rules))
        start = gstart = time.time()
        counter = 0
        for _, rule in enumerate(self.rules):
            if doc.xpath(rule):
                counter += 1
            if _ % 1000 == 0:
                print("iteration: {} out of {}".format(_, len(self.rules)))
                print("time over 1000: {}".format(time.time() - start))
                print("time: {}".format(time.time() - gstart))
                start = time.time()
        print(counter)
        return counter


remover = AdCounter("adList/easylist.txt")
remover.count_ads("http://www.nyt.com")
