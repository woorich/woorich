const selectElementGu = document.getElementById('dynamic-select-gu');
const selectElementDong = document.getElementById('dynamic-select-dong');
const selectElementYear = document.getElementById('dynamic-select-year');
const selectElementQuarter = document.getElementById('dynamic-select-quarter');
let csvArray;
const markers = [];
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
        
        selectElementDong.addEventListener('change',(e)=>{
            const selectedDong = selectElementDong.value;

            markers.forEach(marker => {
                const markerDong = marker._popup._classList.values().next().value;
                
                if (markerDong === selectedDong) {
                    if (!marker.getPopup().isOpen()) {
                        marker.togglePopup();
                        map.flyTo({ center: [marker.getLngLat().lng, marker.getLngLat().lat], zoom: map.getZoom(), duration: 1200 });
                    }
                } else {
                    if (marker.getPopup().isOpen()) {
                        marker.togglePopup();
                    }
                }
                
            });
        })
    });
})
.catch(error => console.error('Error:', error));


////////////////////////////////////////////////////////////////////////////////
fetch(staticUrl+'/data/gu-geo.json')
    .then(response => response.text())
    .then(data => {
        // Add a change event listener to the select element
        data = JSON.parse(data);
        selectElementGu.addEventListener('change', (event) => {
            if (markers){
                markers.forEach(marker =>  marker.remove());
            }
            // Retrieve the selected district value
            const selectedDistrict = event.target.value;

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
                
                // 샘플 데이터 
                const recommended_item = [' ', ' ', ' ', ' ', ' '];
                var url = window.location.protocol + "//" + window.location.host
                const popup = new mapboxgl.Popup({ closeButton: true, offset: 25 }) // Customize popup behavior
                .setLngLat([longitude, latitude])
                .setHTML(`
                    <div class="container rounded" id="${dong_name}">
                        <div id="popup-button-list-${index}" class="d-flex flex-column align-baseline" style="display: block;">
                            <span class='my-2' style="font-family: 'Noto Sans KR', sans-serif;">${gu}, ${dong_name}</span>
                            <a href='${url}/dashboard/report/summary/${dong_code}/${gu}/${dong_name}/2022/4/0' class="btn btn-outline-secondary m-1" id="button-${index}">상권 분석</a>
                            <a href='#' class="btn btn-outline-secondary m-1" id="button-recommend-${index}">업종추천</a>
                        </div>

                        <div id="recommended-list-${index}" style="display: none; text-align:right; padding:5px;">
                            <div style="align-items:center;">
                                <span class='my-2 py-2' style="font-family: 'Noto Sans KR', sans-serif;">${gu}, ${dong_name}</span>
                                <button class="btn m-1" id="button-back-${index}"><i class="bi bi-backspace"></i></button>
                                <div class="container d-flex justify-between mb-3 m-0 p-0">
                                    <button
                                        type="button"
                                        class="d-block btn btn-outline-primary mx-2"
                                        style="font-size: 0.8rem"
                                        value="1"
                                    >
                                        <i class="fas fa-utensils"></i>
                                    </button>
                                    <button
                                        type="button"
                                        class="d-block btn btn-outline-primary mx-2"
                                        style="font-size: 0.8rem"
                                        value="2"
                                    >
                                        <i class="fas fa-handshake"></i>
                                    </button>
                                    <button
                                        type="button"
                                        class="d-block btn btn-outline-primary mx-2"
                                        style="font-size: 0.8rem"
                                        value="3"
                                    >
                                        <i class="fas fa-store"></i>
                                    </button>
                                </div>
                            </div>
                            <div class="text-center my-3" id="predict-job-title">
                                <span>업종 타이틀</span>
                            </div>
                            <div style="display: flex; justify-content: center; align-items: center;">
                                <div id="spinner" class="spinner-border text-primary" style="display: none;" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                            <ul style="list-style: none; padding:0; margin:0; text-align:center;">
                                <div id="prediction_result_list" style="text-align:left;">
                                </div>
                            </ul>
                        </div>

                    </div>
                `)
                .addClassName(dong_name);

                popup.on('open', () => {
                    setTimeout(() => {
                        // Try to get the element again after a delay
                        let recommendButton = document.getElementById(`button-recommend-${index}`);
                        let backButton = document.getElementById(`button-back-${index}`);
                
                        if(recommendButton) {
                            recommendButton.addEventListener('click', () => {
                                document.getElementById(`recommended-list-${index}`).style.display = 'block';
                                document.getElementById(`popup-button-list-${index}`).style.setProperty('display', 'none', 'important');
                            });
                        }
                
                        if(backButton) {
                            backButton.addEventListener('click', () => {
                                document.getElementById(`recommended-list-${index}`).style.display = 'none';
                                document.getElementById(`popup-button-list-${index}`).style.display = 'block';
                            });
                        }
                    }, 0); 
                    
                    setTimeout(() => {
                        const button1 = document.querySelector(`#button-back-${index} ~ .container button[value="1"]`);
                        const button2 = document.querySelector(`#button-back-${index} ~ .container button[value="2"]`);
                        const button3 = document.querySelector(`#button-back-${index} ~ .container button[value="3"]`);
                        const title = document.getElementById('predict-job-title');
                        const prediction_list = document.getElementById('prediction_result_list');
                
                        if(button1) {
                            button1.addEventListener('click', () => {
                                title.textContent="외식업";
                                document.getElementById('spinner').style.display = 'block';
                                document.getElementById('prediction_result_list').style.display = 'none';
                                var url = new URL(window.location.href);
                                fetch(`${url.origin}/dashboard/prediction?arg1=${dong_code}&arg2=1`)
                                    .then(response => response.json())
                                    .then(data => {
                                        prediction_list.innerHTML = ""
                                        if (typeof data.result != 'undefined'){
                                            prediction_list.innerHTML = data.result.map((item, index)=>{
                                                return `<li><h5>${index+1} ${item}</h5></li>`
                                            }).join("")
                                        }
                                        else {
                                            prediction_list.innerHTML = '죄송합니다.\n 데이터가 충분하지 \n 않습니다.'
                                        }
                                    })
                                    .catch(error => {
                                        console.log(error);
                                    })
                                    .finally(() => {
                                        document.getElementById('prediction_result_list').style.display = 'block';
                                        document.getElementById('spinner').style.display = 'none';  // Hide spinner
                                    });
                            });
                        }
                
                        if(button2) {
                            button2.addEventListener('click', () => {
                                title.textContent="서비스업";
                                document.getElementById('spinner').style.display = 'block';
                                document.getElementById('prediction_result_list').style.display = 'none';
                                var url = new URL(window.location.href);
                                fetch(`${url.origin}/dashboard/prediction?arg1=${dong_code}&arg2=2`)
                                    .then(response => response.json())
                                    .then(data => {
                                        prediction_list.innerHTML = ""
                                        if (typeof data.result != 'undefined'){
                                            prediction_list.innerHTML = data.result.map((item, index)=>{
                                                return `<li><h5>${index+1} ${item}</h5></li>`
                                            }).join("")
                                        }
                                        else {
                                            prediction_list.innerHTML = '죄송합니다.\n 데이터가 충분하지 \n 않습니다.'
                                        }
                                    })
                                    .catch(error => {
                                        console.log(error);
                                    })
                                    .finally(() => {
                                        document.getElementById('prediction_result_list').style.display = 'block';
                                        document.getElementById('spinner').style.display = 'none';  // Hide spinner
                                    });
                            });
                        }
                
                        if(button3) {
                            button3.addEventListener('click', () => {
                                title.textContent="소매업";
                                document.getElementById('spinner').style.display = 'block';
                                document.getElementById('prediction_result_list').style.display = 'none';
                                var url = new URL(window.location.href);
                                fetch(`${url.origin}/dashboard/prediction?arg1=${dong_code}&arg2=3`)
                                    .then(response => response.json())
                                    .then(data => {
                                        prediction_list.innerHTML = ""
                                        if (typeof data.result != 'undefined'){
                                            prediction_list.innerHTML = data.result.map((item, index)=>{
                                                return `<li><h5>${index+1} ${item}</h5></li>`
                                            }).join("")
                                        }
                                        else {
                                            prediction_list.innerHTML = '죄송합니다.\n 데이터가 충분하지 \n 않습니다.'
                                        }
                                    })
                                    .catch((error) => {
                                        console.log(error);
                                    })
                                    .finally(() => {
                                        document.getElementById('prediction_result_list').style.display = 'block';
                                        document.getElementById('spinner').style.display = 'none';  // Hide spinner
                                    });
                            });
                        }
                    }, 0); 
                });

                marker.getElement().addEventListener('click', (e) => {
                    // let currentUrl = location.href.split('/');
                    // let currentLat = currentUrl[5];
                    // let currentLong = currentUrl[6];

                    let selectElementDong = document.getElementById('dynamic-select-dong');
                    selectElementDong.value = marker._popup._classList.values().next().value
                    map.flyTo({ center: [longitude, latitude+0.02], zoom: zoom_num, duration: 1200 });
                });
                marker.setPopup(popup);  
                markers.push(marker);
            }
        })

        convertedGeoJsonData = {
            type: 'FeatureCollection',
            features: Object.keys(data).map(key => ({
                type: 'Feature',
                properties: { 
                    description: key,
                    zoom_ratio: data[key]["줌비율"]
                },
                geometry: {
                    type: 'Point',
                    coordinates: [
                        data[key]["위도"], 
                        data[key]["경도"]
                    ]
                }
            }))
        };
});


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
    // map.addLayer({
    //     'id': 'background',
    //     'type': 'background',
    //     'source': 'tileset_data',
    //     'source-layer': 'seoul_gu-3hhcst',
    //     'paint' : {
    //         'background-color': 'hsla(0, 0%, 100%, 0.8)'
    //     }
    // });
    map.addLayer({
        'id': 'fill',
        'type': 'fill',
        'source': 'tileset_data',
        'source-layer': 'seoul_gu-3hhcst',
        'paint': {
            'fill-color': 'hsla(163, 87%, 61%, 0.59)',
            'fill-opacity': 0.75,
            'fill-outline-color': 'hsl(0, 100%, 100%)'
        }
    });

    console.log(convertedGeoJsonData);
    map.addSource('points', {
        'type': 'geojson',
        'data': convertedGeoJsonData
    });
    
    map.addLayer({
        'id': 'points',
        'type': 'symbol',
        'source': 'points',
        'layout': {
            'text-field': ['get', 'description'],
            'text-size': 12
        },
        'paint': {
            'text-color': '#000000'
        }
    }, 'fill');

    // markers.forEach(marker => {
    //     marker.getElement().addEventListener('mouseenter', () => {
    //         marker.togglePopup(); // Show the popup when hovered
    //     });
    
    //     marker.getElement().addEventListener('mouseleave', () => {
    //         marker.togglePopup(); // Hide the popup when not hovered
    //     });

    // });
});
