from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
from bs4 import BeautifulSoup


'''************************************************
* @Function Name : get_finance_info_1
************************************************'''
def get_finance_info_1():

    api = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.xml?crtfc_key="
    crtfc_key ="956243c104077738ebc3c93bd62c3e0c019eb877"

    co_code = "00126380"
    year = "2019"

    '''
    1분기보고서 : 11013
    반기보고서 : 11012
    3분기보고서 : 11014
    사업보고서 : 11011
    '''
    rept_code = "11011"

    '''
    CFS:연결재무제표, OFS:재무제표
    '''
    fs_div = "OFS"

    url = api + crtfc_key + "&corp_code=" + co_code + "&bsns_year=" + year +  "&reprt_code=" + rept_code + "&fs_div=" + fs_div

    resp = urlopen(url)
    resp_dat = resp.read()

    soup = BeautifulSoup(resp_dat, 'html.parser')
    str_xml = str(soup.prettify())
    str_list = str_xml.split('\n')

    with open('./fin_xml.xml', 'w', encoding='utf-8') as f:
        for line in str_list:
            f.writelines(line + '\n')

    return

'''************************************************
* @Function Name : get_finance_info_2
************************************************'''
def get_finance_info_2():

    api = "https://opendart.fss.or.kr/api/fnlttXbrl.xml?crtfc_key="
    crtfc_key ="956243c104077738ebc3c93bd62c3e0c019eb877"

    rcept_no = "20200515001451"     #sam
    rept_code = "11011"

    url = api + crtfc_key + "&rcept_no=" + rcept_no + "&rept_code=" + rept_code
    print(url)

    resp = urlopen(url)
    resp_dat = resp.read()

    with ZipFile(BytesIO(resp_dat)) as zf:
        file_list = zf.namelist()

        while len(file_list) > 0:
            file_name = file_list.pop()
            co_rept = zf.open(file_name).read().decode('euc-kr')
            break

    soup = BeautifulSoup(co_rept, 'html.parser')
    str_xml = str(soup.prettify())
    str_list = str_xml.split('\n')

    with open('./fin_xml.txt', 'w', encoding='utf-8') as f:
        for line in str_list:
            f.writelines(line + '\n')

    return

'''************************************************
* @Function Name : get_finance_all
************************************************'''
def get_finance_all():
    import datetime
    import dart_fss as dart

    # Open DART API KEY 설정
    api_key="956243c104077738ebc3c93bd62c3e0c019eb877"
    dart.set_api_key(api_key=api_key)

    # 현재 날짜 불러오기
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d%H%M')
    # 검색 시작 날짜
    bgn_de = '20170101'
    # 검색 종료 날짜
    end_de = now.strftime('%Y%m%d')

    # 모든 상장된 기업 리스트 불러오기
    corp_list = dart.get_corp_list()

    # 원하는 기업이름 입력
    corp_name = '만도'
    corp_code = corp_list.find_by_corp_name(corp_name=corp_name)[0]
    corp_code = corp_code._info['corp_code']

    print(corp_code)
    corp_code = "01042775"
    print(corp_code)

    # 2019년 01월 01일에 올라온 연결재무제표부터 현재까지 검색
    # 사업 보고서
    # fs = dart.fs.extract(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de, lang='ko', separator=False)
    # 반기 보고서 [report_tp='half']
    # fs = dart.fs.extract(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de, report_tp='half', lang='ko', separator=False)
    # 분기 보고서 [report_tp='quarter']
    fs = dart.fs.extract(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de, report_tp='quarter', lang='ko', separator=False)

    # 재무제표 일괄저장 (default: 실행폴더/fsdata/{corp_code}_{report_tp}.xlsx)
    filename = corp_name + '_' + nowDate + '.xlsx'
    # path = 'C:/Users/User/hb_jeong/Desktop/'
    fs.save(filename=filename)


'''************************************************
* @Function Name : get_corpcode
************************************************'''
def get_corpcode():

    api = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key="
    crtfc_key ="956243c104077738ebc3c93bd62c3e0c019eb877"

    url = api + crtfc_key

    resp = urlopen(url)
    resp_dat = resp.read()

    with ZipFile(BytesIO(resp_dat)) as zf:
        file_list = zf.namelist()

        while len(file_list) > 0:
            file_name = file_list.pop()
            #co_rept = zf.open(file_name).read().decode('euc-kr')
            co_rept = zf.open(file_name).read().decode('utf-8')
            break

    soup = BeautifulSoup(co_rept, 'html.parser')
    str_xml = str(soup.prettify())
    str_list = str_xml.split('\n')

    with open('./co_code.xml', 'w', encoding='utf-8') as f:
        for line in str_list:
            f.writelines(line + '\n')

    return


'''************************************************
* @Class Name : FinanceAccInfo
************************************************'''
class FinanceAccInfo:

    def __init__(self, sj_nm=None, account_nm=None, account_id=None, thstrm_nm=None,
                 thstrm_amount=None, frmtrm_nm=None, frmtrm_amount=None):

        self.sj_nm = sj_nm
        self.account_nm = account_nm
        self.account_id = account_id

        self.thstrm_nm = thstrm_nm              #현재 분기
        self.thstrm_amount = thstrm_amount      #현재 분기 금액
        self.frmtrm_nm = frmtrm_nm              #이전 분기
        self.frmtrm_amount = frmtrm_amount      #이전 분기 금액

        return

'''************************************************
* @Function Name : sub_blank
************************************************'''
def sub_blank(word):
    return word.replace('\n','').lstrip()


'''************************************************
* @Function Name : parse_xml
************************************************'''
match_tag_list = ['<sj_nm>', '<account_nm>', '<account_id>', '<thstrm_nm>', '<thstrm_amount>', '<frmtrm_nm>', '<frmtrm_amount>']
(SJ_NM, ACCOUNT_NM, ACCOUNT_ID, THSTRM_NM, THSTRM_AMOUNT, FRMTRM_NM, FRMTRM_AMOUNT) = range(7)
def parse_xml():
    with open('./fin_xml.xml', 'r', encoding='utf-8') as f:
        xml = f.readlines()
    f.close()

    cnt = 0
    account_list = []
    while(1):
        cur_line = sub_blank(xml[cnt])
        if '</result>' in cur_line:
            break

        elif '<list>' in cur_line:
            fin_acc_obj = FinanceAccInfo()
            while(1):
                sub_line = sub_blank(xml[cnt])
                if '</list>' in sub_line:
                    account_list.append(fin_acc_obj)
                    break
                else:
                    if sub_line in match_tag_list:
                        p = match_tag_list.index(sub_line)
                        get_value = sub_blank(xml[cnt + 1])

                        if p == SJ_NM: fin_acc_obj.sj_nm = get_value
                        elif p == ACCOUNT_NM: fin_acc_obj.account_nm = get_value
                        elif p == ACCOUNT_ID: fin_acc_obj.account_id = get_value

                        elif p == THSTRM_NM: fin_acc_obj.thstrm_nm = get_value
                        elif p == THSTRM_AMOUNT: fin_acc_obj.thstrm_amount = get_value
                        elif p == FRMTRM_NM: fin_acc_obj.frmtrm_nm = get_value
                        elif p == FRMTRM_AMOUNT: fin_acc_obj.frmtrm_amount = get_value

                        else: pass
                    else:
                        pass
                cnt += 1
        cnt += 1
    return account_list


'''************************************************
* @Function Name : sort_account
************************************************'''
def sort_account(account_list):

    for account in account_list:


    return


'''************************************************
* @Function Name : main()
************************************************'''
def main():
    res = parse_xml()


    #get_finance_info_1()
    #get_finance_all()
    #get_corpcode()


if __name__ == '__main__':
    main()


