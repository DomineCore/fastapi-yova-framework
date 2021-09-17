from home_application.api import save_person,test_my_api

url_pattern = [
    ("/",save_person, ["post"]),
    ("/test_api",test_my_api,["post"])
]
