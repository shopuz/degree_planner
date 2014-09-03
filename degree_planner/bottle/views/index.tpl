%include header
<div class="col-md-8">
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
								<td rowspan="3"> {{ 2011 + year }} </td>
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
									<td> <a href="#" data-toggle="modal" data-target="#myModal" id="{{ str(2011+year) + '_' + session_value }}">{{ units[i] }}</a></td>	
								%else:
									<td> <a href="#" data-toggle="modal" data-target="#myModal" id="{{ str(2011+year) + '_' + session_value }}"> &nbsp;</a></td>	
								%end
							%end
							</tr>
						%end
						

					%end



				</table>
			</div> <!-- col-md-8 -->

			<div class="col-md-4">
				<form role="form" action="/" method="post">
					  <div class="form-group">
					    <label for="degree">Choose Degree</label>
					    <select name="degree" class="form-control" id="degree">
						    <option value=""> Choose Degree </option>
						    
						    %for degree_code in all_degrees.keys():
						    	<option value="{{ degree_code }}"> {{ all_degrees[degree_code] }} </option>
						    %end
					    	
							</select>
					  </div>
					   <div class="form-group">
					    <label for="major">Choose Major</label>
					    <select name="major" class="form-control" id="major">
					    	<option value=""> Choose Major </option>
					    	
							</select>
					  </div>
					   <div class="form-group">
					   	<input type="submit" value="Plan Degree" class="btn btn-primary"/>
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
				  	
				  	%if degree_req_units:

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

			</div><!-- col-md-4 -->

			
			<!-- Modal -->
			<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
			  <div class="modal-dialog">
			    <div class="modal-content">
			      <div class="modal-header">
			        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
			        <h4 class="modal-title" id="myModalLabel">Find a unit</h4>
			      </div>
			      <div class="modal-body">
			        <form role="form" >
							  
							    
							    <select class="form-control select_unit" id="planet">
							    	<option value="">  Planet Units</option>

							    	<!--
							    	<option value="ACCG260">	ACCG260	</option>
									<option value="AHIS230">	AHIS230	</option>
									<option value="ANTH106">	ANTH106	</option>
									<option value="ASTR170">	ASTR170	</option>
									<option value="ASTR178">	ASTR178	</option>
									<option value="BBE100">		BBE100	</option>
									<option value="BIOL108">	BIOL108	</option>
									<option value="BIOL260">	BIOL260	</option>
									<option value="BIOL261">	BIOL261	</option>
									<option value="BUSL100">	BUSL100	</option>
									<option value="CBMS123">	CBMS123	</option>
									<option value="ECON131">	ECON131	</option>
									<option value="EDUC108">	EDUC108	</option>
									<option value="EDUC261">	EDUC261	</option>
									<option value="ENV200">		ENV200	</option>
									<option value="ENVE214">	ENVE214	</option>
									<option value="ENVE237">	ENVE237	</option>
									<option value="ENVG262">	ENVG262	</option>
									<option value="GEOS112">	GEOS112	</option>
									<option value="GEOS126">	GEOS126	</option>
									<option value="GEOS204">	GEOS204	</option>
									<option value="ISYS100">	ISYS100	</option>
									<option value="LEX102">		LEX102	</option>
									<option value="LING337">	LING337	</option>
									<option value="MATH109">	MATH109	</option>
									<option value="MATH123">	MATH123	</option>
									<option value="MSM310">		MSM310	</option>
									<option value="PHL260">		PHL260	</option>
									<option value="PHYS159">	PHYS159	</option>
									<option value="PHYS242">	PHYS242	</option>
									<option value="SCOM100">	SCOM100	</option>
									<option value="SOC254">		SOC254	</option>
									<option value="SPED102">	SPED102	</option>
									<option value="STAT170">	STAT170	</option>
									<option value="STAT175">	STAT175	</option>
									-->
							    	</select>
							  
							   
							    <br/>
							    <select class="form-control select_unit" id="people">
							    	<option value="">  People Units</option>
							    	<!--
							    	<option value="ABST100">ABST100</option>
									<option value="ACBE100">ACBE100</option>
									<option value="ACSC100">ACSC100</option>
									<option value="ACSH100">ACSH100</option>
									<option value="AFAS300">AFAS300</option>
									<option value="AHIS120">AHIS120</option>
									<option value="AHIS140">AHIS140</option>
									<option value="AHMG101">AHMG101</option>
									<option value="ANTH151">ANTH151</option>
									<option value="ANTH202">ANTH202</option>
									<option value="ANTH305">ANTH305</option>
									<option value="ASN101">ASN101</option>
									<option value="BBA340">BBA340</option>
									<option value="BCM310">BCM310</option>
									<option value="COGS201">COGS201</option>
									<option value="COGS202">COGS202</option>
									<option value="CUL260">CUL260</option>
									<option value="CUL399">CUL399</option>
									<option value="DANC101">DANC101</option>
									<option value="ECH113">ECH113</option>
									<option value="ECH126">ECH126</option>
									<option value="ECH130">ECH130</option>
									<option value="ECHL213">ECHL213</option>
									<option value="ENGL108">ENGL108</option>
									<option value="ENVG111">ENVG111</option>
									<option value="EUL101">EUL101</option>
									<option value="FBE204">FBE204</option>
									<option value="GEN110">GEN110</option>
									<option value="GEOS251">GEOS251</option>
									<option value="HRM107">HRM107</option>
									<option value="INTS204">INTS204</option>
									<option value="LEX101">LEX101</option>
									<option value="LING109">LING109</option>
									<option value="LING120">LING120</option>
									<option value="LING248">LING248</option>
									<option value="LING290">LING290</option>
									<option value="LING332">LING332</option>
									<option value="LING397">LING397</option>
									<option value="MAS214">MAS214</option>
									<option value="MHIS115">MHIS115</option>
									<option value="MHIS202">MHIS202</option>
									<option value="MHIS211">MHIS211</option>
									<option value="MKTG127">MKTG127</option>
									<option value="MKTG309">MKTG309</option>
									<option value="MUS205">MUS205</option>
									<option value="PHL132">PHL132</option>
									<option value="PHL137">PHL137</option>
									<option value="POL107">POL107</option>
									<option value="POL108">POL108</option>
									<option value="POL304">POL304</option>
									<option value="PSY250">PSY250</option>
									<option value="PSY350">PSY350</option>
									<option value="SOC175">SOC175</option>
									<option value="SOC182">SOC182</option>
									<option value="SOC295">SOC295</option>
									<option value="SOC297">SOC297</option>
									<option value="SOC315">SOC315</option>
							    	-->
									</select>
							  
							   <br/>
							    
							    <select class="form-control select_unit" id="science"> 
							    	<option value="">  Science Units</option>
							    	<option value="COMP111">COMP111</option>
									<option value="COMP115">COMP115</option>
									<option value="COMP125">COMP125</option>
									<option value="COMP188">COMP188</option>
									<option value="COMP202">COMP202</option>
									<option value="COMP225">COMP225</option>
									<option value="COMP226">COMP226</option>
									<option value="COMP229">COMP229</option>
									<option value="COMP233">COMP233</option>
									<option value="COMP247">COMP247</option>
									<option value="COMP249">COMP249</option>
									<option value="COMP255">COMP255</option>
									<option value="COMP260">COMP260</option>
									<option value="COMP329">COMP329</option>
									<option value="COMP330">COMP330</option>
									<option value="COMP332">COMP332</option>
									<option value="COMP333">COMP333</option>
									<option value="COMP334">COMP334</option>
									<option value="COMP343">COMP343</option>
									<option value="COMP344">COMP344</option>
									<option value="COMP347">COMP347</option>
									<option value="COMP348">COMP348</option>
									<option value="COMP350">COMP350</option>
									<option value="COMP352">COMP352</option>
									<option value="COMP355">COMP355</option>
							    	
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