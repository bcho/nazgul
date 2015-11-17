// track script
(function(window) {
    // Constants.
    var DEFAULT_API_HOST = 'http://localhost:5566',
        SCRIPT_NAME = '/track/v1/track.js',
        REPORT_API_ENDPOINT = '/api/v1/report',
        VISITOR_KEY = '__nazgul_visitor';

    // Shadowed variables.
    var console = window.console,
        crypto = window.crypto,
        Date = window.Date,
        document = window.document,
        localStorage = window.localStorage,
        JSON = window.JSON,
        XMLHttpRequest = window.XMLHttpRequest;

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
        req: function(method, url, data, onsetup, onsuccess, onerror) {
            if (!onsetup) { onsetup = function(r) {}; }
            if (!onsuccess) { onsuccess = function(r) {}; }
            if (!onerror) { onerror = function(r) {}; }

            var request = new XMLHttpRequest();
            request.open(method, url, true);
            onsetup(request);
            request.onload = function() {
                if (request.status >= 200 && request.status < 400) {
                    onsuccess(request);
                } else {
                    onerror(request);
                }
            };
            request.onerror = function() { onerror(request); };

            if (data) {
                request.send(data);
            } else {
                request.send();
            }
        },

        post: function(url, onsetup, onsuccess, onerror) {
            this.req('POST', url, onsetup, onsuccess, onerror);
        }
    };

    // Exposed API.
    window.nazgul = {
        setup(settings) {
            if (settings.apiHost) {
                apiHost = settings.apiHost;
            }

            return this;
        },

        log: function(payload) {
            var url = `${apiHost}${REPORT_API_ENDPOINT}`;
            apiClient.post(
                url,
                JSON.stringify(payload),
                function(req) {
                    req.setRequestHeader('Content-Type', 'application/json');
                },
                function(req) {
                    console.log('log sent');
                },
                function(req) {
                    console.error('log send failed');
                }
            );
        },

        // Log click action.
        logClick: function(url) {
            this.log({
                visitor_id: visitor.visitorId,
                action: 'click',
                url: url,
                created_at: nowString(),
            });
        },

        // Log query action.
        logQuery: function(url, keyword) {
            this.log({
                visitor_id: visitor.visitorId,
                action: 'query',
                url: url,
                value: {
                    keyword: keyword
                },
                created_at: nowString()
            });
        }
    };
})(window);
