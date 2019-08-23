import requests
import json 

class IndustryJob():
    def __init__(self, data):
        self.id = data['blueprint_type_id']
        self.runs = data['runs']
        self.type = data['activity_id']
        self.start = data['start_date']
        self.end = data['end_date']
        self.duration = data['duration']
        self.installer = data['installer_id']

def getIndustryJobs():
    url = 'https://esi.evetech.net/latest/corporations/98609084/industry/jobs/?datasource=tranquility&include_completed=false&page=1'
    headers = {'accept': 'application/json', 'authorization': 'Bearer 1|CfDJ8HHFK/DOe6xKoNPHamc0mCUSTj3t4oAtq9lIdnKXy8XKwD4ESdbGuEnO0YuwXLE3NjfFNvXBlJadEcghSAbrfim6qoSuOyCM0NBzl4WthPjMKMHY0bb3kBA+G+UtF6BH1N1Zglovr4DHYp9kza2y/c1/GdskLxmGogSlJE69N5Vx'}
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    jobs = []
    print(r)
    print(data)
    for job in data:
        jobs.append(IndustryJob(job))
    return jobs


print(getIndustryJobs())

#https://login.eveonline.com/oauth/authorize?response_type=code&redirect_uri=http://localhost/oauth-callback&client_id=2ad0d93877ec4d6badd0917d97a18eac&scope=esi-industry.read_corporation_jobs.v1