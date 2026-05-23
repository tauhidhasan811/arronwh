from src.tools.user_contact_info import SaveUserContactInfo, Body

body = Body(
    referred_by="John",
    name="Tauhid Hasan",
    email="test@gmail.com",
    phone="01700000000",
    postcode="1207",
    address="Dhaka"
)

print(SaveUserContactInfo(body))
