import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud

# Define colors for positive, neutral, and negative sentiments
sentiment_colors = {
    'positive': 'rgba(76, 175, 80, 0.8)',   # Green
    'neutral': 'rgba(255, 193, 7, 0.8)',    # Yellow
    'negative': 'rgba(255, 105, 97, 0.8)'   # Red
}

def get_pie_chart(df):
    sentiment_counts = df['label'].value_counts()
    colors = [sentiment_colors[label] for label in sentiment_counts.index]

    fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts, 
                                 marker=dict(colors=colors))])
    fig.update_layout(title_text='Sentiment Distribution')
    img = fig.to_html()
    return img

def get_line_chart(df):
    df['publish_date'] = pd.to_datetime(df['publish_date'])

    # Group by day and calculate sentiment counts
    df_grouped = df.groupby([pd.Grouper(key='publish_date', freq='D'), 'label']).size().unstack(fill_value=0).reset_index()

    # Add missing columns if not present
    for sentiment in ['positive', 'negative', 'neutral']:
        if sentiment not in df_grouped.columns:
            df_grouped[sentiment] = 0

    # Melt the DataFrame for Plotly
    df_melted = df_grouped.melt(id_vars='publish_date', value_vars=['positive', 'negative', 'neutral'],
                                var_name='label', value_name='count')

    # Create line chart using Plotly Express
    fig = px.line(df_melted, x='publish_date', y='count', color='label',
                  labels={'publish_date': 'Date', 'count': 'Sentiment Count', 'label': 'Sentiment'},
                  title='Sentiment Trend Over Time')
    fig.update_layout(xaxis_title='Date', yaxis_title='Sentiment Count', legend_title='Sentiment')
    # Convert Plotly figure to HTML
    img = fig.to_html()
    return img

def get_word_cloud(df):
    text = ' '.join(df['clean_text'].tolist())
    
    # Generate word cloud using WordCloud
    wordcloud = WordCloud(width=800, height=300, background_color='white', colormap='viridis').generate(text)
    
    # Generate Plotly figure with the image
    fig = px.imshow(wordcloud.to_array())
    fig.update_layout(
        title="Word Cloud",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=30, b=0),
        width=800,
        height=300
    )
    
    # Convert Plotly figure to HTML
    fig_html = fig.to_html()
    
    return fig_html

def get_multiple_pie_charts(df):
    source_counts = df['source'].value_counts().head(5).index
    df_top_sources = df[df['source'].isin(source_counts)]

    # Group data by source and label, counting occurrences
    grouped_data = df_top_sources.groupby(['source', 'label']).size().reset_index(name='counts')

    # Create stacked bar chart using Plotly Express
    fig = px.bar(grouped_data, x='source', y='counts', color='label',
                 color_discrete_map=sentiment_colors,
                 labels={'counts': 'Number of Articles', 'label': 'Sentiment'},
                 title='Sentiment Distribution for Top 5 Sources',
                 text='counts')

    # Update layout to remove legend, adjust title size, and bar width
    fig.update_layout(
        barmode='stack',
        xaxis_title=None,  # Adjusted x-axis title
        yaxis_title=None,  # Adjusted y-axis title
        title_font=dict(size=10),  # Smaller title font size
        height=600,  # Adjusted height
        width=300,   # Adjusted width
        showlegend=False,  # Hide legend
        bargap=0.2,   # Decrease bargap to make bars thinner
        margin=dict(l=30)
    )

    # Customize text inside bars for better visibility
    fig.update_traces(textposition='inside', texttemplate='%{text}', textfont_size=10)

    # Convert Plotly figure to HTML
    img = fig.to_html()
    return img
