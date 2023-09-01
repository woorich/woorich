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

data = {
    '종로구': {
        '위도': 37.59552,
        '경도': 126.99046,
        '줌비율' : 12
    },
    '중구': {
        '위도': 37.55918,
        '경도': 126.99627,
        '줌비율' : 12.93
    },
    '용산구': {
        '위도': 37.53014,
        '경도': 126.98315,
        '줌비율': 12.4
    },
    '성동구': {
        '위도': 37.54973,
        '경도': 127.04218,
        '줌비율': 12.4
    },
    '광진구': {
        '위도': 37.54798,
        '경도': 127.0851,
        '줌비율': 12.4
    },
    '동대문구': {
        '위도': 37.58219,
        '경도': 127.05494,
        '줌비율': 12.59
    },
    '중랑구': {
        '위도': 37.59424,
        '경도': 127.09172,
        '줌비율': 12.4
    },
    '성북구': {
        '위도': 37.60399,
        '경도': 127.0174,
        '줌비율': 12.24
    },
    '강북구': {
        '위도': 37.6471,
        '경도': 127.02109,
        '줌비율': 12.05
    },
    '도봉구': {
        '위도': 37.66415,
        '경도': 127.04318,
        '줌비율': 12.05 
    },
    '노원구': {
        '위도': 37.65147,
        '경도': 127.07322,
        '줌비율': 11.86
    },
    '은평구': {
        '위도': 37.61528,
        '경도': 126.91857,
        '줌비율': 11.86
    },
    '서대문구': {
        '위도': 37.58226,
        '경도': 126.93719,
        '줌비율': 12.42
    },
    '마포구': {
        '위도': 37.56177,
        '경도': 126.91402,
        '줌비율': 12.42
    },
    '양천구': {
        '위도': 37.52748,
        '경도': 126.85543,
        '줌비율': 12.96
    },
    '강서구': {
        '위도': 7.56669,
        '경도': 126.82436,
        '줌비율': 12.05
    },
    '구로구': {
        '위도': 37.49738,
        '경도': 126.85789,
        '줌비율': 12.77
    },
    '금천구': {
        '위도': 37.46285,
        '경도': 126.90602,
        '줌비율': 12.4
    },
    '영등포구': {
        '위도': 37.51974,
        '경도': 126.90889,
        '줌비율': 12.18
    },
    '동작구': {
        '위도': 37.49729,
        '경도': 126.94508,
        '줌비율': 12.74
    },
    '관악구': {
        '위도': 37.46832,
        '경도': 126.94891,
        '줌비율': 12.4
    },
    '서초구': {
        '위도': 37.4795,
        '경도': 127.0335,
        '줌비율': 11.68
    },
    '강남구': {
        '위도': 37.49601,
        '경도': 127.06341,
        '줌비율': 11.87
    },
    '송파구': {
        '위도': 37.50532,
        '경도': 127.11579,
        '줌비율': 12.05
    },
    '강동구': {
        '위도': 37.54623,
        '경도': 127.14766,
        '줌비율': 12.24
    },
    '행정구': {
        '위도': 37.5665,
        '경도': 126.978,
        '줌비율': 10.2
    },
};

// Add a change event listener to the select element
selectElementGu.addEventListener('change', (event) => {
    // Retrieve the selected district value
    const selectedDistrict = event.target.value;

    // Use the selected district value to focus the map
    // Replace this with your actual logic to focus on the selected district
    // For example, you can use geocoding or known coordinates to center the map on the selected district.
    // Here's a simplified example

    let lat = data[selectedDistrict]['위도'];
    let long = data[selectedDistrict]['경도'];
    let zoom_num = data[selectedDistrict]['줌비율'];
    console.log(long, lat, zoom_num);
    map.flyTo({ center: [long, lat], zoom: zoom_num });
    
    // Add more conditions for other districts as needed
});