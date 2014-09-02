%include header

  <script src="//code.jquery.com/jquery-1.10.2.js"></script>
   <script src="http://d3js.org/d3.v3.min.js"></script>
    <script src="http://www.jasondavies.com/wordcloud/d3.layout.cloud.js"></script>
    <script>
      function draw_wordcloud(words, word_dict){
        if ($('svg').length )
          $('svg').remove();
        console.log(words);
        
        var fill = d3.scale.category20();
        // accept the word list as a string and process the word list
        // convert &quot; to "
        // convert &#39; to '
        // Finally convert the string into an array
        var formatted_words = words.replace(/&quot;/g, "\"");
        formatted_words = formatted_words.replace(/&#039;/g, "\'");
        var my_words = JSON.parse(formatted_words);
        
          
        var word_dict = word_dict.replace(/&quot;/g, "\"");
        word_dict = word_dict.replace(/&#039;/g, "\'");
        console.log(word_dict);
        word_dict = JSON.parse(word_dict);

        var fontSize = d3.scale.log().range([10, 100]);

        d3.layout.cloud().size([900, 900])
            .words(my_words.map(function(d) {
              return {text: d, size: word_dict[d]};
            }))
            .padding(5)
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d) { return fontSize(+d.size); })
            .on("end", draw)
            .start();
       
        function draw(words) {
          d3.select("#drawing").append("svg")
              .attr("width", 900)
              .attr("height", 900)
            .append("g")
              .attr("transform", "translate(150,150)")
            .selectAll("text")
              .data(words)
            .enter().append("text")
              .style("font-size", function(d) { return d.size + "px"; })
              .style("font-family", "Impact")
              .style("fill", function(d, i) { return fill(i); })
              .attr("text-anchor", "middle")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
              .text(function(d) { return d.text; });
        }
      }
    </script>
    <script>
      function visualise(name){
        
        $.ajax({
            type: 'POST',
            url: '/visualise',
            data: JSON.stringify({ "item_list_name" : name }),
            contentType: "application/json",
            //dataType: "json",
            success: function(response) {
                draw_wordcloud(response['words'], response['word_dict']);
                //alert(response['list']);
                //draw_wordcloud();
            }
        });

      }

    </script>

    
  <h3> Alveo WordCloud </h3>
  <div class="row">
    <div class="col-md-3">
      <div class="panel panel-primary item_ist">
          <div class="panel-heading"> My Item List </div>
          <ul class="list-group">
          %for item in personal_item_list:
           <li class="list-group-item"> <a href="#" onclick="visualise('{{ item['name'] }}')">  {{ item['name'] }} </a> </li>
          %end
          </ul>
          <div class="panel-heading"> Shared List</div>
          <ul class="list-group">
          %for item in shared_item_list:
           <li class="list-group-item"> <a href="#" onclick="visualise('{{ item['name'] }}')">  {{ item['name'] }} </a> </li>
          %end
          </ul>
        </div>
      </div>

    <div class="col-md-9">
      <div id="drawing">
      </div>
    </div>
  
    




%include footer
</html>