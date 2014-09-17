%include header
	<div class="col-md-8">
		<h3> Documentation </h3>
		<p>
		<h4>Features</h4>
			<ol>
				<li> Application Layer on top of Handbook API </li>
				<li> Test Driven Approach to produce the entire code </li>
				<li> Three distinct classes based on their functionality 
					<ol type="a"> 
			     <li><b>Prereq Parser and Evaluator </b>
			     		<ul>
			          <li> handles parsing the requisites of a degree / major / unit </li>
			          <li> converts the string representation of the requisite into a binary tree form </li>
			          <li> finally evaluate a requisite based on the units that a student has already taken</li>
			          <li> update the requirements of a degree and a major </li>
		        	</ul>
			      </li>

			     <li> <b>Handbook</b>
			          - main layer which connects to the Handbook API and fetches all the required information about a degree/ major / unit
			     </li>
			     <li><b> Degree Planner</b>
			          - used to plan the entire degree of a student
			      </li>
			    </ol>
			  </li>
				<li> Bottle Web Interface</li>
			</ol>

		<br/><br/>
		<h4> Process Diagrams </h4>
		<div>
			<img src="/static/images/phase_1.jpg" class="img-responsive" /> <br/> <br/><br/>
			<img src="/static/images/phase_2.jpg" class="img-responsive" />
		</div>

		<h4> Types of Requirements </h4>
			<ol>
				<li> Prereq of a unit </li>
				<li> General Requirements of a Degree </li>
				<li> Foundation Units of a Degree </li>
				<li> Core units of a Major </li>
			</ol>


		<h4> Web Interface </h4>
			<ol>
				<li> Populates the entire list of Degree </li>
				<li> Retrieve the majors corresponding to the Degree </li>
				<li> Plan
					<ul>
				     <li> Gets the requirements and units of Degree / Major </li>
				     <li> For each unit, check the prerequisite, parse the prereq and evaluate the prereq</li>
				     <li> Assumption : Fill in True for the vacant slots in a session and carry on with filling the rest of the slots</li>
				     <li> Update the requirements</li>
				  </ul>
				</li>
				<li> Click on each empty slot to fill a unit
					<ul>
				    <li> Gets all the computing and business units offered in that particular session which satisfy the prerequisite </li>
				    <li> After selecting a unit, an ajax call is made to update the requirements on the right hand side </li>
				  </ul>
				</li>
			</ol>

		<h4>Colour Code of Requirements </h4>
			<span style="color:red" > Red </span> - Unsatisfied Requirement <br/>
			<span style="color:green"> Green </span> - Satisfied Requirement <br/>
		<div class="clearfix"></div>


		</p>
	</div>

%include footer