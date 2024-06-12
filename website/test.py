from intasend import APIService


API_PUBLISHABLE_KEY = "ISPubKey_test_8ff503c9-81b7-4144-88df-4ce1d65a3cdb"
API_TOKEN = "ISSecretKey_test_2d424435-3893-4eb4-ae0f-e0a7e8736288"


serevice = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

create_order = serevice.collect.mpesa_stk_push(phone_number="2541557636517", email="faresosama002@gmail.com", amount=100, currency="USD", narrative="Purchase of goods")

print(create_order)
