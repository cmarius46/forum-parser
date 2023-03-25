from pathlib import Path

import scrapy


class PhpForumSpider(scrapy.Spider):
    name = 'phpforum'

    _forums = [
        {# forum object
            'metadata': {
                'baseForumUrl': 'https://www.php-forum.com/phpforum/',
                'postCssSelector': 'dl.row-item',
                'postXpath' : '//*[@id="page-body"]/div[4]/div/ul[2]/li[1]/dl', 
                'lastPostTimesXpath' : './dd[3]/span/time/@datetime',
                'postAnchorsXpath': './dt/div/a/@href',
                'commentCssSelector':'div.post',
                'commentTextXpath': './div/div[1]/div/div/text()',
                'commentTextCssSelector': 'div.content',
                'commentTimePostedXpath': './div/div[1]/div/p/a/time/@datetime',
                'multiplePagesCssSelector': 'div.pagination',
            },
            'topics': [{
                'url': 'https://www.php-forum.com/phpforum/viewforum.php?f=2',
                
            },]

        },
    ]

    def start_requests(self):
        for forum in self._forums:

            # TODO dynamically 'get topic urls'

            for topic in forum['topics']:
                metadata_copy = forum['metadata']
                metadata_copy['topic'] = topic

                yield scrapy.Request(url=topic['url'], callback=self.parse_topic, cb_kwargs={'topic_metadata': metadata_copy})


    def parse_topic(self, response, topic_metadata):
        posts = response.css(topic_metadata['postCssSelector'])

        last_post_times = posts.xpath(topic_metadata['lastPostTimesXpath']).getall()
        post_anchors = posts.xpath(topic_metadata['postAnchorsXpath']).getall()

        for last_post_time, post_anchor in zip(last_post_times, post_anchors):
            if self._is_recent(last_post_time):
                post_url = topic_metadata['baseForumUrl'] + str(post_anchor[2:])
                yield scrapy.Request(url=post_url, callback=self.process_post, cb_kwargs={'topic_metadata': topic_metadata})


    def process_post(self, response, topic_metadata):
        # process a post from the forum
        if self._has_multiple_pages(response, topic_metadata):
            urls = self._generate_urls(response)
            for url in urls:
                yield scrapy.Request(url=url, callback=self._process_one_page_of_post, cb_kwargs={'topic_metadata': topic_metadata})
        else:
            # one page topic
            self._process_one_page_of_post(response, topic_metadata)


    def send_to_api(self, data): # ,metadata
        # TODO complete
        # this should send the data and metadata
        self._debug_write_to_file(data)


    def _generate_urls(self, response):
        # hardcoded for the first blog.
        # TODO make this as dynamically as possible
        # something like 
        # get first page -> get last page -> get the base url -> generate urls
        urls = [f'https://www.php-forum.com/phpforum/viewtopic.php?t=1225&start={i}' for i in range(0, 250, 25)]
        return urls


    def _process_one_page_of_post(self, page, topic_metadata):
        print('called')
        comments = page.css(topic_metadata['commentCssSelector']) 
        texts = []
        for comment in comments:
            text = comment.xpath(topic_metadata['commentTextXpath']).getall()
            # using .get() causes not getting all the data from the messages

            time_posted = comment.xpath(topic_metadata['commentTimePostedXpath']).get()
            if self._is_recent(time_posted):
                texts.append(text)
                # we don't break on else since we don't know the order of processing
        
        # TODO add something related to the post itself, so that comments on different pages of the same post can be aggregated
        self.send_to_api(texts)


    def _has_multiple_pages(self, topic, topic_metadata):
        has_ul_inside_pagination = topic.xpath('//div[@class="pagination"]/ul').get()
        return has_ul_inside_pagination is not None



    def _is_recent(self, datetime):
        # TODO complete
        return True


    def _post_has_pagination():
        pass


    def _debug_write_to_file(self, data, filename='data.html'):
        with open(filename, 'a', encoding='utf-8') as w_file:
            w_file.write(str(data) + '\n')
