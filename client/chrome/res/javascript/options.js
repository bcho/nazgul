(function() {
    var KEY_API_HOST = '__nazgul_api_host';

    var settingsForm = document.querySelector('#settings-form'),
        apiHost = document.querySelector('[name="api-host"]');

    // Restore settings.
    function restoreSettings() {
        var payload = {};
        payload[KEY_API_HOST] = null;
        chrome.storage.local.get(payload, function(items) {
            if (items[KEY_API_HOST]) {
                apiHost.value = items[KEY_API_HOST];
            }
        });
    }

    // Save settings.
    settingsForm.onsubmit = function(e) {
        e.preventDefault();

        var payload = {};
        payload[KEY_API_HOST] = apiHost.value;

        chrome.storage.local.set(payload, function() {
            alert('保存成功');
        });
    };

    restoreSettings();
})();
