import requests


def get_media_providers(title, year):
    """
    This module web scraps the detail of the hosting platform for that particular media, Movie or TV show.
    """

    # try:
    url = "https://apis.justwatch.com/content/titles/en_IN/popular?body={{%22enable_provider_filter%22:false,%22query%22:%22{}%22,%22monetization_types%22:[],%22page%22:1,%22page_size%22:10}}".format(
        title.replace(" ", "+"))
    result = requests.get(url)
    items = result.json()['items']

    provider_result = requests.get(
        "https://apis.justwatch.com/content/providers/locale/en_IN")
    provider_list = provider_result.json()
    companies = []

    for i in items:
        if str(i['original_release_year']) == str(year):
            providers = i['offers']

            for provider in providers:
                id = provider['provider_id']

                for company in provider_list:
                    if company['id'] == id and company['clear_name'] in ["Netflix", "Amazon Prime Video", "Hotstar", "Jio Cinema"]:

                        data = {"name": company['clear_name'],
                                "url": provider['urls']['standard_web']}
                        if data not in companies:
                            companies.append(data)

    print(companies)
    if companies:
        return companies
    return {"message": "No Streaming Services for this media"}
