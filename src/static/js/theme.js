$('.datepicker').each(function(){
	var picker = new Pikaday({
		field: this
	});
});

$('.carousel').carousel({
  interval: 15000,
    pause: "hover",
    touch: true,
    keyboard: true
    
})

