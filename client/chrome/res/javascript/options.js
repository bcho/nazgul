(function() {
    var KEY_TRACK_SCRIPT = '__nazgul_track_script';

    var settingsForm = document.querySelector('#settings-form'),
        trackScript = document.querySelector('[name="track-script"]');

    // Restore settings.
    function restoreSettings() {
        var payload = {};
        payload[KEY_TRACK_SCRIPT] = null;
        chrome.storage.local.get(payload, function(items) {
            if (items[KEY_TRACK_SCRIPT]) {
                trackScript.value = items[KEY_TRACK_SCRIPT];
            }
        });
    }

    // Save settings.
    settingsForm.onsubmit = function(e) {
        e.preventDefault();

        var payload = {};
        payload[KEY_TRACK_SCRIPT] = trackScript.value;

        chrome.storage.local.set(payload, function() {
            alert('保存成功');
        });
    };

    restoreSettings();
})();
