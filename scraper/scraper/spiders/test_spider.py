from pathlib import Path

import scrapy


class PhpForumSpider(scrapy.Spider):
    name = 'phpforum'

    _forums = [
        {# forum object
            
            # object of type topic
            'metadata': {
                'baseForumUrl': 'https://www.php-forum.com/phpforum/',
                'postCssSelector': 'dl.row-item',
                'postXpath' : '//*[@id="page-body"]/div[4]/div/ul[2]/li[1]/dl', 
                'lastPostTimesXpath' : './dd[3]/span/time/@datetime',
                'postAnchorsXpath': './dt/div/a/@href',
                'commentCssSelector':'post',
                'commentTextXpath': './div/div[1]/div/div/text()',
            },
            'topics': [{
                'url': 'https://www.php-forum.com/phpforum/viewforum.php?f=2',
                
            },]
            # has the same use as postCssSelector

        },
    ]

    def start_requests(self):
        for forum in self._forums:
    #         self.parse_forum(forum)


    # def parse_forum(self, forum):
    #     pass


            # determine the innerForums of this forum
           
            for topic in forum['topics']:
                # TODO rethink the forum object so as not to carry all the unnecessary 
                # information around for no reason

                metadata_copy = forum['metadata']
                metadata_copy['topic'] = topic

                yield scrapy.Request(url=topic['url'], callback=self.parse_topic, cb_kwargs={'topic_metadata': metadata_copy})


    def parse_topic(self, response, topic_metadata):
        posts = response.css(topic_metadata['postCssSelector'])

        last_post_times = posts.xpath(topic_metadata['lastPostTimesXpath']).getall()
        post_anchors = posts.xpath(topic_metadata['postAnchorsXpath']).getall()

        for last_post_time, post_anchor in zip(last_post_times, post_anchors):
            if self._is_recent(last_post_time):
                # print(last_post_time)
                # print(post_anchor)
                self._process_post(post_anchor, topic_metadata)

        # with open('data.html', 'w', encoding='utf-8') as w_file:
        #     for last_post_time, post_anchor in zip(last_post_times, post_anchors):
        #         w_file.write(str(last_post_time) + ' ' + str(post_anchor) + '\n')
            # w_file.write(str(post_anchors))


    def parse_post(self, response, topic_metadata):
        # a post from the forum

        print('yes')
        return
        
        # # functionalitatea originala, de lasat comantata pana dupa debug
        # comments = response.css(topic_metadata['commentCssSelector'])
        # texts = comments.xpath(topic_metadata['commentTextXpath'])
        # print(texts)
        # print()


    def _is_recent(self, time):
        # TODO complete
        return True


    def _process_post(self, anchor, topic_metadata):
        post_url = topic_metadata['baseForumUrl'] + str(anchor[2:])
        self.log(post_url)

        # Nu inteleg dc nu merge yield-ul asta
        # TODO fix
        # daca comentam yield-ul, afiseaza post_url de mai sus.
        # daca nu, nu afiseaza nimic
        # ??????
        yield scrapy.Request(url='https://www.php-forum.com/phpforum/viewtopic.php?t=30175&sid=6f64e21efb9f5658d68c302168e394c1', callback=self.parse_post)
        
        # yield scrapy.Request(url=post_url, callback=self.parse_post, cb_kwargs={'topic_metadata': topic_metadata})
        # yield-ul original, de lasat in pace


    def _post_has_pagination():
        pass

