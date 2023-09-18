fetch(staticUrl + '/data/model-eval-result.csv', {
    headers: {
        'Content-Type': 'text/csv; charset=cp-949' // character encoding
    }
})
.then(response => response.text())
.then(csvData => {
    csvArray = csvData.split('\n').filter(row => row).map(row => row.split(','));
    const header = csvArray[0];
    const hrContainer = document.getElementById('table-head-row');
    hrContainer.innerHTML = header.map((item)=> {
        return `<th class="text-center">${item}</th>`
    }).join("")

    if (header.length > 1) {
        csvArray.shift();
    }
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = csvArray.map((row)=>{
        const tdList = row.map((item)=> {
            return `<td>${item}</td>`
        }).join("")
        return `<tr>${tdList}</tr>`
    }).join("")
})