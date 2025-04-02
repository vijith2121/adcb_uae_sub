import scrapy
# from adcb_uae_sub.items import Product
from lxml import html
import scrapy
from adcb_uae_sub.items import Product
from lxml import html
import os
import re
from scrapy_playwright.page import PageMethod
import html as html_parser


def clean(text):
    if not text:
        return None
    return ' '.join(''.join(text).split()).strip()

class Adcb_uae_subSpider(scrapy.Spider):
    name = "adcb_uae_sub"

    def start_requests(self):
        folder_path = os.path.dirname(os.path.abspath(__file__))
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".mhtml"):
                # file_path = f"file://{os.path.abspath(os.path.join(folder_path, file_name))}"
                # file_path = 'file:///home/vijith/Downloads/DHANOOP%20KALLINGAPURAM%20SUDHARMAN.mhtml'
                # file_path = 'file:///home/vijith/Desktop/vijith/spiders/ADCB_UAE/ADCB_UAE/spiders/878561.mhtml'
                # file_path = 'file:///home/vijith/Downloads/DHANOOP%20KALLINGAPURAM%20SUDHARMAN.mhtml'
                # print(file_path)
                # file_path = 'file:///home/vijith/Downloads/DHANOOP%20KALLINGAPURAM%20SUDHARMAN.mhtml'
                # file_path = 'file:///home/vijith/Desktop/vijith/spiders/ADCB_UAE/ADCB_UAE/spiders/878561.mhtml'
                file_path = 'file:///home/vijith/Desktop/vijith/spiders/ADCB_UAE/ADCB_UAE/spiders/878561%20-%201.mhtml'
                yield scrapy.Request(
                    url=file_path,
                    callback=self.parse,
                )
                return

    def parse(self, response):
        parser = html.fromstring(response.text)

        xpath_address2 = "//td[contains(text(), 'Address')]//parent::tr//following-sibling::tr[1]/td[2]//text()"
        xpath_address3 = "//td[contains(text(), 'Address')]//parent::tr//following-sibling::tr[2]/td[2]//text()"
        xpath_data = "//td[contains(text(), 'CID No.')]//parent::tr//parent::tbody//tr"

        cleaned_text = response.text.replace("=3D", "=").replace("\n", "").replace("\r", "").replace("\t", "").replace("&nbsp;", " ").strip()
        
        # print(cleaned_text)
        # return
        
        try:
            Issue_date  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Issue date')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Issue_date = ''

        if '</td>' in Issue_date:
            Issue_date = Issue_date.split('</td>')[0].strip()
        
        try:
            Next_due_date  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Next due date')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Next_due_date = ''

        if '</td>' in Next_due_date:
            Next_due_date = Next_due_date.split('</td>')[0].strip()

        
        try:
            Total_Overdue_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Total Overdue amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Total_Overdue_amount = ''

        if '</td>' in Total_Overdue_amount:
            Total_Overdue_amount = Total_Overdue_amount.split('</td>')[0].strip()
        
        try:
            Credit_Shield_Flag_or_Uniq_acno  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Credit Shield Flag / Uniq=_acno')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Credit_Shield_Flag_or_Uniq_acno = ''

        if '</td>' in Credit_Shield_Flag_or_Uniq_acno:
            Credit_Shield_Flag_or_Uniq_acno = Credit_Shield_Flag_or_Uniq_acno.split('</td>')[0].strip()

        try:
            Outstanding  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Outstanding')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Outstanding = ''

        if '</td>' in Outstanding:
            Outstanding = Outstanding.split('</td>')[0].strip()

        try:
            Principal_OS  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Principal OS')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Principal_OS = ''

        if '</td>' in Principal_OS:
            Principal_OS = Principal_OS.split('</td>')[0].strip()

        

        items = parser.xpath(xpath_data)
        data = {}
        for item in items:
            items1 = item.xpath('.//td[contains(@class, "ez1")]//text()')
            items2 = item.xpath('.//td[contains(@class, "data")]//text()')
            data1 = [
                i.strip().replace('\r\n', '').replace('&nbs=p;', '').replace('&=nbsp;', '').replace('&nbsp=;', '').replace('=', '').replace('&nbsp;', '') for i in items1 if i.strip().replace('\r\n', '').replace('&nbs=p;', '')
            ]
            data2 = [
                i.strip().replace('\r\n', '').replace('&nbs=p;', '').replace('&=nbsp;', '').replace('&nbsp=;', '').replace('=', '').replace('&nbsp;', '') for i in items2 if i.strip().replace('\r\n', '').replace('&nbs=p;', '')
            ]
            data_items = dict(zip(data1, data2))
            if 'CID No.' in data_items:
                cid_no = clean(''.join(data_items.get('CID No.', '')).strip())
                Card_type = clean(''.join(data_items.get('Card type', '')).strip())
                MinimumPayment_Amount = clean(data_items.get('MinimumPayment Amount', ''))

                data['cid_no'] = cid_no if cid_no else ''
                data['Card_type'] = Card_type if Card_type else ''
                data['MinimumPayment_Amount'] = MinimumPayment_Amount if MinimumPayment_Amount else ''
            elif 'A/C No.' in data_items:
                A_C_no = data_items.get('A/C No.', '')
                Credit_card_limit = clean(data_items.get('Credit card limit', ''))
                Last_statement_date = clean(data_items.get('Last statement date', ''))
                Days_past_due = clean(data_items.get('Days past due', ''))
                if '</td>' in Days_past_due:
                    Days_past_due = Days_past_due.split('</td>')[0].strip()
                if 'td>' in A_C_no:
                    A_C_no = A_C_no.split('td>')[0].strip()

                data['A_C_no'] = A_C_no if A_C_no else ''
                data['Last_statement_date'] = Last_statement_date if Last_statement_date else ''
                data['Credit_card_limit'] = Credit_card_limit if Credit_card_limit else ''
                data['Days_past_due'] = Days_past_due if Days_past_due else ''
        data['Issue_date'] = clean(Issue_date) if Issue_date else ''
        data['Next_due_date'] = clean(Next_due_date) if Next_due_date else ''
        data['Total_Overdue_amount'] = clean(Total_Overdue_amount) if Total_Overdue_amount else ''
        data['Credit_Shield_Flag_or_Uniq_acno'] = clean(Credit_Shield_Flag_or_Uniq_acno) if Credit_Shield_Flag_or_Uniq_acno else ''
        data['Outstanding'] = clean(Outstanding) if Outstanding else ''
        data['Principal_OS'] = clean(Principal_OS) if Principal_OS else ''
        

        print('====================================================')
        print(data)
        print('=====================================================')

                
            #     nationality_passport = data_items.get('Nationality  /  Passport', '').split('/')
            #     nationality, passport_no = clean(''.join(nationality_passport[0]).strip()), clean(''.join(nationality_passport[-1]).strip())
            #     data['cid_no'] = cid_no
            #     data['nationality'] = nationality
            #     data['passport_no'] = passport_no
            # elif 'Name' in data_items:
            #     gender_date_of_birth = data_items.get('Gender  /  Date Of Birth', '').split('/')
            #     gender, date_of_birth = gender_date_of_birth[0].strip(), gender_date_of_birth[-1].strip()
            #     office_number = data_items.get('Office1  /  Office 2 Number', '').replace('/', '').strip()
            #     data['name'] = clean(data_items.get('Name', ''))
            #     data['gender'] = clean(gender)
            #     data['date_of_birth'] = clean(date_of_birth)


        # data['total_os'] = clean(total_os_elements) if total_os_elements else None
        # data['employer_name'] = clean(employer_name) if employer_name else None
        # data['Mobile_Number'] = clean(Mobile_Number) if Mobile_Number else None
        # data['Office_Numbers'] = clean(Office_Numbers) if Office_Numbers else None
        # data['Reference_name_mobile'] = clean(Ref_name_mobile) if Ref_name_mobile else None
        # data['Email_ID'] = clean(Email_ID) if Email_ID else None
        # data['Home_Country_Number'] = clean(Home_Country_Number) if Home_Country_Number else None
        # data['Designation_Occupation'] = clean(Designation_Occupation) if Designation_Occupation else None
        # data['Emirates_id'] = clean(Emirates_id) if Emirates_id else None
        # data['address'] = clean(address) if address else None
        # data['Residence_number'] = clean(Residence_number) if Residence_number else None
        # yield Product(**data)
