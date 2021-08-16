const webcamElement = document.getElementById('webcam');

const canvasElement = document.getElementById('canvas');

const snapSoundElement = document.getElementById('snapSound');

const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);


var photosTaken = 0; 

$("#webcam-switch").change(function () {
    photosTaken = 0
    if(this.checked){
        webcam.start()
            .then(result =>{
               cameraStarted();
               console.log("webcam started");
            })
            .catch(err => {
                displayError();
            });
    }
    else {        
        cameraStopped();
        webcam.stop();
        console.log("webcam stopped");
    }        
});

$('#cameraFlip').click(function() {
    webcam.flip();
    webcam.start();  

});

$('#closeError').click(function() {
    $("#webcam-switch").prop('checked', false).change();
});

function displayError(err = ''){
    if(err!=''){
        $("#errorMsg").html(err);
    }
    $("#errorMsg").removeClass("d-none");
}

function cameraStarted(){
    $('.header-desktop').css("position","");
    $('.md-modal').addClass('md-show');
    $('#msg-min-data').addClass('d-none')
    $('#train-data-container').empty()
    $("#train-instructions").text("Take 2 photos front facing the camera");

    $("#errorMsg").addClass("d-none");
    $('.flash').hide();
    $("#webcam-caption").html("on");
    $("#webcam-control").removeClass("webcam-off");
    $("#webcam-control").addClass("webcam-on");
    $(".webcam-container").removeClass("d-none");
    if( webcam.webcamList.length > 1){
        $("#cameraFlip").removeClass('d-none');
    }
    $("#wpfront-scroll-top-container").addClass("d-none");
    window.scrollTo(0, 0); 
    $('body').css('overflow-y','hidden');


}

function cameraStopped(){
    $('.header-desktop').css('position','fixed');
    $("#errorMsg").addClass("d-none");
    $("#wpfront-scroll-top-container").removeClass("d-none");
    $("#webcam-control").removeClass("webcam-on");
    $("#webcam-control").addClass("webcam-off");
    $("#cameraFlip").addClass('d-none');
    $(".webcam-container").addClass("d-none");
    $("#webcam-caption").html("Click to Start Camera");
    $('.md-modal').removeClass('md-show');
    $("#post-cam").removeClass('d-none')

}

$("#take-photo").click(function () {
    photosTaken += 1;
    beforeTakePhoto();
    let picture = webcam.snap();
    console.log(picture)
    document.querySelector('#download-photo').href = picture;

    $("#train-data-container").append(
        '<div class="col-lg-2 col-md-2 col-xs-2 thumb">'
                + '<img class="img-responsive train-dataset" src=" '+ picture +' " alt="">'
        + '</div>'
        ); 
        
    afterTakePhoto();
});

function beforeTakePhoto(){
    $('.flash')
        .show() 
        .animate({opacity: 0.3}, 500) 
        .fadeOut(500)
        .css({'opacity': 0.7});
    window.scrollTo(0, 0); 
    $('#webcam-control').addClass('d-none');
    $('#cameraControls').addClass('d-none');
}

function afterTakePhoto(){
    webcam.stop();
    $('#canvas').removeClass('d-none');
    $('#take-photo').addClass('d-none');
    $('#download-photo').addClass('d-none');
    $('#cameraControls').removeClass('d-none');
    $("#train-instructions").text("");

    if (photosTaken == 6) {
      $('#resume-camera').addClass('d-none');
      $('#exit-app').removeClass('d-none');
    } else {
        $('#exit-app').addClass('d-none');
        $('#resume-camera').removeClass('d-none');
        $("#post-cam").removeClass('d-none')

    }

}


function removeCapture(){
    $('#canvas').addClass('d-none');
    $('#webcam-control').removeClass('d-none');
    $('#cameraControls').removeClass('d-none');
    $('#take-photo').removeClass('d-none');
    $('#exit-app').addClass('d-none');
    $('#download-photo').addClass('d-none');
    $('#resume-camera').addClass('d-none');

    if (photosTaken == 2) {
        $("#train-instructions").text("Take 2 photos facing your left side");
    } else if (photosTaken == 4) {
        $("#train-instructions").text("Take 2 photos facing your right side");
    }
     else {
        $("#train-instructions").text("");

    }

}

$("#resume-camera").click(function () {
    webcam.stream()
        .then(facingMode =>{
            removeCapture();
        });
});

$("#exit-app").click(function () {
    removeCapture();
    $("#webcam-switch").prop("checked", false).change();
    $("#post-cam").removeClass('d-none')

});

