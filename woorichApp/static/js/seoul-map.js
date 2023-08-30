mapboxgl.accessToken = 'pk.eyJ1Ijoid29veW9vbndpbm5pZSIsImEiOiJjbGx1anJkdWsxY29kM2Zuem1naWpqdWc2In0.SAvOfExJLVtezNxgW8GAig'
const map = new mapboxgl.Map({
    container: 'map-container', // container ID
    center: [126.9779692, 37.566535], // starting position [lng, lat]
    zoom: 10.2, // starting zoom
    style: 'mapbox://styles/mapbox/light-v10', // style URL or style object
    
    hash: true, // sync `center`, `zoom`, `pitch`, and `bearing` with URL
    // Use `transformRequest` to modify requests that begin with `http://myHost`.
    language: "auto",
    transformRequest: (url, resourceType) => {
        if (resourceType === 'Source' && url.startsWith('http://myHost')) {
            return {
                url: url.replace('http', 'https'),
                headers: {'my-custom-header': true},
                credentials: 'include'  // Include cookies for cross-origin requests
            };
        }
    }
});
map.on('load', function() {
    
    map.addSource('tileset_data', {
        "url": "mapbox://wooyoonwinnie.aahbjlxw",
        "type": "vector"
    });
    map.addLayer({
        'id': 'background',
        'type': 'background',
        'source': 'tileset_data',
        'source-layer': 'seoul_gu-3hhcst',
        'paint' : {
            'background-color': 'hsla(0, 0%, 100%, 1)'
        }
    });
    map.addLayer({
        'id': 'fill',
        'type': 'fill',
        'source': 'tileset_data',
        'source-layer': 'seoul_gu-3hhcst',
        'paint': {
            'fill-color': 'hsla(248, 53%, 58%, 0.5)',
            'fill-opacity': 0.75,
            'fill-outline-color': 'hsl(0, 100%, 100%)'
        }
    });

});

function show_report() {
    var selectedGu = document.getElementById('dynamic-select-gu').value;

    var selectedDong = document.getElementById('dynamic-select-dong').value;

    // Display the selected texts or perform any other action
    console.log("Selected 행정구: " + selectedGu + "\nSelected 행정동: " + selectedDong);

    var resultDiv = document.getElementById('result'); // Replace 'result' with the actual ID of your <div>
    resultDiv.innerHTML = "<br> 선택된 행정구: " + "<h3>" + selectedGu + "</h3>" + "<br> 선택된 행정동: " + "<h3>" + selectedDong+"</h3><br>";
}

////////////////////////////////////////////////////////////////////////////////

const selectElementGu = document.getElementById('dynamic-select-gu');
const selectElementDong = document.getElementById('dynamic-select-dong');

const staticUrl = document.currentScript.getAttribute('staticUrl');
// Replace 'administrative_dongs.csv' with the path to your CSV file
fetch(staticUrl + 'gu-dong-data.csv', {
    headers: {
        'Content-Type': 'text/csv; charset=cp-949' // Specify the character encoding
    }
})
.then(response => response.text()) // Read the CSV file as text
.then(csvData => {
    // Parse the CSV data into an array of objects
    const csvArray = csvData.split('\n').map(row => row.split(','));

    // Remove the header row if present (optional)
    const header = csvArray[0];
    if (header.length > 1) {
        csvArray.shift();
    }

    const guSet = new Set(); // Use a Set to store unique 행정구 values

    // Loop through the data to populate 행정구 dropdown and collect unique values
    csvArray.forEach(row => {
        const guValue = row[2]; // Assuming 행정구 is in column 3 (index 2)
        if (guValue) {
            guSet.add(guValue); // Add 행정구 value to the Set if it's not undefined
        }
    });

    // Populate the 행정구 dropdown with unique values
    guSet.forEach(guValue => {
        const option = document.createElement('option');
        option.value = guValue;
        option.text = guValue;
        selectElementGu.appendChild(option);
    });

    // Add an event listener to 행정구 dropdown to dynamically populate 행정동 dropdown
    selectElementGu.addEventListener('change', () => {
        // Clear existing options in 행정동 dropdown
        selectElementDong.innerHTML = '';

        const selectedGu = selectElementGu.value;

        // Loop through the data to find matching 행정동 values for the selected 행정구
        csvArray.forEach(row => {
            const guValue = row[2]; // Assuming 행정구 is in column 3 (index 2)
            const dongValue = row[3]; // Assuming 행정동 is in column 4 (index 3)

            if (guValue === selectedGu) {
                const option = document.createElement('option');
                option.value = dongValue;
                option.text = dongValue;
                selectElementDong.appendChild(option);
            }
        });
    });
})
.catch(error => console.error('Error:', error));