
import csv
import requests
import json
import tkinter
import customtkinter  # <- import the CustomTkinter module


def start_getting_data():
    print("button pressed")
    store_id = '22995503'
    menu_id = '15432549'

    cookie_session_id = []
    with open('cookies.txt') as f:
        lines = f.readlines()
        for coki in lines:
            if 'portal-web.sid' in coki:
                sid_cookie = coki.split()[-1]
                cookie_session_id.append(sid_cookie)

    def Get_Modifyer_data(item_ids):

        params1 = {
            'operation': 'GetExtrasForStore',
        }

        json_data1 = {
            'operationName': 'GetExtrasForStore',
            'variables': {
                'storeId': store_id,
            },
            'query': 'fragment menuItemExtra on MenuItemExtra {\n  id\n  isActive\n  isSuspended\n  name\n  merchantSuppliedId\n  minNumOptions\n  maxNumOptions\n  numFreeOptions\n  sharedBy {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment menuItemExtraOption on MenuItemExtraOption {\n  id\n  name\n  sortId\n  isActive\n  description\n  basePrice\n  price\n  isSuspended\n  __typename\n}\n\nquery GetExtrasForStore($storeId: ID!) {\n  getExtrasForStore(storeId: $storeId) {\n    ...menuItemExtra\n    options {\n      ...menuItemExtraOption\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        Get_Modifiyers = requests.post('https://www.doordash.com/merchant/mx-menu-tools-bff/graphql', headers=headers,
                                       params=params1, cookies=cookies, json=json_data1)
        print(Get_Modifiyers.status_code)

        Modifiyer_data = json.loads(Get_Modifiyers.text)

        for data_modifiyer in Modifiyer_data['data']['getExtrasForStore']:
            if data_modifiyer['isActive'] == True:
                item_sharBy_ids = [all_id['id'] for all_id in data_modifiyer['sharedBy']]
                if item_ids in item_sharBy_ids:
                    modifyer_id = data_modifiyer['id']
                    modif_merchantSuppliedID = data_modifiyer['merchantSuppliedId']
                    modifiyer_name = data_modifiyer['name']
                    modifiyer_options = [f"{option_data['id']} <> {option_data['name']} <> {option_data['price']}" for
                                         option_data in data_modifiyer['options']]
                    return modifyer_id, modif_merchantSuppliedID, modifiyer_name, modifiyer_options

    cookies = {
        "portal-web.sid": f"{cookie_session_id[0]}"
    }

    headers = {
        'Host': 'www.doordash.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Apollographql-Client-Name': 'SSMEV2',
        'Apollographql-Client-Version': '2.370.0',
        # 'Content-Length': '736',
        'Origin': 'https://www.doordash.com',
        'Dnt': '1',
        'Referer': f'https://www.doordash.com/merchant/menu/v2/{menu_id}/?store_id={store_id}&t=1693255392161',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    headers11 = {
        'Host': 'merchant-portal.doordash.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Apollographql-Client-Name': 'APP-MERCHANT',
        'Apollographql-Client-Version': '5.735.0',
        # 'Content-Length': '736',
        'Origin': 'https://www.doordash.com',
        'Dnt': '1',
        'Referer': 'https://www.doordash.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    params = {
        'operation': 'GetMenuStructure',
    }

    json_data = {
        'operationName': 'GetMenuStructure',
        'variables': {
            'menuIds': [],
            'storeId': store_id,
            'excludeArchivedCategories': True,
        },
        'query': 'query GetMenuStructure($menuIds: [ID!]!, $storeId: ID!, $excludeArchivedCategories: Boolean) {\n  getMenuStructure(\n    menuIds: $menuIds\n    storeId: $storeId\n    excludeArchivedCategories: $excludeArchivedCategories\n  ) {\n    storeId\n    menus {\n      id\n      name\n      subtitle\n      categories {\n        id\n        name\n        menuId\n        subtitle\n        merchantSuppliedId\n        isActive\n        sortId\n        isEverythingBikeFriendly\n        itemIds\n        __typename\n      }\n      isActive\n      itemIds\n      __typename\n    }\n    itemIds\n    __typename\n  }\n}\n',
    }

    Get_menu_data = requests.post(
        'https://merchant-portal.doordash.com/mx-menu-tools-bff/graphql',
        params=params,
        cookies=cookies,
        headers=headers11,
        json=json_data,
    )
    print(Get_menu_data.status_code)

    Currant_Get_data = json.loads(Get_menu_data.text)

    All_Item_ids = []
    for Data in Currant_Get_data['data']['getMenuStructure']['menus'][1]['categories']:
        if Data['isActive'] == True:
            Category_id1 = Data['id']
            Category_Name1 = Data['name']
            print(Category_Name1)
            for category_item in Data['itemIds']:
                j_data = [category_item, Category_id1, Category_Name1]
                All_Item_ids.append(j_data)

    Get_all_item_id = [i[0] for i in All_Item_ids]

    params1 = {
        'operation': 'GetItemsByItemIds',
    }
    json_data1 = {
        'operationName': 'GetItemsByItemIds',
        'variables': {
            'includeDailyQuantityLimit': False,
            'itemIds': Get_all_item_id,
            'storeId': store_id,
        },
        'query': 'query GetItemsByItemIds($itemIds: [ID!]!, $storeId: ID!, $includeDailyQuantityLimit: Boolean! = false) {\n  getItemsByItemId(itemIds: $itemIds, storeId: $storeId) {\n    items {\n      id\n      name\n      price\n      basePrice\n      description\n      sortId\n      merchantSuppliedId\n      minAgeRequirement\n      isAlcohol\n      storeInternalSku\n      photoId\n      imageUrl\n      isBikeFriendly\n      isDashpassExclusive\n      extraIds\n      menuIds\n      extras {\n        sortId\n        extraId: id\n        __typename\n      }\n      photoId\n      dailyQuantityLimit @include(if: $includeDailyQuantityLimit)\n      isSoldOut @include(if: $includeDailyQuantityLimit)\n      __typename\n    }\n    __typename\n  }\n}\n',
    }
    response1 = requests.post(
        'https://www.doordash.com/merchant/mx-menu-tools-bff/graphql',
        params=params1,
        cookies=cookies,
        headers=headers,
        json=json_data1,
    )

    print(response1.status_code)

    data_by_item_id = json.loads(response1.text)

    for data_by_item in data_by_item_id['data']['getItemsByItemId']['items']:
        item_id = data_by_item['id']
        item_name = data_by_item['name'].strip()
        item_price = data_by_item['price']
        x = 0

        def retun_category_name_id(item_id):
            for ctgory in All_Item_ids:
                # print(ctgory)
                if item_id == ctgory[0]:
                    Category_id = ctgory[1]
                    Category_Name = ctgory[2]
                    return ctgory

        Category_info = retun_category_name_id(item_id)

        #
        # Category_Name = [c_name[2] if c_name[0] == item_id else '' for c_name in All_Item_ids][0]
        # Category_id = [c_name[1] if c_name[0] == item_id else '' for c_name in All_Item_ids][0]

        # print(item_name)
        if item_price == 0:

            sub_modifyer_item = Get_Modifyer_data(item_id)
            if sub_modifyer_item:
                modifyer_id = list(sub_modifyer_item)[0]
                supplyerID = list(sub_modifyer_item)[1]
                modifiyer_name = list(sub_modifyer_item)[2]
                for sub_data in list(sub_modifyer_item)[-1]:
                    print(sub_data)
                    option_ids = sub_data.split(' <> ')[0]
                    option_name = sub_data.split(' <> ')[1]
                    option_price = float(sub_data.split(' <> ')[2])

                    save_in_csv = [item_name.strip(), option_name.strip(), option_price / 100, "", Category_info[1],
                                   item_id, modifyer_id, option_ids]
                    with open(f'Doordash Items.csv', 'a', newline='') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(save_in_csv)
                        csvFile.close()
                        print(f"Done: {item_name}")
        else:

            save_in_csv = [Category_info[2], item_name.strip(), item_price / 100, "", Category_info[1], item_id]
            with open(f'Doordash Items.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(save_in_csv)
                csvFile.close()
                print(f"Done: {item_name}")
    root_tk.after(1000, lambda: root_tk.destroy())


root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("600x240")
root_tk.title("DoorDash Start Process")
# Use CTkButton instead of tkinter Button
label = customtkinter.CTkLabel(master=root_tk,
                               text="Exported My DoorDash Menu in CSV File",
                               width=600,
                               height=25,
                               text_color="Black",
                               corner_radius=8)
label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=root_tk,text="Start", corner_radius=10, command=start_getting_data)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()

root_tk1 = tkinter.Tk()  # create the Tk window like you normally do
root_tk1.geometry("600x240")
root_tk1.title("DoorDash Notification")

# Use CTkButton instead of tkinter Button
label1 = customtkinter.CTkLabel(master=root_tk1,
                                text="Your DoorDash Menu Exported in CSV File",
                                width=600,
                                height=25,
                                text_color="Black",
                                corner_radius=8)
label1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
root_tk1.mainloop()
