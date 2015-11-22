// track script
(function(window) {
    // Constants.
    var DEFAULT_API_HOST = 'http://localhost:5566',
        SCRIPT_NAME = '/track/v1/track.js',
        REPORT_API_ENDPOINT = '/api/v1/report',
        VISITOR_KEY = '__nazgul_visitor';

    var ACTION_CLICK = 'click',
        ACTION_QUERY = 'query';

    // Shadowed variables.
    var console = window.console,
        crypto = window.crypto,
        Date = window.Date,
        document = window.document,
        encodeURIComponent = window.encodeURIComponent,
        localStorage = window.localStorage,
        JSON = window.JSON,
        XMLHttpRequest = window.XMLHttpRequest,
        pageHref = document.location.href;

    // XXX support modern browser only.
    function generateUUID() {
        var tmpl = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx';

        return tmpl.replace(/[xy]/g, function(c) {
            var r = crypto.getRandomValues(new Uint8Array(1))[0] % 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);

            return v.toString(16);
        });
    }

    function nowString() {
        return (new Date()).toISOString();
    }

    function Visitor(visitorId) {
        this.visitorId = visitorId || generateUUID();

        this.persistence();
    }

    Visitor.prototype.persistence = function() {
        var dump = JSON.stringify({
            'visitor_id': this.visitorId
        });
        localStorage[VISITOR_KEY] = dump;
    };

    // Current session visitor.
    var visitor = (function() {
        var storedVisitor = localStorage[VISITOR_KEY];
        if (storedVisitor === undefined) {
            return new Visitor();
        }

        try {
            return new Visitor(JSON.parse(storedVisitor).visitor_id);
        } catch (e) {
            console.warn(e);
            return new Visitor();
        }
    })();

    // Default api host.
    var apiHost = (function() {
        var s = document.querySelector(`script[src$="${SCRIPT_NAME}"]`);
        if (!s) {
            console.warn('invalid setup');
            return DEFAULT_API_HOST;
        }
        var host = s.src.match(/https?:\/\/[^\/]*/);
        if (!host) {
            console.warn('invalid setup');
            return DEFAULT_API_HOST;
        }
        return host[0];
    })();

    // Simple api client.
    var apiClient = {
        getBeacon: function(url, data, onsuccess) {
            var encodedData = encodeURIComponent(JSON.stringify(data)),
                image = new Image(1, 1);
            image.src = url + (url.indexOf('?') == -1 ? '?' : '&') + 'data=' + encodedData;
            image.onload = onsuccess;
        }
    };

    function log(payload) {
        var url = `${apiHost}${REPORT_API_ENDPOINT}`;
        apiClient.getBeacon(url, payload, function() {
            console.log('log sent');
        });
    }

    // Log query action.
    function logQuery(form) {
        log({
            visitor_id: visitor.visitorId,
            action: 'query',
            url: pageHref,
            referer: document.referrer,
            created_at: nowString(),

            value: form
        });
    }

    // Log click action.
    function logClick(destUrl) {
        log({
            visitor_id: visitor.visitorId,
            action: 'click',
            url: pageHref,
            referer: document.referrer,
            created_at: nowString(),

            value: {
                from_url: pageHref,
                dest_url: destUrl
            }
        });
    }

    function injectClick() {
        var links = document.querySelectorAll('a');
        for (var i = 0; i < links.length; i++) {
            links[i].onclick = function(e) {
                var target = e.target;
                if (!target || !target.href) {
                    return;
                }
                logClick(target.href);
            }
        }
    }

    function injectQuery() {
        var forms = document.querySelectorAll('form');
        for (var i = 0; i < forms.length; i++) {
            forms[i].onsubmit = function(e) {
                e.preventDefault();

                var target = e.target;
                if (!target) {
                    return;
                }

                var formValue = {};

                var inputs = target.querySelectorAll('input');
                for (var j = 0; j < inputs.length; j++) {
                    if (inputs[j].type != 'text' && inputs[j].type != 'search') {
                        continue;
                    }
                    if (!inputs[j].name) {
                        continue;
                    }
                    formValue[inputs[j].name] = inputs[j].value;
                }

                logQuery({
                    form_action: target.action,
                    form_id: target.id,
                    form_value: formValue
                });

                window.setTimeout(function() {
                    target.submit();
                }, 150);
            }
        }
    }

    // Exposed API.
    window.nazgul = {
        log: log,
        logClick: logClick,
        logQuery: logQuery,

        // Inject actions.
        inject: function() {
            injectClick();
            injectQuery();
        }
    };

    window.nazgul.inject();
})(window);
