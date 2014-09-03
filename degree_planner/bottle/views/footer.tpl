</div> <!-- container -->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script>
    	var mytarget;
    	$('#myModal').on('show.bs.modal', function (e) {
			  mytarget = e.relatedTarget;
			  console.log(mytarget.id);
			  $.ajax({
	            type: 'POST',
	            url: '/populate_modal',
	            data: JSON.stringify({ 'year_session' : mytarget.id }),
	            contentType: "application/json",
	            //dataType: "json",
	            success: function(response) {
	                // Fill out the People Dropdown
	                $('#people').empty().append('<option> Choose People Unit </option>');
	                for (var k in response['people_units']){
	                	var option = '<option value= "'+ k + '"> ' + response['people_units'][k] + '</option>';
	                	$('#people').append(option);
	                }
	                 // Fill out the Planet Dropdown
	                $('#planet').empty().append('<option> Choose Planet Unit </option>');
	                for (var k in response['planet_units']){
	                	var option = '<option value= "'+ k + '"> ' + response['planet_units'][k] + '</option>';
	                	$('#planet').append(option);
	                }
	                
	            }
	        });


			});

			$(function() {
			// insert selected unit from modal into the table cell
			    $("button#submit").click(function(){
			    	$('.select_unit').each(function(){
			    		if ($(this).val())
			    			selected_unit = $(this).val();
			    			//alert($(this).val());
			    	});
			    	//alert(selected_unit);
			    	mytarget.text = selected_unit;

			    	$('#myModal').modal('hide');
			    });
			  });
			
			// allow only one unit to be chosen from the modal popup
			$(document).ready(function(){
				$('.select_unit').change(function(){
					console.log($(this).siblings('select'));
					$(this).siblings('select').each(function(){
						$(this).val('');
					});
				});
			});
			
    </script>

    <script>
	    function populate_major(degree_code){
	        
	        $.ajax({
	            type: 'POST',
	            url: '/populate_major',
	            data: JSON.stringify({ "degree_code" : degree_code }),
	            contentType: "application/json",
	            //dataType: "json",
	            success: function(response) {
	                // Fill out the Major Dropdown
	                $('#major').empty().append('<option> Choose Major </option>');
	                for (var k in response['majors']){
	                	var option = '<option value= "'+ k + '"> ' + response['majors'][k] + '</option>';
	                	$('#major').append(option);
	                }
	                
	            }
	        });

	      }
	    $(document).ready(function(){
	    	$('#degree').change(function(){
	    		populate_major($(this).val())

	    	});

	    });

    </script>
    <br/><br/>
  </body>
</html>