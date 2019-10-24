var selected_circ;
var no_cands = 0;
var css_transition_time = 600;

function generateRegistryTableBody(data){
  var html = '';
  for(var i=0; i<data.length; i++){
    t = data[i];
    
    html += '<tr><td>'+t.no+'</td><td >'+t.reg_area+'</td><td><a target="_blank" href="'+t.map_url+'">'+t.polling_station+'</a></td><td>'+t.electors+'</td></tr>';

    }
  return html;

}


function generateCandidatesTableBody(data){
  var html = '';


  no_cands = 0;
  for(var i=0; i<data.length; i++){
    t = data[i];
    no_cands++;
    var logo = logo_data[t.icon_name]  || ''
    var gender = gender_svg[t.gender]
    
    html += '<tr><td>'+t.no+'</td><td class="gender">'+gender+'</td><td>'+t.name+'</td><td >'+t.party+'</td><td>'+logo+'</td></tr>';

    }


  jQuery('.no-cands').text(no_cands);
  return html;

}

function calculateTotalElectors(circ){
  var no = 0;
  for(var i=0;i<circ.length;i++){
    no += circ[i].electors;
  }
  return no;

}

function loadCirconscription(div){
  jQuery('.card.transition').hide();
  if(!scrollfirst){

   
  
      jQuery('html,body').animate({
    scrollTop: jQuery("#info").offset().top
    }, '550');


   



  }else{
      jQuery('html,body').animate({
    scrollTop: jQuery("html").offset().top
    }, '550');

  }
  scrollfirst=false;



  jQuery('.circ').removeClass('selected');
  jQuery(div).addClass('selected');
  var circ = jQuery(div).attr('class').split(/\s+/)[1].replace('c','');
  selected_circ = circ;
  //console.log("click circ:",circ);

  var circ_no = circ;
  
  if (circ.toString().length == 1) {
            circ_no = "0" + circ;
  }
  jQuery('.const-no-block').text(circ_no);


  jQuery('.const-name').text(results[circ-1].name);
  jQuery('.ret-officer').text(results[circ-1].returning_officer);
  jQuery('.centre-de-depouillement').text(results[circ-1].centre_depouillement);
  jQuery('.nomination-center').text(results[circ-1].nomination_center);



  var  centre_votes = registry_data[circ].length;
  jQuery('.centres-de-vote').text(centre_votes);


  jQuery('.ret-pic').css({backgroundImage:"url('./elections_assets/img/"+results[circ-1].ret_file_name+"')"});
  //console.log("url('./assets/img/"+results[circ-1].ret_file_name+"');");
  var electors = calculateTotalElectors(registry_data[circ])
  jQuery('.electors').text(electors);


  var tbody = generateRegistryTableBody(registry_data[circ]);
  jQuery('.vote-center-ctn table tbody').html(tbody);
  loadResults(circ, "2014");
  jQuery('.year-select.2014').focus();

  var tbody2 = generateCandidatesTableBody(candidates_data[circ]);
  jQuery('.cand-ctn table tbody').html(tbody2);

  jQuery(".card.transition").fadeIn(css_transition_time);
  return circ;

}

function buildResultsTableBody(circ, year){
  var html = '';
  var data = results_data[circ][year];
  
  for(var i=0; i<data.length; i++){
    t = data[i]
    html += '<tr><td>'+t.no+'</td><td>'+t.name+'</td><td>'+t.party+'</td><td>'+t.votes+'</td><td>'+t.perc_votes+'</td></tr>';
    }

  return html;

}

function loadResults(selected_circ, year){
  jQuery('.year-select').removeClass('selected');
  jQuery('.year-select.'+year).addClass('selected');
  var table_data = buildResultsTableBody(selected_circ, year);
  jQuery('.results-table-ctn table tbody').html(table_data);

}