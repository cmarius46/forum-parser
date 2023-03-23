from pathlib import Path

import scrapy


class PhpForumSpider(scrapy.Spider):
    name = 'phpforum'

    def start_requests(self):
        urls = [
            'https://www.php-forum.com/phpforum/viewforum.php?f=2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # threads_list = response.xpath('//*[@id="page-body"]/div[4]/div/ul[2]/li[1]/dl').get()
    
        threads_list = response.css("dl.row-item.sticky_read").getall()

        # self.log(str(response))

        # self.log('------------------------------------')
        # self.log(str(threads_list))
        # self.log('------------------------------------')

        filename = f'data.html'
        self.log(str(filename))


        with open('data.html', 'w') as w_file:
            w_file.write(str(threads_list))
        self.log(f'Saved file {filename}')

