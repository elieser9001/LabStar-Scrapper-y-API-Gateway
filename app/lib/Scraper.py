import json

class LabStar:
    def __init__(self, session_manager):
        self.session = session_manager.session
        self.bearer = session_manager.bearer
        
        self.api_headers = {
            'Host': 'ls-api.labstar.com',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Sec-Ch-Ua-Mobile': '?0',
            'Authorization': 'Bearer ' + self.bearer,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36',
            'Sec-Ch-Ua-Platform': '""',
            'Origin': 'https://gro3x.labstar.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://gro3x.labstar.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    
    def get_attachment_by_case(self, case_id):
        params = {
            'limit': '999',
        }

        response = self.session.get(
            f'https://ls-api.labstar.com/case/attachment/findByCase/{case_id}',
            params=params,
            headers=self.api_headers,
        )
        
        return json.loads(response.text)

    def get_checkin_clients(self):
        data = {
            'take': '12',
            'skip': '0',
            'page': '1',
            'pageSize': '12',
            'sortField': 'createdOn',
            'sortDir': 'DESC',
            'tab': 'checkin',
            'cmd': 'search_result',
            'checkin_client_value': '0',
            'checkin_manufacture_value': '-1',
            'start_1_step': 'true',
            'start_multi_step': 'true',
            'manu_1_step': 'true',
            'manu_multi_step': 'true',
            'manu_outsource': 'true',
            'manuTypes': '-1',
            'page_name': 'manufacture_manager',
            'page_cmd': '',
            'search_sorting': 'createdOn DESC',
            'ship_id_params': '',
            'post_searchbox_autocomplete': '',
            'post_searchbox_value': '',
            'post_searchbox_text': '',
            'post_searchbox_cat': '',
            'oriTitle': 'Manufacturing Manager',
            'searchbox_autocomplete': '',
            'searchbox_value': '',
            'searchbox_text': '',
            'searchbox_cat': '',
        }

        response = self.session.post(
            'https://gro3x.labstar.com/pages/admin/handler.asp',
            data=data,
        )
        
        return json.loads(response.text)
    
    def get_case_items(self, case_id):
        response = self.session.get(f'https://ls-api.labstar.com/case/record/caseItem/{case_id}', headers=self.api_headers)
        
        return json.loads(response.text)

    def get_case_instructions(self, case_id):
        response = self.session.get(f'https://ls-api.labstar.com/case/initialEntry/{case_id}', headers=self.api_headers)
        
        json_response = json.loads(response.text)
        
        return json_response['data']['caseInformation']['instructions']

    def get_case_notes(self, case_id):
        response = self.session.get(f'https://ls-api.labstar.com/case/note/{case_id}?limit=999', headers=self.api_headers)

        return json.loads(response.text)
    
    def get_case_dr_preferences(self, case_id):
        response = self.session.get(f'https://ls-api.labstar.com/doctor/preferenceForm/{case_id}?limit=999', headers=self.api_headers)
        
        print(response.text)

        return json.loads(response.text)
