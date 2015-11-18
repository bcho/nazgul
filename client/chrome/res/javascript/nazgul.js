(function() {
    var KEY_TRACK_SCRIPT = '__nazgul_track_script',
        trackScript = 'http://localhost:5566/track/v1/track.js';

    function loadScripts(script) {
        var ele = document.createElement('script'),
            loaded = false;
        ele.setAttribute('type', 'text/javascript');
        ele.setAttribute('src', script);
        document.getElementsByTagName('body')[0].appendChild(ele);
    }

    var payload = {};
    payload[KEY_TRACK_SCRIPT] = null;
    chrome.storage.local.get(payload, function(items) {
        if (items[KEY_TRACK_SCRIPT]) {
            trackScript = items[KEY_TRACK_SCRIPT];
        }

        loadScripts(trackScript);
    });
})();
