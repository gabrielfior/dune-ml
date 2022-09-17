import json


if __name__ == "__main__":

    with open('posts.json') as f:
        d = json.load(f)
        print(d)

    items = d['data']['explorePublications']['items']
    content = []
    for item in items:
        content.append(item['metadata']['content'])

    print("Run")
