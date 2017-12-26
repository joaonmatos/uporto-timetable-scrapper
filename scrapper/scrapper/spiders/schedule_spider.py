import scrapy
import getpass
from ..items import Class
from scrapy.http import Request, FormRequest
from ..con_info import ConInfo

class ClassSpider(scrapy.Spider):
    name = "schedules"
    allowed_domains = ['sigarra.up.pt']
    login_page = 'https://sigarra.up.pt/'

    def start_requests(self):
        """This function is called before crawling starts."""
        yield Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request. The login form needs the following parameters:
            p_app : 162 -> This is always 162
            p_amo : 55 -> This is always 55
            p_address : WEB_PAGE.INICIAL -> This is always 'WEB_PAGE.INICIAL'
            p_user : username -> This is the username used to login
            p_pass : password -> This is the password used to login
        """
        self.user = input("User: ")
        self.passw = getpass.getpass()
        return FormRequest.from_response(response,
                                         formdata={
                                             'p_app': '162', 'p_amo': '55',
                                             'p_address': 'WEB_PAGE.INICIAL',
                                             'p_user': self.user,
                                             'p_pass': self.passw},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in. It is done by checking if a button's value is
        'Terminar sessão', that translates to 'Sign out', meaning the login was successful.
        It also verifies if the login failed due to incorrect credentials, in case the button's
        value equals 'Iniciar sessão', that translates to 'Sign in',
        meaning the credentials were wrong or due to a change in website structure.
        """
        result = response.xpath(
            '//div[@id="caixa-validacao-conteudo"]/button[@type="submit"]/@value').extract_first()

        if result == "Terminar sessão":
            self.log("Successfully logged in. Let's start crawling!")
            # Spider will now call the parse method with a request
            return self.classRequests()
        elif result == "Iniciar sessão":
            print('Login failed. Please try again.')
            self.log('Login failed. Please try again.')
        else:
            print('Unexpected result. Website structure may have changed.')
            self.log('Unexpected result. Website structure may have changed.')

    def classRequests(self):
        con_info = ConInfo()
        with con_info.connection.cursor() as cursor:
            sql = "SELECT id, url FROM `class` LIMIT 1"
            cursor.execute(sql)
            self.classes = cursor.fetchall()
        con_info.connection.close()

        self.log("Crawling {} classes".format(len(self.classes)))
        for clazz in self.classes:
            yield scrapy.http.FormRequest(
                url=clazz[1],
                meta={'class_id': clazz[0]},
                callback=self.extractSchedule)
    
    def extractSchedule(self, response):
        for schedule in response.xpath('//table[@class="horario"]'):
            # This array represents the rowspans left in the current row
            # It is used because when a row has rowspan > 1, the table
            # will seem to be missing a column and can cause out of sync errors
            # between the HTML table and its memory representation
            rowspans = [0, 0, 0, 0, 0, 0]
            for row in schedule.xpath('./tr[not(th)]'):
                for col in row.xpath('./td[not(contains(@class, "k"))]'):
                        print(col)


           