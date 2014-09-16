%include header
<div class="col-md-8">
			<div>
				Degree Planner is an effort to ease a complex situation faced by each student while planning their entire degree. This is just a demo of a utility which can prove to be of great importance for all the students. Currently, the system is able to handle the following Degrees/Majors:
				<ul>
					<li> Bachelor of Information Technology - All Majors </li>
					<li> Bachelor of Information Technology - Games Design and Development </li>
					<li> Bachelor of Commerce - Accounting Major </li>
				</ul>	
			</div>
		    %if selected_degree:
				<h4>
					Degree: {{ selected_degree }} <br/>
					Major: {{ selected_major }}<br/>

				</h4>
			%end

				<br/>
		    <table class="prod" cellspacing="0" cellpadding="0">
					%for year in xrange(3):
						
						%for session in xrange(3):
							<tr>
							%if session == 0:
								<td rowspan="3"> {{ int(degree_year) + year }} </td>
							%end
							<td>S{{session + 1}}</td>

							%if session % 2 == 0:
								% session_value = 's1'
							%else:
								% session_value = 's2'
							%end


							
							
							% no_of_cells = 4
							%if session == 2:
								% no_of_cells = 2
								% units = []
								% session_value = 's3'
							%else:
								%if sorted_years:
								% units = all_available_units[sorted_years[year]][session][session_value]	
								%else:
									% units = []
								%end
							%end

							%for i in xrange(no_of_cells):
								%if (i < len(units)):
									<td> <a href="#" data-toggle="modal" data-target="#myModal" id="{{ str(int(degree_year)+year) + '_' + session_value }}">{{ units[i] }}</a></td>	
								%else:
									<td> <a href="#" data-toggle="modal" data-target="#myModal" id="{{ str(int(degree_year)+year) + '_' + session_value }}"> &nbsp;</a></td>	
								%end
							%end
							</tr>
						%end
						

					%end



				</table>
			<div>
</div>	
			</div> <!-- col-md-8 -->

			<div class="col-md-4">
				<form role="form" action="/" method="post">
					  <div class="form-group">
					    <label for="degree">Choose Degree</label> <br/>
					    <select name="degree" id="degree">
						    <option value=""> Choose Degree </option>
						    
						    %for degree_code in all_degrees.keys():
						    	<option value="{{ degree_code }}"> {{ all_degrees[degree_code] }} </option>
						    %end
					    	
							</select>
					  </div>
					   <div class="form-group">
					    <label for="major">Choose Major</label> <br/>
					    <select name="major"  id="major">
					    	<option value=""> Choose Major </option>
					    	
							</select>
					  </div>
					   <div class="form-group">
					   	<input type="submit" value="Plan Degree" class="btn btn-primary"/>
					   	<span id="imgSpinner2" style="display:none;"> <img src="/static/images/loading_img.gif" width="25" height="25"/> </span>
					   </div>
					</form>

				<div class="panel panel-primary">
					<div class="panel-heading">
						%if selected_degree:
				    		<h3 class="panel-title">Degree Requirements for {{ selected_degree }}</h3>
				    	%else:
				    		<h3 class="panel-title">Degree Requirements</h3>
				    	%end
				  	</div>
				  	
				  	%if gen_degree_req:

					     <!-- List group -->
						  <ul class="list-group">
						    <li class="list-group-item" id="degree_req_units"> 
						    	%for req in degree_req_units:
						    		<span class="degree_req_unit">
							    		%if req in updated_degree_req_units:
							    			
								    			<input type="checkbox" >
								    				<label class="req_unsatisfied">  {{ req }} </label>
								    			</input>  <br/>
								    		
							    		%else:
							    			<input type="checkbox" disabled="disabled"  checked >
							    				<label class="req_satisfied"> {{ req }}  </label>

							    			</input>  <br/>
										%end
									</span>
								%end
							    
						    </li>
						  
						    <li class="list-group-item" id="gen_degree_req">
							    %for req in gen_degree_req.keys():
						    		%if updated_gen_degree_req[req] == 0:
						    			<input type="checkbox" disabled="disabled"  checked> 
						    				<label class="req_satisfied"> {{ req }} : 0 </label>
						    			</input>  <br/>
						    		%else:
						    			<input type="checkbox">
						    				<label class="req_unsatisfied">  {{ req }} : {{ updated_gen_degree_req[req] }} </label>
						    			</input>  <br/>
									%end
								%end
							    
						    	
						    </li>
						    
						  </ul>
					%end
				  

				</div>

				<div class="panel panel-primary" >
					<div class="panel-heading">
					%if selected_major:
				    	<h3 class="panel-title">Major Requirements for {{ selected_major }}</h3>
				    %else:
				    	<h3 class="panel-title">Major Requirements</h3>
				    %end
				  </div>
				  	
				     <!-- List group -->
					  <ul class="list-group">
					  <li class="list-group-item" id="major_req_units"> 
					  	%if major_req_units:
						    %for req in major_req_units:
					    		%if req in updated_major_req_units:
					    			<input type="checkbox">
					    				<label class="req_unsatisfied">  {{ req }} </label>
					    			</input>  <br/>
					    		%else:
					    			<input type="checkbox" disabled="disabled"  checked>
					    				<label class="req_satisfied">  {{ req }} </label>
					    			</input>  <br/>
								%end
							%end
						%end
					   </li>
					    
					  </ul>
				  

				</div>
				<div>
					Project Source : <a href="http://github.com/shopuz/degree_planner">Github</a>
				</div>
			</div><!-- col-md-4 -->

			
			<!-- Modal -->
			<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
			  <div class="modal-dialog">
			    <div class="modal-content">
			      <div class="modal-header">
			        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
			        <h4 class="modal-title" id="myModalLabel">Find a unit</h4>
			        <span id="imgSpinner1"> <img src="/static/images/loading_img.gif" width="25" height="25"/> </span>
			      </div>
			      <div class="modal-body">
			        <form role="form" >
							  
							    
							    <select class=" select_unit" id="planet">
							    	<option value="">  Planet Units</option>
								</select>
							  
							   
							    <br/>
							    <br/>
							    <select class=" select_unit" id="people">
							    	<option value="">  People Units</option>
							    </select>
							  
							   <br/>
							   <br/>
							    
							    <select class=" select_unit" id="computing"> 
							    	<option value="">  Computing Units</option>
							    </select>
							  	<br/>
							  	<br/>
							  	<select class=" select_unit" id="business"> 
							    	<option value="">  Business / Economics Units</option>
							    </select>

							  
							</form>
			      </div>
			      <div class="modal-footer">
			        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
			         <button class="btn btn-success" id="submit">Select</button>
			        
			      </div>
			    </div>
			  </div>
			</div>

%include footer			
