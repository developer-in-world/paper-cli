import requests
query = "Q-Star Meets Scalable Posterior Sampling"
words = query.strip().split()
search_query = " AND ".join(f'all:"{word}"' for word in words)
print("Search Query:", search_query)
params = {
    'search_query': search_query,
    'start': 0,
    'max_results': 3,
    'sortBy': 'submittedDate',
    'sortOrder': 'descending'
}
try:
    response = requests.get('http://export.arxiv.org/api/query', params=params)
    print("URL:", response.url)
    
    import xml.etree.ElementTree as ET
    root = ET.fromstring(response.content)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text
        print("FOUND TITLE:", title.replace('\n', ' '))
except Exception as e:
    print(e)
