import asposewordscloud

words_api = asposewordscloud.WordsApi(
    client_id='d04669c8-a183-4b73-84f6-a956a38c1e26',
    client_secret='134a5fe73fc1202079c6cbe7042d9ac1')

doc = open('Dzho_Grey_-_Sotsialnaya_inzheneria_i_etichny_khaking_na_praktike_2023.pdf', 'rb')
request = asposewordscloud.models.requests.ConvertDocumentRequest(document=doc,
                                                                  format='epub')
convert = words_api.convert_document(request)
