const selectElementGu = document.getElementById('dynamic-select-gu');
const selectElementDong = document.getElementById('dynamic-select-dong');

//const staticUrl = document.currentScript.getAttribute('staticUrl');
fetch(staticUrl + 'gu-dong-coord-data.csv', {
    headers: {
        'Content-Type': 'text/csv; charset=cp-949' // character encoding
    }
})
.then(response => response.text())
.then(csvData => {
    const csvArray = csvData.split('\n').map(row => row.split(','));

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
        console.log(selectedGu);

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
        console.log(urlString, selectElementGu.value);


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
            'fill-color': 'hsla(248, 53%, 58%, 0.5)',
            'fill-opacity': 0.75,
            'fill-outline-color': 'hsl(0, 100%, 100%)'
        }
    });
    
    const markers = []
    // Fetch and add markers and popups
    fetch(staticUrl + 'gu-dong-coord-data.csv')
    .then(response => response.text())
    .then(csvData => {             
        const rows = csvData.split('\n');
        for(let i=0; i < rows.length;i++){
            let item = rows[i].split(',');
            let dong_code = item[1];
            let index = item[0];
            let gu = item[2];
            let dong_name = item[3];
            let latitude = parseFloat(item[4]);
            let longitude = parseFloat(item[5]);
            console.log(dong_code, gu, dong_name, latitude, longitude);
            if (!isNaN(latitude) && !isNaN(longitude)){
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
        }
    })
    .catch(error => console.error('Error loading CSV:', error));

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

    fetch(staticUrl+'gu-dong-coord-data.csv')
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
                console.log(dong_code, gu, dong, latitude, longitude);
                window.location.href = `/dashboard/report?dong_code=${dong_code}&gu=${gu}&dong=${dong}`;
                break;
            }
        }
    })
    .catch(error => console.error('Error loading CSV:', error));
}

////////////////////////////////////////////////////////////////////////////////