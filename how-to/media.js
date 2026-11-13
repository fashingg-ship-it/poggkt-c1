/*
  POGGKT how-to media slots.
  Fill in a value between the quotes, save, and push. Nothing else needs to change.
  The printed QR codes do not change.
*/
window.POGGKT_MEDIA = {

  // Main video for each pad. Paste the YouTube link. Leave "" until the video is published.
  video: {
    knee: "",
    shoulder: "",
    hip: "",
    foot: ""
  },

  // Optional short YouTube video for one step. Adds a "Watch this step" button under that picture.
  stepVideo: {
    "fill": "",
    "connect": "",
    "remote": "",
    "wear-knee": "",
    "wear-shoulder": "",
    "wear-hip": "",
    "wear-foot": ""
  },

  // Pictures. Put the file in how-to/photos/ and write its path here, for example "photos/fill.jpg".
  // A slot stays empty until its picture is set.
  photo: {
    // Pad cards on the first page. 6:5 works best (1200 x 1000).
    "pad-knee": "",
    "pad-shoulder": "",
    "pad-hip": "",
    "pad-foot": "",

    // Step pictures. Landscape 8:5 works best (1280 x 800).
    "fill": "",
    "connect": "",
    "remote": "",
    "wear-knee": "",
    "wear-shoulder": "",
    "wear-hip": "",
    "wear-foot": ""
  }
};
