/*
   
   Table Of Content
   
   1. Preloader
   2. Smooth Scroll
   3. Scroll Naviagation Background Change with Sticky Navigation
   4. Mobile Navigation Hide or Collapse on Click
   5. Scroll To Top
   6. Typed.js
   7. Parallax Background
   8. Portfolio Filtering
   9. Magnific Popup
  10. Testimonial Carousel/Slider
  11. Statistics Counter
  12. Google Map
 

*/


(function ($) {
    'use strict';

    jQuery(document).ready(function () {

        var timefrom;
		var timeto;
       /* Preloader */
        $(window).on('load', function() {
          $('body').addClass('loaded');
		  $("#first_load_all").click();
        });
		 
		//adding the code for websockets ---start----
			var ws = new WebSocket("ws://10.201.0.62:8888/ws"); //"ws://10.201.2.85:8888/ws"
			ws.onopen = function(evt) {
			  var conn_status = document.getElementById('conn_text');
			  conn_status.innerHTML = "Connection status: Connected!"
			  $("#conn_text_1").text("Connection status: Connected!");
			};
			ws.onmessage = function(evt) {				
			 var d = new Date();
			 timeto = d.getTime();
			  var newMessage = document.createElement('p');
			  var msg = JSON.parse(evt.data);
			  if(msg.Labels){
				  var len_envi = msg.Labels.length;
				  var txt_envi = "";
                  if(len_envi > 0){
                    for(var i=0;i<len_envi;i++){
                        if(msg.Labels[i].Name && msg.Labels[i].Confidence){
							var name_1 = msg.Labels[i].Name.toString();
							var confience_1 = msg.Labels[i].Confidence.toFixed(2).toString();
                            txt_envi += "<tr><td>"+name_1+"</td><td>"+confience_1+"</td></tr>";
                        }
                    }
                    if(txt_envi){
                        $("#table_envi").append(txt_envi).removeClass("hideme_envi");
                    }
                }
			  }
			  else {
			  $("#temp_text").text(msg.temp.toString());
			  $("#humid_text").text(msg.humid.toString());
			  $("#Total_Time_Taken").text((timeto-timefrom).toString()+"micro seconds");
			  }	
			 
			};
			ws.onclose = function(evt) {
			  conn_text.innerHTML = "Connection status: Connection closed";
			  $("#conn_text_1").text("Connection status: Connection closed");
			};
			$("#car_down").click(function(evt) {
			  evt.preventDefault();
			  var message = "rev";
			  ws.send(message);
			});
			$("#car_stop").click(function(evt) {
			  evt.preventDefault();
			  var message = "stop";
			  ws.send(message);
			});
			$("#car_up").click(function(evt) {
			  evt.preventDefault();
			  var message = "up";
			  ws.send(message);
			});
			$("#car_right").click(function(evt) {
			  evt.preventDefault();
			  var message = "right";
			  ws.send(message);
			});
			$("#car_left").click(function(evt) {
			  evt.preventDefault();
			  var message = "left";
			  ws.send(message);
			});
			$("#btn_temp_humid").click(function(evt){
			  evt.preventDefault();
			  var message = "get";			  
			  var d = new Date();
			  timefrom = d.getTime();
			  ws.send(message);
			});
			$("#btn_get_envi_info").click(function(evt){
			  evt.preventDefault();
			  var message = "envi";
			  ws.send(message);
			});
			
		//adding the code for websockets --end--
		
		
		//adding the code for MQTT Communication through AWS ---------------------------------------Start----
		
		//adding the code for MQTT Communication through AWS ---------------------------------------End----
		
		
       /* Smooth Scroll */

        $('a.smoth-scroll').on("click", function (e) {
            var anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: $(anchor.attr('href')).offset().top - 50
            }, 1000);
            e.preventDefault();
        });


       
       /* Scroll Naviagation Background Change with Sticky Navigation */
		 
        $(window).on('scroll', function () {
            if ($(window).scrollTop() > 100) {
                $('.header-top-area').addClass('navigation-background');
            } else {
                $('.header-top-area').removeClass('navigation-background');
            }
        });
		
		
		
		
       /* Mobile Navigation Hide or Collapse on Click */
		
        $(document).on('click', '.navbar-collapse.in', function (e) {
            if ($(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle') {
                $(this).collapse('hide');
            }
        });
        $('body').scrollspy({
            target: '.navbar-collapse',
            offset: 195
        
		 });
		 
		
		
		
        /* Scroll To Top */
		
        $(window).scroll(function(){
        if ($(this).scrollTop() >= 500) {
            $('.scroll-to-top').fadeIn();
         } else {
            $('.scroll-to-top').fadeOut();
         }
	   });
	
	
	    $('.scroll-to-top').click(function(){
		  $('html, body').animate({scrollTop : 0},800);
		  return false;
	    });
		
		
		
		
        /* Typed.js */
		
        $(window).load(function(){
        $(".typing").typed({
            strings: ["Want to hack stuff?", "Bored of being a good person?", "EnziCarz is here to help you hack."],    /* You can change the home section typing text from
	                                                                                            here and do not use "&" use "and" */
            typeSpeed: 50
          });
         });
        
		 
        /* Parallax Background */

        $(window).stellar({
            responsive: true,
            horizontalScrolling: false,
            hideDistantElements: false,
            horizontalOffset: 0,
            verticalOffset: 0,
        });

        
		
		
        /* Portfolio Filtering */

        $('.portfolio-inner').mixItUp();


       
        /* Magnific Popup */

        $('.portfolio-popup').magnificPopup({
            type: 'image',
			
            gallery: { enabled: true },
			zoom: { enabled: true,
			        duration: 500
					
          },
		  
         image:{
               markup: '<div class="mfp-figure portfolio-pop-up">'+
               '<div class="mfp-close"></div>'+
               '<div class="mfp-img"></div>'+
               '<div class="mfp-bottom-bar portfolio_title">'+
               '<div class="mfp-title"></div>'+
               '<div class="mfp-counter"></div>'+
               '</div>'+
               '</div>',

               titleSrc:function(item){
                return item.el.attr('title');
              }
            }
		  
		  
          });

       
	   
		 
        /* Testimonial Carousel/Slider */

        $(".testimonial-carousel-list").owlCarousel({
            items: 1,
            autoPlay: true,
            stopOnHover: false,
            navigation: true,
            navigationText: ["<i class='fa fa-long-arrow-left fa-2x owl-navi'></i>", "<i class='fa fa-long-arrow-right fa-2x owl-navi'></i>"],
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [980, 1],
            itemsTablet: [768, 1],
            itemsTabletSmall: false,
            itemsMobile: [479, 1],
            autoHeight: true,
            pagination: false,
            transitionStyle : "backSlide"
        });
		
		
		
		
        /* Statistics Counter */
		
        $('.statistics').appear(function() {
           var counter = $(this).find('.statistics-count');
           var toCount = counter.data('count');
      
           $(counter).countTo({
           from: 0,
           to: toCount,
           speed: 5000,
           refreshInterval: 50
           })
           });
		   
		  
         
         /* Google Map */
		 
         $('#my-address').gMap({
            zoom: 5,
            scrollwheel: true,
            maptype: 'ROADMAP',
            markers:[
            {
            address: "Boulder",  /* You can change your address from here */
            html: "<b>Address</b>: <br> University of Colorado Boulder,Boulder, Colorado, U.S.A.",   /* You can change display address text from here */
            popup: true
            }
            ]
            });
              
		   
            });

   })(jQuery);