window.onload = function(){
  $('.loading').fadeOut();
  floatText();
  openDetail();
  openSubcontents();
  openBooksInfo();
  closeContents();
  updateContents();
  deleteContents();
};

function floatText(){
  $('#default-text').animate({marginTop: '-=10px'}, 800).animate({marginTop: '+=10px'}, 800);
  setTimeout('floatText()', 1600);
}


function openDetail(){
  try{
    var btn = document.getElementById("detail-btn");
    btn.onclick = function(){
      $("#nav-items").slideToggle();
    };
  }
  catch(e){
    console.log(e);
  }
};


function openSubcontents(){
  var btns = document.getElementsByClassName("sub-content-btn");
  var sub_data = []
  for (var i = 0; i < btns.length; i++) {
    sub_data.push(btns[i].dataset.sub);
  };
  for (var i = 0; i < btns.length; i++) {
    btns[i].onclick = function(){
      var sub = this.dataset.sub;
      for (var i = 0; i < sub_data.length; i++) {
        if (sub_data[i] == sub) {
          console.log(sub+"がクリックされました");
          document.getElementById(sub+"-area").classList.add("show");
          document.getElementById(sub).classList.add("show");
        }
        else {
          document.getElementById(sub_data[i]+"-area").classList.remove("show");
          document.getElementById(sub_data[i]).classList.remove("show");
        };
      };
    };
  };
};

function openBooksInfo(){
  var keyword_boxes = document.getElementsByClassName("keyword-box");
  for (var i = 0; i < keyword_boxes.length; i++) {
    keyword_boxes[i].onclick = function(){
        var class_names = this.className;
        if (class_names.match("active")) {
          this.classList.remove("active");
          var show_keyword_info = this.dataset.showKeywordInfo;
          var show_keyword_library = this.dataset.showKeywordLibrary;
          $("#"+show_keyword_library+" "+"."+show_keyword_info).slideUp();
        }else{
          this.classList.add("active");
          var show_keyword_info = this.dataset.showKeywordInfo;
          var show_keyword_library = this.dataset.showKeywordLibrary;
          $("#"+show_keyword_library+" "+"."+show_keyword_info).slideDown();
        };
    };
  };
};

function closeContents(){
  var close_btns = document.getElementsByClassName("close-btn");
  for (var i = 0; i < close_btns.length; i++) {
    close_btns[i].onclick = function(){
      var parent = this.parentNode;
      var close_contents_id = parent.id;
      $("#"+close_contents_id).removeClass("show");
    };
  };
};

function updateContents(){
  var btn = document.getElementById("update-input-btn");
  btn.onclick = function(){
    $('.loading').fadeIn();
  };
};

function defaultInput(){
  var btn = document.getElementById("default-input-btn");
  btn.onclick = function(){
    $('.loading').fadeIn();
  };
};

function deleteContents(){
  var btns = document.getElementsByClassName("delete-btn");
  for (var i = 0; i < btns.length; i++) {
    btns[i].onclick = function(){
      $('.loading').fadeIn();
    };
  };
};
