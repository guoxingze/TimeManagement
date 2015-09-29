	$('.flip-clock-label').hide();
	var workingEvent = "";
	var ifStopClock = false;
	var clock;
	$('#totalAchieve').text(0);
	$('#todayAchieve').text(0);




	$(document).ready(function() {
		//set color box
		$.colorbox.settings.close = 'Exit';

	    //initial clock
		clock = $('.clock').FlipClock(0, {
		        clockFace: 'MinuteCounter',
		        countdown: true,
		        callbacks: {
		        	stop: function() {
		        		if(!ifStopClock){
		        			showCompleteBox();
		        			disableStop();
		        			enableStart();
		        		}
		        		//reset stop flag
		        		ifStopClock = false;

		        	}
		        }
		    });

		//initial freewal
		var wall = new Freewall("#freewall");
		wall.reset({
			selector: '.brick',
			animate: true,
			cellW: 160,
			cellH: 160,
			delay: 50,
			onResize: function() {
				wall.fitWidth();
			}
		});
		wall.fitWidth();

		//ajax to inital achievements 
			updateAchieve();
	});



//setup model for knockout.js 
function AppViewModel() {
    var self = this;
    self.newEventName= ko.observable("");
    self.eventList = ko.observableArray([]);
    self.completedList = ko.observableArray([]);
    self.completeEventName = ko.observable("");
    self.checkEvent = function(){
    	console.log("test check")
    }


    self.addToDoEvent = function() {
    	var newEventName = $("#newEventName").val();
        saveNewEvent(newEventName);
        // self.eventList.push({ name: newEventName });
        self.eventList.splice(0,0,{ name: newEventName });
        // $("#newEventName").val('');
        self.newEventName("");
    };

    self.addCompletedEvent = function(name,time) {
    	console.log('test addCompletedEvent')
        // self.completedList.push({ name: name,time:time});
        self.completedList.splice(0,0,{ name: name,time:time});
        // $("#newEventName").val('');
        self.newEventName("");
    };

    self.removeSelected = function(input) {
    	self.eventList.remove(input)
    	deleteNewEvent(input['name'])
    };

    self.selectEvent = function() {
		console.log("input = " + input)
    };

    self.saveInColorBox = function(){
    	console.log("save completed event");
		var completeEventName = $('#completeEventName').val()
		completeTomato(completeEventName);
		$.colorbox.close();
		self.completeEventName("");
    }


    console.log("size of newEventName = " + newEventName.length);
}

// 'enter' key listener for new event name
	function enterInput(event){

	      if(event.keyCode==13){
			window.vm.addToDoEvent();
		}
	}


	function checkEvent(element){
	$('.eventCheck').not(element).each(function(){
         $(this).attr('checked', false);
     });

	if(element.checked){
		workingEvent = element.value
	}else{
		workingEvent = ""
	}
	console.log('value = ' + workingEvent)

	}

//update achievement
	function updateAchieve(){
		console.log("update achieve");
		$.ajax({
		  type: "POST",
		  url: "../api/update_achieve",
		  dataType: 'json',
		  data: JSON.stringify({"time":getCurrentDate()})
		})
		.done(function( data ) { // check why I use done
		    console.log("today = " + data['today'])
		    console.log("total = " + data['total'])
		    $('#totalAchieve').text(data['total']);
		    $('#todayAchieve').text(data['today']);
		    // $('.voteCount').text(data['story']['vote_count']);
		});
	}

	function disableStop(){
		$("#stopClock").prop('disabled', true);
	}

	function enableStop(){
		$("#stopClock").prop('disabled', false);
	}

	function disableStart(){
		$("#startClock").prop('disabled', true);
	}

	function enableStart(){
		$("#startClock").prop('disabled', false);
	}




	function setTimer(time){
		 clock.setTime(time);
		 clock.start();
		 enableStop();
		 disableStart();
	}

	function stopTimer(){
		ifStopClock = true;
		clock.reset();
		$.colorbox.close();
	}

	function continueWorking(){
		$.colorbox.close();
		clock.start();
		enableStop();
		disableStart();
	}
	function dropWork(){
		clock.stop();
		showStopBox();
	}
	function completeTomato(completedTomato){
		$.ajax({
		  type: "POST",
		  url: "../api/complete",
		  dataType: 'json',
		  data: JSON.stringify({ "eventName": completedTomato, "time":getCurrentDate()})
		})
		.done(function( data ) { // check why I use done
		    console.log( "event added");
		    window.vm.addCompletedEvent(data['name'],data['time']);
		    console.log("today = " + data['today'])
		    console.log("total = " + data['total'])
		    $('#totalAchieve').text(data['total']);
		    $('#todayAchieve').text(data['today']);
		    // $('.voteCount').text(data['story']['vote_count']);
		});
	}

	function saveNewEvent(newEventName){
		console.log("enter ajax test");
		$.ajax({
		  type: "POST",
		  url: "../api/save",
		  dataType: 'json',
		  data: JSON.stringify({ "eventName": newEventName, "time":getCurrentDate()})
		})
		.done(function( data ) { // check why I use done
		    console.log( "event added");
		    // $('.voteCount').text(data['story']['vote_count']);
		});
	}

	function deleteNewEvent(eventName){
		$.ajax({
		  type: "PUT",
		  url: "../api/delete",
		  dataType: 'json',
		  data: JSON.stringify({ "eventName": eventName})
		})
		.done(function( data ) { // check why I use done
		    console.log( "event deleted");
		    // $('.voteCount').text(data['story']['vote_count']);
		});
	}


	function showCompleteBox(){
		window.vm.completeEventName("");
		console.log("show completed color box");
		window.vm.completeEventName(workingEvent);
		$.colorbox({inline:true, width:"450px",height:"155px", overlayClose: false, href:"#completedColorBox"});
		// $("#completeEventName").val(workingEvent);
	}

	function showStopBox(){
		$.colorbox({inline:true, width:"450px",height:"155px", overlayClose: false, href:"#dropEventColorBox"});
	}



	function getCurrentDate(){
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var hh = today.getHours();
		var min = today.getMinutes();
		var yyyy = today.getFullYear();
		var ss = today.getSeconds();

		if(dd<10){
		    dd='0'+dd
		} 
		if(mm<10){
		    mm='0'+mm
		} 

		if(hh<10){
		    hh='0'+hh
		}

		if(min<10){
		    min='0'+min
		} 

		if(ss<10){
		    ss='0'+ss
		} 

		var result = yyyy +'-' + mm +'-'+ dd +' ' + hh + ':' + min + ':' + ss;
		return result
	}


	function switchTutorial(){
		// console.log($('#tutorialCheck').prop('checked'))
		if($('#tutorialCheck').prop('checked')){
			updateIfViewTutorial(false)
		}else{
			updateIfViewTutorial(true)				
		}
	}

	function showHelp(){
		$.colorbox({inline:true, width:"1200",height:"480px", overlayClose: false, href:"#tutorialColorBox"});
	}
	
	function updateIfViewTutorial(ifView){
		$.ajax({
		  type: "PUT",
		  url: "../api/update_tutorial",
		  dataType: 'json',
		  data: JSON.stringify({"ifView":ifView})
		})
		.done(function( data ) { // check why I use done
		    console.log("today = " + data['today'])
		});
	}
