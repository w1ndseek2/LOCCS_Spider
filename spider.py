import requests
import multiprocessing
from randomHP import random_header, random_proxy
from redis import StrictRedis
import myRedis
import re
from urllib import parse
from lxml import html
import multiprocessing as mp
import logging
import coloredlogs
import traceback
from config import SPIDER_PROCESS_NUM, SPIDER_NAME

log = logging.getLogger(__name__)
coloredlogs.install(
    logger=log,
    level="DEBUG",
    fmt="[%(levelname)s] %(message)s"
)


class Spider:
    def check_if_login_form(self, content):
        if len(re.findall(
            r"type[ ]*=[ ]*['\"]password['\"]",
            content, flags=re.IGNORECASE | re.MULTILINE
        )) != 0:
            return True
        else:
            return False

    def simple_request(self, url):
        log.info("[+] now crawing: %s" % url)
        try:
            r = requests.get(
                url, headers=random_header(),
                timeout=5, proxies={}
            )

            #del from todo
            try:
                redis_manager.del_todo(url)
                log.info("success [+] delete from todo")
            except Exception as e:
                log.exception("error [-] when delete from todo")
                redis_manager.add_error(url)

            if r.status_code == 200:
                try:
                    if self.check_if_login_form(str(r.content)):
                        log.warning("[+] login form found! " + url)
                        try:
                            redis_manager.add_login_form(url)
                            log.info("success [+] add to login form")
                        except Exception as e:
                            log.exception("error [-] when add to login form")
                            redis_manager.add_error(url)
                    else:
                        log.warning("[-] login form not found")

                    try:
                        redis_manager.add_finish(url)
                        log.info("success [+] add to finish")
                    except Exception as e:
                        log.exception("error [-] when add to finish")
                        redis_manager.add_error(url)

                    return str(r.content)

                except Exception as e:
                    log.exception("error [-] when check if login form")
                    redis_manager.add_error(url)
            else:
                log.info(str(r.status_code) + " [+] " + str(url))
                #add to forbidden
                try:
                    redis_manager.add_forbidden(url)
                    log.warning("success [+] add to forbidden")
                except Exception as e:
                    log.exception("error [-] when add to forbidden")
                    redis_manager.add_error(url)

        except Exception as e:
            #del from todo , add to timeout
            try:
                redis_manager.del_todo(url)
                log.info("success [+] delete from todo")
            except Exception as e:
                log.exception("error [-] when delete from todo")
                redis_manager.add_error(url)

            try:
                redis_manager.add_timeout(url)
                log.warning("success [+] add to timeout")
            except Exception as e:
                redis_manager.add_error(url)
                log.exception("error [-] when add to timeout")

    def url_last_part(self, url):
        domain = parse.urlparse(url).netloc
        domain_split = domain.split('.')
        split_len = len(domain_split)
        _url = domain_split[split_len-2] + '.' + domain_split[split_len-1]
        return _url

    def extension_check(self, url):
        extension = url.split('.')[-1]
        black_extension_list = ['pdf', 'mp4', 'mp3', 'js', 'css', 'txt', 'jpg', 'svg', 'png', 'gif',
                                'zip', 'bmp', 'swf', 'rar', '7z', 'mov', 'avi', 'iso', 'exe', 'pptx', 'xlsx', 'doc']
        if extension not in black_extension_list:
            return True
        else:
            return False

    def crawl_more_urls(self, father_url, content):

        log.info("[+] now crawing " + father_url + " for more urls")
        _father_url = self.url_last_part(father_url)
        #extract links & add to todo
        try:
            webpage = html.fromstring(content)
            links = webpage.xpath('//a/@href')
            for i in links:
                if i[:4] == "http":
                    if self.extension_check(i):
                        _url = self.url_last_part(i)
                        if _url == _father_url:
                            log.debug(i)
                            redis_manager.add_todo(i)

        except Exception as e:
            log.exception("error [+] when crawling for more urls")
            redis_manager.add_error(father_url)

    def crawl(self, urls, l):
        url = job_accquire(urls, l)
        # log.debug("crawling "+url)
        content = self.simple_request(url)
        if content:
            self.crawl_more_urls(url, content)


def todo_init(redis_manager: myRedis.Manage_Redis):
    redis_manager.read_from_conf()
    log.debug(redis_manager.status())
    todo_urls = redis_manager.get_todo()
    finish_urls = redis_manager.get_finish()
    timeout_urls = redis_manager.get_timeout()
    forbidden_urls = redis_manager.get_forbidden()
    urls = todo_urls - finish_urls - timeout_urls - forbidden_urls
    return urls


def job_accquire(urls, l):
    l.acquire()
    log.debug(urls)
    url = urls.pop()
    log.debug(urls)
    l.release()
    return url


if __name__ == "__main__":
    log.warning("[+] crawling raw http contents, without rendering js")
    with mp.Manager() as manager:
        redis_manager = myRedis.Manage_Redis()
        spider = Spider()
        todo_init(redis_manager)
        todo_urls = redis_manager.get_todo()
        finish_urls = redis_manager.get_finish()
        timeout_urls = redis_manager.get_timeout()
        forbidden_urls = redis_manager.get_forbidden()
        urls = todo_urls - finish_urls - timeout_urls - forbidden_urls
        log.debug(len(urls))

        urls = manager.list(urls)  # share memory
        l = mp.Lock()

        while True:
            for i in range(SPIDER_PROCESS_NUM):
                p = mp.Process(target=spider.crawl, args=(urls, l))
                p.start()
            p.join()
