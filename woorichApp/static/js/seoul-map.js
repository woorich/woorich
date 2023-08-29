mapboxgl.accessToken = 'pk.eyJ1Ijoid29veW9vbndpbm5pZSIsImEiOiJjbGx1ZWl2ZjkxOWt0M2RtbGY3MWl5N29jIn0.Ksbm1ZDp2VptXVlOldqguw';
const map = new mapboxgl.Map({
    container: 'map-container', // container ID
    center: [126.9779692, 37.566535], // starting position [lng, lat]
    zoom: 11, // starting zoom
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
