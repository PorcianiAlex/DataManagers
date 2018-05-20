import cssselect
import requests
import os
import time
import lxml.html
import multiprocessing as mp
import concurrent.futures as cf
from selenium import webdriver


class AdCounter(object):
    """
    This class applies elemhide rules from AdBlock Plus to an lxml document or element object.
    One or more AdBlock Plus filter subscription files must be provided.

    Matcher and matcher2 are utility functions used for parallelism.
    The three functions count_ads do the same thing, but the sequential one doubles the exec time.
    There is no sensible difference between multithreading and multiprocessing (~1% time gain with multithreading
    using 10*n_cpu threads vs multiprocessing using 2*n_cpu processes)
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
                    if line[:2] != '@@':
                        try:
                            self.rules.append(translator.css_to_xpath(line[2:]))
                        except cssselect.SelectorError:
                            # just skip bad selectors
                            pass

        n_thread = mp.cpu_count()
        l_query = len(self.rules)
        # create one large query by joining them the xpath | (or) operator
        self.xpath_query_list = []
        for _ in range(n_thread):
            start = int(_*l_query/n_thread)
            stop = int((_+1)*l_query/n_thread)
            self.xpath_query_list.append('|'.join(self.rules[start:stop]))

    def matcher(self, doc, query_position):
        tree = lxml.html.document_fromstring(doc)
        return len(tree.xpath(self.xpath_query_list[query_position]))

    def count_ads(self, url):
        """
        Convert webpage content to lxml document.
        Counts ads from an lxml document or element object.
        """

        html = requests.get(url).text
        args = [(html, i) for i in range(mp.cpu_count()*2)]
        with mp.Pool(processes=mp.cpu_count()) as pool:
            return sum(pool.starmap(self.matcher, args))

    def count_ads_loop(self, url):
        html = requests.get(url).text
        doc = lxml.html.document_fromstring(html)
        counter = 0
        for _, rule in enumerate(self.rules):
            if doc.xpath(rule):
                counter += 1
        return counter

    def matcher2(self, doc, query_position):
        return len(doc.xpath(self.xpath_query_list[query_position]))

    def count_ads_th(self, url):
        html = requests.get(url).text
        doc = lxml.html.document_fromstring(html)
        data = 0
        with cf.ThreadPoolExecutor(max_workers=5*mp.cpu_count()) as executor:
            future_pool = {executor.submit(self.matcher2, doc, i): i for i in range(mp.cpu_count())}
            for future in cf.as_completed(future_pool):
                data += future.result()
        return data

    def iframe_detector(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        html_source = driver.page_source
        print(len(driver.find_elements_by_xpath("//iframe")))
        return html_source.count("<iframe")
       # return len(driver.find_elements_by_xpath("//iframe"))

"""-------------------Testing frame-------------------"""
if __name__ == '__main__':
    remover = AdCounter("adList/easylist.txt")
    start = time.time()
    print(remover.iframe_detector("http://www.nyt.com"))
    print("th time: {}".format(time.time() - start))
#    start = time.time()
#    print(remover.count_ads_loop("http://www.nyt.com"))
#    print("loop time: {}".format(time.time() - start))
