export default {
    props: ["feature", "value"],
    methods: {
        formatFeature(feature, value) {
            switch (value) {
                case -1:
                    return `-${feature}`;
                case +1:
                    return `+${feature}`;
                case -0.5:
                    return `-+${feature}`;
                case +0.5:
                    return `+-${feature}`;
                default:
                    return `${value}${feature}`;
            }
            if (value < 0) return `-${feature}`;
            if (value > 0) return `+${feature}`;
            return `0${feature}`;
        },
    },
    template: `
        <span>{{formatFeature(feature, value)}}</span>
    `
}