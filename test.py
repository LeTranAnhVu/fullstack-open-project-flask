import blurhash

with open('/Users/user/Documents/me/python/flask_api/main/resources/images/3bb1616a048b5bc2eb033ca3616d29f6.jpg', 'rb') as file:
    print(blurhash.encode(file,x_components=4, y_components=3))