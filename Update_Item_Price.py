
import csv
import requests
import tkinter
import customtkinter  # <- import the CustomTkinter module

def start_updatting_data():
    print("click")
    cookie_session_id = []
    with open('cookies.txt') as f:
        lines = f.readlines()
        for coki in lines:
            if 'portal-web.sid' in coki:
                sid_cookie = coki.split()[-1]
                cookie_session_id.append(sid_cookie)
    cookies = {
        "portal-web.sid": f"{cookie_session_id[0]}"
    }

    headers = {
        'Host': 'merchant-portal.doordash.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Apollographql-Client-Name': 'APP-MERCHANT',
        'Apollographql-Client-Version': '5.739.0',
        'Origin': 'https://www.doordash.com',
        'Dnt': '1',
        'Referer': 'https://www.doordash.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',

    }

    params = {
        'operation': 'SaveFullMenuMutation',
    }
    with open(f"Doordash Items.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            # category_name = lines[0]
            item_name = lines[1].strip()
            option_price = int(lines[2].replace(".",""))
            update_price = lines[3]
            category_id = lines[4]
            item_id = lines[5]

            if update_price:
                print(item_name)
                try:
                    modifyer_id = lines[6]
                    option_id = lines[7]
                    if option_id:

                        params11 = {
                            'operation': 'UpdateModifier',
                        }
                        json_data11 = {
                            'operationName': 'UpdateModifier',
                            'variables': {
                                'id': modifyer_id,
                                'options': [
                                    {
                                        'id': option_id,
                                        'actionType': 'update',
                                        'entity': {
                                            'id': option_id,
                                            'sortId': 0,
                                            'name': item_name,
                                            'price': option_price,
                                            'basePrice': None,
                                        },
                                    },
                                ],
                            },
                            'query': 'mutation UpdateModifier($id: ID!, $name: String, $minNumOptions: Float, $maxNumOptions: Float, $minAggregateOptionsQuantity: Float, $maxAggregateOptionsQuantity: Float, $minOptionChoiceQuantity: Float, $maxOptionChoiceQuantity: Float, $numFreeOptions: Float, $merchantSuppliedId: String, $items: [ItemLinkageInput!], $options: [OptionLinkageInput!]) {\n  updateModifier(\n    id: $id\n    name: $name\n    minNumOptions: $minNumOptions\n    maxNumOptions: $maxNumOptions\n    minAggregateOptionsQuantity: $minAggregateOptionsQuantity\n    maxAggregateOptionsQuantity: $maxAggregateOptionsQuantity\n    minOptionChoiceQuantity: $minOptionChoiceQuantity\n    maxOptionChoiceQuantity: $maxOptionChoiceQuantity\n    numFreeOptions: $numFreeOptions\n    merchantSuppliedId: $merchantSuppliedId\n    items: $items\n    options: $options\n  ) {\n    status\n    ids {\n      uuid\n      id\n      __typename\n    }\n    __typename\n  }\n}\n',
                        }

                        response11 = requests.post(
                            'https://merchant-portal.doordash.com/mx-menu-tools-bff/graphql',
                            params=params11,
                            cookies=cookies,
                            headers=headers,
                            json=json_data11,
                        )
                        print(response11.status_code)
                    else:

                        json_data = {
                            'operationName': 'SaveFullMenuMutation',
                            'variables': {
                                'menu': {
                                    'id': '15432549',
                                },
                                'categories': [],
                                'items': [
                                    {
                                        'price': option_price,
                                        'basePrice': None,
                                        'categoryId': category_id,
                                        'description': '',
                                        'isAlcohol': None,
                                        'merchantSuppliedId': 'fffba98f-2336-4d04-b39f-c184d2f20131',
                                        'id': item_id,
                                        'name': item_name,
                                        'sortId': 0,
                                        'extrasList': [],
                                    },
                                ],
                                'extras': [],
                                'options': [],
                                'storeId': '22995503',
                            },
                            'query': 'mutation SaveFullMenuMutation($menu: SaveFullMenuMenuInput!, $categories: [SaveFullMenuCategoryInput!], $items: [SaveFullMenuItemInput!], $extras: [SaveFullMenuItemExtraInput!], $options: [SaveFullMenuItemExtraOptionInput!], $storeId: ID) {\n  saveFullMenu(\n    menu: $menu\n    categories: $categories\n    items: $items\n    extras: $extras\n    options: $options\n    storeId: $storeId\n  ) {\n    uuid\n    id\n    __typename\n  }\n}\n',
                        }

                        update_price_response = requests.post(
                            'https://merchant-portal.doordash.com/mx-menu-tools-bff/graphql',
                            params=params,
                            cookies=cookies,
                            headers=headers,
                            json=json_data,
                        )
                        print(update_price_response.status_code)


                except:

                    json_data = {
                        'operationName': 'SaveFullMenuMutation',
                        'variables': {
                            'menu': {
                                'id': '15432549',
                            },
                            'categories': [],
                            'items': [
                                {
                                    'price': option_price,
                                    'basePrice': None,
                                    'categoryId': category_id,
                                    'description': '',
                                    'isAlcohol': None,
                                    'merchantSuppliedId': 'fffba98f-2336-4d04-b39f-c184d2f20131',
                                    'id': item_id,
                                    'name':  item_name,
                                    'sortId': 0,
                                    'extrasList': [],
                                },
                            ],
                            'extras': [],
                            'options': [],
                            'storeId': '22995503',
                        },
                        'query': 'mutation SaveFullMenuMutation($menu: SaveFullMenuMenuInput!, $categories: [SaveFullMenuCategoryInput!], $items: [SaveFullMenuItemInput!], $extras: [SaveFullMenuItemExtraInput!], $options: [SaveFullMenuItemExtraOptionInput!], $storeId: ID) {\n  saveFullMenu(\n    menu: $menu\n    categories: $categories\n    items: $items\n    extras: $extras\n    options: $options\n    storeId: $storeId\n  ) {\n    uuid\n    id\n    __typename\n  }\n}\n',
                    }

                    update_price_response = requests.post(
                        'https://merchant-portal.doordash.com/mx-menu-tools-bff/graphql',
                        params=params,
                        cookies=cookies,
                        headers=headers,
                        json=json_data,
                    )
                    print(update_price_response.status_code)
    root_tk.after(1000, lambda: root_tk.destroy())


root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("600x240")
root_tk.title("DoorDash Start Process")
# Use CTkButton instead of tkinter Button
label = customtkinter.CTkLabel(master=root_tk,
                               text="Update DoorDash Menu Price",
                               width=600,
                               height=25,
                               text_color="Black",
                               corner_radius=8)
label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=root_tk,text="Update Price", corner_radius=10, command=start_updatting_data)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()


root_tk1 = tkinter.Tk()  # create the Tk window like you normally do
root_tk1.geometry("600x240")
root_tk1.title("DoorDash Notification")

# Use CTkButton instead of tkinter Button
label1 = customtkinter.CTkLabel(master=root_tk1,
                                text="DoorDash Price Updated Successfully.",
                                width=600,
                                height=25,
                                text_color="Black",
                                corner_radius=8)
label1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
root_tk1.mainloop()
