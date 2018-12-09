BASE_PATH = "http://data.csail.mit.edu/soundnet/actions3/";

CAT_NAMES = {
    'vertical_orientation': 'Vertical',
    'post-processing': 'Post processing',
    'captions/text/watermarks': 'Text',
    'non-natural_videos (e.g. cartoons)': 'Non-natural', 
    'other': 'Other', 
    'degraded_format': 'Degraded', 
    'uncomfortable': 'Uncomfortable', 
    'inappropriate_(sexual)': "Sexuality", 
    'inappropriate_(nudity)': "Nudity", 
    'inappropriate_(violence)': "Violence", 
    'inappropriate_(profanity)': "Profanity"
}

$(document).ready(function() {
    $.ajax({
        url: "example_data.json",
        dataType: 'json',
        type: 'GET',
        success: function(data) {
            // assume we just have a list of videos 
            showData(data);
        }
    });
})

function showData(data) {
  // start with the clean stuff
  makeCategory('clean', data.clean);
  $.each(data, function(cat_tag, cat_data) {
    if (cat_tag != 'clean') makeCategory(cat_tag, cat_data);
  })
}

function makeCategory(tag, data) {
  var container = $('<div class="category-container ' + tag + '"></div>');
  var header = $('<h3 class="ui fitted horizontal divider header" style="margin-top: 30px">' + data.name + '</h3>');
  var description = $('<h4 class="ui fitted header" style="text-align:center">' + data.size + ' instances</h4>')
  container.append(header);
  container.append(description);
  addVideoGrid(container, tag, data);
  $('#task').append(container);
}

function addVideoGrid(container, tag, data) {
  var grid = $('<div id="graph-grid" class="ui centered grid container"></div>');
  data.examples.forEach(function(example, i) {
    var div = $('<div style="float:left; margin:10px" class="ui segment"><video controls autoplay loop muted width="320" height="240"><source src="" type="video/mp4">Your browser does not support the video tag.</video></div>');
    div.find('source').attr('src', BASE_PATH + example.url);

    var violations = example.violations.map(function(elt) { return CAT_NAMES[elt]; })
    var tags = $('<div class="tags"><p style="color: red; text-align:left">' + violations.join(", ") + '</p></div>');

    var feedback = [];
    example.feedback.forEach(function(fb, i) {
      fb = fb.trim();
      if (fb.length > 0) {
        feedback.push(fb);
      }
    })
    var text_feedback = feedback.length > 0 ? '<b>Feedback: </b>"' + feedback.join("; ") + '"' : '';
    var feedback = $('<div class="feedback"><p style="text-align:left">' + text_feedback + '</p></div>');
    div.append(tags);
    div.append(feedback);
    grid.append(div);
  });
  container.append(grid);
}

function gup(name) {
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var tmpURL = window.location.href;
    var results = regex.exec( tmpURL );
    if (results == null) return "";
    else return results[1];
}
  