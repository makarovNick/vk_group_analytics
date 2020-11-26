#!/usr/bin/env python3

from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd


def build_chart_edu_wordcloud(df, output_file):
    titles = df[~pd.isnull(df.university_name)]['university_name'].values

    word_cloud_dict = dict(Counter(titles).most_common(50))

    wordcloud = (
        WordCloud(
            width=500, height=500, margin=0,
            background_color="rgba(255, 255, 255, 0)", mode="RGBA",
            colormap="ocean", contour_width=None, collocations=False
        )
        .generate_from_frequencies(word_cloud_dict)
    )

    plt.figure(figsize=(3.2, 3.2), facecolor='w')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_file, format='svg', bbox_inches='tight')
