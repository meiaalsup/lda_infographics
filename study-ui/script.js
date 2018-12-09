//BASE_PATH = "http://data.csail.mit.edu/soundnet/actions3/";
//SUBMIT_URL = "data";
DEBUG = false;
IM_ID = null;
IM_DATA = null;

$(document).ready(function() {
    DEBUG = gup("debug") == "true";

    //var data_path = gup("data");
    //if (data_path.length == 0) data_path = "sample";
    var data_path = "sample";
    var im_id = gup('im_id') ? gup('im_id') : '0';
    var n_seconds = gup('n_s');
    if (n_seconds.length > 0) {
      n_seconds = parseInt(n_seconds);
    } else {
      n_seconds = 2;
    }
    console.log("Using data file with name", data_path);
    console.log("Showing for " + n_seconds + " seconds");
    $.ajax({
        url: "data/" + data_path + ".json",
        dataType: 'json',
        type: 'GET',
        success: function(data) {
            console.log(data);
            // assume we just have a list of videos 
            var im_data = data[im_id];
            IM_ID = im_id;
            IM_DATA = im_data;
            console.log('im_data', im_data);
            preload_im(im_data.url);
            addChecks(im_data);
            showData(im_data, n_seconds);
        }
    });
});  

function preload_im(img_url) {
  var img = new Image();
  img.src = img_url;
  img.onload = (function() {
    console.log("loaded");
    $('#show-image').removeClass('loading');
  });  
}

function addChecks(im_data) {
  var categories = im_data.categories;
  categories.forEach(function(cat) {
    var safeLabel = getSafeVersion(cat);
    var checkbox = '<div class="field"><label>' + cat + ':</label><input type="text " name="' + safeLabel + '"></div>'
    $(".form").find(".grouped.fields").append(checkbox);
  });
}

function getSafeVersion(label) {
  return label.replace(" ", "_").toLowerCase();
}

function showData(im_data, n_seconds) {
  // put the image in the box 
  var im_path = im_data.url;
  $('#infographic-img').attr('src', im_path);

  // click button to show image 
  $("#show-image").click(showImage.bind(this, im_data, n_seconds));
}

function showImage(im_data, n_seconds) {
  $('#instructions').hide();
  $('#infographic-img-container').show();
  setTimeout(hideImage.bind(this, im_data), n_seconds*1000)
}

function hideImage(im_data) {
  $('#infographic-img-container').hide();
  $('#categories-container').show();
  $('#submit-button').click(function() {
    var data = collectData();
    console.log(data);
    $('#data-submitted').text(JSON.stringify(data));
    $('#categories-container').hide();
    $('#done').show();
  })
}

function collectData() {
  answers = {}
  $('.field').each(function(i, elt) {
    var name = $(elt).find('input').attr("name");
    var val = $(elt).find('input').val();
    answers[name] = val;
  })
  return {
    'im_id': IM_ID,
    'im_data': IM_DATA,
    'answers': answers
  }
}

function gup(name) {
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var tmpURL = window.location.href;
    var results = regex.exec( tmpURL );
    if (results == null) return "";
    else return results[1];
}
  