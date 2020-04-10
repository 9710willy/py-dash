
//api for testing
const api_url_us = 'https://api.covid19api.com/total/country/united-states/status/confirmed';

// api url for country list
const country_api = 'https://api.covid19api.com/countries';

//append country slug & condition string
var cases_active = "https://api.covid19api.com/country/" ;
const confirmed = "/status/confirmed";
const recovered = "/status/recovered";
const deaths = "/status/deaths";

window.addEventListener('load', setup);

function setup(){
    const ctx = document.getElementById('myChart').getContext('2d');
    const US_cases = getData();
    const myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: US_cases.dates,
        datasets: [
          {
            label: 'Cases in the United States',
            data: US_cases.cases,
            fill: false,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderWidth: 1
          }
        ]
      },
      options: {}
    });
  }
  
  function getData() {
    const response = fetch(api_url_us);
    const data_us = response.json();
    const dates = [];
    const cases = [];
  
    Object.entries(data_us).forEach(([key, value]) => {
          if(key == "Date")
          {
              dates.push(value.substring(5,10));
          }
          else if(key == "Cases")
          {
              cases.push([value]);
          }
      });
      return {dates, cases};
  }

// Select map tab
$(".graph-tab").click(function(){
    $(".graph-tab").css("background-color", "whitesmoke");
    $(this).css("background-color", "rgb(211, 211, 211)");
 
    if($(this).text() == "Linear"){
 
    }else if($(this).text() == "Logarithmic"){
    }

 });

