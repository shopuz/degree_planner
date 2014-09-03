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

			    	// update the degree/major requirements
			    	$.ajax({
			            type: 'POST',
			            url: '/update_requirements',
			            data: JSON.stringify({ "selected_unit" : selected_unit }),
			            contentType: "application/json",
			            //dataType: "json",
			            success: function(response) {
			            	// Update the Requirements on the right pane
			            	// Degree Requirement Units
			            	degree_req_units = response['updated_degree_req_units']
			            	if (degree_req_units.length > 0)
			            		{
			            			$('#degree_req_units input:not(:checked) + label').each(function(){
			            				if ($.inArray($(this).text(), degree_req_units) == -1) {
			            					$(this).removeClass('req_unsatisfied').addClass('req_satisfied');
			            					$(this).prev('input').prop('checked', true);
			            					$(this).attr('disabled', 'disabled');
			            				}

			            			});
			            		}
			            		

			            	// General Degree Requirements
			            	gen_degree_req  = response['updated_gen_degree_req'];
			            	$('#gen_degree_req').text("");
			            	for (var k in gen_degree_req){
		            			if (gen_degree_req[k] == 0)
		            				{
					    			$('#gen_degree_req').append('<input type="checkbox" disabled="disabled"  checked> <label class="req_satisfied">' + k + ': 0  </label></input>  <br/>');
		            				}
					    		else
					    		{
					    			$('#gen_degree_req').append('<input type="checkbox">  <label class="req_unsatisfied">' + k + ' : ' + gen_degree_req[k] +  '</label></input>  <br/>');
					    		}
								
							
			            	}


			            	// Major Requirement Units
			            	major_req_units = response['updated_major_req_units']
			            	if  (major_req_units.length > 0)
			            		{
			            			console.log(major_req_units);
			            			$('#major_req_units input:not(:checked) + label').each(function(){
			            				
			            				console.log($(this).text());
			            				if ($.inArray($.trim($(this).text()), major_req_units) == -1) {
			            					$(this).removeClass('req_unsatisfied').addClass('req_satisfied');
			            					$(this).prev('input').prop('checked', true);
			            					$(this).prev('input').prop('disabled', true);
			            				}

			            			});
			            		}
			            	else
			            	{
			            		$('#major_req_units input:not(:checked) + label').each(function(){
			            			$(this).removeClass('req_unsatisfied').addClass('req_satisfied');
			            					$(this).prev('input').prop('checked', true);
			            					$(this).prev('input').prop('disabled', true);
			            				});

			            	}


			            }
			        });

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