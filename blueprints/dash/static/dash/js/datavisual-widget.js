window.addEventListener('load', setup);

async function setup(){
    const ctx2 = document.getElementById('active-bar').getContext('2d');
    const World = await getData();
    const myChart2 = new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: World.dates,
        datasets: [
          {
            label: 'Active Cases',
            data: World.cases_active,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderWidth: 1
          }
        ]
      },
      options: {
          title: {
            display: true,
            text: 'Active Cases (World)'
        },
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  }

    //get data from csv
    async function getData() {

        const response_confirmed = await fetch('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv');
        const data_confirmed = await response_confirmed.text();
        const response_deaths = await fetch('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        const data_deaths = await response_deaths.text();
        const response_recovered = await fetch('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
        const data_recovered = await response_recovered.text();

        const dates = [];
        var cases_active = [];
        const first_row = data_confirmed.split('\n')[0].split(',');
    
        for(var i = 4; i < first_row.length; ++i)
        {
          var date = first_row[i].substring(0,4);
          if(date[date.length-1] == '/') { date = date.substring(0,3); }
          dates.push(date);
        }
    
        const second_row = data_confirmed.split('\n').slice(1)[0].split(',');
    
        for(var i = 4; i < second_row.length; ++i)
        {
          cases_active.push(parseInt(second_row[i]));
        }
    
        const rows_after_two = data_confirmed.split('\n').slice(2);
        const rat_death = data_deaths.split('\n').slice(2);
        const rat_recovered = data_recovered.split('\n').slice(2);

        for(var i = 0; i < rows_after_two.length; ++i)
        {
          const cols = rows_after_two[i].split(',');
          const cols2 = rat_death[i].split(',');
          const cols3 = rat_recovered[i].split(',');
          for(var j = 4; j < cols.length; ++j)
          {
            cases_active[j] += parseInt(cols[j])-(parseInt(cols2[j])+parseInt(cols3[j]));
          }
        }
        return {dates, cases_active};
      }