import streamlit as st
import plotly.express as px
import pandas as pd

from collections import Counter
from itertools import combinations

import cloudinary_service


@st.cache
def get_images_with_tags():
    return cloudinary_service.get_all_images_with_tags()


all_images = get_images_with_tags()

all_tags = []
all_tags_lists = []
for image in all_images:
    tags = image["tags"]
    if not tags or "person" in tags:
        continue
    all_tags.extend(tags)
    all_tags_lists.append(tags)

tag_counter = Counter(all_tags)

sorted_tags = [item for item in sorted(tag_counter.items(), key=lambda x: -x[1])]
sorted_tag_strings = [f"{item[0]} ({item[1]})" for item in sorted_tags]

combs = []
for tags_per_image in all_tags_lists:
    for comb in combinations(tags_per_image, 2):
        combs.append(comb)

most_common_combs = Counter(combs).most_common(20)


def show_images(images):
    columns = st.columns(3)
    for idx, img in enumerate(images):
        col = columns[idx % 3]
        url = img["url"]
        if url.endswith(".heic"):
            url = url[:-5] + ".jpg"
        with col:
            st.image(url)
            st.markdown(f"[Link]({url})")


def image_page():
    options = sorted_tag_strings[:20]
    for item in most_common_combs:
        options.append(f"{item[0][0]}, {item[0][1]} ({item[1]})")

    tag = st.selectbox("Select tag", options)

    idx = tag.find("(")
    tag = tag[: idx - 1]
    if "," in tag:
        # multiple tags
        tag1, tag2 = tag.split(",")
        tag1, tag2 = tag1.strip(), tag2.strip()
        images_with_tag = [
            img for img in all_images if tag1 in img["tags"] and tag2 in img["tags"]
        ]
    else:
        images_with_tag = [img for img in all_images if tag in img["tags"]]
    show_images(images_with_tag)


def stats_page(min_tags_number=20):
    filtered_tags = {
        k: v
        for k, v in sorted(tag_counter.items(), key=lambda x: -x[1])
        if v >= min_tags_number
    }
    labels = list(filtered_tags.keys())
    counts = list(filtered_tags.values())

    st.markdown(f"#### Top {min_tags_number} Tags")

    df = pd.DataFrame(list(zip(labels, counts)), columns=["Tags", "Counts"])
    fig = px.pie(df, values="Counts", names="Tags")
    fig.update_traces(textinfo="label+percent")
    fig.update_layout(width=700, height=700)
    st.plotly_chart(fig)

    st.markdown(f"#### Top 5 Tags")
    df = pd.DataFrame(list(zip(labels[:5], counts[:5])), columns=["Tags", "Counts"])
    fig = px.bar(df, x="Tags", y="Counts")
    fig.update_layout(width=800, height=500)
    st.plotly_chart(fig)

    st.markdown(f"#### Most common combinations")

    labels = [str(x[0]) for x in most_common_combs][::-1]
    counts = [x[1] for x in most_common_combs][::-1]

    df = pd.DataFrame(list(zip(labels, counts)), columns=["Combinations", "Counts"])
    fig = px.bar(df, x="Counts", y="Combinations", orientation="h")
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)


if __name__ == "__main__":
    options = ("Image Gallery", "Image Stats")
    selection = st.sidebar.selectbox("Menu", options)

    if selection == "Image Gallery":
        st.title("Image Gallery")
        image_page()
    else:
        st.title("Image Stats")
        stats_page()
