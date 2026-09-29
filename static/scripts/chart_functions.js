// chart functions

// constants
const default_font = "'Montserrat', 'sans-serif'";
const default_col = "#00004d";

// plots the doughnut chart with track genres
function genre_doughnut_chart (track_features) {

  // define the data and the labels
  var labels = Object.keys(track_features.genres_dict);
  var data = Object.values(track_features.genres_dict);

    // chart configurations
  var config = {
    type: 'doughnut',

    // chart data
    data: {
      labels: labels,
      datasets: [{
        data: data
      }]
    },

    // chart options
    options: {

      // general chart layout
      layout: {
        padding: {
          right: 0
        }
      },

      // title settings
      title:{
        display: true,
        position: 'top',
        fontFamily: default_font,
        text: "Playlist Genres",
        fontSize: 45,
        padding: 20,
        fontColor: default_col
      },

      // legend settings
      legend: {
        display: true,
        fullWidth: false,
        position: "bottom",
        align: "start",
        labels: {
          fontFamily: default_font
        }
      },

      // chart plugins
      plugins: {

        // fill in chart colors automatically
        colorschemes: {
          scheme: 'tableau.RedGold21'
        }
      }
    }
  };

  // select the canvas and create the chart
  var ctx = document.querySelector('#Chart1').getContext('2d');
  new Chart(ctx, config);
};

// plots the line chart with track features
function feature_line_chart(track_features) {

  var track_feature_values = track_features.track_feature_values;

  // define the x-axis label
  var xlabel = track_features.track_nums;

  // define the dataset
  var datasets = [];
  var hidden = false;

  // save the label for each track feature
  for (var key in track_feature_values) {

    // exclude the loudness and tempo
    if (key != "loudness" && key != "tempo") {

      let dataset = {
        "label": key,
        "data": track_feature_values[key],
        "hidden": hidden
      };
      datasets.push(dataset)
    }

    // make sure only the first feature is displayed automatically
    hidden = true;
  }

  // chart configurations
  var config = {
    type: 'line',

    // chart data
    data: {
      labels: xlabel,
      datasets: datasets
    },

    // chart options
    options: {

      // title settings
      title: {
        display: true,
        position: 'top',
        fontFamily: default_font,
        text: "Playlist Features",
        fontSize: 45,
        padding: 20,
        fontColor: default_col
      },

      // scale settings
      scales: {

        // y-axis settings
        yAxes: [{
          ticks: {
            min: 0,
            max: 1,
            beginAtZero: true
          }
        }],

        // x-axis settings
        xAxes: [{
          scaleLabel: {
            display:true,
            labelString: 'Tracks',
            fontSize: 15,
            fontFamily: default_font
          }
        }]
      },

      // legend settings
      legend: {
        labels: {
          fontFamily: default_font
        }
      },

      // tooltip hover settings
      tooltips: {
        callbacks: {
          beforeLabel: (tooltipItem) => {

            var index = tooltipItem.index;
            var names = track_features.track_names;

            // show the track name in the hover window
            var title = names[index];
            return title;
          }
        }
      },

      // chart plugins
      plugins: {

        // fill in chart colors automatically
        colorschemes: {
          scheme: 'brewer.PiYG7'
        }
      }
    }
  };

  // select the canvas and create the chart
  var ctx = document.querySelector('#Chart4').getContext('2d');
  new Chart(ctx, config);
};

// plots the line chart with track tempo and loudness
function tempo_loudness_line_chart(track_features) {

  var track_feature_values = track_features.track_feature_values

  // define the x-axis label
  var xlabel = track_features.track_nums


  // chart configurations
  var config = {
    type: 'line',

    // chart data
    data: {
      labels: xlabel,
      datasets: [{
        label: "Loudness",
        yAxisID: "loudness",
        data: track_feature_values.loudness,
      },
      {
        label: "Tempo",
        yAxisID: "tempo",
        data: track_feature_values.tempo,
      }]
    },

    // chart options
    options: {

      // title settings
      title: {
        display: true,
        position: "top",
        fontFamily: default_font,
        text: "Playlist Tempo and Loudness",
        fontSize: 45,
        padding: 20,
        fontColor: default_col
      },

      // legend settings
      legend: {
        labels: {
          fontFamily: default_font
        }
      },

      // scale settings
      scales: {

        // y-axis settings
        yAxes: [{
          id: "loudness",
          scaleLabel: {
            display:true,
            labelString: "Loudness in decibel (dB)",
            fontSize: 15,
            fontFamily: default_font
          },
          type: "linear",
          position: "left",
          ticks: {
            min: -60,
            max: 0
          }
        },
        {
          id: "tempo",
          scaleLabel: {
            display:true,
            labelString: 'tempo in beats per minute (bpm)',
            fontSize: 15,
            fontFamily: default_font
          },
          type: 'linear',
          position: 'right',
          ticks: {
            beginAtZero: true
          }
        }],

        // x-axis settings
        xAxes: [{
          scaleLabel: {
            display:true,
            labelString: 'Tracks',
            fontSize: 15,
            fontFamily: default_font
          }
        }]
      },

      // tooltip settings
      tooltips: {
        callbacks: {
          beforeLabel: (tooltipItem) => { 
            var index = tooltipItem.index;
            var names = track_features.track_names;

            // show the track name in the hover window
            var title = names[index];
            return title;
          }
        }
      }
    }
  };


  // select the canvas and create the chart
  var ctx = document.querySelector('#Chart3').getContext('2d');
  new Chart(ctx, config);
};

// plots the radar chart with average track feature values
function feature_radar_chart (track_features, seal_features) {

  // define the data and the labels
  var labels = Object.keys(track_features.avg_track_feature_values);
  var data = Object.values(track_features.avg_track_feature_values);

  // select the playlist name to use in the chart
  var playlist_name = document.querySelector("#statistics_title").innerHTML

  // create the curent users playlist dataset
  var datasets = [{
      label: playlist_name,
      data: data,
      borderColor: 'rgba(210, 95, 95, 1)',
      backgroundColor: 'rgba(210, 95, 95, 0.5)',
      pointBackgroundColor: 'rgba(210, 95, 95, 1)',
      pointBorderColor: 'rgba(210, 95, 95, 1)'
    }];

  // loop through the seal playlist datasets
  for (var seal_feature of seal_features) {

    // add the playlist name and data to the datasets list
    var data_temp = Object.values(seal_feature.track_features.avg_track_feature_values);

    dataset = {
     label: seal_feature.playlist_name,
     data: data_temp
   };

   datasets.push(dataset);
  }

  // chart configurations
  var config = {
    type: 'radar',

    // chart data
    data: {
      labels: labels,
      datasets: datasets
    },

    // chart options
    options: {

      // title settings
      title:{
        display: true,
        position: 'top',
        fontFamily: default_font,
        text: "Average Playlist Features",
        fontSize: 45,
        padding: 20,
        fontColor: default_col
      },

      // legend settings
      legend: {
        labels: {
          fontFamily: default_font
        }
      },

      // scale settings
      scale: {
        pointLabels : {
          fontSize:15,
          fontFamily: default_font,
        },
        angleLines: {
          display: true
        }
      }
    }
  };

  // select the canvas and create the charts
  var ctx = document.querySelector('#Chart2').getContext('2d');
  new Chart(ctx, config);
};
