const selectElementGu = document.getElementById('dynamic-select-gu');
const selectElementDong = document.getElementById('dynamic-select-dong');
let csvArray;
//const staticUrl = document.currentScript.getAttribute('staticUrl');
fetch(staticUrl + '/data/gu-dong-coord-data.csv', {
    headers: {
        'Content-Type': 'text/csv; charset=cp-949' // character encoding
    }
})
.then(response => response.text())
.then(csvData => {
    csvArray = csvData.split('\n').map(row => row.split(','));
    const header = csvArray[0];
    if (header.length > 1) {
        csvArray.shift();
    }

    const guSet = new Set();

    csvArray.forEach(row => {
        const guValue = row[2];
        if (guValue) {
            guSet.add(guValue);
        }
    });

    guSet.forEach(guValue => {
        const option = document.createElement('option');
        option.value = guValue;
        option.text = guValue;
        selectElementGu.appendChild(option);
    });

    selectElementGu.addEventListener('change', () => {
        selectElementDong.innerHTML = '';

        const selectedGu = selectElementGu.value;

        csvArray.forEach(row => {
            const guValue = row[2];
            const dongValue = row[3];

            if (guValue === selectedGu) {
                const option = document.createElement('option');
                option.value = dongValue;
                option.text = dongValue;
                selectElementDong.appendChild(option);
            }
        });

        // map 의 focusing 변경 + 색 강조 + map의 해당 구역은 popup 띄우기 
        var urlString = location.href;


    });
})
.catch(error => console.error('Error:', error));

//////////////////////////////////////////////////////////////////////////////////

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
            'background-color': 'hsla(0, 0%, 100%, 0.8)'
        }
    });
    map.addLayer({
        'id': 'fill',
        'type': 'fill',
        'source': 'tileset_data',
        'source-layer': 'seoul_gu-3hhcst',
        'paint': {
            'fill-color': 'hsla(335, 100%, 73%, 0.32)',
            'fill-opacity': 0.75,
            'fill-outline-color': 'hsl(0, 100%, 100%)'
        }
    });
    

    // markers.forEach(marker => {
    //     marker.getElement().addEventListener('mouseenter', () => {
    //         marker.togglePopup(); // Show the popup when hovered
    //     });
    
    //     marker.getElement().addEventListener('mouseleave', () => {
    //         marker.togglePopup(); // Hide the popup when not hovered
    //     });

    // });
});

/////////////////////////////////////////////////////////////////////////////////////

function show_report() {
    var selectedGu = document.getElementById('dynamic-select-gu').value;
    var selectedDong = document.getElementById('dynamic-select-dong').value;

    console.log("Selected 행정구: " + selectedGu + "\nSelected 행정동: " + selectedDong);

    var resultDiv = document.getElementById('result');
    resultDiv.innerHTML = "<br> 선택된 행정구: " + "<h3>" + selectedGu + "</h3>" + "<br> 선택된 행정동: " + "<h3>" + selectedDong+"</h3><br>";

    fetch(staticUrl+'/data/gu-dong-coord-data.csv')
    .then(response => response.text())
    .then(csvData => {
        const rows = csvData.split('\n');
        for(let i=0; i < rows.length;i++){
            let item = rows[i].split(',');
            let dong_code = item[1];
            let gu = item[2];
            let dong = item[3];
            let latitude = item[4];
            let longitude = item[5];
            if ((selectedGu == gu) && (selectedDong == dong)) {
                window.location.href = `/dashboard/report?dong_code=${dong_code}&gu=${gu}&dong=${dong}`;
                break;
            }
        }
    })
    .catch(error => console.error('Error loading CSV:', error));
}

////////////////////////////////////////////////////////////////////////////////

fetch(staticUrl+'/data/gu-geo.json')
    .then(response => response.text())
    .then(data => {
        // Add a change event listener to the select element
        data = JSON.parse(data);
        const markers = [];
        selectElementGu.addEventListener('change', (event) => {
            if (markers){
                markers.forEach(marker =>  marker.remove());
            }
            // Retrieve the selected district value
            const selectedDistrict = event.target.value;

            // Use the selected district value to focus the map
            // Replace this with your actual logic to focus on the selected district
            // For example, you can use geocoding or known coordinates to center the map on the selected district.
            // Here's a simplified example

            let lat = data[selectedDistrict]['위도'];
            let long = data[selectedDistrict]['경도'];
            let zoom_num = data[selectedDistrict]['줌비율'];
            map.flyTo({ center: [long, lat], zoom: zoom_num });
            
            // Add more conditions for other districts as needed
            const dongs_in_gu = [];
            // Fetch and add markers and popups
            for(i in csvArray){
                let item = csvArray[i];
                let gu = item[2];
                let latitude = parseFloat(item[4]);
                let longitude = parseFloat(item[5]);
                if ((selectedDistrict == gu) && !isNaN(latitude) && !isNaN(longitude)){
                    dongs_in_gu.push(item);        
                }
            } 
            for(i in dongs_in_gu){
                let item = dongs_in_gu[i];
                let index = item[0];
                let dong_code = item[1];
                let gu = item[2];
                let dong_name = item[3];
                let latitude = parseFloat(item[4]);
                let longitude = parseFloat(item[5]);

                const marker = new mapboxgl.Marker({color: 'white'})
                .setLngLat([longitude, latitude])
                .addTo(map);
        
                const popup = new mapboxgl.Popup({ closeButton: false, offset: 25 }) // Customize popup behavior
                .setLngLat([longitude, latitude])
                .setHTML(`
                    <div class="container d-flex flex-column align-baseline px-2 rounded">
                        <span class='my-2' style="font-family: 'Noto Sans KR', sans-serif;">${gu}, ${dong_name}</span>
                        <a href='/dashboard/report?dong_code=${dong_code}&gu=${gu}&dong=${dong_name}' class="btn btn-outline-secondary m-1" id="button-${index}">상권 분석</a>
                        <a href='#' class="btn btn-outline-secondary m-1" id="button-${index}">업종추천</a>
                    </div>
                `)

                marker.setPopup(popup);  
                markers.push(marker);
            }
    })
});
