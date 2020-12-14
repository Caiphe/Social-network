$(document).ready(function(){
  $('#modal-btn').click(function(){
    $('.ui.modal')
    .modal('show')
  ;
  })

  let display = false

  $(".cmt_btn").click(function () {
    if (display===false) {
      $(this).next(".comment-box").show("slow");
      display=true
    } else {
      $(this).next(".comment-box").hide("slow");
      display=false
    }  
  });
  
})