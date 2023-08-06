import Feature from "./Feature.js";
import TranscriptFormatted from "./TranscriptFormatted.js";

export default {
    props: ["steps", "detailHoverIndex", "nFeatures", "alphabet"],
    components: { Feature, TranscriptFormatted, },
    methods: {
        stepFeatureCost(step) {
            return `${this.costFormatted(step.cost)} / ${this.nFeatures}`
        },
        costFormatted(cost) {
            let rounded = Math.round(100 * this.nFeatures * cost, 2) / 100
            return `${rounded}`
        },

    },
    template: `
        <div id="detail">
            <table class="feature-steps">
                <thead>
                    <th>Action</th>
                    <th>Cost</th>
                    <th>From</th>
                    <th>To</th>
                    <th>Features</th>
                </thead>
                <tbody>
                    <tr v-for="step, n in steps"
                        @mouseover="detailHoverIndex = n"
                        @mouseleave="detailHoverIndex = null"
                        :class="['action-' + step.action.toLowerCase()]"
                    >
                    <td>{{step.action}}</td>
                    <td>{{stepFeatureCost(step)}}</td>
                    <td>
                        <span v-if="step.expected">
                            <TranscriptFormatted :transcript="[step.expected]" :alphabet="alphabet" />
                        </span>
                    </td>
                    <td>
                        <span v-if="step.actual">
                            <TranscriptFormatted :transcript="[step.actual]" :alphabet="alphabet" />
                        </span>
                    </td>
                    <td>
                        <ul class="feature-collection with-brackets">
                            <li v-for="value, feature in step.features">
                                <Feature :feature="feature" :value="value" />
                            </li>
                        </ul>
                    </td>
                </tr>

                </tbody>
            </table>
        </div>`
}