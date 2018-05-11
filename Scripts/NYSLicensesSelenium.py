#Lindsay Poirier created this script with inspiration and guidance from http://toddhayton.com/2015/05/14/using-selenium-to-scrape-aspnet-pages-with-ajax-pagination/
import re
import string
import urlparse
import requests
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

class LicenseScraper(object):
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.url = "https://aca.licensecenter.ny.gov/aca/GeneralProperty/PropertyLookUp.aspx?isLicensee=Y"
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(self.url)

        # Select license type from dropdown; this one selects "Appearance Enhancement Business"
        selectLicense = Select(self.driver.find_element_by_id('ctl00_PlaceHolderMain_refLicenseeSearchForm_ddlLicenseType'))
        selectLicense.select_by_index(4)

        # Input New York as City
        inputCity = self.driver.find_element_by_id('ctl00_PlaceHolderMain_refLicenseeSearchForm_txtCity')
        inputCity.send_keys('New York')
        self.driver.find_element_by_id('ctl00_PlaceHolderMain_btnNewSearch').click()
        
        # Wait for results to finish loading
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.find_element_by_id('divGlobalLoading').is_displayed() == False)
        self.driver.save_screenshot('screenie.png') #If you'd like to check results

        # Create CSV file
        f = csv.writer(open("AES_NYC_Licenses.csv", "w"))
        f.writerow(["license number", "name", "business name","address","county","issue date","effective date","expiration date","status"]) # Write column headers as the first line



        """This site is extremely slow, and I faced numerous time-outs. Rather than recollecting all of the previous data, if you face a time-out, you can uncomment the script below to skip to the last page that you scraped rounded down to the nearest 10.
        startPage = 10
        startPageSelected = 1
        
        while startPage < [FILL THIS WITH LAST PAGE SCRAPED ROUNDED DOWN TO 10]:
            
            try:
                next_page_elem_start = self.driver.find_element_by_xpath("//a[text()='%d']" % startPage)
            except NoSuchElementException:
                try:
                    next_page_elem_start = self.driver.find_element_by_xpath("//a[text()='Next >']")
                except NoSuchElementException:
                    break # no more pages
                else:
                    startPage += 10
                    startPageSelected += 10
                    print 'About to click next. Start page = ', startPage, '\n'
                    print 'Selected page = ', startPageSelected, '\n'
                    next_page_elem_start.click()
                    
                    def next_page_start_a(driver):
                        selected_start_a = driver.find_element_by_xpath("//span[text()='%d']" % startPageSelected).get_attribute('class')
                        return 'SelectedPageButton' in selected_start_a
                    
                    wait = WebDriverWait(self.driver, 90)
                    wait.until(next_page_start_a)
                        
                        else:
                            print 'About to click on', startPage, '\n'
                                next_page_elem_start.click()
                                    
                                    def next_page_start_span(driver):
                                        selected_start_span = driver.find_element_by_xpath("//span[text()='%d']" % startPage).get_attribute('class')
                                            return 'SelectedPageButton' in selected_start_span
                                                
                                                wait = WebDriverWait(self.driver, 90)
                                                    wait.until(next_page_start_span)
                                                        print 'Loaded', startPage, '\n'
                                                            
        pageno = [FILL THIS WITH LAST PAGE SCRAPED ROUNDED DOWN TO 10]"""
        """IF YOU UNCOMMENT THE ABOVE, COMMENT THIS: pageno = 2"""
        pageno = 2

        
        while True:
            s = BeautifulSoup(self.driver.page_source, 'html.parser') #parse the page
            
            
            for a in s.findAll(id=re.compile(r'lnkLicenseRefNumber$')):
                License = a.text
                LicenseLink = License.replace(" ","%20")
                LicenseURL = "https://aca.licensecenter.ny.gov/aca/GeneralProperty/LicenseeDetail.aspx?LicenseeNumber=" + LicenseLink #follow the link to the license
                print LicenseURL

                LicenseRequest = requests.get(LicenseURL)
                LicenseSoup = BeautifulSoup(LicenseRequest.text)
                LicenseNumber = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblLicenseeNumber_value")
                LicenseName = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblContactName_value")
                BusinessName = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblLicenseeBusinessName_value")
                LicenseAddress = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblLicenseeAddress_value")
                LicenseCounty = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblLicenseeTitle_value")
                LicenseIssue = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblLicenseIssueDate_value")
                LicenseEffective = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblBusinessExpirationDate_value")
                LicenseExpiration = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblExpirationDate_value")
                LicenseStatus = LicenseSoup.find(id="ctl00_PlaceHolderMain_licenseeGeneralInfo_lblBusinessName2_value")
                f.writerow([LicenseNumber.text.encode('utf-8'), LicenseName.text.replace(u'\xa0', " ").encode('utf-8'), BusinessName.text.encode('utf-8'), LicenseAddress.text.replace(u'\xa0', " ").encode('utf-8'), LicenseCounty.text.encode('utf-8'), LicenseIssue.text.encode('utf-8'), LicenseEffective.text.encode('utf-8'), LicenseExpiration.text.encode('utf-8'), LicenseStatus.text.encode('utf-8')])

            # Pagination
            try:
                next_page_elem = self.driver.find_element_by_xpath("//a[text()='%d']" % pageno)
            except NoSuchElementException:
                try:
                    next_page_elem = self.driver.find_element_by_xpath("//a[text()='Next >']")
                except NoSuchElementException:
                    break # no more pages
                
            print 'page ', pageno, '\n'
            next_page_elem.click()
                
            def next_page(driver):
                selected = driver.find_element_by_xpath("//span[text()='%d']" % pageno).get_attribute('class')
                return 'SelectedPageButton' in selected
                
            wait = WebDriverWait(self.driver, 60)
            wait.until(next_page)
                
            pageno += 1

        self.driver.quit()

if __name__ == '__main__':
    scraper = LicenseScraper()
    scraper.scrape()
