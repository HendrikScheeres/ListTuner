// load DOM content
document.addEventListener("DOMContentLoaded", () => {

  // get the playlist id
  const playlist_id = document.querySelector("#statistics").dataset.playlist_id;

  //initialize new requests
  const request = new XMLHttpRequest();
  request.open("POST", "/statistics");

  // callback function for when request completes
  request.onload = () => {

    // remove the loading bars
    let loadbars = document.querySelectorAll(".loader")
    loadbars.forEach(loadbar => {
      loadbar.remove()
    })

    // extract JSON data from request
    const data = JSON.parse(request.responseText);

    // check if request was succesful
    if(!data.success) {
      alert("Could not load charts. Try logging out and back in again")
    }
    else {
      const track_features = data.track_features;
      const seal_features = data.seal_features;

      // use the response data to plot the charts
      genre_doughnut_chart(track_features);
      tempo_loudness_line_chart(track_features);
      feature_line_chart(track_features);
      feature_radar_chart(track_features, seal_features);
    }
  }

  // add data to send with request
  const data = new FormData();
  data.append("playlist_id", playlist_id);

  // send request
  request.send(data);

});
