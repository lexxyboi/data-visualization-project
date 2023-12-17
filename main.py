# Import libraries
from flask import Flask, render_template
import pandas as pd
import plotly.express as px

# Store flask app into a variable (app)
app = Flask(__name__, static_url_path='/static')

# Load the CSV file
df = pd.read_csv('earthquakes-23k.csv')

### app routes ###


@app.route('/')
def index():
    # Get the total number of earthquakes
    total_earthquakes = len(df)

    # Find the lowest magnitude and its date
    lowest_magnitude_row = df.loc[df['Magnitude'].idxmin()]
    lowest_magnitude = lowest_magnitude_row['Magnitude']
    lowest_magnitude_date = lowest_magnitude_row['Date']

    # Find the highest magnitude and its date
    highest_magnitude_row = df.loc[df['Magnitude'].idxmax()]
    highest_magnitude = highest_magnitude_row['Magnitude']
    highest_magnitude_date = highest_magnitude_row['Date']

    # Select the last 500 values
    df_last_500 = df.tail(500)

    # Create a dot map using Plotly Express
    dot_map_fig = px.scatter_geo(df_last_500, lat='Latitude', lon='Longitude', hover_name='Date',
                                 projection='orthographic', title='')

    # Convert the dot map to HTML
    dot_map_html = dot_map_fig.to_html(full_html=False)

    # Create a scatter plot using Plotly Express
    fig = px.scatter_geo(df_last_500, lat='Latitude', lon='Longitude', color='Magnitude', size='Magnitude',
                         hover_name='Date', projection='natural earth',
                         title='')

    # Set the center and zoom to show the entire Earth
    fig.update_geos(center=dict(lat=0, lon=0), projection_scale=1)

    # Convert the plot to HTML
    plot_html = fig.to_html(full_html=False)

   # Set magnitude thresholds
    magnitude_thresholds = [5, 6, 7]

    # Count earthquakes above each magnitude threshold
    counts = [len(df[df['Magnitude'] > threshold])
              for threshold in magnitude_thresholds]

    return render_template('index.html', plot=plot_html, dot=dot_map_html,
                           total_earthquakes=total_earthquakes,
                           lowest_magnitude=lowest_magnitude, lowest_magnitude_date=lowest_magnitude_date,
                           highest_magnitude=highest_magnitude, highest_magnitude_date=highest_magnitude_date,
                           magnitude_counts=counts, magnitude_labels=magnitude_thresholds)


# Start Development Server
if __name__ == "__main__":
    app.run(debug=True)
