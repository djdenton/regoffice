// Daniel Denton 2014
// Based on ASlider by Varun Naik

var duration = 10;
var script = "Companies";


var getCompanies = function() {
    $("#companies").load(script, function( data ) { 
         firstSlide();
    });
}

var firstSlide = function() {
   
   $(".aslide:first").addClass('visible');

   setTimeout( function(){ 
        currentSlide = $(".aslide:first");       
        advanceSlide(currentSlide);
    }
    , parseInt(duration) * 1000 );
}

var advanceSlide = function(currentSlide) {

    var nextSlide = $(currentSlide).next('.aslide');
    
    if (nextSlide.length == 0) { // Loop to the first slide if we are on the last slide now
        nextSlide = $(currentSlide).parent().children('.aslide:first-child');
    }

    $(currentSlide).toggleClass("visible");
    $(nextSlide).toggleClass("visible");

    setTimeout( function(){ 
        advanceSlide(nextSlide);
    }
    , parseInt(duration) * 1000 );

}