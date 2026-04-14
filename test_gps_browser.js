// Test GPS in Browser Console
// Copy and paste this into your browser's developer console (F12)

console.log('🧪 Testing GPS in browser...');

if (navigator.geolocation) {
    console.log('✅ Geolocation API is supported');
    
    navigator.geolocation.getCurrentPosition(
        function(position) {
            console.log('✅ GPS SUCCESS!');
            console.log('📍 Latitude:', position.coords.latitude);
            console.log('📍 Longitude:', position.coords.longitude);
            console.log('📍 Accuracy:', position.coords.accuracy + ' meters');
        },
        function(error) {
            console.log('❌ GPS ERROR:', error.message);
            console.log('Error Code:', error.code);
            switch(error.code) {
                case 1:
                    console.log('🚫 Permission denied - Allow location in browser settings');
                    break;
                case 2:
                    console.log('📍 Position unavailable - Check device location settings');
                    break;
                case 3:
                    console.log('⏰ Timeout - GPS took too long to respond');
                    break;
            }
        },
        {
            enableHighAccuracy: false,
            timeout: 15000,
            maximumAge: 300000
        }
    );
} else {
    console.log('❌ Geolocation API not supported');
}