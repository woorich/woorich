document.addEventListener('DOMContentLoaded', (event) => {
    const url = new URL(window.location.href);
  
    // Assuming the URL format is http://127.0.0.1:5000/dashboard/report/{reportType}/{dongCode}/{gu}/{dong}/{year}/{quarter}/{jobCode}
    const urlSegments = url.pathname.split('/');
    const reportType = urlSegments[3]; // The report type segment (sales, environment, or population)
    const dongCode = urlSegments[4]; // The dong code segment
    const currentGu = urlSegments[5]; // The gu segment
    const currentDong = urlSegments[6]; // The dong segment
    const year = urlSegments[7]; // The year segment
    const quarter = urlSegments[8]; // The quarter segment
    const jobCode = urlSegments[9]; // The job code segment
  
    const yearSelect = document.getElementById('dynamic-select-year');
    const quarterSelect = document.getElementById('dynamic-select-quarter');
  
    // Populate year select element with options from 2017 to 2022
    for (let i = 2017; i <= 2022; i++) {
      const option = document.createElement('option');
      option.value = i;
      option.text = i;
      yearSelect.appendChild(option);
    }
  
    // Populate quarter select element with options from 1 to 4
    for (let i = 1; i <= 4; i++) {
      const option = document.createElement('option');
      option.value = i;
      option.text = `${i} 분기`;
      quarterSelect.appendChild(option);
    }
  
    // Adding a submit button and defining its click event handler
    const submitButton = document.createElement('button');
    submitButton.textContent = '제출';
    submitButton.classList.add('btn', 'btn-outline-secondary');
    submitButton.addEventListener('click', () => {
      const selectedYear = yearSelect.value;
      const selectedQuarter = quarterSelect.value;
  
      if (selectedYear !== '년도' && selectedQuarter !== '분기') {
        var url = window.location.protocol + "//" + window.location.host + window.location.pathname;
        window.location.href = `${url}/${reportType}/${dongCode}/${currentGu}/${currentDong}/${selectedYear}/${selectedQuarter}/${jobCode}`;
      } else {
        alert('Please select a valid year and quarter.');
      }
    });
  
    document.querySelector('.input-group').appendChild(submitButton);
  });
  
  
  