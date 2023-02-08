class TakeOneVideo extends HTMLElement {
    constructor() {
        super();

        this.player = null;
        this.videoURL = null;

        //have this default to our prod service
        this.takeOneBaseURL = this.getAttribute('base-url');
        this.clientId = this.getAttribute('client-id');
        this.videoId = this.getAttribute('video-id');
    }

    static get observedAttributes() { return ['client-id', 'video-id', 'base-url']; }

    connectedCallback() {        
        let video = document.createElement("video-js");
        video.setAttribute('controls', '');
        video.setAttribute('preload', 'auto');
        this.appendChild(video);
        this.player = videojs(video);
        this.player.fill(true);
        let qualityLevels = this.player.qualityLevels();
        qualityLevels.on('addqualitylevel', function(event) {
            let qualityLevel = event.qualityLevel;

            if (qualityLevel.height >= 720) {
                qualityLevel.enabled = true;
            } else {
                qualityLevel.enabled = false;
            }
        });

        this.clientId = this.getAttribute('client-id');
        this.videoId = this.getAttribute('video-id');
        this.takeOneBaseURL = this.getAttribute('base-url');
        this.fetchVideoURL();
    }

    attributeChangedCallback(attrName, oldValue, newValue) {
        if (this.isConnected) {
            if (attrName == 'client-id') {
                this.clientId = newValue;
                this.fetchVideoURL();
            }
            else if (attrName == 'video-id') {
                this.videoId = newValue;
                this.fetchVideoURL();
            }
            else if (attrName == 'base-url') {
                this.takeOneBaseURL = newValue;
                this.fetchVideoURL();
            }
        }
    }

    getAspectRatio(videoFormat) {
        if (videoFormat == "landscape") {
            return "16:9"
        }
        else if (videoFormat == "portrait") {
            return "9:16"
        }
        else {
            return "1:1"
        }
    }

    fetchVideoURL() {
        if (this.clientId && this.videoId && this.takeOneBaseURL && this.player) {
            const comp = this
            const requestURL = `${this.takeOneBaseURL}/api/v1/external/videos/${this.clientId}/${this.videoId}`
            fetch(requestURL).then(function(response) {
                return response.json();
            }).then(function(responseJSON) {
                const src = responseJSON.src;
                const type = responseJSON.type;
                const videoFormat = responseJSON.video_format;
                if (comp.videoURL != src) {
                    comp.videoURL = src
                    comp.player.aspectRatio(comp.getAspectRatio(videoFormat));
                    comp.player.src({
                        src: src,
                        type: type
                    });
                }
            });
        }
    }
}

customElements.define('take-one-video', TakeOneVideo);